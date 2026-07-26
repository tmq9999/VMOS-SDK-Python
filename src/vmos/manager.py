"""Profile Manager — the profile-driven orchestrator of the framework.

The framework has one **canonical** :class:`vmos.profile.Profile` (the source of
truth) and several **independent backends** that each apply *part* of it to a
device. The :class:`ProfileManager` is the single coordinator:

.. code-block:: text

    Profile (canonical JSON)
      -> ProfileManager.apply(profile)
           |-- SystemApplierBackend   (Layer 1: build.prop via resetprop + Magisk module)
           |-- JavaHookBackend        (Layer 2: persist.vmos.spoof.* + XPose plugin scope)
           |-- <future backends>      (native hook, service/system hook, ...)
      -> ProfileManager.verify(profile)  -> read back + diff per backend

Design contract (why this exists instead of ``setImei()`` / ``setAndroidId()``):

* **Every backend READS the Profile.** No backend hard-codes identity; adding a
  new backend never means touching the Profile schema.
* **One call provisions everything.** ``manager.apply(profile)`` fans the single
  Profile out to every registered backend, so changing the Profile changes the
  whole device — that is the whole point of the framework.
* **Backends are independent and optional.** Register only the layers you want
  (e.g. Layer 1 only on a device where no app hook is loaded).

Backends deliberately reuse the verified appliers in :mod:`vmos.spoof` via the
Profile's bridge methods (:meth:`Profile.to_device_profile`,
:meth:`Profile.identity_kwargs`, :meth:`Profile.identity_props`).
"""

from __future__ import annotations

import abc
import re
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional

from .exceptions import ProfileValidationError
from .profile import Profile, validate
from .spoof import (
    PadRootShell,
    app_scoped_targets,
    apply_profile as _layer1_apply,
    load_xpose_plugin,
    remove_spoof as _layer1_remove,
    remove_xpose_plugin,
    set_build_props,
    set_identity_props,
    verify_profile as _layer1_verify,
)

if TYPE_CHECKING:  # pragma: no cover
    from .client import VMOSClient

__all__ = [
    "Backend",
    "SystemApplierBackend",
    "JavaHookBackend",
    "ProfileManager",
    "standard_manager",
]

_PKG_SAFE = re.compile(r"[^A-Za-z0-9]+")


# --------------------------------------------------------------------------- #
# Backend abstraction
# --------------------------------------------------------------------------- #
class Backend(abc.ABC):
    """One independent applier of (part of) a :class:`Profile`.

    A backend maps a slice of the canonical Profile onto a device mechanism. It
    must not hard-code identity — it reads everything from the ``profile`` passed
    to :meth:`apply` / :meth:`verify`.
    """

    #: Stable identifier used in result dicts (e.g. ``"system_applier"``).
    name: str = "backend"
    #: Informational identity layer (1 = system/build, 2 = app-hook getters, ...).
    layer: int = 0
    #: Profile sections this backend consumes (informational / for reporting).
    sections: tuple = ()

    @abc.abstractmethod
    def apply(self, profile: Profile) -> Dict[str, Any]:
        """Apply this backend's slice of ``profile`` to the device."""

    def verify(self, profile: Profile) -> Dict[str, Any]:
        """Read applied values back and diff against ``profile``.

        Default: report that this backend has no read-back oracle. Override in
        backends that can verify.
        """
        return {"backend": self.name, "supported": False}

    def remove(self) -> Dict[str, Any]:
        """Undo what :meth:`apply` installed (best-effort). Default: no-op."""
        return {"backend": self.name, "removed": False, "supported": False}


class SystemApplierBackend(Backend):
    """Layer 1 — build identity via ``resetprop`` + a persistent Magisk module.

    Consumes the ``build``/``display``/``identity.android_id`` slice through
    :meth:`Profile.to_device_profile` and delegates to the live-verified
    :func:`vmos.spoof.apply_profile` / :func:`vmos.spoof.verify_profile` /
    :func:`vmos.spoof.remove_spoof`.
    """

    name = "system_applier"
    layer = 1
    sections = ("build", "display")

    def __init__(
        self,
        client: "VMOSClient",
        pad_code: str,
        *,
        persist: bool = True,
        set_android_id: bool = True,
    ) -> None:
        self.client = client
        self.pad_code = pad_code
        self.persist = persist
        self.set_android_id = set_android_id

    def apply(self, profile: Profile) -> Dict[str, Any]:
        dp = profile.to_device_profile()
        result = _layer1_apply(
            self.client, self.pad_code, dp,
            persist=self.persist, set_android_id=self.set_android_id,
        )
        return {"backend": self.name, **result}

    def verify(self, profile: Profile) -> Dict[str, Any]:
        dp = profile.to_device_profile()
        result = _layer1_verify(self.client, self.pad_code, dp)
        return {"backend": self.name, **result}

    def remove(self) -> Dict[str, Any]:
        _layer1_remove(self.client, self.pad_code)
        return {"backend": self.name, "removed": True}


class JavaHookBackend(Backend):
    """Layer 2 — framework-held getters + ``Build.*`` via the private XPose plugin.

    Sets the ``persist.vmos.spoof.*`` values the plugin returns for
    ``getImei``/``getSubscriberId``/``AdvertisingIdClient.getId``/
    ``WifiInfo.getMacAddress``/``Build.getSerial``/``MediaDrm``/
    ``Settings.Secure`` (read from :meth:`Profile.identity_kwargs`), and — when
    ``spoof_build`` is on (default) — the ``persist.vmos.spoof.build.*`` values the
    plugin uses to spoof ``Build.MODEL``/``BRAND``/``FINGERPRINT``/… app-scoped
    (from :meth:`Profile.build_hook_kwargs`). When an APK source is given it also
    loads the plugin into each ``profile.runtime.target_apps`` package via ``apmt``.

    **Scoping (denylist model).** ``apmt`` is per-package with no wildcard, so the
    scope is *"every installed app EXCEPT GMS/Play"*. With ``auto_scope_all=True``
    the backend enumerates the pad's installed packages minus
    :data:`vmos.spoof.GMS_DENYLIST` (plus ``scope_denylist_extra``) at apply time
    and writes them onto ``profile.runtime.target_apps`` — so GMS/Play keep their
    genuine identity and never crash. Newly-installed apps are not covered until a
    re-run. The plugin's ``appMain`` enforces the same denylist defensively.

    The plugin is built once (see ``xpose_plugin/``); provide ``apk_url`` or
    ``apk_path`` only when it needs (re)loading. If neither is given, the backend
    just refreshes the per-device props (assumes the plugin is already loaded).
    """

    name = "java_hook"
    layer = 2
    sections = ("build", "telephony", "identity", "network")

    def __init__(
        self,
        client: "VMOSClient",
        pad_code: str,
        *,
        apk_url: Optional[str] = None,
        apk_path: Optional[str] = None,
        plugin_name: str = "vmos_profile",
        persist_module: bool = True,
        spoof_build: bool = True,
        auto_scope_all: bool = False,
        scope_denylist_extra: Optional[Iterable[str]] = None,
    ) -> None:
        if apk_url and apk_path:
            raise ValueError("provide at most one of apk_url or apk_path")
        self.client = client
        self.pad_code = pad_code
        self.apk_url = apk_url
        self.apk_path = apk_path
        self.plugin_name = plugin_name
        self.persist_module = persist_module
        self.spoof_build = spoof_build
        self.auto_scope_all = auto_scope_all
        self.scope_denylist_extra = scope_denylist_extra

    def _patch_name(self, pkg: str) -> str:
        return f"{self.plugin_name}_{_PKG_SAFE.sub('_', pkg).strip('_')}"

    def apply(self, profile: Profile) -> Dict[str, Any]:
        # Optionally derive the scope = "all installed apps EXCEPT GMS/Play" and
        # write it onto the profile so both this backend and callers see it.
        scoped_note = None
        if self.auto_scope_all:
            shell = PadRootShell(self.client, self.pad_code)
            targets = app_scoped_targets(shell, extra_denylist=self.scope_denylist_extra)
            profile.runtime.target_apps = targets
            scoped_note = (f"auto-scoped {len(targets)} installed app(s) minus the "
                           f"GMS/Play denylist; re-run after installing new apps "
                           f"(apmt is per-package, no wildcard)")
        # Layer-2 identity getters (persist.vmos.spoof.*).
        props = set_identity_props(
            self.client, self.pad_code,
            persist_module=self.persist_module, **profile.identity_kwargs(),
        )
        # Layer-2 app-scoped Build.* (persist.vmos.spoof.build.*), unless disabled.
        build_props: Dict[str, str] = {}
        if self.spoof_build:
            build_props = set_build_props(
                self.client, self.pad_code,
                persist_module=self.persist_module, **profile.build_hook_kwargs(),
            )
        loaded: List[Dict[str, Any]] = []
        targets = list(profile.runtime.target_apps)
        has_apk = bool(self.apk_url or self.apk_path)
        if targets and has_apk:
            for pkg in targets:
                out = load_xpose_plugin(
                    self.client, self.pad_code,
                    name=self._patch_name(pkg), target_pkg=pkg,
                    apk_url=self.apk_url, apk_path=self.apk_path,
                )
                loaded.append({"pkg": pkg, "name": self._patch_name(pkg), "out": out})
        note = scoped_note
        if targets and not has_apk:
            load_note = ("plugin load skipped: no apk_url/apk_path given "
                         "(assuming the plugin is already loaded); props still refreshed")
            note = f"{note}; {load_note}" if note else load_note
        elif not targets:
            empty_note = "no runtime.target_apps in profile: props set but no app scoped"
            note = f"{note}; {empty_note}" if note else empty_note
        return {"backend": self.name, "props_set": props, "build_props_set": build_props,
                "loaded": loaded, "note": note}

    def verify(self, profile: Profile) -> Dict[str, Any]:
        """Read the ``persist.vmos.spoof.*`` props back with ``getprop``.

        This confirms the per-device values are *set*. It does NOT prove the
        app-side hook returns them — that requires reading a scoped device-info
        app (screenshot / device-info oracle), which the Verification component
        handles. ``service call`` / ``getprop`` of the real props are never valid
        oracles for the Java hook.
        """
        want = profile.identity_props()
        if not want:
            return {"backend": self.name, "ok": True, "checks": {},
                    "note": "profile has no Layer-2 identity values"}
        shell = PadRootShell(self.client, self.pad_code)
        script = " ; ".join(f'echo "{k}=$(getprop {k})"' for k in want)
        out = shell.sh(script)
        got: Dict[str, str] = {}
        for line in out.splitlines():
            if "=" in line:
                k, _, v = line.partition("=")
                got[k.strip()] = v.strip()
        checks: Dict[str, Any] = {}
        ok = True
        for k, wv in want.items():
            gv = got.get(k, "")
            match = gv == wv
            ok = ok and match
            checks[k] = {"want": wv, "got": gv, "match": match}
        return {"backend": self.name, "ok": ok, "checks": checks,
                "note": "verifies persist.vmos.spoof.* are set; app-observed values "
                        "need a scoped device-info app (see Verification)"}

    def remove(self) -> Dict[str, Any]:
        """Remove any plugin patches this backend would have loaded (by name)."""
        removed: List[str] = []
        # We can only remove patches we know the names of; without a profile here
        # we remove nothing destructive. Callers with the profile can pass target
        # packages to remove_for().
        return {"backend": self.name, "removed": removed,
                "note": "call remove_for(profile) to unload named patches"}

    def remove_for(self, profile: Profile) -> Dict[str, Any]:
        """Unload the XPose patches this backend created for ``profile``'s targets."""
        outs = []
        for pkg in profile.runtime.target_apps:
            outs.append({"pkg": pkg,
                         "out": remove_xpose_plugin(self.client, self.pad_code, self._patch_name(pkg))})
        return {"backend": self.name, "removed": [o["pkg"] for o in outs], "detail": outs}


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #
class ProfileManager:
    """Coordinate a canonical :class:`Profile` across independent backends.

    Register backends (or use :func:`standard_manager`) then call
    :meth:`apply` / :meth:`verify` / :meth:`remove` with a single Profile.

    Parameters
    ----------
    client, pad_code:
        Recorded on the manager for reference/reporting; backends hold their own
        client/pad (usually the same). Either may be ``None`` for offline use.
    backends:
        Iterable of :class:`Backend`. Order is preserved (Layer 1 before Layer 2
        is recommended so build props settle before the hook reads them).
    validate_before_apply:
        When true (default), :meth:`apply` raises
        :class:`~vmos.exceptions.ProfileValidationError` if the Profile has any
        ``error``-level issue — an invalid identity is never provisioned.
    """

    def __init__(
        self,
        client: Optional["VMOSClient"] = None,
        pad_code: Optional[str] = None,
        backends: Optional[List[Backend]] = None,
        *,
        validate_before_apply: bool = True,
    ) -> None:
        self.client = client
        self.pad_code = pad_code
        self.backends: List[Backend] = list(backends) if backends else []
        self.validate_before_apply = validate_before_apply

    def register(self, backend: Backend) -> "ProfileManager":
        """Add a backend; returns ``self`` for chaining."""
        self.backends.append(backend)
        return self

    # -- lifecycle ------------------------------------------------------- #
    def apply(self, profile: Profile) -> Dict[str, Any]:
        """Provision ``profile`` through every registered backend.

        Validates first (unless disabled), then runs each backend's
        :meth:`Backend.apply` in registration order, aggregating results.
        """
        issues = validate(profile)
        if self.validate_before_apply and any(i["level"] == "error" for i in issues):
            raise ProfileValidationError(issues)
        results: List[Dict[str, Any]] = []
        for backend in self.backends:
            results.append({
                "backend": backend.name, "layer": backend.layer,
                "result": backend.apply(profile),
            })
        return {
            "pad_code": self.pad_code,
            "profile": profile.meta.get("name", ""),
            "validation": issues,
            "backends": results,
        }

    def verify(self, profile: Profile) -> Dict[str, Any]:
        """Read back and diff ``profile`` through every backend.

        ``ok`` is the AND of every backend that reports an ``ok`` field.
        """
        results: List[Dict[str, Any]] = []
        ok = True
        for backend in self.backends:
            res = backend.verify(profile)
            if "ok" in res:
                ok = ok and bool(res["ok"])
            results.append({"backend": backend.name, "layer": backend.layer, "result": res})
        return {"pad_code": self.pad_code, "ok": ok, "backends": results}

    def remove(self, profile: Optional[Profile] = None) -> Dict[str, Any]:
        """Undo what the backends installed (best-effort).

        Pass ``profile`` so backends that need target packages (the Java hook)
        can unload the exact patches they created.
        """
        results: List[Dict[str, Any]] = []
        for backend in self.backends:
            if profile is not None and hasattr(backend, "remove_for"):
                results.append({"backend": backend.name, "result": backend.remove_for(profile)})
            else:
                results.append({"backend": backend.name, "result": backend.remove()})
        return {"pad_code": self.pad_code, "backends": results}


def standard_manager(
    client: "VMOSClient",
    pad_code: str,
    *,
    apk_url: Optional[str] = None,
    apk_path: Optional[str] = None,
    persist: bool = True,
    validate_before_apply: bool = True,
    auto_scope_all: bool = False,
    scope_denylist_extra: Optional[Iterable[str]] = None,
) -> ProfileManager:
    """A :class:`ProfileManager` wired with the two verified backends.

    Layer 1 (:class:`SystemApplierBackend`) then Layer 2
    (:class:`JavaHookBackend`) — the combined provisioning proven live. Provide
    ``apk_url``/``apk_path`` only when the XPose plugin needs (re)loading.

    Set ``auto_scope_all=True`` to have the Java Hook Backend scope **every
    installed app EXCEPT GMS/Play** (:data:`vmos.spoof.GMS_DENYLIST` plus
    ``scope_denylist_extra``) at apply time — the GMS-safe app-scoped model.
    """
    return ProfileManager(
        client, pad_code,
        backends=[
            SystemApplierBackend(client, pad_code, persist=persist),
            JavaHookBackend(client, pad_code, apk_url=apk_url, apk_path=apk_path,
                            persist_module=persist, auto_scope_all=auto_scope_all,
                            scope_denylist_extra=scope_denylist_extra),
        ],
        validate_before_apply=validate_before_apply,
    )
