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

import base64
import os
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional

from .exceptions import VMOSAPIError

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
    "enable_magisk_headless",
    "query_magisk_payload_url",
    "MAGISK_OSS_QUERY_URL",
    "lsposed_ready",
    "enable_lsposed_ui",
    "scope_lsposed_module",
    "set_identity_props",
    "load_xpose_plugin",
    "list_xpose_plugins",
    "remove_xpose_plugin",
    "GMS_EXCLUDED_PACKAGES",
    "PIXEL_10_PRO_A17",
    "PIXEL_10_A17",
    "PIXEL_10_PRO_XL_A17",
    # Headless root-stack (Magisk + Zygisk-Next + LSPosed) — verified sequence.
    "install_root_stack_headless",
    "stage_root_stack_install",
    "verify_root_stack",
    "wait_for_file_download",
    "wait_for_pad_ready",
    "pad_online",
    "wait_for_pad_online",
    "resolve_pad_code",
    "coerce_task_ids",
    "PAD_NOT_READY_CODE",
    "ROOT_STACK_MODULES",
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
# Deep IMEI / IMSI / ICCID / android_id spoofing therefore requires a framework
# hook — an APK that hooks TelephonyManager.getImei()/getSubscriberId()/... and
# Settings.Secure ANDROID_ID inside the target app. Two supported paths:
#
#   1. PRIVATE XPose plugin (recommended) — VMOS ships its native XPose
#      framework in-image (`/system/bin/apmt`, confirmed working), so a plugin
#      built against its API is ALWAYS compatible and fully private. Build the
#      plugin in `xpose_plugin/`, then load it headlessly with
#      `load_xpose_plugin()` + `set_identity_props()` (below). See
#      docs/en/xpose-custom-hook.md.
#   2. LSposed module — enable the framework (enable_lsposed_ui), install a
#      spoof module APK, and scope it (scope_lsposed_module). The framework
#      bundled with VMOS's Kitsune is OLD (libxposed API mismatch), so a fresh
#      LSPosed manager must replace it first; the private XPose path avoids this.
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


def coerce_task_ids(task_ids: Any) -> List[int]:
    """Normalize a task-id container to a flat list of **integers**.

    VMOS's ``padTaskDetail`` / ``fileTaskDetail`` accept **only** the integer-array
    body ``{"taskIds":[<int>, ...]}``. The object form
    ``{"taskIds":[{"taskId":N}]}`` is rejected with ``code=100013``
    (参数类型或格式错误) — a real-device-verified gotcha. This coerces the shapes
    callers commonly produce (a bare int, a list of ints, or a list of
    ``{"taskId": N}`` dicts) into the accepted integer array, so every task-detail
    call in this module is submitted in the correct format.
    """
    if task_ids is None:
        return []
    if isinstance(task_ids, (str, bytes, int)) or not isinstance(task_ids, (list, tuple, set)):
        task_ids = [task_ids]
    out: List[int] = []
    for item in task_ids:
        if isinstance(item, dict):
            item = item.get("taskId")
        if item is None:
            continue
        out.append(int(item))
    return out


#: VMOS async-task status enum. ``1`` pending, ``2`` running, ``3`` complete;
#: negatives are failures (``-1`` all-failed, ``-2`` partial, ``-3`` cancelled,
#: ``-4`` timeout). ``4``/``5`` are tolerated as terminal for older image variants.
def _task_terminal(status: Any) -> bool:
    """True when an async task has reached a terminal state (success or failure)."""
    if status == 3 or status in (4, 5):
        return True
    return isinstance(status, int) and status < 0


#: Business code returned by ``asyncCmd`` while an instance is still rebooting /
#: not yet ready (``实例状态未就绪``). Tolerated (retried) by :func:`wait_for_pad_ready`.
PAD_NOT_READY_CODE = 110031

#: On-device Magisk module directory ids installed by ``install_modules.sh``:
#: ``zygisksu`` = Zygisk-Next, ``zygisk_lsposed`` = LSPosed (JingMatrix fork).
ROOT_STACK_MODULES = ("zygisksu", "zygisk_lsposed")


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
        if self.device:
            # Build.BOARD / Build.HARDWARE track the device codename on Pixels
            # (e.g. cheetah->cheetah). Keep them consistent with ro.product.*.device
            # so an app doesn't see model=blazer but board/hardware=cheetah.
            # (ro.board.platform is the SoC name; set it via extra_props per model.)
            props["ro.product.board"] = self.device
            props["ro.hardware"] = self.device
            props["ro.boot.hardware"] = self.device
        props.update(self.extra_props)
        return props


# Ready-made presets — REAL fingerprints from the authoritative Pixel-Props/build.prop
# dataset (release 20260711, CP2A.260705.006 = Android 17 / SDK 37). Codenames:
# blazer = Pixel 10 Pro, frankel = Pixel 10, mustang = Pixel 10 Pro XL.
PIXEL_10_PRO_A17 = DeviceProfile(
    model="Pixel 10 Pro",
    brand="google",
    manufacturer="Google",
    device="blazer",
    product_name="blazer",
    fingerprint="google/blazer/blazer:17/CP2A.260705.006/15641320:user/release-keys",
    release="17",
    sdk=37,
    security_patch="2026-07-05",
)

#: Pixel 10 (base, codename frankel) — Android 17 / SDK 37.
PIXEL_10_A17 = DeviceProfile(
    model="Pixel 10", brand="google", manufacturer="Google",
    device="frankel", product_name="frankel",
    fingerprint="google/frankel/frankel:17/CP2A.260705.006/15641320:user/release-keys",
    release="17", sdk=37, security_patch="2026-07-05",
)

#: Pixel 10 Pro XL (codename mustang) — Android 17 / SDK 37.
PIXEL_10_PRO_XL_A17 = DeviceProfile(
    model="Pixel 10 Pro XL", brand="google", manufacturer="Google",
    device="mustang", product_name="mustang",
    fingerprint="google/mustang/mustang:17/CP2A.260705.006/15641320:user/release-keys",
    release="17", sdk=37, security_patch="2026-07-05",
)


class PadRootShell:
    """Run root shell commands on a real-device instance via ``instance.async_cmd``.

    The VMOS async command shell is already root on real devices, so no ``su``
    is used. Each call blocks until the async task reaches a terminal state and
    returns the command's stdout/stderr text.
    """

    def __init__(
        self,
        client: "VMOSClient",
        pad_code: str,
        *,
        poll_timeout: float = 60.0,
        poll_interval: float = 2.0,
    ) -> None:
        self._client = client
        self.pad_code = pad_code
        self.poll_timeout = poll_timeout
        self.poll_interval = poll_interval

    def sh(self, script: str) -> str:
        """Execute ``script`` in the instance's root shell; return its output.

        Polls ``padTaskDetail`` with the integer-array body form
        (``{"taskIds":[<int>]}``) required by the gateway — the object form is
        rejected with ``code=100013`` (see :func:`coerce_task_ids`).
        """
        resp = self._client.instance.async_cmd(pad_codes=[self.pad_code], script_content=script)
        task_id = resp[0].get("taskId") if isinstance(resp, list) and resp else None
        if task_id is None:
            raise RuntimeError(f"async_cmd did not return a taskId: {resp!r}")
        deadline = time.time() + self.poll_timeout
        while time.time() < deadline:
            info = self._client.tasks.pad_task_detail(task_ids=coerce_task_ids(task_id))[0]
            if _task_terminal(info.get("taskStatus")):
                return (info.get("taskResult") or info.get("errorMsg") or "").strip()
            time.sleep(self.poll_interval)
        raise TimeoutError(f"command did not finish within {self.poll_timeout}s: {script[:60]!r}")

    def is_root(self) -> bool:
        return self.sh("id -u").strip().endswith("0")


def magisk_ready(shell: "PadRootShell") -> bool:
    """True when Kitsune Magisk's ``resetprop`` binary is present on the instance."""
    out = shell.sh(f"[ -x {MAGISK_BIN} ] && echo YES || echo NO")
    return "YES" in out


#: VMOS/ArmCloud cloud-Magisk OSS payload record endpoint. Queried directly from
#: the pad; live-verified to need **no auth** (``createBy: "no_auth"``).
MAGISK_OSS_QUERY_URL = "https://openapi-hk.armcloud.net/openapi/open/magisk/rom/oss/record/query"

#: Compact on-pad **download** script for :func:`enable_magisk_headless` — ``curl``
#: the payload ``.gz`` into ``$WORKDIR`` and report only the return code + size (the
#: verbose transfer log is discarded to stay under the async_cmd output cap). The
#: extract/install steps run separately via :func:`stage_root_stack_install` so the
#: two entry points (curl download vs. ``uploadFileV3``) share one install path.
#: ``__URL__`` / ``__WORKDIR__`` are substituted before sending.
_MAGISK_DOWNLOAD_SH = (
    'WORKDIR=__WORKDIR__; mkdir -p "$WORKDIR"; '
    'curl -sk --max-time 180 -o "$WORKDIR/magisk_payload.gz" "__URL__" >/dev/null 2>&1; '
    'echo "DL_RC=$? SIZE=$(wc -c < "$WORKDIR/magisk_payload.gz" 2>/dev/null)"'
)


def query_magisk_payload_url(shell: "PadRootShell", pad_code: str) -> str:
    """Return the cloud-Magisk ``.gz`` payload URL from the OSS record.

    Queried **on the pad** (which sits in ArmCloud's network) via ``curl``; the
    endpoint needs no auth. Raises if no ``.gz`` URL is found.
    """
    body = '{"padCode":"%s"}' % pad_code
    cmd = (
        "curl -sk --max-time 30 -X POST %s -H 'Content-Type: application/json' -d %s "
        "| grep -oE 'https://[^\"]+\\.gz' | head -1"
        % (_sh_quote(MAGISK_OSS_QUERY_URL), _sh_quote(body))
    )
    out = shell.sh(cmd).strip()
    url = out.splitlines()[0].strip() if out else ""
    if not (url.startswith("https://") and url.endswith(".gz")):
        raise RuntimeError(f"could not obtain a Magisk payload .gz URL (got {out[:120]!r})")
    return url


def enable_magisk_headless(
    client: "VMOSClient",
    pad_code: str,
    *,
    payload_url: Optional[str] = None,
    workdir: str = "/debug_ramdisk",
    restart: bool = False,
    install_modules: bool = True,
) -> Dict[str, Any]:
    """Install cloud Magisk (+ Zygisk-Next + LSPosed) **headlessly** via an on-pad
    ``curl`` download — no Toolbox UI, no ``switchRoot``, no ``su``.

    This is the ``curl``-download variant. For the full real-device-verified flow
    (``uploadFileV3`` download + md5 wait + restart + active-state verification)
    prefer :func:`install_root_stack_headless`.

    The VMOS async shell already runs as ``uid=0`` (``u:r:xu_daemon:s0``), which is
    enough to drop the cloud-Magisk payload into ``workdir`` and install it:

    1. Obtain the payload ``.gz`` URL (``payload_url`` or an on-pad OSS query).
    2. ``curl`` it onto the pad.
    3. Extract to ``workdir`` and run ``install.sh`` **and** (``install_modules=True``,
       the default) ``install_modules.sh`` — the latter stages Zygisk-Next +
       LSPosed. Success is verified by an on-device **state check** (Magisk prop,
       binaries, module dirs), not by parsing the truncatable task output.
    4. ``resetprop`` works **immediately**; the Magisk daemon / Zygisk / LSPosed
       activate only after a reboot — pass ``restart=True`` for that.

    Returns a summary dict (``installed`` is the overall state-verified result).
    """
    shell = PadRootShell(client, pad_code, poll_timeout=200.0)
    if not shell.is_root():
        raise RuntimeError("instance shell is not root — is this a real-device instance?")
    if magisk_ready(shell):
        return {"pad_code": pad_code, "already_installed": True}
    # writability check (proves the no-switchRoot root can install)
    pv = shell.sh(f"mkdir -p {workdir} && touch {workdir}/.vmos_rw && echo RW=$? && rm -f {workdir}/.vmos_rw")
    if "RW=0" not in pv:
        raise RuntimeError(f"{workdir} not writable by the async shell: {pv.strip()[:120]}")
    url = payload_url or query_magisk_payload_url(shell, pad_code)
    # 1-2. Download the payload onto the pad (compact output).
    dl = shell.sh(_MAGISK_DOWNLOAD_SH.replace("__URL__", url).replace("__WORKDIR__", workdir))
    if "DL_RC=0" not in dl:
        raise RuntimeError(f"payload download failed: {dl.strip()[:160]}")
    # 3. Extract + install (+ modules); verify by on-device state (Bug-fix #3 + GAP fix).
    install = stage_root_stack_install(
        shell,
        payload_path=workdir.rstrip("/") + "/magisk_payload.gz",
        workdir=workdir,
        install_modules=install_modules,
    )
    result: Dict[str, Any] = {
        "pad_code": pad_code,
        "payload_url": url,
        "installed": install["ok"],
        "magisk_cloud_prop": install["magisk_prop"] or "?",
        "install_rc": install["install_rc"],
        "modules_rc": install["modules_rc"],
        "binaries": install["binaries"],
        "modules": install["modules"],
        "log_tail": install["log_tail"],
    }
    if install["ok"] and restart:
        client.instance.restart(pad_codes=[pad_code])
        result["restart_requested"] = True
    return result


# --------------------------------------------------------------------------- #
# Headless root-stack (Magisk + Zygisk-Next + LSPosed) — real-device-verified.
#
# The known-good sequence (P2-ARCH-001 / P4-DEV-001), encoded in
# :func:`install_root_stack_headless`, avoids three real-device-verified traps:
#
#   * Bug #1 — task polling MUST use the integer-array body {"taskIds":[<int>]}
#     (see :func:`coerce_task_ids`); the object form returns code=100013.
#   * Bug #2 — fileTaskDetail returns data:null for uploadFileV3 tasks on this
#     tenant, so completion is detected by polling the file's md5/size ON the
#     device (:func:`wait_for_file_download`).
#   * Bug #3 — VMOS truncates async task output, so install success is verified by
#     a separate compact **state** check (:func:`stage_root_stack_install` /
#     :func:`verify_root_stack`), not by parsing verbose install output.
# --------------------------------------------------------------------------- #

def _kv(out: str, key: str) -> str:
    """Return the value of the first ``KEY=value`` line in ``out`` (or "")."""
    prefix = key + "="
    for line in out.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return ""


def _download_probe_script(remote_path: str) -> str:
    """Compact on-device probe: emit ``SIZE=`` and ``MD5=`` for ``remote_path``."""
    path = _sh_quote(remote_path)
    return (
        f'f={path}; '
        'if [ -s "$f" ]; then '
        'echo "SIZE=$(wc -c < "$f" 2>/dev/null)"; '
        "echo \"MD5=$(md5sum \"$f\" 2>/dev/null | cut -d' ' -f1)\"; "
        'else echo "SIZE=0"; echo "MD5="; fi'
    )


def _parse_download_probe(out: str) -> "tuple":
    size_text = _kv(out, "SIZE")
    try:
        size = int(size_text or 0)
    except ValueError:
        size = 0
    return size, _kv(out, "MD5")


def wait_for_file_download(
    shell: "PadRootShell",
    remote_path: str,
    *,
    expected_md5: Optional[str] = None,
    expected_size: Optional[int] = None,
    timeout: float = 240.0,
    interval: float = 5.0,
    stable_polls: int = 2,
) -> Dict[str, Any]:
    """Wait until ``remote_path`` has finished downloading **on the device**.

    Bug-fix #2: ``uploadFileV3`` downloads are asynchronous (~tens of seconds for
    the ~27 MB payload) and ``fileTaskDetail`` returns ``data: null`` for these
    tasks on this tenant — so it cannot signal completion. Instead this polls the
    file directly via ``async_cmd``:

    * if ``expected_md5`` is given → ready when the on-device ``md5sum`` matches;
    * else if ``expected_size`` is given → ready when the byte size matches and is
      stable across ``stable_polls`` consecutive polls;
    * else → ready when the size is non-zero and stable across ``stable_polls`` polls.

    Returns ``{"ready", "size", "md5", "polls", "detail"}``; never raises on a
    not-yet-ready file (returns ``ready=False`` at timeout).
    """
    want_md5 = expected_md5.lower() if expected_md5 else None
    script = _download_probe_script(remote_path)
    deadline = time.time() + timeout
    last_size = -1
    stable = 0
    size = 0
    md5 = ""
    polls = 0
    while time.time() < deadline:
        polls += 1
        size, md5 = _parse_download_probe(shell.sh(script))
        if want_md5 is not None:
            if md5 and md5.lower() == want_md5:
                return {"ready": True, "size": size, "md5": md5, "polls": polls, "detail": "md5-match"}
        else:
            if size > 0 and size == last_size:
                stable += 1
                if (expected_size is None or size == expected_size) and stable >= stable_polls:
                    return {"ready": True, "size": size, "md5": md5, "polls": polls, "detail": "size-stable"}
            else:
                stable = 0
        last_size = size
        time.sleep(interval)
    return {"ready": False, "size": size, "md5": md5, "polls": polls, "detail": "timeout"}


def _stage_install_script(payload_path: str, workdir: str, install_modules: bool) -> str:
    """Build the compact extract+install script (Bug-fix #3: verify by state).

    Verbose ``install.sh`` / ``install_modules.sh`` output is redirected to
    on-device log files (VMOS truncates ``taskResult``, so scanning verbose output
    for a completion marker yields false failures). Success is proven by the
    compact state lines emitted at the end. ``install.sh`` sets
    ``ro.sys.cloud.magisk=1`` and installs Magisk to ``/data/adb``;
    ``install_modules.sh`` installs Zygisk-Next + LSPosed (guarded by the prop).
    """
    payload = _sh_quote(payload_path)
    wd = _sh_quote(workdir)
    lines = [
        "set -u",
        f"WORKDIR={wd}",
        f"PAYLOAD={payload}",
        'cd "$WORKDIR" 2>/dev/null || { echo NO_WORKDIR; exit 91; }',
        'test -s "$PAYLOAD" || { echo NO_PAYLOAD; exit 90; }',
        "rm -rf init magisk_env",
        'tar -xf "$PAYLOAD" > "$WORKDIR/extract.log" 2>&1 || { echo EXTRACT_FAIL; tail -3 "$WORKDIR/extract.log"; exit 92; }',
        "test -f magisk_env/install.sh || { echo NO_INSTALL_SH; exit 93; }",
        "chmod 755 magisk_env/*.sh 2>/dev/null",
        'sh magisk_env/install.sh > "$WORKDIR/install.log" 2>&1; echo "INSTALL_RC=$?"',
    ]
    if install_modules:
        lines.append('sh magisk_env/install_modules.sh > "$WORKDIR/modules.log" 2>&1; echo "MODULES_RC=$?"')
    lines.append('echo "PROP=$(getprop ro.sys.cloud.magisk)"')
    lines.append(
        "for f in magisk64 magisk32 magiskpolicy magiskboot busybox; do "
        '[ -x /data/adb/magisk/$f ] && echo "BIN_OK=$f" || echo "BIN_MISS=$f"; done'
    )
    if install_modules:
        lines.append(
            "for m in zygisksu zygisk_lsposed; do "
            '[ -e /data/adb/modules/$m ] && echo "MOD_OK=$m" || echo "MOD_MISS=$m"; done'
        )
    lines.append("echo STAGE_DONE")
    return "\n".join(lines) + "\n"


def stage_root_stack_install(
    shell: "PadRootShell",
    *,
    payload_path: str = "/sdcard/Download/magisk_payload.gz",
    workdir: str = "/debug_ramdisk",
    install_modules: bool = True,
) -> Dict[str, Any]:
    """Extract the payload and run ``install.sh`` (+ ``install_modules.sh``) on device.

    Bug-fix #3: verbose installer output is redirected to on-device logs and
    success is verified by a **separate compact state check** — the Magisk prop
    (``ro.sys.cloud.magisk``), the five Magisk binaries under ``/data/adb/magisk``,
    and the Zygisk-Next / LSPosed module dirs under ``/data/adb/modules`` — rather
    than by parsing the truncatable ``taskResult`` for a marker.

    Returns ``{"ok", "install_rc", "modules_rc", "magisk_prop", "binaries",
    "modules", "log_tail"}``.
    """
    out = shell.sh(_stage_install_script(payload_path, workdir, install_modules))

    def _rc(marker: str) -> Optional[int]:
        text = _kv(out, marker)
        if not text:
            return None
        try:
            return int(text)
        except ValueError:
            return None

    prop = _kv(out, "PROP")
    binaries = {b: (f"BIN_OK={b}" in out) for b in ("magisk64", "magisk32", "magiskpolicy", "magiskboot", "busybox")}
    modules = {m: (f"MOD_OK={m}" in out) for m in ROOT_STACK_MODULES}
    install_rc = _rc("INSTALL_RC")
    modules_rc = _rc("MODULES_RC") if install_modules else None
    ok = (
        "STAGE_DONE" in out
        and install_rc == 0
        and prop == "1"
        and all(binaries.values())
        and (not install_modules or (modules_rc == 0 and all(modules.values())))
    )
    return {
        "ok": ok,
        "install_rc": install_rc,
        "modules_rc": modules_rc,
        "magisk_prop": prop,
        "binaries": binaries,
        "modules": modules,
        "log_tail": out.strip()[-600:],
    }


def _verify_script() -> str:
    """Compact post-reboot verification script (fits the async_cmd byte cap)."""
    return (
        'echo "PROP=$(getprop ro.sys.cloud.magisk)"\n'
        'echo "MAGISKVER=$(/data/adb/magisk/magisk64 -v 2>/dev/null || echo NONE)"\n'
        'echo "BOOT=$(getprop sys.boot_completed)"\n'
        '(ps -A 2>/dev/null || ps 2>/dev/null) | grep -w lspd >/dev/null 2>&1 && echo "LSPD=running" || echo "LSPD=absent"\n'
        '(ps -A 2>/dev/null || ps 2>/dev/null) | grep -q "zn-nsdaemon" && echo "ZN=running" || echo "ZN=absent"\n'
        "for m in zygisksu zygisk_lsposed; do "
        "if [ -e /data/adb/modules/$m ] && [ ! -f /data/adb/modules/$m/disable ] "
        "&& [ ! -f /data/adb/modules/$m/remove ]; then echo \"MOD_ENABLED=$m\"; "
        'else echo "MOD_OFF=$m"; fi; done\n'
        "echo VERIFY_DONE\n"
    )


def verify_root_stack(shell: "PadRootShell") -> Dict[str, Any]:
    """Verify (post-reboot) that Magisk + Zygisk-Next + LSPosed are truly **active**.

    Gates (all required for ``ok``):

    1. ``ro.sys.cloud.magisk == 1`` (persists across reboot — confirmed) and
       ``magisk64 -v`` returns a version.
    2. Zygisk-Next module enabled (``/data/adb/modules/zygisksu`` present, no
       ``disable``/``remove`` flag).
    3. LSPosed module enabled (``/data/adb/modules/zygisk_lsposed``).
    4. The ``lspd`` daemon is running (``ps -A | grep -w lspd``) — the decisive
       "LSPosed is ON" signal; a running ``lspd`` can only be forked once Zygisk
       loaded LSPosed into zygote, so it transitively proves Zygisk-Next is active.

    Returns a dict of gate results plus the trimmed raw output.
    """
    out = shell.sh(_verify_script())
    prop = _kv(out, "PROP")
    magisk_ver = _kv(out, "MAGISKVER")
    modules_enabled = {m: (f"MOD_ENABLED={m}" in out) for m in ROOT_STACK_MODULES}
    lspd_running = "LSPD=running" in out
    zygisk_next_running = "ZN=running" in out
    magisk_active = prop == "1" and bool(magisk_ver) and magisk_ver != "NONE"
    ok = (
        magisk_active
        and lspd_running
        and modules_enabled["zygisksu"]
        and modules_enabled["zygisk_lsposed"]
    )
    return {
        "ok": ok,
        "magisk_active": magisk_active,
        "magisk_prop": prop,
        "magisk_version": magisk_ver,
        "lspd_running": lspd_running,
        "zygisk_next_running": zygisk_next_running,
        "modules_enabled": modules_enabled,
        "boot_completed": _kv(out, "BOOT"),
        "raw": out.strip()[-600:],
    }


def _iter_pad_records(value: Any) -> Iterable[Dict[str, Any]]:
    """Yield pad-record dicts (those carrying ``padCode``/``*Status``) from a response."""
    if isinstance(value, dict):
        if "cvmStatus" in value or "vmStatus" in value or "padCode" in value:
            yield value
        for nested in value.values():
            yield from _iter_pad_records(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            yield from _iter_pad_records(nested)


def pad_online(client: "VMOSClient", pad_code: str) -> bool:
    """True when ``pad_code`` reports online in ``userPadList``.

    Uses the **verified working** body form ``{"padCodes":[<str>]}`` (plural key,
    array value), passed via ``**extra`` because the generated wrapper exposes only
    singular ``padCode`` (the external harness's ``{"padCode":[...]}`` form is
    wrong). Online = ``cvmStatus == 100`` (tenant-observed) OR ``vmStatus == 1``
    (documented); both are accepted.
    """
    data = client.phone.user_pad_list(padCodes=[pad_code])
    for record in _iter_pad_records(data):
        code = str(record.get("padCode") or record.get("pad_code") or "")
        if code and code != pad_code:
            continue
        for field_name, online_value in (("cvmStatus", 100), ("vmStatus", 1)):
            raw = record.get(field_name)
            if raw is None:
                continue
            try:
                if int(raw) == online_value:
                    return True
            except (TypeError, ValueError):
                continue
    return False


def wait_for_pad_online(
    client: "VMOSClient",
    pad_code: str,
    *,
    timeout: float = 300.0,
    interval: float = 5.0,
) -> bool:
    """Poll :func:`pad_online` until the instance is online or ``timeout`` elapses."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if pad_online(client, pad_code):
            return True
        time.sleep(interval)
    return pad_online(client, pad_code)


def wait_for_pad_ready(
    client: "VMOSClient",
    pad_code: str,
    *,
    timeout: float = 420.0,
    interval: float = 10.0,
    probe: str = "echo READY_OK",
    probe_timeout: float = 40.0,
) -> Dict[str, Any]:
    """Wait for a (re)booting instance to accept ``async_cmd`` again.

    After :func:`restart`, ``async_cmd`` raises :class:`VMOSAPIError` with code
    ``110031`` (``实例状态未就绪``) until the instance is ready. This tolerates that
    code (and transient transport/timeout errors), retrying the probe until it runs
    successfully. Returns ``{"ready", "elapsed", "attempts", "detail"}``; it does
    not raise for the tolerated not-ready condition (other API errors propagate).
    """
    shell = PadRootShell(client, pad_code, poll_timeout=probe_timeout)
    start = time.time()
    deadline = start + timeout
    attempts = 0
    detail = ""
    while time.time() < deadline:
        attempts += 1
        try:
            out = shell.sh(probe)
            if "READY_OK" in out:
                return {"ready": True, "elapsed": round(time.time() - start, 1),
                        "attempts": attempts, "detail": out.strip()[:120]}
            detail = out.strip()[:120]
        except VMOSAPIError as exc:
            if getattr(exc, "code", None) != PAD_NOT_READY_CODE:
                raise
            detail = f"{PAD_NOT_READY_CODE} {exc.msg}"[:120]
        except (TimeoutError, RuntimeError) as exc:
            detail = str(exc)[:120]
        time.sleep(interval)
    return {"ready": False, "elapsed": round(time.time() - start, 1),
            "attempts": attempts, "detail": detail}


#: Environment variables consulted (in order) for the default instance pad code.
PAD_CODE_ENV_VARS = ("VMOS_PAD_CODE", "VMOS_PADCODE", "PADCODE")


def resolve_pad_code(pad_code: Optional[str] = None) -> str:
    """Return ``pad_code`` if given, else the first non-empty pad-code env var.

    Accepts ``VMOS_PAD_CODE`` (canonical) plus the ``VMOS_PADCODE`` / ``PADCODE``
    aliases injected by some credential stores. Raises :class:`ValueError` if none
    is set.
    """
    if pad_code:
        return pad_code
    for name in PAD_CODE_ENV_VARS:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    raise ValueError("no pad code provided and none of " + ", ".join(PAD_CODE_ENV_VARS) + " is set")


def install_root_stack_headless(
    client: "VMOSClient",
    pad_code: Optional[str] = None,
    *,
    payload_url: str,
    expected_md5: Optional[str] = None,
    expected_size: Optional[int] = None,
    remote_dir: str = "/sdcard/Download/",
    file_name: str = "magisk_payload.gz",
    workdir: str = "/debug_ramdisk",
    restart: bool = True,
    download_timeout: float = 240.0,
    ready_timeout: float = 420.0,
    poll_interval: float = 5.0,
    install_modules: bool = True,
) -> Dict[str, Any]:
    """Install Magisk + Zygisk-Next + LSPosed **headlessly**, the real-device-verified way.

    Encodes the known-good sequence (no Toolbox UI, no ``switchRoot``, no ``su``):

    1. ``upload_file_v3`` the payload ``.gz`` (VMOS-managed async download into
       ``remote_dir``; ``autoInstall=0``).
    2. Wait for the download by polling the file's md5/size **on the device**
       (:func:`wait_for_file_download`) — ``fileTaskDetail`` returns ``null`` here.
    3. Extract to ``workdir`` and run ``install.sh && install_modules.sh`` with logs
       redirected, verifying success by on-device **state**
       (:func:`stage_root_stack_install`).
    4. ``restart`` the instance headlessly.
    5. Wait for reboot readiness, tolerating code ``110031``
       (:func:`wait_for_pad_ready`).
    6. Verify Magisk / LSPosed / Zygisk are truly active (:func:`verify_root_stack`).

    ``pad_code`` falls back to the environment (:func:`resolve_pad_code`). Returns a
    stage-by-stage summary dict. Raises :class:`RuntimeError` if the shell is not
    root, the download never completes, or the install state check fails.
    """
    pad_code = resolve_pad_code(pad_code)
    if not (isinstance(payload_url, str) and payload_url.startswith("https://")):
        raise ValueError("payload_url must be an https:// URL to the Magisk payload .gz")
    shell = PadRootShell(client, pad_code, poll_timeout=200.0)
    if not shell.is_root():
        raise RuntimeError("instance shell is not root — is this a real-device instance?")

    remote_path = remote_dir.rstrip("/") + "/" + file_name
    result: Dict[str, Any] = {
        "pad_code": pad_code,
        "payload_url": payload_url,
        "remote_path": remote_path,
    }

    # 1. Upload — VMOS-managed async download onto the device.
    client.apps.upload_file_v3(
        pad_codes=[pad_code],
        url=payload_url,
        customize_file_path=remote_dir,
        file_name=file_name,
        auto_install=0,
        md5=expected_md5,
    )

    # 2. Wait for the download by md5/size on the device (Bug-fix #2).
    download = wait_for_file_download(
        shell,
        remote_path,
        expected_md5=expected_md5,
        expected_size=expected_size,
        timeout=download_timeout,
        interval=poll_interval,
    )
    result["download"] = download
    if not download["ready"]:
        raise RuntimeError(f"payload download did not complete on device: {download}")

    # 3. Extract + install + install_modules; verify by state (Bug-fix #3).
    install = stage_root_stack_install(
        shell, payload_path=remote_path, workdir=workdir, install_modules=install_modules
    )
    result["install"] = install
    if not install["ok"]:
        raise RuntimeError(f"root-stack install failed (state check): {install}")

    if not restart:
        result["restarted"] = False
        return result

    # 4. Restart headlessly.
    client.instance.restart(pad_codes=[pad_code])
    result["restarted"] = True

    # 5. Wait for reboot readiness (tolerate code 110031).
    ready = wait_for_pad_ready(client, pad_code, timeout=ready_timeout, interval=poll_interval)
    result["ready"] = ready
    if not ready["ready"]:
        result["verified"] = {"ok": False, "detail": "instance not ready after restart"}
        return result

    # 6. Verify LSPosed / Zygisk are truly ON.
    result["verified"] = verify_root_stack(shell)
    return result


def resetprop_command(props: Dict[str, str]) -> str:
    """Build a single shell command that resetprops every ``props`` entry."""
    return " ; ".join(resetprop_commands(props))


def resetprop_commands(props: Dict[str, str]) -> List[str]:
    """One ``resetprop -n`` command per property (for batched execution)."""
    return [f"{MAGISK_BIN} resetprop -n {_sh_quote(k)} {_sh_quote(v)}"
            for k, v in props.items()]


#: The pad's async command channel truncates input at roughly 2 KB. A single
#: command longer than that is cut mid-token and (for an unterminated quote)
#: fails to run at all — silently applying **nothing**. Keep every batch well
#: under the cap. Live-verified 2026-07: a 4148-byte resetprop of 50 deep build
#: props applied ZERO props; the same props in <=1.4 KB batches applied all 50.
ASYNC_CMD_MAX_BYTES = 1400


def _run_batched(
    shell: "PadRootShell",
    commands: List[str],
    *,
    limit: int = ASYNC_CMD_MAX_BYTES,
    sep: str = " ; ",
) -> int:
    """Run ``commands`` in the fewest ``sep``-joined batches that each stay under
    ``limit`` bytes. Returns the number of batches sent.

    Guards every large on-device command (resetprop sets, file payloads) against
    the async_cmd input cap (:data:`ASYNC_CMD_MAX_BYTES`). A single command
    longer than ``limit`` is still sent on its own (can't be split further).
    """
    batch: List[str] = []
    size = 0
    sent = 0
    for cmd in commands:
        extra = len(cmd) + (len(sep) if batch else 0)
        if batch and size + extra > limit:
            shell.sh(sep.join(batch))
            sent += 1
            batch, size = [], 0
            extra = len(cmd)
        batch.append(cmd)
        size += extra
    if batch:
        shell.sh(sep.join(batch))
        sent += 1
    return sent


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
    """The module's ``module.prop`` — the six Magisk-required fields with an
    **integer** ``versionCode``. Bumped to v1.1 now that the module persists BOTH
    the build props and the ``persist.vmos.spoof.*`` identity inputs via
    ``system.prop`` (so Magisk treats the changed module as an update)."""
    return (
        f"id={MODULE_ID}\n"
        "name=VMOS Device Spoof\n"
        "version=v1.1\n"
        "versionCode=2\n"
        "author=vmos-sdk\n"
        "description=Persistent build-prop + identity-input spoof (canonical Profile). "
        "Re-applied every boot at post-fs-data via system.prop.\n"
    )


def _write_file(shell: "PadRootShell", path: str, content: str, *, mode: str = "0644") -> None:
    """Write a file on the instance, safe for payloads over the async_cmd cap.

    The content is base64-encoded and appended in small chunks, then decoded on
    device (``base64 -d``). This avoids both shell-quoting hazards and the input
    truncation that a single large heredoc would hit (see :data:`ASYNC_CMD_MAX_BYTES`).
    """
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    parent = _sh_quote(path.rsplit("/", 1)[0])
    p = _sh_quote(path)
    tmp = _sh_quote(path + ".b64")
    shell.sh(f"mkdir -p {parent}; : > {path + '.b64'}")
    step = 800  # base64 chars per append -> ~<900 B command, well under the cap
    for i in range(0, len(b64), step):
        shell.sh(f"printf '%s' {_sh_quote(b64[i:i + step])} >> {path + '.b64'}")
    shell.sh(f"base64 -d {tmp} > {p} && chmod {mode} {p} && rm -f {tmp}")


def _parse_prop_lines(text: str) -> "OrderedDict[str, str]":
    """Parse ``key=value`` property lines into an ordered map (skips blanks/comments)."""
    props: "OrderedDict[str, str]" = OrderedDict()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key:
            props[key] = value.strip()
    return props


def _read_module_system_prop(shell: "PadRootShell") -> "OrderedDict[str, str]":
    """Return the module's current ``system.prop`` as an ordered map (empty if absent)."""
    out = shell.sh(f"cat {_sh_quote(_MODULE_DIR + '/system.prop')} 2>/dev/null || true")
    return _parse_prop_lines(out)


def _write_module_system_prop(
    shell: "PadRootShell", new_props: Dict[str, str]
) -> "OrderedDict[str, str]":
    """Merge ``new_props`` into the module's ``system.prop`` and write the union back.

    ``system.prop`` is Magisk's single boot-time property file, re-applied via
    ``resetprop`` at **post-fs-data** (before Zygote/GMS read). Two independent
    layers contribute to it — the build props (:func:`install_persistence`) and the
    ``persist.vmos.spoof.*`` identity inputs (:func:`set_identity_props`) — and they
    run in either order, so each **merges** rather than overwrites: existing keys are
    preserved, ``new_props`` win on conflict, and repeated identical calls neither
    grow nor duplicate the file (idempotent). Written through :func:`_write_file`, so
    it respects the async_cmd input cap.
    """
    merged = _read_module_system_prop(shell)
    for key, value in new_props.items():
        merged[key] = value
    content = "".join(f"{k}={v}\n" for k, v in merged.items())
    _write_file(shell, f"{_MODULE_DIR}/system.prop", content)
    return merged


def install_persistence(shell: "PadRootShell", profile: "DeviceProfile") -> None:
    """Install boot-time persistence via BOTH a Magisk ``service.d`` script and a
    module ``system.prop`` (whichever Magisk processes first wins; both are safe)."""
    props = profile.build_props()
    # 1) General Magisk boot script (run on every boot by magiskd).
    _write_file(shell, _SERVICE_D, _service_script(props, profile.android_id), mode="0755")
    # 2) Magisk module with system.prop (applied very early, at post-fs-data, before
    #    apps start). system.prop is the UNION of build props + identity inputs, so
    #    merge to preserve any persist.vmos.spoof.* keys set by set_identity_props.
    _write_file(shell, f"{_MODULE_DIR}/module.prop", _module_prop())
    _write_module_system_prop(shell, props)
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
    # Apply in input-cap-safe batches (a single huge resetprop command is
    # truncated by async_cmd and silently applies nothing — see _run_batched).
    _run_batched(shell, resetprop_commands(props))
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


def remove_spoof(client: "VMOSClient", pad_code: str, *, clear_runtime: bool = True) -> None:
    """Remove the persistent spoof payload (Magisk module + service.d script).

    With ``clear_runtime`` (default) the currently-applied spoof properties are also
    deleted from the live prop area via ``magisk64 resetprop --delete <key>`` — so
    scoped apps stop seeing spoofed values **immediately**, without waiting for a
    reboot (design §E.3). The keys cleared are those the module persists (read from
    ``system.prop``) plus the known ``persist.vmos.spoof.*`` identity inputs (in case
    ``system.prop`` is already gone). Build props revert to their genuine values on
    the next reboot — apply a genuine Profile to fully restore identity before then.
    """
    shell = PadRootShell(client, pad_code)
    if clear_runtime:
        keys: List[str] = list(_read_module_system_prop(shell).keys())
        for key in _IDENTITY_PROPS.values():
            if key not in keys:
                keys.append(key)
        if keys:
            _run_batched(
                shell,
                [f"{MAGISK_BIN} resetprop --delete {_sh_quote(k)}" for k in keys],
            )
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


def scope_lsposed_module(
    client: "VMOSClient",
    pad_code: str,
    module_pkg: str,
    scope_pkgs: "List[str]",
    *,
    sqlite3_bin: str = "/data/local/tmp/sqlite3",
    db_path: str = "/data/adb/lspd/config/modules_config.db",
    enabled: bool = True,
    user_id: int = 0,
) -> Dict[str, Any]:
    """Enable + scope an LSPosed module by editing ``modules_config.db`` directly.

    LSPosed has no CLI; scope lives in a SQLite DB (``modules`` + ``scope``
    tables) that is root-owned. Android ships no ``sqlite3``, so provide a
    **static aarch64 ``sqlite3`` binary** on the device at ``sqlite3_bin`` first
    (e.g. ``curl`` a prebuilt static build onto the pad and ``chmod 755`` — the
    async shell is root and the pad has ``curl``). The module must already be
    installed (LSPosed auto-adds a disabled row to ``modules`` when it detects
    the APK). Reboot after this call for the change to take effect.

    Returns the post-edit ``modules``/``scope`` dump.

    .. important::
       **Live finding (VMOS Kitsune):** enabling + scoping works and LSPosed
       *loads* the module into scoped processes, BUT modules built against the
       **new libxposed API** (e.g. DeviceSpoofLab-Hooks) fail to initialise on
       VMOS's **older bundled LSPosed** (``NoSuchMethodException`` on
       ``XposedModuleImpl.<init>``). Use a module built for the classic Xposed
       API (``de.robv.android.xposed`` — e.g. AndroidFaker) to match the shipped
       framework, or upgrade the ``zygisk_lsposed`` module.
    """
    shell = PadRootShell(client, pad_code)
    q = "'"
    en = 1 if enabled else 0
    stmts = [f"UPDATE modules SET enabled={en}, auto_include={en} WHERE module_pkg_name={q}{module_pkg}{q};"]
    for pkg in scope_pkgs:
        stmts.append(
            f"INSERT OR IGNORE INTO scope(mid,app_pkg_name,user_id) "
            f"VALUES((SELECT mid FROM modules WHERE module_pkg_name={q}{module_pkg}{q}),{q}{pkg}{q},{user_id});"
        )
    sql = "".join(stmts)
    shell.sh(f'{sqlite3_bin} "{db_path}" "{sql}"')
    modules = shell.sh(f'{sqlite3_bin} "{db_path}" "SELECT module_pkg_name,enabled FROM modules;"')
    scope = shell.sh(f'{sqlite3_bin} "{db_path}" "SELECT app_pkg_name FROM scope;"')
    return {"module": module_pkg, "enabled": enabled, "modules": modules, "scope": scope}


#: system properties the XPose spoof plugin reads (see xpose_plugin/).
_IDENTITY_PROPS = {
    "imei": "persist.vmos.spoof.imei",
    "meid": "persist.vmos.spoof.meid",
    "imsi": "persist.vmos.spoof.imsi",
    "iccid": "persist.vmos.spoof.iccid",
    "line1": "persist.vmos.spoof.line1",
    "android_id": "persist.vmos.spoof.androidid",
    "gaid": "persist.vmos.spoof.gaid",          # Google Advertising ID
    "oaid": "persist.vmos.spoof.oaid",          # MSA OAID (best-effort, per target SDK)
    "wifi_mac": "persist.vmos.spoof.wifimac",   # WifiInfo.getMacAddress()
    "bssid": "persist.vmos.spoof.bssid",        # WifiInfo.getBSSID()
    "serial": "persist.vmos.spoof.serial",      # Build.getSerial()
    "drm_id": "persist.vmos.spoof.drmid",       # MediaDrm/Widevine device id (hex)
}


def set_identity_props(
    client: "VMOSClient",
    pad_code: str,
    *,
    imei: Optional[str] = None,
    meid: Optional[str] = None,
    imsi: Optional[str] = None,
    iccid: Optional[str] = None,
    line1: Optional[str] = None,
    android_id: Optional[str] = None,
    gaid: Optional[str] = None,
    oaid: Optional[str] = None,
    wifi_mac: Optional[str] = None,
    bssid: Optional[str] = None,
    serial: Optional[str] = None,
    drm_id: Optional[str] = None,
    persist_module: bool = True,
) -> Dict[str, str]:
    """Set the ``persist.vmos.spoof.*`` props the XPose spoof plugin reads.

    These decouple the (build-once) XPose plugin from per-device values: the
    plugin returns them for ``getImei()`` / ``getSubscriberId()`` /
    ``AdvertisingIdClient.getId()`` / ``WifiInfo.getMacAddress()`` /
    ``Build.getSerial()`` / ``MediaDrm`` / ``Settings.Secure`` etc. in scoped
    apps. Applied immediately via Magisk ``resetprop`` for the current session;
    when ``persist_module`` is true they are also written into a **valid**
    ``vmos_spoof`` Magisk module (``module.prop`` + ``system.prop``) so Magisk
    re-applies them at every boot (post-fs-data, before apps read them) — that
    module is the reboot-durable mechanism, replacing the volatile runtime
    ``resetprop -n``. ``system.prop`` is merged with any build props already there
    (:func:`install_persistence`), so the two layers never clobber each other.
    ``custom.conf`` is kept only as a remove/regenerate manifest (overwritten each
    call — never appended, which previously grew the file unboundedly).

    ``drm_id`` is a hex string (decoded to bytes by the plugin). Only the
    arguments you pass are set. Returns the ``prop -> value`` map written.
    """
    shell = PadRootShell(client, pad_code)
    values = {"imei": imei, "meid": meid, "imsi": imsi, "iccid": iccid,
              "line1": line1, "android_id": android_id, "gaid": gaid,
              "oaid": oaid, "wifi_mac": wifi_mac, "bssid": bssid,
              "serial": serial, "drm_id": drm_id}
    to_set = {_IDENTITY_PROPS[k]: v for k, v in values.items() if v}
    if not to_set:
        return {}
    _run_batched(shell, resetprop_commands(to_set))
    if persist_module:
        # Persist as a VALID Magisk module so the identity inputs survive reboot,
        # re-applied every boot at post-fs-data via system.prop (NOT the volatile
        # runtime `resetprop -n`, which is lost on reboot). All writes go through
        # _write_file / _write_module_system_prop, respecting ASYNC_CMD_MAX_BYTES.
        _write_file(shell, f"{_MODULE_DIR}/module.prop", _module_prop())
        # system.prop is merged so Layer-1 build props (install_persistence) survive.
        _write_module_system_prop(shell, to_set)
        # custom.conf is kept ONLY as a manifest for remove/regenerate — OVERWRITE,
        # never append (the old `>>` grew the file on every call).
        conf_lines = "FILE_ENABLED\n" + "".join(f"ENABLED,{k},{v}\n" for k, v in to_set.items())
        _write_file(shell, f"{_MODULE_DIR}/config/custom.conf", conf_lines)
        # Ensure the module is enabled (no disable/remove flags).
        shell.sh(f"rm -f {_MODULE_DIR}/disable {_MODULE_DIR}/remove 2>/dev/null; true")
    return to_set


#: Packages that MUST NEVER be app-scoped with an identity hook. GMS and the Play
#: Store are designed to read the device's *real* identity IDs; injecting spoofed
#: IDs into them desyncs GMS's own view (checkin / Play Integrity / attestation) and
#: risks crashes or an "uncertified" verdict (design §B). Identity IDs are spoofed
#: **app-scoped** into target apps only — never these two. Build props (``ro.*``)
#: may still be system-wide, as a coherent & genuine set.
GMS_EXCLUDED_PACKAGES = ("com.google.android.gms", "com.android.vending")


def load_xpose_plugin(
    client: "VMOSClient",
    pad_code: str,
    *,
    name: str,
    target_pkg: str,
    apk_url: Optional[str] = None,
    apk_path: Optional[str] = None,
) -> str:
    """Load an XPose hook plugin into ``target_pkg`` via VMOS's native ``apmt``.

    Provide exactly one of ``apk_url`` (``apmt ... -u``) or ``apk_path``
    (``apmt ... -f``). Use ``target_pkg="android"`` to hook SystemServer.
    Restart the target app afterwards. Returns ``apmt``'s output.

    No LSPosed needed — ``apmt`` is built into the VMOS image. Build the plugin
    from ``xpose_plugin/`` (see its README).

    **Hard guard (design §B):** refuses ``com.google.android.gms`` and
    ``com.android.vending`` — an identity hook must never be injected into GMS or
    the Play Store (they must observe the real identity). Raises :class:`ValueError`
    for those packages, even if a caller passes them explicitly.
    """
    if bool(apk_url) == bool(apk_path):
        raise ValueError("provide exactly one of apk_url or apk_path")
    if target_pkg in GMS_EXCLUDED_PACKAGES:
        raise ValueError(
            f"refusing to load an identity hook into {target_pkg!r}: GMS/Play must read "
            "the real device identity (design §B). Scope identity hooks to target apps "
            "only, never com.google.android.gms / com.android.vending."
        )
    shell = PadRootShell(client, pad_code)
    src = f"-u {_sh_quote(apk_url)}" if apk_url else f"-f {_sh_quote(apk_path)}"
    return shell.sh(f"apmt patch add -n {_sh_quote(name)} -p {_sh_quote(target_pkg)} {src}")


def list_xpose_plugins(client: "VMOSClient", pad_code: str) -> str:
    """Return ``apmt patch list`` output (loaded XPose plugins)."""
    return PadRootShell(client, pad_code).sh("apmt patch list")


def remove_xpose_plugin(client: "VMOSClient", pad_code: str, name: str) -> str:
    """Remove an XPose plugin by name (``apmt patch del -n <name>``)."""
    return PadRootShell(client, pad_code).sh(f"apmt patch del -n {_sh_quote(name)}")


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
