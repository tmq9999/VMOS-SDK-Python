"""Webhook callback parsing tests using payload examples from the official docs."""

import pytest

from vmos.callbacks import CallbackEvent, parse_callback


def test_app_install_callback():
    payload = {
        "endTime": 1734939747000,
        "padCode": "AC22030022001",
        "taskBusinessType": 1003,
        "taskContent": "",
        "taskId": 10613,
        "taskResult": "Success",
        "taskStatus": 3,
    }
    ev = parse_callback(payload)
    assert ev.kind == "app_install"
    assert ev.pad_code == "AC22030022001"
    assert ev.task_id == 10613
    assert ev.succeeded


def test_file_upload_callback_uses_result_bool():
    payload = {
        "errorCode": None,
        "fileId": "cfec132ab3c4e1aff5515c4467d9bbe460",
        "padCode": "AC22030022001",
        "result": True,
        "taskBusinessType": 1009,
        "taskId": 10659,
    }
    ev = parse_callback(payload)
    assert ev.kind == "file_upload"
    assert ev.succeeded
    assert ev.get("fileId") == "cfec132ab3c4e1aff5515c4467d9bbe460"


def test_adb_command_callback_detected_without_known_type():
    payload = {
        "cmd": "cd /root;ls",
        "cmdResult": "...",
        "padCode": "AC22030022001",
        "taskId": 10614,
        "taskStatus": 3,
        "taskBusinessType": 999999,
    }
    ev = parse_callback(payload)
    assert ev.kind in ("adb_command", "unknown")
    assert ev.succeeded


def test_failed_task():
    ev = parse_callback({"taskBusinessType": 1004, "taskStatus": -1, "taskResult": "Failed"})
    assert ev.kind == "app_uninstall"
    assert not ev.succeeded


def test_unknown_kind_keeps_raw():
    ev = parse_callback({"foo": "bar"})
    assert ev.kind == "unknown"
    assert ev.raw == {"foo": "bar"}
    assert isinstance(ev, CallbackEvent)


def test_non_dict_rejected():
    with pytest.raises(TypeError):
        parse_callback([1, 2, 3])  # type: ignore[arg-type]
