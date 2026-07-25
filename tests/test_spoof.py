"""Unit tests for the device-spoofing toolkit (mocked shell — no network/device)."""

from vmos import DeviceProfile
from vmos.spoof import (
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
