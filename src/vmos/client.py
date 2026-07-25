"""Sync and async clients for the VMOS Cloud OpenAPI.

Quickstart
----------
::

    from vmos import VMOSClient

    client = VMOSClient(access_key="ak_...", secret_key="sk_...")
    pads = client.instance.pad_detail(rows=10)          # list cloud phones
    info = client.instance.pad_info(pad_code="AC3201...")

Credentials can also be supplied through the ``VMOS_ACCESS_KEY`` /
``VMOS_SECRET_KEY`` environment variables (the aliases ``VMOS_ACCESS_KEY_ID`` /
``VMOS_SECRET_ACCESS_KEY`` are also accepted for credential stores that inject
those names).

Async::

    from vmos import AsyncVMOSClient

    async with AsyncVMOSClient() as client:
        pads = await client.instance.pad_detail(rows=10)
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Mapping, Optional
from urllib.parse import urlencode

import httpx

from .auth import V2Signer
from .exceptions import VMOSAPIError, VMOSHTTPError
from .models import APIResponse

__all__ = [
    "VMOSClient",
    "AsyncVMOSClient",
    "DEFAULT_BASE_URL",
    "ACCESS_KEY_ENV_VARS",
    "SECRET_KEY_ENV_VARS",
]

DEFAULT_BASE_URL = "https://api.vmoscloud.com"
_DEFAULT_TIMEOUT = 60.0
_RETRY_BACKOFF = 0.5

#: Environment variables consulted (in order) for the access key. The canonical
#: ``VMOS_ACCESS_KEY`` is tried first (backward compatible); ``VMOS_ACCESS_KEY_ID``
#: is an accepted alias because some credential stores inject that name.
ACCESS_KEY_ENV_VARS = ("VMOS_ACCESS_KEY", "VMOS_ACCESS_KEY_ID")
#: Environment variables consulted (in order) for the secret key. ``VMOS_SECRET_KEY``
#: is tried first; ``VMOS_SECRET_ACCESS_KEY`` is an accepted alias.
SECRET_KEY_ENV_VARS = ("VMOS_SECRET_KEY", "VMOS_SECRET_ACCESS_KEY")


def _env_first(*names: str) -> str:
    """Return the first non-empty (stripped) environment variable among ``names``."""
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def _encode_json(payload: Mapping[str, Any]) -> str:
    """Serialize a JSON body once, compactly - the same string is signed and sent."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def _encode_query(query: Mapping[str, Any]) -> str:
    """Serialize a query string once - the same string is signed and sent."""
    items = {k: v for k, v in query.items() if v is not None}
    return urlencode(items)


def _parse_envelope(resp: httpx.Response, path: str) -> APIResponse:
    if resp.status_code != 200:
        raise VMOSHTTPError(
            f"HTTP {resp.status_code} for {path}",
            status_code=resp.status_code,
            body=resp.text[:2000],
        )
    try:
        payload = resp.json()
    except Exception as exc:  # noqa: BLE001 - normalize any JSON decode failure
        raise VMOSHTTPError(
            f"Non-JSON response for {path}: {resp.text[:200]!r}",
            status_code=resp.status_code,
            body=resp.text[:2000],
        ) from exc
    if not isinstance(payload, dict):
        raise VMOSHTTPError(f"Unexpected response shape for {path}", body=resp.text[:2000])
    return APIResponse.from_json(payload)


class _BaseClient:
    """Shared configuration & request preparation for sync/async clients."""

    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = 2,
    ) -> None:
        access_key = access_key or _env_first(*ACCESS_KEY_ENV_VARS)
        secret_key = secret_key or _env_first(*SECRET_KEY_ENV_VARS)
        self._signer = V2Signer(access_key, secret_key)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))

    # -- request preparation -------------------------------------------------
    def _prepare(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        files: Any = None,
    ) -> Dict[str, Any]:
        """Build url / headers / content for an exactly-as-signed request."""
        method = method.upper()
        url = self.base_url + path
        headers: Dict[str, str] = {}
        content: Optional[bytes] = None

        if files is not None:
            # Multipart upload: per V2 spec the file body is NOT signed.
            sign_payload = ""
            request_kwargs: Dict[str, Any] = {"files": files}
            if json_body:
                request_kwargs["data"] = {
                    k: v for k, v in json_body.items() if v is not None
                }
        elif method == "GET":
            qs = _encode_query(query or {})
            sign_payload = qs
            if qs:
                url = f"{url}?{qs}"
            request_kwargs = {}
        else:
            body = _encode_json(dict(json_body or {}))
            sign_payload = body
            content = body.encode("utf-8")
            headers["Content-Type"] = "application/json"
            request_kwargs = {"content": content}

        headers.update(self._signer.headers(path, sign_payload))
        return {"method": method, "url": url, "headers": headers, **request_kwargs}


class VMOSClient(_BaseClient):
    """Synchronous VMOS Cloud OpenAPI client.

    Parameters
    ----------
    access_key / secret_key:
        VMOS credentials (console: Developer -> API). Fall back to the
        ``VMOS_ACCESS_KEY`` / ``VMOS_SECRET_KEY`` environment variables (or their
        ``VMOS_ACCESS_KEY_ID`` / ``VMOS_SECRET_ACCESS_KEY`` aliases).
    base_url:
        API host, defaults to ``https://api.vmoscloud.com``.
    timeout:
        Per-request timeout in seconds (default 60).
    max_retries:
        Retries on *connection* errors only (the request was never delivered),
        with exponential backoff. Default 2.
    http_client:
        Optional pre-configured ``httpx.Client`` (useful for proxies/testing).
    """

    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = 2,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(access_key, secret_key, base_url=base_url, timeout=timeout, max_retries=max_retries)
        self._http = http_client or httpx.Client(timeout=timeout)
        self._owns_http = http_client is None
        self._attach_namespaces()

    def _attach_namespaces(self) -> None:
        from .api import SYNC_NAMESPACES

        for attr, cls in SYNC_NAMESPACES.items():
            setattr(self, attr, cls(self))

    # -- core request --------------------------------------------------------
    def request_raw(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        files: Any = None,
    ) -> APIResponse:
        """Send a signed request and return the full :class:`APIResponse` envelope.

        Does **not** raise on business errors (``code != 200``); it only raises
        :class:`VMOSHTTPError` for transport-level failures.
        """
        kwargs = self._prepare(method, path, json_body=json_body, query=query, files=files)
        attempt = 0
        while True:
            try:
                resp = self._http.request(**kwargs)
                break
            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                if attempt >= self.max_retries:
                    raise VMOSHTTPError(f"Connection to {self.base_url} failed: {exc}") from exc
                time.sleep(_RETRY_BACKOFF * (2**attempt))
                attempt += 1
            except httpx.HTTPError as exc:
                raise VMOSHTTPError(f"Request to {path} failed: {exc}") from exc
        return _parse_envelope(resp, path)

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        files: Any = None,
    ) -> Any:
        """Send a signed request and return the ``data`` field.

        Raises :class:`VMOSAPIError` (or a subclass) when ``code != 200``.
        This is the method every generated endpoint wrapper calls.
        """
        envelope = self.request_raw(method, path, json_body=json_body, query=query, files=files)
        if not envelope.ok:
            raise VMOSAPIError.from_payload(envelope.raw, path=path)
        return envelope.data

    # -- lifecycle -----------------------------------------------------------
    def close(self) -> None:
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> "VMOSClient":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()


class AsyncVMOSClient(_BaseClient):
    """Asynchronous VMOS Cloud OpenAPI client (``httpx.AsyncClient`` based).

    Accepts the same parameters as :class:`VMOSClient`.
    """

    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = 2,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        super().__init__(access_key, secret_key, base_url=base_url, timeout=timeout, max_retries=max_retries)
        self._http = http_client or httpx.AsyncClient(timeout=timeout)
        self._owns_http = http_client is None
        self._attach_namespaces()

    def _attach_namespaces(self) -> None:
        from .api import ASYNC_NAMESPACES

        for attr, cls in ASYNC_NAMESPACES.items():
            setattr(self, attr, cls(self))

    async def request_raw(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        files: Any = None,
    ) -> APIResponse:
        """Async variant of :meth:`VMOSClient.request_raw`."""
        import asyncio

        kwargs = self._prepare(method, path, json_body=json_body, query=query, files=files)
        attempt = 0
        while True:
            try:
                resp = await self._http.request(**kwargs)
                break
            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                if attempt >= self.max_retries:
                    raise VMOSHTTPError(f"Connection to {self.base_url} failed: {exc}") from exc
                await asyncio.sleep(_RETRY_BACKOFF * (2**attempt))
                attempt += 1
            except httpx.HTTPError as exc:
                raise VMOSHTTPError(f"Request to {path} failed: {exc}") from exc
        return _parse_envelope(resp, path)

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        files: Any = None,
    ) -> Any:
        """Async variant of :meth:`VMOSClient.request`."""
        envelope = await self.request_raw(method, path, json_body=json_body, query=query, files=files)
        if not envelope.ok:
            raise VMOSAPIError.from_payload(envelope.raw, path=path)
        return envelope.data

    async def aclose(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> "AsyncVMOSClient":
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.aclose()
