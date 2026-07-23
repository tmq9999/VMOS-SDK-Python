"""Base classes shared by all generated API namespaces."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional

if TYPE_CHECKING:  # pragma: no cover
    from ..client import AsyncVMOSClient, VMOSClient

__all__ = ["SyncAPIResource", "AsyncAPIResource", "build_payload"]


def build_payload(named: Mapping[str, Any], extra: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    """Merge documented params (skipping ``None``) with caller-supplied extras.

    ``extra`` lets callers pass parameters added by VMOS after this SDK
    release without waiting for an update - they are sent verbatim.
    """
    payload: Dict[str, Any] = {k: v for k, v in named.items() if v is not None}
    if extra:
        payload.update(extra)
    return payload


class SyncAPIResource:
    """A namespace of endpoint wrappers bound to a :class:`vmos.VMOSClient`."""

    def __init__(self, client: "VMOSClient") -> None:
        self._client = client


class AsyncAPIResource:
    """A namespace of endpoint wrappers bound to a :class:`vmos.AsyncVMOSClient`."""

    def __init__(self, client: "AsyncVMOSClient") -> None:
        self._client = client
