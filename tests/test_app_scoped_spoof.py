"""Unit tests for the app-scoped Build.* spoof + GMS/Play denylist scoping and the
prop-key reconciliation (mocked shell — no network/device).

Covers P5-DEV-006:

* prop-key correctness — the Python side writes the EXACT keys the compiled XPose
  plugin reads (``persist.vmos.spoof.{...,line,androidid,wifimac,drmid}`` and the
  new ``persist.vmos.spoof.build.*``);
* denylist target enumeration — "all installed apps EXCEPT GMS/Play";
* build-prop writing — ``set_build_props`` + ``Profile.build_hook_*`` + the Java
  Hook Backend integration.
"""

import re

from vmos.profile import generate_profile
from vmos.spoof import (
    _BUILD_PROPS,
    _IDENTITY_PROPS,
    GMS_DENYLIST,
    MAGISK_BIN,
    app_scoped_targets,
    list_installed_packages,
    set_build_props,
    set_identity_props,
)

_RESETPROP = re.compile(r"resetprop -n '([^']*)' '([^']*)'")

#: The exact set of prop keys the compiled plugin reads (SANDBOX-verified against
#: the plugin dex; see design P5-ARCH-005). The Python side must write these.
_PLUGIN_IDENTITY_READS = {
    "persist.vmos.spoof." + suffix
    for suffix in (
        "imei", "meid", "imsi", "iccid", "line", "androidid",
        "gaid", "oaid", "wifimac", "bssid", "serial", "drmid",
    )
}
_PLUGIN_BUILD_READS = {
    "persist.vmos.spoof.build." + suffix
    for suffix in (
        "model", "manufacturer", "brand", "device",
        "product", "fingerprint", "release",
    )
}


# --------------------------------------------------------------------------- #
# Fakes
# --------------------------------------------------------------------------- #
class FakeShell:
    """Minimal PadRootShell stand-in: replies to ``sh`` via a handler."""

    def __init__(self, handler):
        self._handler = handler
        self.scripts = []

    def sh(self, script):
        self.scripts.append(script)
        return self._handler(script)


class FakePadClient:
    """VMOSClient stand-in capturing async_cmd scripts + replaying resetprop writes."""

    def __init__(self, handler):
        self._handler = handler
        self.scripts = []
        self.props = {}
        self._tid = 0
        self._last = ""
        client = self

        class _Instance:
            def async_cmd(self, pad_codes, script_content):
                client.scripts.append(script_content)
                client._last = script_content
                for k, v in _RESETPROP.findall(script_content):
                    client.props[k] = v
                client._tid += 1
                return [{"taskId": client._tid}]

        class _Tasks:
            def pad_task_detail(self, task_ids):
                return [{"taskStatus": 3, "taskResult": client._handler(client._last)}]

        self.instance = _Instance()
        self.tasks = _Tasks()


def _root_reply(script):
    s = script.strip()
    if s == "id -u":
        return "0"
    if "-x" in s and MAGISK_BIN in s:
        return "YES"
    if "apmt patch" in s:
        return "add Patch success"
    return ""


# --------------------------------------------------------------------------- #
# 1. Prop-key correctness — the reconciliation bug fix
# --------------------------------------------------------------------------- #
def test_identity_prop_keys_match_plugin_reads_exactly():
    # Every prop key the SDK writes must be one the plugin actually reads.
    assert set(_IDENTITY_PROPS.values()) == _PLUGIN_IDENTITY_READS


def test_line1_kwarg_writes_dot_line_key_not_line1():
    # The reconciliation: kwarg stays `line1`, but the prop key is `.line`.
    assert _IDENTITY_PROPS["line1"] == "persist.vmos.spoof.line"
    assert "persist.vmos.spoof.line1" not in _IDENTITY_PROPS.values()


def test_androidid_wifimac_drmid_family_keys():
    # The flagged family already collapses to the no-underscore plugin keys.
    assert _IDENTITY_PROPS["android_id"] == "persist.vmos.spoof.androidid"
    assert _IDENTITY_PROPS["wifi_mac"] == "persist.vmos.spoof.wifimac"
    assert _IDENTITY_PROPS["drm_id"] == "persist.vmos.spoof.drmid"


def test_set_identity_props_writes_dot_line_key():
    client = FakePadClient(_root_reply)
    out = set_identity_props(client, "ACP1", line1="84987654321")
    assert out == {"persist.vmos.spoof.line": "84987654321"}
    joined = "\n".join(client.scripts)
    assert "persist.vmos.spoof.line " in joined or "'persist.vmos.spoof.line'" in joined
    assert "persist.vmos.spoof.line1" not in joined


def test_profile_identity_props_uses_dot_line_key():
    prof = generate_profile("pixel10pro", "VN", "Viettel", seed=1)
    prof.telephony.line1 = "84987654321"
    props = prof.identity_props()
    assert props["persist.vmos.spoof.line"] == "84987654321"
    assert "persist.vmos.spoof.line1" not in props


# --------------------------------------------------------------------------- #
# 2. Build-prop writing (persist.vmos.spoof.build.*)
# --------------------------------------------------------------------------- #
def test_build_prop_map_keys_match_plugin():
    # The 7 string fields the plugin spoofs, plus the disabled-by-default sdk_int.
    assert set(_BUILD_PROPS.values()) - {"persist.vmos.spoof.build.sdk_int"} == _PLUGIN_BUILD_READS
    assert _BUILD_PROPS["sdk_int"] == "persist.vmos.spoof.build.sdk_int"


def test_set_build_props_writes_expected_keys():
    client = FakePadClient(_root_reply)
    out = set_build_props(
        client, "ACP1",
        model="Pixel 10 Pro", manufacturer="Google", brand="google",
        device="blazer", product="blazer",
        fingerprint="google/blazer/blazer:17/CP2A/1:user/release-keys",
        release="17",
    )
    assert out["persist.vmos.spoof.build.model"] == "Pixel 10 Pro"
    assert out["persist.vmos.spoof.build.fingerprint"].startswith("google/blazer")
    assert out["persist.vmos.spoof.build.release"] == "17"
    joined = "\n".join(client.scripts)
    assert "persist.vmos.spoof.build.model" in joined and "Pixel 10 Pro" in joined
    # SDK_INT must NOT be written unless explicitly asked for (risky, off by default).
    assert "persist.vmos.spoof.build.sdk_int" not in joined


def test_set_build_props_only_writes_non_empty():
    client = FakePadClient(_root_reply)
    out = set_build_props(client, "ACP1", model="Pixel 10 Pro")  # only one field
    assert out == {"persist.vmos.spoof.build.model": "Pixel 10 Pro"}
    joined = "\n".join(client.scripts)
    assert "persist.vmos.spoof.build.brand" not in joined


def test_set_build_props_empty_is_noop():
    client = FakePadClient(_root_reply)
    out = set_build_props(client, "ACP1")
    assert out == {}
    # nothing resetprop'd (no build prop should appear)
    assert not any("persist.vmos.spoof.build" in s for s in client.scripts)


def test_set_build_props_sdk_int_opt_in_stringified():
    client = FakePadClient(_root_reply)
    out = set_build_props(client, "ACP1", sdk_int=36)
    assert out == {"persist.vmos.spoof.build.sdk_int": "36"}


def test_profile_build_hook_props_and_kwargs():
    prof = generate_profile("pixel10pro", "VN", "Viettel", seed=1)
    props = prof.build_hook_props()
    assert props["persist.vmos.spoof.build.model"] == "Pixel 10 Pro"
    assert props["persist.vmos.spoof.build.brand"] == "google"
    assert props["persist.vmos.spoof.build.fingerprint"] == prof.build.fingerprint
    # SDK_INT is intentionally never emitted here.
    assert not any(k.endswith(".sdk_int") for k in props)
    kwargs = prof.build_hook_kwargs()
    assert kwargs["model"] == "Pixel 10 Pro"
    assert "sdk_int" not in kwargs
    # kwargs feed set_build_props directly.
    assert set(kwargs).issubset({
        "model", "manufacturer", "brand", "device", "product", "fingerprint", "release",
    })


# --------------------------------------------------------------------------- #
# 3. Denylist target enumeration ("all installed EXCEPT GMS/Play")
# --------------------------------------------------------------------------- #
_PM_OUTPUT = "\n".join([
    "package:com.google.android.gms",
    "package:com.android.vending",
    "package:com.google.android.gsf",
    "package:com.liuzh.deviceinfo",
    "package:com.example.beta",
    "package:com.example.alpha",
    "package:com.example.alpha",  # duplicate -> deduped
])


def test_gms_denylist_contents():
    assert GMS_DENYLIST == frozenset({
        "com.google.android.gms",
        "com.android.vending",
        "com.google.android.gsf",
    })


def test_list_installed_packages_parses_and_sorts():
    shell = FakeShell(lambda s: _PM_OUTPUT)
    pkgs = list_installed_packages(shell)
    assert pkgs == [
        "com.android.vending",
        "com.example.alpha",
        "com.example.beta",
        "com.google.android.gms",
        "com.google.android.gsf",
        "com.liuzh.deviceinfo",
    ]
    # queried both user (-3) and system (-s) sets
    joined = "\n".join(shell.scripts)
    assert "pm list packages -3" in joined and "pm list packages -s" in joined


def test_app_scoped_targets_excludes_gms_play():
    shell = FakeShell(lambda s: _PM_OUTPUT)
    targets = app_scoped_targets(shell)
    assert targets == ["com.example.alpha", "com.example.beta", "com.liuzh.deviceinfo"]
    for denied in GMS_DENYLIST:
        assert denied not in targets


def test_app_scoped_targets_extra_denylist():
    shell = FakeShell(lambda s: _PM_OUTPUT)
    targets = app_scoped_targets(shell, extra_denylist=["com.example.beta"])
    assert targets == ["com.example.alpha", "com.liuzh.deviceinfo"]
    # base denylist still applies alongside the extra
    assert "com.google.android.gms" not in targets


def test_list_installed_packages_ignores_non_package_lines():
    shell = FakeShell(lambda s: "some warning\npackage:com.only.one\n\n")
    assert list_installed_packages(shell) == ["com.only.one"]


# --------------------------------------------------------------------------- #
# 4. JavaHookBackend integration — build props + auto-scope denylist
# --------------------------------------------------------------------------- #
def _pad_reply(script):
    s = script.strip()
    if "pm list packages" in s:
        return _PM_OUTPUT
    return _root_reply(script)


def test_java_hook_writes_build_props_from_profile():
    from vmos import JavaHookBackend

    pad = FakePadClient(_pad_reply)
    backend = JavaHookBackend(pad, "ACP1")  # no apk source; just refresh props
    res = backend.apply(generate_profile("pixel10pro", "VN", "Viettel", seed=1))
    # Build.* props written app-scoped, straight from the profile's build section.
    assert pad.props["persist.vmos.spoof.build.model"] == "Pixel 10 Pro"
    assert pad.props["persist.vmos.spoof.build.brand"] == "google"
    assert res["build_props_set"]["persist.vmos.spoof.build.model"] == "Pixel 10 Pro"
    # SDK_INT never auto-written (risky).
    assert "persist.vmos.spoof.build.sdk_int" not in pad.props


def test_java_hook_spoof_build_can_be_disabled():
    from vmos import JavaHookBackend

    pad = FakePadClient(_pad_reply)
    backend = JavaHookBackend(pad, "ACP1", spoof_build=False)
    res = backend.apply(generate_profile("pixel10pro", "VN", "Viettel", seed=1))
    assert res["build_props_set"] == {}
    assert not any(k.startswith("persist.vmos.spoof.build.") for k in pad.props)
    # identity props are still written
    assert pad.props["persist.vmos.spoof.imei"]


def test_java_hook_auto_scope_all_enumerates_minus_denylist():
    from vmos import JavaHookBackend

    pad = FakePadClient(_pad_reply)
    backend = JavaHookBackend(
        pad, "ACP1", apk_url="https://h/p.apk", auto_scope_all=True,
    )
    prof = generate_profile("pixel10pro", "VN", "Viettel", seed=1)  # no target_apps
    res = backend.apply(prof)
    loaded_pkgs = [entry["pkg"] for entry in res["loaded"]]
    # scope = every installed app EXCEPT GMS/Play, written back onto the profile
    assert loaded_pkgs == ["com.example.alpha", "com.example.beta", "com.liuzh.deviceinfo"]
    assert prof.runtime.target_apps == loaded_pkgs
    for denied in GMS_DENYLIST:
        assert denied not in loaded_pkgs
    # one apmt patch per package (apmt is per-package, no wildcard)
    joined = "\n".join(pad.scripts)
    assert joined.count("apmt patch add") == 3
    assert "auto-scoped" in res["note"]


def test_java_hook_auto_scope_all_extra_denylist():
    from vmos import JavaHookBackend

    pad = FakePadClient(_pad_reply)
    backend = JavaHookBackend(
        pad, "ACP1", apk_url="https://h/p.apk", auto_scope_all=True,
        scope_denylist_extra=["com.example.beta"],
    )
    prof = generate_profile("pixel10pro", "VN", "Viettel", seed=1)
    res = backend.apply(prof)
    loaded_pkgs = [entry["pkg"] for entry in res["loaded"]]
    assert loaded_pkgs == ["com.example.alpha", "com.liuzh.deviceinfo"]
