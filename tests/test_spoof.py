"""Unit tests for the device-spoofing toolkit (mocked shell — no network/device)."""

import base64
import re

from vmos import DeviceProfile
from vmos.spoof import (
    ASYNC_CMD_MAX_BYTES,
    MAGISK_BIN,
    PIXEL_10_PRO_A17,
    apply_profile,
    resetprop_command,
    verify_profile,
)


def test_profile_expands_build_props():
    p = DeviceProfile(model="Pixel 10 Pro", brand="google", manufacturer="Google",
                      device="frankel", release="17", sdk=37, deep=True)
    props = p.build_props()
    assert props["ro.product.model"] == "Pixel 10 Pro"
    assert props["ro.product.system.model"] == "Pixel 10 Pro"      # deep partition variant
    assert props["ro.product.vendor.brand"] == "google"
    assert props["ro.build.version.release"] == "17"
    assert props["ro.build.version.sdk"] == "37"
    # Build.BOARD / Build.HARDWARE track the codename (consistency fix)
    assert props["ro.product.board"] == "frankel"
    assert props["ro.hardware"] == "frankel"
    assert props["ro.boot.hardware"] == "frankel"


def test_profile_shallow_skips_partitions():
    p = DeviceProfile(model="X", deep=False)
    keys = list(p.build_props())
    assert "ro.product.model" in keys
    assert not any(".system." in k for k in keys)


def test_resetprop_command_quotes_values():
    cmd = resetprop_command({"ro.product.model": "Pixel 10 Pro"})
    assert cmd == f"{MAGISK_BIN} resetprop -n 'ro.product.model' 'Pixel 10 Pro'"


def test_resetprop_command_escapes_single_quotes():
    cmd = resetprop_command({"k": "a'b"})
    assert "'a'\\''b'" in cmd


def test_resetprop_commands_one_per_prop():
    from vmos.spoof import resetprop_commands
    cmds = resetprop_commands({"a": "1", "b": "2"})
    assert len(cmds) == 2
    assert cmds[0] == f"{MAGISK_BIN} resetprop -n 'a' '1'"


def test_run_batched_stays_under_input_cap():
    from vmos.spoof import ASYNC_CMD_MAX_BYTES, _run_batched, resetprop_commands

    sent = []

    class _Shell:
        def sh(self, script):
            sent.append(script)

    # 60 props -> a single joined command would be far over the ~2 KB cap.
    props = {f"ro.test.item{i}": f"value-{i:03d}" for i in range(60)}
    cmds = resetprop_commands(props)
    batches = _run_batched(_Shell(), cmds)
    assert batches >= 2                                   # actually split
    assert all(len(s) <= ASYNC_CMD_MAX_BYTES for s in sent)  # every batch safe
    joined = " ; ".join(sent)
    for c in cmds:                                        # nothing dropped
        assert c in joined


def test_apply_profile_batches_large_prop_set():
    from vmos.spoof import ASYNC_CMD_MAX_BYTES
    client = FakePadClient(_reply)
    apply_profile(client, "ACP1", PIXEL_10_PRO_A17, persist=False)
    # the deep prop set must never be sent as one over-cap command
    resetprop_scripts = [s for s in client.scripts if "resetprop -n 'ro.product.model'" in s]
    assert resetprop_scripts, "model resetprop must be present"
    assert all(len(s) <= ASYNC_CMD_MAX_BYTES for s in client.scripts)


class FakePadClient:
    """Minimal VMOSClient stand-in capturing async_cmd scripts and scripting replies."""

    def __init__(self, replies):
        self._replies = replies
        self.scripts = []
        self._tid = 0
        client = self

        class _Instance:
            def async_cmd(self, pad_codes, script_content):
                client.scripts.append(script_content)
                client._tid += 1
                return [{"taskId": client._tid}]

        class _Tasks:
            def pad_task_detail(self, task_ids):
                # reply chosen by call order
                idx = len(client.scripts) - 1
                out = client._replies(client.scripts[idx]) if callable(client._replies) else ""
                return [{"taskStatus": 3, "taskResult": out}]

        self.instance = _Instance()
        self.tasks = _Tasks()


def _reply(script):
    if script.strip() == "id -u":
        return "0"
    if MAGISK_BIN in script and "-x" in script:
        return "YES"
    if "getprop" in script:
        # emulate that resetprop stuck
        return "\n".join([
            "ro.product.model=Pixel 10 Pro",
            "ro.product.brand=google",
            "ro.build.version.release=17",
            "ro.build.version.sdk=37",
            "ro.build.fingerprint=" + PIXEL_10_PRO_A17.fingerprint,
        ])
    if "settings get" in script:
        return "abc123"
    return ""


def test_apply_profile_runs_expected_steps():
    client = FakePadClient(_reply)
    summary = apply_profile(client, "ACP1", PIXEL_10_PRO_A17, persist=True)
    assert summary["applied"] > 0 and summary["persisted"] is True
    assert summary["android_id_attempted"] is False  # preset has no android_id
    assert "android_id_note" in summary
    joined = "\n".join(client.scripts)
    assert "id -u" in joined
    assert f"{MAGISK_BIN} resetprop -n 'ro.product.model' 'Pixel 10 Pro'" in joined
    assert "/data/adb/service.d/99-vmos-spoof.sh" in joined          # persistence installed
    assert "/data/adb/modules/vmos_spoof/system.prop" in joined      # module system.prop


def test_verify_profile_reports_matches():
    client = FakePadClient(_reply)
    result = verify_profile(client, "ACP1", PIXEL_10_PRO_A17)
    assert result["ok"] is True
    assert result["checks"]["ro.product.model"]["got"] == "Pixel 10 Pro"
    assert result["checks"]["ro.build.version.sdk"]["match"] is True


# Compact state output emitted by the stage/install script (Bug-fix #3): every
# Magisk binary present, both modules staged, prop set, RCs zero.
_STAGE_OK_OUTPUT = "\n".join([
    "INSTALL_RC=0",
    "MODULES_RC=0",
    "PROP=1",
    "BIN_OK=magisk64", "BIN_OK=magisk32", "BIN_OK=magiskpolicy",
    "BIN_OK=magiskboot", "BIN_OK=busybox",
    "MOD_OK=zygisksu", "MOD_OK=zygisk_lsposed",
    "STAGE_DONE",
])


def _magisk_headless_reply(s):
    if s.strip() == "id -u":
        return "0"
    if MAGISK_BIN in s and "-x" in s:
        return "NO"                       # not installed yet -> proceed
    if ".vmos_rw" in s:
        return "RW=0"                      # /debug_ramdisk writable
    if "record/query" in s:               # OSS payload query (no auth)
        return "https://oss-hk.armcloud.net/prod/raw_magisk/abc123.gz"
    if "DL_RC" in s:                       # compact curl download script
        return "DL_RC=0 SIZE=27219650"
    if "magisk_env/install.sh" in s:      # extract + install (+ modules) stage
        return _STAGE_OK_OUTPUT
    return ""


def test_enable_magisk_headless_flow():
    from vmos.spoof import enable_magisk_headless
    client = FakePadClient(_magisk_headless_reply)
    res = enable_magisk_headless(client, "ACP1")
    assert res["installed"] is True
    assert res["payload_url"].endswith(".gz")
    assert res["magisk_cloud_prop"] == "1"
    # GAP fix: install_modules.sh ran and staged BOTH Zygisk-Next + LSPosed
    assert res["modules"] == {"zygisksu": True, "zygisk_lsposed": True}
    assert res["install_rc"] == 0 and res["modules_rc"] == 0
    joined = "\n".join(client.scripts)
    assert "record/query" in joined            # queried the OSS payload URL
    assert "magisk_env/install.sh" in joined    # ran the installer
    assert "magisk_env/install_modules.sh" in joined  # ran the modules installer
    # never used the forbidden paths
    assert "switchRoot" not in joined and "su -c" not in joined


def test_enable_magisk_headless_skips_if_present():
    from vmos.spoof import enable_magisk_headless
    client = FakePadClient(lambda s: "0" if s.strip() == "id -u"
                           else ("YES" if (MAGISK_BIN in s and "-x" in s) else ""))
    res = enable_magisk_headless(client, "ACP1")
    assert res.get("already_installed") is True


def test_apply_requires_root():
    import pytest

    client = FakePadClient(lambda s: "2000" if s.strip() == "id -u" else "")
    with pytest.raises(RuntimeError):
        apply_profile(client, "ACP1", PIXEL_10_PRO_A17)


def test_scope_lsposed_module_builds_sql():
    from vmos.spoof import scope_lsposed_module
    client = FakePadClient(lambda s: "")
    out = scope_lsposed_module(client, "ACP1", "com.devicespooflab.hooks",
                               ["android", "com.android.vending"])
    joined = "\n".join(client.scripts)
    assert "UPDATE modules SET enabled=1" in joined
    assert "com.devicespooflab.hooks" in joined
    assert "INSERT OR IGNORE INTO scope" in joined
    assert "'android'" in joined and "'com.android.vending'" in joined
    assert out["module"] == "com.devicespooflab.hooks" and out["enabled"] is True


def test_set_identity_props_uses_resetprop():
    from vmos.spoof import set_identity_props
    client = FakePadClient(lambda s: "")
    out = set_identity_props(client, "ACP1", imei="356789012345678", android_id="a1b2c3d4e5f60718")
    joined = "\n".join(client.scripts)
    assert "persist.vmos.spoof.imei" in joined and "356789012345678" in joined
    assert "persist.vmos.spoof.androidid" in joined
    assert out["persist.vmos.spoof.imei"] == "356789012345678"


def test_load_xpose_plugin_builds_apmt():
    from vmos.spoof import load_xpose_plugin
    client = FakePadClient(lambda s: "add Patch:vmosid success")
    load_xpose_plugin(client, "ACP1", name="vmosid", target_pkg="com.x", apk_url="https://h/p.apk")
    joined = "\n".join(client.scripts)
    assert "apmt patch add -n 'vmosid' -p 'com.x' -u 'https://h/p.apk'" in joined


def test_load_xpose_plugin_requires_one_source():
    import pytest
    from vmos.spoof import load_xpose_plugin
    client = FakePadClient(lambda s: "")
    with pytest.raises(ValueError):
        load_xpose_plugin(client, "ACP1", name="n", target_pkg="p")  # neither url nor path


def test_set_identity_props_extended_surfaces():
    from vmos.spoof import set_identity_props
    client = FakePadClient(lambda s: "")
    out = set_identity_props(client, "ACP1", gaid="38400000-8cf0-11bd-b23e-10b96e40000d",
                             wifi_mac="02:00:00:11:22:33", serial="1A2B3C4D",
                             drm_id="deadbeefcafe0011")
    joined = "\n".join(client.scripts)
    assert "persist.vmos.spoof.gaid" in joined
    assert "persist.vmos.spoof.wifimac" in joined and "02:00:00:11:22:33" in joined
    assert "persist.vmos.spoof.serial" in joined
    assert out["persist.vmos.spoof.drmid"] == "deadbeefcafe0011"
    # unset fields must not be written
    assert "persist.vmos.spoof.imei" not in joined


# --------------------------------------------------------------------------- #
# Persistence / valid-Magisk-module tests (P5-DEV-003).
#
# The runtime-only `resetprop -n` did not survive reboot; the fix makes
# set_identity_props (and apply_profile's persist path) generate a VALID Magisk
# module (module.prop + system.prop) that Magisk re-applies at post-fs-data, with
# custom.conf kept only as an OVERWRITTEN manifest. These tests model the device
# filesystem (base64 chunk -> decode, `cat` read-back) so they can assert the
# ACTUAL file contents and the read-merge-write behavior of system.prop.
# --------------------------------------------------------------------------- #
class FileModelingFakePad:
    """VMOSClient stand-in that also models ``_write_file`` and ``cat``.

    It reconstructs files written via the base64-chunk protocol
    (``: > f.b64`` -> ``printf '%s' <chunk> >> f.b64`` -> ``base64 -d f.b64 > f``)
    and serves them back on ``cat``, so tests can assert real file contents and the
    merge semantics of the module's ``system.prop``. Also tracks ``resetprop -n``
    (set) and ``resetprop --delete`` (clear) into a prop store.
    """

    _RESETPROP = re.compile(r"resetprop -n '([^']*)' '([^']*)'")
    _RESETDEL = re.compile(r"resetprop --delete '([^']*)'")
    _TRUNC = re.compile(r": > (\S+\.b64)")
    _APPEND = re.compile(r"printf '%s' '([^']*)' >> (\S+\.b64)")
    _DECODE = re.compile(r"base64 -d '([^']+)' > '([^']+)'")
    _RMRF = re.compile(r"rm -rf ([^\s;]+)")
    _CAT = re.compile(r"^cat '([^']+)'")

    def __init__(self):
        self.props = {}
        self.files = {}
        self._b64 = {}
        self.scripts = []
        self._tid = 0
        self._last = ""
        pad = self

        class _Instance:
            def async_cmd(self, pad_codes, script_content):
                pad.scripts.append(script_content)
                pad._last = script_content
                pad._apply(script_content)
                pad._tid += 1
                return [{"taskId": pad._tid}]

        class _Tasks:
            def pad_task_detail(self, task_ids):
                return [{"taskStatus": 3, "taskResult": pad._output(pad._last)}]

        self.instance = _Instance()
        self.tasks = _Tasks()

    def _apply(self, script):
        for k, v in self._RESETPROP.findall(script):
            self.props[k] = v
        for k in self._RESETDEL.findall(script):
            self.props.pop(k, None)
        m = self._TRUNC.search(script)
        if m:
            self._b64[m.group(1)] = ""
        m = self._APPEND.search(script)
        if m:
            self._b64[m.group(2)] = self._b64.get(m.group(2), "") + m.group(1)
        m = self._DECODE.search(script)
        if m:
            raw = self._b64.get(m.group(1), "")
            try:
                self.files[m.group(2)] = base64.b64decode(raw).decode("utf-8")
            except Exception:  # noqa: BLE001
                self.files[m.group(2)] = ""
        for target in self._RMRF.findall(script):
            target = target.strip("'")
            for path in list(self.files):
                if path == target or path.startswith(target + "/"):
                    del self.files[path]

    def _output(self, script):
        s = script.strip()
        if s == "id -u":
            return "0"
        if "-x" in s and MAGISK_BIN in s:
            return "YES"
        m = self._CAT.match(s)
        if m:
            return self.files.get(m.group(1), "")
        return ""


_MODULE = "/data/adb/modules/vmos_spoof"


def test_set_identity_props_writes_valid_module():
    from vmos.spoof import set_identity_props
    pad = FileModelingFakePad()
    set_identity_props(pad, "ACP1", imei="356789012345678",
                       android_id="a1b2c3d4e5f60718",
                       gaid="38400000-8cf0-11bd-b23e-10b96e40000d")
    # (1) module.prop is a valid module: the 6 required fields, integer versionCode.
    mod = pad.files[f"{_MODULE}/module.prop"]
    for field_ in ("id=", "name=", "version=", "versionCode=", "author=", "description="):
        assert field_ in mod
    assert "id=vmos_spoof" in mod
    vcode = next(l.split("=", 1)[1] for l in mod.splitlines() if l.startswith("versionCode="))
    assert vcode.isdigit() and int(vcode) >= 1
    # (2) system.prop carries the identity inputs (the reboot-durable mechanism).
    sysprop = pad.files[f"{_MODULE}/system.prop"]
    assert "persist.vmos.spoof.imei=356789012345678" in sysprop
    assert "persist.vmos.spoof.androidid=a1b2c3d4e5f60718" in sysprop
    assert "persist.vmos.spoof.gaid=38400000-8cf0-11bd-b23e-10b96e40000d" in sysprop
    # (3) custom.conf is a manifest: header + one ENABLED line per key.
    conf = pad.files[f"{_MODULE}/config/custom.conf"]
    assert conf.startswith("FILE_ENABLED")
    assert "ENABLED,persist.vmos.spoof.imei,356789012345678" in conf


def test_set_identity_props_overwrites_custom_conf_no_duplication():
    from vmos.spoof import set_identity_props
    pad = FileModelingFakePad()
    for _ in range(3):                       # repeated calls must not grow the files
        set_identity_props(pad, "ACP1", imei="356789012345678")
    conf = pad.files[f"{_MODULE}/config/custom.conf"]
    assert conf.count("FILE_ENABLED") == 1
    assert conf.count("ENABLED,persist.vmos.spoof.imei,") == 1   # overwritten, not appended
    sysprop = pad.files[f"{_MODULE}/system.prop"]
    assert sysprop.count("persist.vmos.spoof.imei=") == 1        # merged, not duplicated


def test_set_identity_props_merges_with_build_props_in_system_prop():
    # Standard manager order: Layer 1 (apply_profile) then Layer 2 (identity).
    from vmos.spoof import apply_profile, set_identity_props
    pad = FileModelingFakePad()
    apply_profile(pad, "ACP1", PIXEL_10_PRO_A17, persist=True)
    set_identity_props(pad, "ACP1", imei="356789012345678")
    sysprop = pad.files[f"{_MODULE}/system.prop"]
    # Layer-1 build props AND Layer-2 identity input coexist (neither clobbered).
    assert "ro.product.model=Pixel 10 Pro" in sysprop
    assert "ro.build.fingerprint=" + PIXEL_10_PRO_A17.fingerprint in sysprop
    assert "persist.vmos.spoof.imei=356789012345678" in sysprop


def test_build_props_merge_preserves_identity_inputs_reverse_order():
    # Reverse order must be just as safe (Layer 2 first, then Layer 1).
    from vmos.spoof import apply_profile, set_identity_props
    pad = FileModelingFakePad()
    set_identity_props(pad, "ACP1", imei="356789012345678")
    apply_profile(pad, "ACP1", PIXEL_10_PRO_A17, persist=True)
    sysprop = pad.files[f"{_MODULE}/system.prop"]
    assert "persist.vmos.spoof.imei=356789012345678" in sysprop   # preserved
    assert "ro.product.model=Pixel 10 Pro" in sysprop             # added


def test_set_build_props_merges_with_identity_in_system_prop_and_writes_valid_module():
    # Regression (P5-DEV-010): set_build_props now persists through the SAME valid
    # Magisk module as set_identity_props. Its app-scoped Build.* keys
    # (persist.vmos.spoof.build.*) are MERGED into system.prop — never clobbering the
    # identity inputs (persist.vmos.spoof.*) — so a reboot re-applies BOTH layers via
    # the one module, regardless of call order (was: an unbounded `>>` custom.conf
    # append that nothing reads at boot).
    from vmos.spoof import set_build_props, set_identity_props

    # (a) identity first, then build props: both coexist in system.prop.
    pad = FileModelingFakePad()
    set_identity_props(pad, "ACP1", imei="356789012345678")
    set_build_props(pad, "ACP1", model="Pixel 10 Pro", manufacturer="Google",
                    fingerprint="google/comet/comet:16/AP4A.000000.000/13:user/release-keys")
    sysprop = pad.files[f"{_MODULE}/system.prop"]
    assert "persist.vmos.spoof.imei=356789012345678" in sysprop            # identity preserved
    assert "persist.vmos.spoof.build.model=Pixel 10 Pro" in sysprop        # build merged in
    assert "persist.vmos.spoof.build.manufacturer=Google" in sysprop
    assert "persist.vmos.spoof.build.fingerprint=" in sysprop
    # set_build_props(persist_module=True) writes a VALID module, not custom.conf.
    mod = pad.files[f"{_MODULE}/module.prop"]
    for field_ in ("id=", "name=", "version=", "versionCode=", "author=", "description="):
        assert field_ in mod
    vcode = next(l.split("=", 1)[1] for l in mod.splitlines() if l.startswith("versionCode="))
    assert vcode.isdigit() and int(vcode) >= 1

    # (b) reverse order (build first, then identity) is equally safe and idempotent.
    pad2 = FileModelingFakePad()
    set_build_props(pad2, "ACP1", model="Pixel 10 Pro")
    set_identity_props(pad2, "ACP1", imei="356789012345678")
    sysprop2 = pad2.files[f"{_MODULE}/system.prop"]
    assert "persist.vmos.spoof.build.model=Pixel 10 Pro" in sysprop2       # build preserved
    assert "persist.vmos.spoof.imei=356789012345678" in sysprop2           # identity added
    assert sysprop2.count("persist.vmos.spoof.build.model=") == 1          # merged, not duplicated
    assert sysprop2.count("persist.vmos.spoof.imei=") == 1


def test_set_identity_props_respects_input_cap():
    # Design: a single 4148-byte async_cmd applied ZERO props; every batch/chunk
    # (resetprop sets AND the base64 file writes) must stay under the cap.
    from vmos.spoof import set_identity_props
    pad = FileModelingFakePad()
    set_identity_props(
        pad, "ACP1",
        imei="356789012345678", meid="A1000012345678", imsi="452040123456789",
        iccid="8984040000123456789", line1="+84901234567",
        android_id="a1b2c3d4e5f60718", gaid="38400000-8cf0-11bd-b23e-10b96e40000d",
        oaid="00000000-1111-2222-3333-444455556666", wifi_mac="02:00:00:11:22:33",
        bssid="02:00:00:44:55:66", serial="1A2B3C4D", drm_id="deadbeefcafe0011",
    )
    assert pad.scripts
    assert all(len(s) <= ASYNC_CMD_MAX_BYTES for s in pad.scripts)


def test_set_identity_props_persist_module_false_writes_no_module():
    from vmos.spoof import set_identity_props
    pad = FileModelingFakePad()
    set_identity_props(pad, "ACP1", imei="356789012345678", persist_module=False)
    assert pad.files == {}                                            # no module written
    assert pad.props["persist.vmos.spoof.imei"] == "356789012345678"  # runtime still set


def test_load_xpose_plugin_refuses_gms_and_vending():
    import pytest

    from vmos.spoof import GMS_DENYLIST, load_xpose_plugin
    # GMS_DENYLIST is the single source of truth (folds in the old
    # GMS_EXCLUDED_PACKAGES); GMS + Play must always be in it.
    assert {"com.google.android.gms", "com.android.vending"} <= set(GMS_DENYLIST)
    for pkg in GMS_DENYLIST:
        pad = FileModelingFakePad()
        with pytest.raises(ValueError):
            load_xpose_plugin(pad, "ACP1", name="n", target_pkg=pkg, apk_url="https://h/p.apk")
        assert not any("apmt patch add" in s for s in pad.scripts)   # nothing deployed


def test_remove_spoof_deletes_runtime_keys():
    from vmos.spoof import remove_spoof
    pad = FileModelingFakePad()
    remove_spoof(pad, "ACP1")
    joined = "\n".join(pad.scripts)
    # design §E.3: clear runtime values immediately via resetprop --delete
    assert f"{MAGISK_BIN} resetprop --delete 'persist.vmos.spoof.imei'" in joined
    assert "resetprop --delete 'persist.vmos.spoof.gaid'" in joined
    assert _MODULE in joined                                          # module removed too
    # opt-out path issues no deletes
    pad2 = FileModelingFakePad()
    remove_spoof(pad2, "ACP1", clear_runtime=False)
    assert not any("resetprop --delete" in s for s in pad2.scripts)


def test_remove_spoof_clears_union_from_system_prop():
    from vmos.spoof import apply_profile, remove_spoof, set_identity_props
    pad = FileModelingFakePad()
    apply_profile(pad, "ACP1", PIXEL_10_PRO_A17, persist=True)
    set_identity_props(pad, "ACP1", imei="356789012345678")
    assert "ro.product.model=" in pad.files[f"{_MODULE}/system.prop"]  # sanity
    del pad.scripts[:]                                                 # inspect remove phase only
    remove_spoof(pad, "ACP1")
    joined = "\n".join(pad.scripts)
    assert "resetprop --delete 'ro.product.model'" in joined          # build prop (from system.prop)
    assert "resetprop --delete 'persist.vmos.spoof.imei'" in joined   # identity input
