"""Unit tests for the headless root-stack flow (Magisk + Zygisk-Next + LSPosed).

All HTTP/device interaction is mocked. These cover the three real-device-verified
bug fixes plus the reboot-readiness and env-var-alias behavior:

* Bug #1 — task polling uses the integer-array body ``{"taskIds":[<int>]}``.
* Bug #2 — download completion is detected by md5/size on the device (never
  ``fileTaskDetail``).
* Bug #3 — install success is verified by on-device **state**, not by parsing
  truncatable async task output.
* Reboot readiness tolerates business code 110031 (instance not ready).
* Env-var aliases for the pad code (VMOS_PAD_CODE / VMOS_PADCODE / PADCODE).
"""

import json

import httpx
import pytest

from vmos import VMOSClient
from vmos.exceptions import VMOSAPIError
from vmos.spoof import (
    PAD_NOT_READY_CODE,
    PadRootShell,
    coerce_task_ids,
    install_root_stack_headless,
    pad_online,
    resolve_pad_code,
    stage_root_stack_install,
    verify_root_stack,
    wait_for_file_download,
    wait_for_pad_ready,
)

# --- fixtures / fakes ------------------------------------------------------- #

# Compact state output emitted by the stage/install script (Bug-fix #3).
_STAGE_OK = "\n".join([
    "INSTALL_RC=0",
    "MODULES_RC=0",
    "PROP=1",
    "BIN_OK=magisk64", "BIN_OK=magisk32", "BIN_OK=magiskpolicy",
    "BIN_OK=magiskboot", "BIN_OK=busybox",
    "MOD_OK=zygisksu", "MOD_OK=zygisk_lsposed",
    "STAGE_DONE",
])

# Post-reboot verification output with every gate passing.
_VERIFY_OK = "\n".join([
    "PROP=1",
    "MAGISKVER=27.0-kitsune",
    "BOOT=1",
    "LSPD=running",
    "ZN=running",
    "MOD_ENABLED=zygisksu",
    "MOD_ENABLED=zygisk_lsposed",
    "VERIFY_DONE",
])


class FakeShell:
    """Duck-typed :class:`PadRootShell`: returns scripted output, records scripts."""

    def __init__(self, reply):
        self._reply = reply
        self.scripts = []

    def sh(self, script):
        self.scripts.append(script)
        return self._reply(script)


class FakeRootClient:
    """Full fake VMOSClient for the orchestrator: scripted async_cmd + recorders.

    ``pad_task_detail`` asserts every polled task id is an ``int`` — a standing
    guard that the whole flow submits the integer-array body form (Bug #1).
    """

    def __init__(self, reply, *, pad_records=None):
        self._reply = reply
        self._tid = 0
        self._last = ""
        self.scripts = []
        self.uploads = []
        self.restarts = []
        self.user_pad_list_calls = []
        self._pad_records = [] if pad_records is None else pad_records
        outer = self

        class _Instance:
            def async_cmd(self, pad_codes, script_content):
                outer.scripts.append(script_content)
                outer._last = outer._reply(script_content)
                outer._tid += 1
                return [{"taskId": outer._tid}]

            def restart(self, pad_codes):
                outer.restarts.append(list(pad_codes))
                return [{"taskId": 9999}]

        class _Tasks:
            def pad_task_detail(self, task_ids):
                assert all(isinstance(t, int) for t in task_ids), task_ids
                return [{"taskStatus": 3, "taskResult": outer._last}]

        class _Apps:
            def upload_file_v3(self, pad_codes, **kwargs):
                outer.uploads.append({"pad_codes": list(pad_codes), **kwargs})
                return [{"taskId": 5000}]

        class _Phone:
            def user_pad_list(self, **kwargs):
                outer.user_pad_list_calls.append(kwargs)
                return outer._pad_records

        self.instance = _Instance()
        self.tasks = _Tasks()
        self.apps = _Apps()
        self.phone = _Phone()


class ReadinessClient:
    """async_cmd raises ``error_code`` for the first ``fail_times`` calls, then OK."""

    def __init__(self, *, fail_times, error_code=PAD_NOT_READY_CODE):
        self.fail_times = fail_times
        self.error_code = error_code
        self.calls = 0
        outer = self

        class _Instance:
            def async_cmd(self, pad_codes, script_content):
                outer.calls += 1
                if outer.calls <= outer.fail_times:
                    raise VMOSAPIError(outer.error_code, "实例状态未就绪")
                return [{"taskId": 1}]

        class _Tasks:
            def pad_task_detail(self, task_ids):
                assert all(isinstance(t, int) for t in task_ids)
                return [{"taskStatus": 3, "taskResult": "READY_OK"}]

        self.instance = _Instance()
        self.tasks = _Tasks()


class PhoneClient:
    """Fake exposing only ``phone.user_pad_list`` (records the body kwargs)."""

    def __init__(self, records):
        self._records = records
        self.calls = []
        outer = self

        class _Phone:
            def user_pad_list(self, **kwargs):
                outer.calls.append(kwargs)
                return outer._records

        self.phone = _Phone()


# --- Bug #1: integer-array task polling ------------------------------------- #

def test_coerce_task_ids_normalizes_shapes():
    assert coerce_task_ids([{"taskId": 5}]) == [5]           # object form -> ints
    assert coerce_task_ids(7) == [7]                          # bare int
    assert coerce_task_ids([1, 2, 3]) == [1, 2, 3]            # already ints
    assert coerce_task_ids([{"taskId": 1}, 2]) == [1, 2]      # mixed
    assert coerce_task_ids([{"taskId": "9"}]) == [9]          # stringy ids -> int
    assert coerce_task_ids(None) == []
    assert coerce_task_ids([{"other": 1}]) == []              # no taskId -> skipped


def test_pad_root_shell_sends_integer_array_task_ids():
    bodies = []

    def handler(request):
        path = request.url.path
        body = json.loads(request.content.decode("utf-8")) if request.content else {}
        if path.endswith("/asyncCmd"):
            return httpx.Response(200, json={"code": 200, "msg": "ok", "ts": 1, "data": [{"taskId": 42}]})
        if path.endswith("/padTaskDetail"):
            bodies.append(body)
            return httpx.Response(200, json={"code": 200, "msg": "ok", "ts": 1,
                                             "data": [{"taskStatus": 3, "taskResult": "hi"}]})
        return httpx.Response(200, json={"code": 200, "msg": "ok", "ts": 1, "data": {}})

    client = VMOSClient("ak", "sk", http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    shell = PadRootShell(client, "ACP1", poll_timeout=5, poll_interval=0)
    out = shell.sh("echo hi")
    assert out == "hi"
    assert bodies, "padTaskDetail must have been polled"
    # The gateway rejects the object form; the wire body must be integer-array.
    assert bodies[0] == {"taskIds": [42]}
    assert all(isinstance(t, int) for t in bodies[0]["taskIds"])


# --- Bug #2: md5 / size download wait --------------------------------------- #

def test_wait_for_file_download_md5_match():
    md5 = "7800ffacdc2112216c3d0b278e2a8d28"
    calls = {"n": 0}

    def reply(script):
        calls["n"] += 1
        if calls["n"] < 3:                      # still downloading, wrong md5
            return "SIZE=1000\nMD5=deadbeef"
        return f"SIZE=27219650\nMD5={md5}"

    shell = FakeShell(reply)
    res = wait_for_file_download(
        shell, "/sdcard/Download/magisk_payload.gz",
        expected_md5=md5.upper(),               # case-insensitive match
        timeout=5, interval=0,
    )
    assert res["ready"] is True
    assert res["md5"] == md5
    assert res["polls"] == 3
    assert res["detail"] == "md5-match"
    assert "md5sum" in shell.scripts[0]         # probed on-device, not fileTaskDetail


def test_wait_for_file_download_size_stable():
    seq = [100, 5000, 27219650, 27219650, 27219650, 27219650]
    state = {"i": 0}

    def reply(script):
        value = seq[min(state["i"], len(seq) - 1)]
        state["i"] += 1
        return f"SIZE={value}\nMD5="

    res = wait_for_file_download(FakeShell(reply), "/sdcard/Download/x.gz",
                                timeout=5, interval=0, stable_polls=2)
    assert res["ready"] is True
    assert res["size"] == 27219650
    assert res["detail"] == "size-stable"


def test_wait_for_file_download_timeout():
    shell = FakeShell(lambda s: "SIZE=0\nMD5=")
    res = wait_for_file_download(shell, "/sdcard/Download/x.gz",
                                expected_md5="abc", timeout=0.02, interval=0.001)
    assert res["ready"] is False
    assert res["detail"] == "timeout"


# --- Bug #3: state-based install verification ------------------------------- #

def test_stage_root_stack_install_ok():
    shell = FakeShell(lambda s: _STAGE_OK)
    res = stage_root_stack_install(shell, payload_path="/sdcard/Download/magisk_payload.gz")
    assert res["ok"] is True
    assert res["install_rc"] == 0 and res["modules_rc"] == 0
    assert res["magisk_prop"] == "1"
    assert all(res["binaries"].values())
    assert res["modules"] == {"zygisksu": True, "zygisk_lsposed": True}
    script = shell.scripts[0]
    assert "install_modules.sh" in script          # GAP fix: modules installer runs
    assert 'install.log' in script                 # verbose output redirected (Bug-fix #3)


def test_stage_root_stack_install_detects_missing_module():
    out = "\n".join([
        "INSTALL_RC=0", "MODULES_RC=0", "PROP=1",
        "BIN_OK=magisk64", "BIN_OK=magisk32", "BIN_OK=magiskpolicy",
        "BIN_OK=magiskboot", "BIN_OK=busybox",
        "MOD_OK=zygisksu", "MOD_MISS=zygisk_lsposed", "STAGE_DONE",
    ])
    res = stage_root_stack_install(FakeShell(lambda s: out))
    assert res["ok"] is False
    assert res["modules"]["zygisk_lsposed"] is False


def test_stage_root_stack_install_detects_prop_and_binary_failure():
    out = "\n".join(["INSTALL_RC=1", "PROP=", "BIN_MISS=magisk64", "STAGE_DONE"])
    res = stage_root_stack_install(FakeShell(lambda s: out))
    assert res["ok"] is False
    assert res["install_rc"] == 1
    assert res["binaries"]["magisk64"] is False


def test_stage_root_stack_install_without_modules():
    out = "\n".join([
        "INSTALL_RC=0", "PROP=1",
        "BIN_OK=magisk64", "BIN_OK=magisk32", "BIN_OK=magiskpolicy",
        "BIN_OK=magiskboot", "BIN_OK=busybox", "STAGE_DONE",
    ])
    shell = FakeShell(lambda s: out)
    res = stage_root_stack_install(shell, install_modules=False)
    assert res["ok"] is True
    assert res["modules_rc"] is None
    assert "install_modules.sh" not in shell.scripts[0]


def test_verify_root_stack_all_gates_pass():
    res = verify_root_stack(FakeShell(lambda s: _VERIFY_OK))
    assert res["ok"] is True
    assert res["magisk_active"] is True
    assert res["lspd_running"] is True
    assert res["zygisk_next_running"] is True
    assert res["modules_enabled"] == {"zygisksu": True, "zygisk_lsposed": True}


def test_verify_root_stack_fails_without_lspd():
    out = "\n".join([
        "PROP=1", "MAGISKVER=27.0", "BOOT=1", "LSPD=absent", "ZN=running",
        "MOD_ENABLED=zygisksu", "MOD_ENABLED=zygisk_lsposed", "VERIFY_DONE",
    ])
    res = verify_root_stack(FakeShell(lambda s: out))
    assert res["ok"] is False                    # files present but not truly ON
    assert res["lspd_running"] is False


def test_verify_root_stack_fails_without_magisk_prop():
    out = "\n".join([
        "PROP=0", "MAGISKVER=NONE", "BOOT=1", "LSPD=absent", "ZN=absent",
        "MOD_OFF=zygisksu", "MOD_OFF=zygisk_lsposed", "VERIFY_DONE",
    ])
    res = verify_root_stack(FakeShell(lambda s: out))
    assert res["ok"] is False
    assert res["magisk_active"] is False


# --- reboot readiness (110031 tolerance) ------------------------------------ #

def test_wait_for_pad_ready_tolerates_110031():
    client = ReadinessClient(fail_times=2)          # two "not ready", then OK
    res = wait_for_pad_ready(client, "ACP1", timeout=5, interval=0)
    assert res["ready"] is True
    assert res["attempts"] == 3


def test_wait_for_pad_ready_reraises_other_api_errors():
    client = ReadinessClient(fail_times=99, error_code=100013)
    with pytest.raises(VMOSAPIError):
        wait_for_pad_ready(client, "ACP1", timeout=5, interval=0)


def test_wait_for_pad_ready_timeout_returns_not_ready():
    client = ReadinessClient(fail_times=10 ** 9)    # never ready
    res = wait_for_pad_ready(client, "ACP1", timeout=0.02, interval=0.001)
    assert res["ready"] is False
    assert "110031" in res["detail"]


# --- userPadList online check (plural padCodes) ----------------------------- #

def test_pad_online_uses_plural_padcodes_and_cvmstatus():
    client = PhoneClient([{"padCode": "ACP1", "cvmStatus": 100}])
    assert pad_online(client, "ACP1") is True
    assert client.calls[0] == {"padCodes": ["ACP1"]}   # verified working body form


def test_pad_online_accepts_vmstatus_fallback():
    client = PhoneClient([{"padCode": "ACP1", "vmStatus": 1}])
    assert pad_online(client, "ACP1") is True


def test_pad_online_false_when_offline():
    client = PhoneClient([{"padCode": "ACP1", "cvmStatus": 0, "vmStatus": 0}])
    assert pad_online(client, "ACP1") is False


def test_pad_online_walks_nested_payload():
    client = PhoneClient({"list": [
        {"padCode": "OTHER", "cvmStatus": 0},
        {"padCode": "ACP1", "cvmStatus": 100},
    ]})
    assert pad_online(client, "ACP1") is True


# --- pad-code env aliases --------------------------------------------------- #

def test_resolve_pad_code_prefers_explicit(monkeypatch):
    monkeypatch.setenv("VMOS_PAD_CODE", "ENV1")
    assert resolve_pad_code("EXPLICIT") == "EXPLICIT"


def test_resolve_pad_code_env_alias(monkeypatch):
    for name in ("VMOS_PAD_CODE", "VMOS_PADCODE", "PADCODE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("VMOS_PADCODE", "ALIAS_PAD")   # credential-store alias
    assert resolve_pad_code() == "ALIAS_PAD"


def test_resolve_pad_code_missing_raises(monkeypatch):
    for name in ("VMOS_PAD_CODE", "VMOS_PADCODE", "PADCODE"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ValueError):
        resolve_pad_code()


# --- full orchestrator ------------------------------------------------------ #

def _happy_reply(md5):
    def reply(script):
        s = script.strip()
        if s == "id -u":
            return "0"
        if "md5sum" in script:                 # download probe
            return f"SIZE=27219650\nMD5={md5}"
        if "magisk_env/install.sh" in script:  # extract + install (+ modules)
            return _STAGE_OK
        if "READY_OK" in script:               # reboot-readiness probe
            return "READY_OK"
        if "MAGISKVER" in script:              # post-reboot verification
            return _VERIFY_OK
        return ""
    return reply


def test_install_root_stack_headless_happy_path():
    md5 = "7800ffacdc2112216c3d0b278e2a8d28"
    client = FakeRootClient(_happy_reply(md5))
    res = install_root_stack_headless(
        client, "ACP1",
        payload_url="https://cdn.example/magisk_payload.gz",
        expected_md5=md5, poll_interval=0, download_timeout=5, ready_timeout=5,
    )
    # Step 1: upload_file_v3 with the real-device-verified arguments.
    up = client.uploads[0]
    assert up["pad_codes"] == ["ACP1"]
    assert up["url"] == "https://cdn.example/magisk_payload.gz"
    assert up["customize_file_path"] == "/sdcard/Download/"
    assert up["file_name"] == "magisk_payload.gz"
    assert up["auto_install"] == 0
    assert up["md5"] == md5
    # Steps 2-6: each stage reported success.
    assert res["download"]["ready"] is True and res["download"]["detail"] == "md5-match"
    assert res["install"]["ok"] is True
    assert res["restarted"] is True and client.restarts == [["ACP1"]]
    assert res["ready"]["ready"] is True
    assert res["verified"]["ok"] is True


def test_install_root_stack_headless_requires_https():
    client = FakeRootClient(lambda s: "0")
    with pytest.raises(ValueError):
        install_root_stack_headless(client, "ACP1", payload_url="http://insecure/x.gz")


def test_install_root_stack_headless_raises_and_skips_restart_on_bad_install():
    md5 = "abc123"
    bad_stage = "\n".join([
        "INSTALL_RC=0", "MODULES_RC=1", "PROP=1",
        "BIN_OK=magisk64", "BIN_OK=magisk32", "BIN_OK=magiskpolicy",
        "BIN_OK=magiskboot", "BIN_OK=busybox",
        "MOD_OK=zygisksu", "MOD_MISS=zygisk_lsposed", "STAGE_DONE",
    ])

    def reply(script):
        s = script.strip()
        if s == "id -u":
            return "0"
        if "md5sum" in script:
            return f"SIZE=10\nMD5={md5}"
        if "magisk_env/install.sh" in script:
            return bad_stage
        return ""

    client = FakeRootClient(reply)
    with pytest.raises(RuntimeError):
        install_root_stack_headless(
            client, "ACP1", payload_url="https://cdn/x.gz",
            expected_md5=md5, poll_interval=0, download_timeout=5,
        )
    assert client.restarts == []       # install failed -> never rebooted
