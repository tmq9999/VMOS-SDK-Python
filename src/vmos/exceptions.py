"""Exception hierarchy for the VMOS Cloud SDK.

All SDK errors derive from :class:`VMOSError`, so callers can use a single
``except VMOSError`` for blanket handling, or catch specific subclasses.
"""

from __future__ import annotations

from typing import Any, Optional

__all__ = [
    "VMOSError",
    "VMOSHTTPError",
    "VMOSAPIError",
    "VMOSAuthError",
    "VMOSRateLimitError",
]

#: Business codes that indicate an authentication / signing problem.
AUTH_ERROR_CODES = {
    2019: "Signature verification failed",
    2031: "Invalid key (AccessKey not found)",
    2032: "Required header missing",
    2033: "Timestamp expired or malformed",
}

#: Business codes that indicate throttling.
RATE_LIMIT_CODES = {1218}


class VMOSError(Exception):
    """Base class for every error raised by this SDK."""


class VMOSHTTPError(VMOSError):
    """Transport-level failure: non-2xx HTTP status or malformed response body.

    Attributes
    ----------
    status_code:
        HTTP status code (``None`` when the response never arrived).
    body:
        Raw response text, when available.
    """

    def __init__(self, message: str, *, status_code: Optional[int] = None, body: Optional[str] = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class VMOSAPIError(VMOSError):
    """The API answered with a business error (``code != 200``).

    Attributes
    ----------
    code:
        VMOS business status code (e.g. ``1002``).
    msg:
        Human-readable message returned by the API.
    ts:
        Server timestamp (milliseconds), when present.
    data:
        Any ``data`` payload attached to the error response.
    path:
        Request path that produced the error.
    """

    def __init__(
        self,
        code: int,
        msg: str,
        *,
        ts: Optional[int] = None,
        data: Any = None,
        path: Optional[str] = None,
    ) -> None:
        super().__init__(f"VMOS API error {code}: {msg}" + (f" (path={path})" if path else ""))
        self.code = code
        self.msg = msg
        self.ts = ts
        self.data = data
        self.path = path

    @classmethod
    def from_payload(cls, payload: dict, path: Optional[str] = None) -> "VMOSAPIError":
        """Build the most specific error subclass for an API error payload."""
        code = payload.get("code", -1)
        msg = str(payload.get("msg", "unknown error"))
        kwargs = {"ts": payload.get("ts"), "data": payload.get("data"), "path": path}
        if code in AUTH_ERROR_CODES:
            return VMOSAuthError(code, msg, **kwargs)
        if code in RATE_LIMIT_CODES:
            return VMOSRateLimitError(code, msg, **kwargs)
        return cls(code, msg, **kwargs)


class VMOSAuthError(VMOSAPIError):
    """Authentication / signature problem (codes 2019, 2031, 2032, 2033)."""


class VMOSRateLimitError(VMOSAPIError):
    """The API rejected the request due to throttling (e.g. code 1218)."""
