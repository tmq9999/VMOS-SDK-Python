"""Device-profile spoofing toolkit for VMOS cloud **real devices**.

Turn one real-device instance into an arbitrary device profile — including
models VMOS's ADI-template catalog does not offer (e.g. a custom "Pixel 10 Pro
/ Android 17 / SDK 37") — for resellers who want a differentiated product.

Why this works (all verified live on a Pixel 7 Pro real device, 2026-07):

* The VMOS async ADB shell (`instance.async_cmd`) runs as **root**
  (`uid=0`, SELinux context ``u:r:xu_daemon:s0``) — no ``su`` grant needed.
* Kitsune Magisk (``io.github.huskydg.magisk``) ships ``resetprop``
  (``/data/adb/magisk/magisk64 resetprop``), which rewrites read-only
  ``ro.*`` build properties that the VMOS property API **cannot** change on a
  real device (per-key ``updatePadProperties`` is silently ignored there).

So the pipeline is: enable Kitsune Magisk once → ``resetprop`` the build
identity for the current session → drop a Magisk boot payload so the spoof
**survives reboots** → optionally set the legacy ``android_id``.

Prerequisite: **Kitsune Magisk must be enabled** on the instance (Toolbox →
Magisk (Mask) → ON). :func:`magisk_ready` checks this; :func:`enable_magisk_ui`
automates the Toolbox toggle when it is not yet on.

.. warning::
   Only spoofs software/``build.prop``-level identity. Hardware-backed
   attestation (TEE key attestation, Play Integrity STRONG) cannot be spoofed
   by any software method. Use for legitimate device-variety reselling and set
   realistic expectations with customers.
"""

from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:  # pragma: no cover
    from .client import VMOSClient

__all__ = [
    "DeviceProfile",
    "PadRootShell",
    "MAGISK_BIN",
    "apply_profile",
    "verify_profile",
    "remove_spoof",
    "magisk_ready",
    "enable_magisk_ui",
    "lsposed_ready",
    "enable_lsposed_ui",
    "PIXEL_10_PRO_A17",
]

# ---------------------------------------------------------------------------
# What is / isn't spoofable on a VMOS real device (live-verified 2026-07):
#
#   ✅ build.prop identity (ro.product.*, ro.build.*, version.release/sdk,
#      fingerprint)  -> resetprop (this toolkit). Persists via Magisk module.
#   ❌ IMEI          -> held by the RIL/telephony framework, NOT a system prop;
#      resetprop has no effect. `service call iphonesubinfo 1` is the oracle.
#   ❌ OAID          -> no shell/prop lever exposed.
#   ❌ android_id    -> `settings put secure android_id` is IGNORED on VMOS real
#      devices (verified, incl. --user 0). apply_profile still attempts it (works
#      on some virtual images) but verify_profile will report the truth.
#
# Deep IMEI / OAID / android_id spoofing therefore requires a framework hook:
# enable LSposed (enable_lsposed_ui) AND install an Xposed device-spoofing
# module (an APK that hooks TelephonyManager.getImei(), the OAID SDK, and
# Settings.Secure ANDROID_ID). VMOS's Kitsune ships the LSposed *framework*
# (Zygisk module `zygisk_lsposed`, `lspd` daemon) but no spoofing module and no
# readily-scriptable Manager UI, so that module step is out of scope here.
# ---------------------------------------------------------------------------

#: Kitsune Magisk main binary on VMOS real devices (exposes the ``resetprop`` applet).
MAGISK_BIN = "/data/adb/magisk/magisk64"
#: Magisk module id used for persistent boot-time spoofing.
MODULE_ID = "vmos_spoof"
_MODULE_DIR = f"/data/adb/modules/{MODULE_ID}"
_SERVICE_D = "/data/adb/service.d/99-vmos-spoof.sh"

# Android partitions whose per-partition product props also expose Build.MODEL etc.
# Setting all of them makes the spoof consistent against apps that read a specific
# partition's prop rather than the top-level ro.product.*.
_PARTITIONS = ("", "system.", "vendor.", "odm.", "product.", "system_ext.", "bootimage.")
_PRODUCT_FIELDS = ("brand", "manufacturer", "model", "device", "name")


def _sh_quote(value: str) -> str:
    """Single-quote a value for POSIX sh (safe for spaces, slashes, colons)."""
    return "'" + str(value).replace("'", "'\\''") + "'"


@dataclass
class DeviceProfile:
    """Target device identity to spoof onto a real-device instance.

    Only the fields you set are written. ``model`` is required; everything else
    is optional. ``deep=True`` (default) also writes the per-partition product
    props (``ro.product.system.model`` etc.) so the spoof is consistent across
    the many places Android exposes ``Build.MODEL`` / ``Build.BRAND``.
    """

    model: str
    brand: str = "google"
    manufacturer: Optional[str] = None
    device: Optional[str] = None
    product_name: Optional[str] = None
    fingerprint: Optional[str] = None
    release: Optional[str] = None            # ro.build.version.release  (e.g. "17")
    sdk: Optional[int] = None                # ro.build.version.sdk      (e.g. 37)
    security_patch: Optional[str] = None     # ro.build.version.security_patch
    android_id: Optional[str] = None         # 16-hex legacy Settings.Secure.ANDROID_ID
    extra_props: Dict[str, str] = field(default_factory=dict)
    deep: bool = True

    def build_props(self) -> "OrderedDict[str, str]":
        """Expand this profile into an ordered ``prop_key -> value`` map."""
        props: "OrderedDict[str, str]" = OrderedDict()
        fields = {
            "brand": self.brand,
            "manufacturer": self.manufacturer or self.brand,
            "model": self.model,
            "device": self.device,
            "name": self.product_name or self.device,
        }
        partitions = _PARTITIONS if self.deep else ("",)
        for part in partitions:
            for key in _PRODUCT_FIELDS:
                val = fields.get(key)
                if val:
                    props[f"ro.product.{part}{key}"] = val
        if self.fingerprint:
            for part in ("", "system.", "vendor.", "product."):
                props[f"ro.{part}build.fingerprint" if part else "ro.build.fingerprint"] = self.fingerprint
        if self.release is not None:
            props["ro.build.version.release"] = str(self.release)
            props["ro.build.version.release_or_codename"] = str(self.release)
        if self.sdk is not None:
            props["ro.build.version.sdk"] = str(self.sdk)
        if self.security_patch:
            props["ro.build.version.security_patch"] = self.security_patch
        props.update(self.extra_props)
        return props


# A ready-made example profile: a device VMOS does not offer in its catalog.
PIXEL_10_PRO_A17 = DeviceProfile(
    model="Pixel 10 Pro",
    brand="google",
    manufacturer="Google",
    device="frankel",
    product_name="frankel",
    fingerprint="google/frankel/frankel:17/BP1A.250101.001/13000000:user/release-keys",
    release="17",
    sdk=37,
    security_patch="2026-07-05",
)


class PadRootShell:
    """Run root shell commands on a real-device instance via ``instance.async_cmd``.

    The VMOS async command shell is already root on real devices, so no ``su``
    is used. Each call blocks until the async task reaches a terminal state and
    returns the command's stdout/stderr text.
    """

    def __init__(self, client: "VMOSClient", pad_code: str, *, poll_timeout: float = 60.0) -> None:
        self._client = client
        self.pad_code = pad_code
        self.poll_timeout = poll_timeout

    def sh(self, script: str) -> str:
        """Execute ``script`` in the instance's root shell; return its output."""
        resp = self._client.instance.async_cmd(pad_codes=[self.pad_code], script_content=script)
        task_id = resp[0].get("taskId") if isinstance(resp, list) and resp else None
        if task_id is None:
            raise RuntimeError(f"async_cmd did not return a taskId: {resp!r}")
        deadline = time.time() + self.poll_timeout
        while time.time() < deadline:
            info = self._client.tasks.pad_task_detail(task_ids=[task_id])[0]
            if info.get("taskStatus") in (3, -1, 4, 5):
                return (info.get("taskResult") or info.get("errorMsg") or "").strip()
            time.sleep(2)
        raise TimeoutError(f"command did not finish within {self.poll_timeout}s: {script[:60]!r}")

    def is_root(self) -> bool:
        return self.sh("id -u").strip().endswith("0")


def magisk_ready(shell: "PadRootShell") -> bool:
    """True when Kitsune Magisk's ``resetprop`` binary is present on the instance."""
    out = shell.sh(f"[ -x {MAGISK_BIN} ] && echo YES || echo NO")
    return "YES" in out


def resetprop_command(props: Dict[str, str]) -> str:
    """Build a single shell command that resetprops every ``props`` entry."""
    parts = [
        f"{MAGISK_BIN} resetprop -n {_sh_quote(k)} {_sh_quote(v)}"
        for k, v in props.items()
    ]
    return " ; ".join(parts)


def _service_script(props: Dict[str, str], android_id: Optional[str]) -> str:
    lines = [
        "#!/system/bin/sh",
        "# Generated by vmos.spoof — persistent device-profile spoof (runs at boot).",
        'until [ "$(getprop sys.boot_completed)" = "1" ]; do sleep 2; done',
    ]
    for k, v in props.items():
        lines.append(f"{MAGISK_BIN} resetprop -n {_sh_quote(k)} {_sh_quote(v)}")
    if android_id:
        lines.append(f"settings put secure android_id {_sh_quote(android_id)}")
    return "\n".join(lines) + "\n"


def _module_prop() -> str:
    return (
        f"id={MODULE_ID}\n"
        "name=VMOS Device Spoof\n"
        "version=v1.0\n"
        "versionCode=1\n"
        "author=vmos-sdk\n"
        "description=Persistent build.prop device-identity spoof for reseller profiles.\n"
    )


def _write_file(shell: "PadRootShell", path: str, content: str, *, mode: str = "0644") -> None:
    """Write a file on the instance using a heredoc (root shell)."""
    # 'EOF' quoted so the payload is written verbatim (no shell expansion).
    shell.sh(f"mkdir -p {_sh_quote(path.rsplit('/', 1)[0])}")
    shell.sh(f"cat > {_sh_quote(path)} <<'VMOS_EOF'\n{content}VMOS_EOF\nchmod {mode} {_sh_quote(path)}")


def install_persistence(shell: "PadRootShell", profile: "DeviceProfile") -> None:
    """Install boot-time persistence via BOTH a Magisk ``service.d`` script and a
    module ``system.prop`` (whichever Magisk processes first wins; both are safe)."""
    props = profile.build_props()
    # 1) General Magisk boot script (run on every boot by magiskd).
    _write_file(shell, _SERVICE_D, _service_script(props, profile.android_id), mode="0755")
    # 2) Magisk module with system.prop (applied very early, before apps start).
    system_prop = "".join(f"{k}={v}\n" for k, v in props.items())
    _write_file(shell, f"{_MODULE_DIR}/module.prop", _module_prop())
    _write_file(shell, f"{_MODULE_DIR}/system.prop", system_prop)
    if profile.android_id:
        _write_file(
            shell,
            f"{_MODULE_DIR}/service.sh",
            "#!/system/bin/sh\n"
            'until [ "$(getprop sys.boot_completed)" = "1" ]; do sleep 2; done\n'
            f"settings put secure android_id {_sh_quote(profile.android_id)}\n",
            mode="0755",
        )
    # Ensure module is enabled (no disable/remove flags).
    shell.sh(f"rm -f {_MODULE_DIR}/disable {_MODULE_DIR}/remove 2>/dev/null; touch {_MODULE_DIR}/update 2>/dev/null; true")


def apply_profile(
    client: "VMOSClient",
    pad_code: str,
    profile: "DeviceProfile",
    *,
    persist: bool = True,
    set_android_id: bool = True,
) -> Dict[str, Any]:
    """Apply ``profile`` to a real-device instance.

    Steps: verify root + Magisk → ``resetprop`` the build identity for the live
    session → (optional) set ``android_id`` → (optional) install boot
    persistence. Returns a summary dict; raises :class:`RuntimeError` if the
    instance is not a rooted Magisk real device.
    """
    shell = PadRootShell(client, pad_code)
    if not shell.is_root():
        raise RuntimeError("instance shell is not root — is this a real-device instance?")
    if not magisk_ready(shell):
        raise RuntimeError(
            "Kitsune Magisk not enabled (no resetprop). Enable it first: Toolbox -> "
            "Magisk (Mask) -> ON, or call enable_magisk_ui()."
        )
    props = profile.build_props()
    shell.sh(resetprop_command(props))
    if set_android_id and profile.android_id:
        # NOTE: verified ineffective on VMOS real devices (settings write ignored);
        # kept for virtual images. Trust verify_profile for the real outcome.
        shell.sh(f"settings put secure android_id {_sh_quote(profile.android_id)}")
    if persist:
        install_persistence(shell, profile)
    return {"pad_code": pad_code, "applied": len(props), "persisted": persist,
            "android_id_attempted": bool(profile.android_id and set_android_id),
            "android_id_note": "settings write is ignored on VMOS real devices; "
                               "needs an LSposed spoofing module"}


def verify_profile(client: "VMOSClient", pad_code: str, profile: "DeviceProfile") -> Dict[str, Any]:
    """Read back the live props via ``getprop`` and compare to the profile.

    Returns ``{"ok": bool, "checks": {key: {"want", "got", "match"}}}`` for the
    top-level identity props (ignores the per-partition duplicates)."""
    shell = PadRootShell(client, pad_code)
    checks: Dict[str, Any] = {}
    want = OrderedDict()
    want["ro.product.model"] = profile.model
    want["ro.product.brand"] = profile.brand
    if profile.release is not None:
        want["ro.build.version.release"] = str(profile.release)
    if profile.sdk is not None:
        want["ro.build.version.sdk"] = str(profile.sdk)
    if profile.fingerprint:
        want["ro.build.fingerprint"] = profile.fingerprint
    script = " ; ".join(f'echo "{k}=$(getprop {k})"' for k in want)
    out = shell.sh(script)
    got = {}
    for line in out.splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            got[k.strip()] = v.strip()
    all_ok = True
    for k, wv in want.items():
        gv = got.get(k, "")
        match = gv == str(wv)
        all_ok = all_ok and match
        checks[k] = {"want": wv, "got": gv, "match": match}
    if profile.android_id:
        gv = shell.sh("settings get secure android_id").strip()
        match = gv == profile.android_id
        all_ok = all_ok and match
        checks["android_id"] = {"want": profile.android_id, "got": gv, "match": match}
    return {"ok": all_ok, "checks": checks}


def remove_spoof(client: "VMOSClient", pad_code: str) -> None:
    """Remove the persistent spoof payload (module + service.d). Runtime props
    reset on the next reboot; call with a genuine profile to fully restore."""
    shell = PadRootShell(client, pad_code)
    shell.sh(f"rm -f {_SERVICE_D}; rm -rf {_MODULE_DIR}; true")


# --------------------------------------------------------------------------- #
# Toolbox UI automation to enable Kitsune Magisk on a fresh instance.
# Coordinates are resolution-relative; verify with a screenshot if the Toolbox
# layout differs on your image version.
# --------------------------------------------------------------------------- #
def enable_magisk_ui(client: "VMOSClient", pad_code: str, *, settle: float = 30.0) -> bool:
    """Best-effort headless enable of Kitsune Magisk via the Toolbox UI.

    Launches Toolbox, scrolls to the Magisk (Mask) toggle, taps it and confirms
    the reminder dialog. Returns True if Magisk becomes ready afterward. If the
    Toolbox layout differs, drive the taps manually with ``instance.screenshot``
    + ``touch.simulate_click`` / an ``input tap`` via ``async_cmd``.
    """
    shell = PadRootShell(client, pad_code)
    if magisk_ready(shell):
        return True
    size = shell.sh("wm size")  # e.g. "Physical size: 1440x3120"
    try:
        w, h = (int(x) for x in size.split(":")[-1].strip().split("x"))
    except Exception:  # noqa: BLE001
        w, h = 1440, 3120
    shell.sh("am start -n com.android.expansiontools/com.android.tools.home.MainActivity")
    time.sleep(4)
    # Scroll down to reveal the Magisk (Mask) toggle.
    for _ in range(3):
        client.touch.simulate_swipe(
            [pad_code], direction="BOTTOM_TO_TOP",
            start_x=w // 2, start_y=int(h * 0.78), end_x=w // 2, end_y=int(h * 0.22),
            width=w, height=h,
        )
        time.sleep(2)
    # The Magisk (Mask) toggle sits near the right edge of its row; exact y varies,
    # so tap via input tap using observed ratios (right ~86% width).
    shell.sh(f"input tap {int(w * 0.86)} {int(h * 0.345)}")
    time.sleep(2)
    # Confirm the "Kind Reminder" dialog (Confirm button ~ right-center, ~55% height).
    shell.sh(f"input tap {int(w * 0.67)} {int(h * 0.557)}")
    time.sleep(settle)
    return magisk_ready(shell)


def lsposed_ready(shell: "PadRootShell") -> bool:
    """True when the LSposed framework is active (``lspd`` daemon + zygisk module)."""
    out = shell.sh(
        "ls -d /data/adb/modules/zygisk_lsposed /data/adb/lspd 2>/dev/null; "
        "ps -A 2>/dev/null | grep -c '[l]spd'"
    )
    return "zygisk_lsposed" in out or "/data/adb/lspd" in out


def enable_lsposed_ui(client: "VMOSClient", pad_code: str, *, reboot: bool = True) -> bool:
    """Best-effort headless enable of the LSposed framework via the Toolbox UI.

    Requires Kitsune Magisk to be enabled first (LSposed depends on it). Toggles
    the "Lsposed" switch (just below "Magisk (Mask)"), confirms the reminder
    dialog and — because LSposed loads through Zygisk at boot — restarts the
    instance so the framework activates.

    .. note::
       This only installs the LSposed **framework**. To actually spoof IMEI /
       OAID / android_id you must additionally install and activate an Xposed
       device-spoofing **module** (an APK) through the LSposed Manager — that
       module is not shipped by VMOS and is outside this toolkit's scope.
    """
    shell = PadRootShell(client, pad_code)
    if not magisk_ready(shell):
        raise RuntimeError("Enable Kitsune Magisk first (LSposed depends on it).")
    if lsposed_ready(shell):
        return True
    size = shell.sh("wm size")
    try:
        w, h = (int(x) for x in size.split(":")[-1].strip().split("x"))
    except Exception:  # noqa: BLE001
        w, h = 1440, 3120
    shell.sh("am start -n com.android.expansiontools/com.android.tools.home.MainActivity")
    time.sleep(4)
    for _ in range(3):
        client.touch.simulate_swipe(
            [pad_code], direction="BOTTOM_TO_TOP",
            start_x=w // 2, start_y=int(h * 0.78), end_x=w // 2, end_y=int(h * 0.22),
            width=w, height=h,
        )
        time.sleep(2)
    # "Lsposed" toggle sits one row below Magisk (~43% height on the scrolled view).
    shell.sh(f"input tap {int(w * 0.86)} {int(h * 0.43)}")
    time.sleep(2)
    shell.sh(f"input tap {int(w * 0.67)} {int(h * 0.55)}")  # Confirm dialog
    time.sleep(5)
    if reboot:
        try:
            client.instance.restart(pad_codes=[pad_code])
        except Exception:  # noqa: BLE001
            pass
        time.sleep(90)
        for _ in range(8):
            if shell.sh("getprop sys.boot_completed").strip() == "1":
                break
            time.sleep(15)
    return lsposed_ready(shell)
