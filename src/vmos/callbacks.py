"""Helpers for VMOS webhook callbacks.

VMOS pushes task results (ADB commands, file uploads, app operations, image
upgrades, instance status changes, ...) to a callback URL you configure in the
VMOS web console. This module parses those JSON payloads into a typed
:class:`CallbackEvent`.

Usage (e.g. inside a Flask/FastAPI handler)::

    from vmos.callbacks import parse_callback

    @app.post("/vmos/callback")
    def vmos_callback(payload: dict):
        event = parse_callback(payload)
        if event.kind == "app_install" and event.succeeded:
            ...
        return {"ok": True}

Notes
-----
* ``taskBusinessType`` discriminates the callback kind (e.g. 1003 = app
  installation). Unknown types parse fine - ``kind`` falls back to ``"unknown"``
  and every field stays accessible via :attr:`CallbackEvent.raw`.
* ``taskStatus`` values: 3 = success, negative / other values indicate
  failure states; check ``taskResult`` for details.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

__all__ = ["CallbackEvent", "parse_callback", "TASK_BUSINESS_TYPES"]

#: Known ``taskBusinessType`` discriminator values -> event kind.
TASK_BUSINESS_TYPES: Dict[int, str] = {
    1003: "app_install",
    1004: "app_uninstall",
    1005: "app_stop",
    1006: "app_restart",
    1007: "app_start",
    1009: "file_upload",
    4001: "user_image_upload",
}

#: ``taskStatus`` value that marks a successfully finished task.
TASK_STATUS_SUCCESS = 3


@dataclass
class CallbackEvent:
    """A parsed VMOS callback payload.

    Attributes not covered by the common fields remain available in
    :attr:`raw` (e.g. ``cmd`` / ``cmdResult`` for ADB command callbacks,
    ``apps`` for app-operation callbacks, ``fileId`` for uploads).
    """

    kind: str
    task_business_type: Optional[int] = None
    task_id: Optional[int] = None
    pad_code: Optional[str] = None
    task_status: Optional[int] = None
    task_result: Optional[str] = None
    end_time: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def succeeded(self) -> bool:
        """``True`` when the task finished successfully.

        Uses ``taskStatus == 3`` when present, otherwise falls back to the
        boolean ``result`` field (used by e.g. file-upload callbacks).
        """
        if self.task_status is not None:
            return self.task_status == TASK_STATUS_SUCCESS
        result = self.raw.get("result")
        if isinstance(result, bool):
            return result
        return str(self.task_result or "").lower() == "success"

    def get(self, key: str, default: Any = None) -> Any:
        """Access any extra payload field by its original (camelCase) name."""
        return self.raw.get(key, default)


def parse_callback(payload: Dict[str, Any]) -> CallbackEvent:
    """Parse a VMOS callback JSON payload into a :class:`CallbackEvent`."""
    if not isinstance(payload, dict):
        raise TypeError(f"callback payload must be a dict, got {type(payload).__name__}")
    tbt = payload.get("taskBusinessType")
    kind = TASK_BUSINESS_TYPES.get(tbt, "unknown") if isinstance(tbt, int) else "unknown"
    if kind == "unknown":
        # Distinguish a couple of well-known payload shapes without taskBusinessType.
        if "cmd" in payload or "cmdResult" in payload:
            kind = "adb_command"
        elif "padStatus" in payload or "vmStatus" in payload:
            kind = "instance_status"
    return CallbackEvent(
        kind=kind,
        task_business_type=tbt if isinstance(tbt, int) else None,
        task_id=payload.get("taskId"),
        pad_code=payload.get("padCode"),
        task_status=payload.get("taskStatus"),
        task_result=payload.get("taskResult"),
        end_time=payload.get("endTime"),
        raw=payload,
    )
