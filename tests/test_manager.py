"""Unit tests for the Profile Manager orchestrator (mocked shell — no device).

Uses a *stateful* fake pad: it records every ``resetprop`` write and replays it
on ``getprop``, so ``manager.apply(profile)`` followed by
``manager.verify(profile)`` round-trips through both backends exactly as it would
on a real device.
"""

import re

import pytest

from vmos import (
    JavaHookBackend,
    ProfileManager,
    ProfileValidationError,
    SystemApplierBackend,
    generate_profile,
    standard_manager,
)
from vmos.spoof import MAGISK_BIN

_RESETPROP = re.compile(r"resetprop -n '([^']*)' '([^']*)'")
_GETPROP = re.compile(r"getprop ([\w.]+)")
_ANDROID_ID_PUT = re.compile(r"settings put secure android_id '([^']*)'")


class StatefulFakePad:
    """VMOSClient stand-in that models a rooted Magisk pad's prop store."""

    def __init__(self):
        self.props = {}
        self.settings_android_id = ""
        self.scripts = []
        self._tid = 0
        self._last = ""
        pad = self

        class _Instance:
            def async_cmd(self, pad_codes, script_content):
                pad.scripts.append(script_content)
                pad._last = script_content
                pad._apply_writes(script_content)
                pad._tid += 1
                return [{"taskId": pad._tid}]

        class _Tasks:
            def pad_task_detail(self, task_ids):
                return [{"taskStatus": 3, "taskResult": pad._output(pad._last)}]

        class _Touch:
            def simulate_swipe(self, *a, **k):
                return [{"taskId": 1}]

        self.instance = _Instance()
        self.tasks = _Tasks()
        self.touch = _Touch()

    def _apply_writes(self, script):
        for k, v in _RESETPROP.findall(script):
            self.props[k] = v
        m = _ANDROID_ID_PUT.search(script)
        if m:
            self.settings_android_id = m.group(1)

    def _output(self, script):
        s = script.strip()
        if s == "id -u":
            return "0"
        if "-x" in s and MAGISK_BIN in s:
            return "YES"
        if "settings get secure android_id" in s:
            return self.settings_android_id
        if "getprop" in s and "echo" in s:
            return "\n".join(f"{k}={self.props.get(k, '')}" for k in _GETPROP.findall(s))
        if "apmt patch" in s:
            return "add Patch success"
        return ""


def _profile():
    return generate_profile(
        "pixel10pro", "VN", "Viettel", seed=20260724,
        target_apps=["com.liuzh.deviceinfo", "com.ytheekshana.deviceinfo"],
    )


def test_standard_manager_registers_both_backends():
    mgr = standard_manager(StatefulFakePad(), "ACP1")
    assert [b.name for b in mgr.backends] == ["system_applier", "java_hook"]
    assert [b.layer for b in mgr.backends] == [1, 2]


def test_apply_drives_all_backends_from_one_profile():
    pad = StatefulFakePad()
    mgr = standard_manager(pad, "ACP1")
    prof = _profile()
    out = mgr.apply(prof)
    names = [b["backend"] for b in out["backends"]]
    assert names == ["system_applier", "java_hook"]
    # Layer 1 wrote the build identity via resetprop
    assert pad.props["ro.product.model"] == "Pixel 10 Pro"
    assert pad.props["ro.build.version.sdk"] == "37"
    # Layer 2 wrote the framework-held identity props, straight from the profile
    assert pad.props["persist.vmos.spoof.imei"] == prof.telephony.imei[0]
    assert pad.props["persist.vmos.spoof.gaid"] == prof.identity.gaid
    assert pad.props["persist.vmos.spoof.androidid"] == prof.identity.android_id


def test_apply_then_verify_roundtrips_ok():
    pad = StatefulFakePad()
    mgr = standard_manager(pad, "ACP1")
    prof = _profile()
    mgr.apply(prof)
    result = mgr.verify(prof)
    assert result["ok"] is True
    per = {b["backend"]: b["result"] for b in result["backends"]}
    assert per["system_applier"]["ok"] is True
    assert per["java_hook"]["ok"] is True
    assert per["java_hook"]["checks"]["persist.vmos.spoof.imei"]["match"] is True


def test_apply_rejects_invalid_profile():
    pad = StatefulFakePad()
    mgr = standard_manager(pad, "ACP1")
    prof = _profile()
    prof.telephony.imei = ["123"]  # invalid IMEI -> error-level issue
    with pytest.raises(ProfileValidationError) as exc:
        mgr.apply(prof)
    assert any(i["field"].startswith("telephony.imei") for i in exc.value.errors)
    # nothing should have been written
    assert "ro.product.model" not in pad.props


def test_validation_can_be_disabled():
    pad = StatefulFakePad()
    prof = _profile()
    prof.telephony.imei = ["123"]
    mgr = standard_manager(pad, "ACP1", validate_before_apply=False)
    out = mgr.apply(prof)  # must not raise
    assert out["backends"][0]["backend"] == "system_applier"


def test_java_hook_loads_plugin_into_targets_when_apk_given():
    pad = StatefulFakePad()
    backend = JavaHookBackend(pad, "ACP1", apk_url="https://h/p.apk", plugin_name="vmos_profile")
    res = backend.apply(_profile())
    loaded_pkgs = [l["pkg"] for l in res["loaded"]]
    assert loaded_pkgs == ["com.liuzh.deviceinfo", "com.ytheekshana.deviceinfo"]
    joined = "\n".join(pad.scripts)
    assert "apmt patch add -n 'vmos_profile_com_liuzh_deviceinfo' -p 'com.liuzh.deviceinfo' -u 'https://h/p.apk'" in joined


def test_java_hook_skips_load_without_apk_but_sets_props():
    pad = StatefulFakePad()
    backend = JavaHookBackend(pad, "ACP1")  # no apk source
    res = backend.apply(_profile())
    assert res["loaded"] == []
    assert "skipped" in res["note"]
    assert pad.props["persist.vmos.spoof.imsi"]  # props still written


def test_manager_apply_is_offline_safe_for_construction():
    # A manager with no client/pad can still be built and hold backends.
    mgr = ProfileManager(backends=[])
    assert mgr.backends == []
    assert mgr.apply.__doc__  # sanity: method present


def test_java_hook_excludes_gms_and_vending_from_scoping():
    # Design §B hard guard: an identity hook must NEVER be deployed into GMS or the
    # Play Store (they must read the real identity). Even if a profile lists them,
    # load_xpose_plugin must never be called for those two packages.
    pad = StatefulFakePad()
    prof = generate_profile(
        "pixel10pro", "VN", "Viettel", seed=20260724,
        target_apps=["com.google.android.gms", "com.android.vending", "com.liuzh.deviceinfo"],
    )
    backend = JavaHookBackend(pad, "ACP1", apk_url="https://h/p.apk", plugin_name="vmos_profile")
    res = backend.apply(prof)
    assert [l["pkg"] for l in res["loaded"]] == ["com.liuzh.deviceinfo"]  # only the real app
    assert res["excluded"] == ["com.google.android.gms", "com.android.vending"]
    joined = "\n".join(pad.scripts)
    assert "apmt patch add" in joined                       # the real app WAS scoped
    assert "com.google.android.gms" not in joined           # GMS never touched
    assert "com.android.vending" not in joined              # Play never touched
    # props are still set for the whole device (system-wide inputs are inert for GMS)
    assert pad.props["persist.vmos.spoof.imei"] == prof.telephony.imei[0]
