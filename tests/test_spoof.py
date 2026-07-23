"""Unit tests for the device-spoofing toolkit (mocked shell — no network/device)."""

import httpx

from vmos import DeviceProfile
from vmos.spoof import (
    MAGISK_BIN,
    PIXEL_10_PRO_A17,
    PadRootShell,
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
