"""Response envelope model for the VMOS Cloud SDK.

Every VMOS endpoint answers with the same JSON envelope::

    {"code": 200, "msg": "success", "ts": 1756021167163, "data": ...}

SDK methods return ``data`` directly (raising :class:`~vmos.exceptions.VMOSAPIError`
when ``code != 200``). The full envelope is available through the
``*_raw`` client helpers, which return an :class:`APIResponse`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

__all__ = ["APIResponse"]


@dataclass
class APIResponse:
    """Parsed VMOS response envelope."""

    code: int
    msg: str
    ts: Optional[int] = None
    data: Any = None
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def ok(self) -> bool:
        """``True`` when the business status code is 200."""
        return self.code == 200

    @classmethod
    def from_json(cls, payload: dict) -> "APIResponse":
        return cls(
            code=payload.get("code", -1),
            msg=str(payload.get("msg", "")),
            ts=payload.get("ts"),
            data=payload.get("data"),
            raw=payload,
        )
