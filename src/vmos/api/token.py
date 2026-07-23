"""SDK temporary token issuance (STS) for client-side SDK authentication, and token clearing.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["TokenAPI", "AsyncTokenAPI"]


class TokenAPI(SyncAPIResource):
    """SDK temporary token issuance (STS) for client-side SDK authentication, and token clearing."""

    def sts_token_by_pad_code(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Get SDK Temporary Token by padCode.

        ``POST /vcpcloud/api/padApi/stsTokenByPadCode``

        Args:
            pad_code: Instance ID (padCode) (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/stsTokenByPadCode", json_body=payload)

    def clear_sts_token(
        self,
        token: str,
        **extra: Any,
    ) -> Any:
        """Clear SDK Authorization Token.

        ``POST /vcpcloud/api/padApi/clearStsToken``

        Args:
            token: The token to be cleared (API: ``token``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"token": token}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/clearStsToken", json_body=payload)


class AsyncTokenAPI(AsyncAPIResource):
    """Async variant of :class:`TokenAPI`."""

    async def sts_token_by_pad_code(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Get SDK Temporary Token by padCode.

        ``POST /vcpcloud/api/padApi/stsTokenByPadCode``

        Args:
            pad_code: Instance ID (padCode) (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/stsTokenByPadCode", json_body=payload)

    async def clear_sts_token(
        self,
        token: str,
        **extra: Any,
    ) -> Any:
        """Clear SDK Authorization Token.

        ``POST /vcpcloud/api/padApi/clearStsToken``

        Args:
            token: The token to be cleared (API: ``token``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"token": token}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/clearStsToken", json_body=payload)
