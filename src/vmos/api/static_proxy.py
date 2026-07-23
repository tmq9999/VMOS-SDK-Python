"""Static residential IP service: goods, orders, proxy creation/renewal and management.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["StaticProxyAPI", "AsyncStaticProxyAPI"]


class StaticProxyAPI(SyncAPIResource):
    """Static residential IP service: goods, orders, proxy creation/renewal and management."""

    def proxy_good_list(
        self,
        **extra: Any,
    ) -> Any:
        """Get Static Residential Product List.

        ``GET /vcpcloud/api/padApi/proxyGoodList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/proxyGoodList", query=payload)

    def get_proxy_region(
        self,
        **extra: Any,
    ) -> Any:
        """Get Supported Countries/Cities for Static Residential Products.

        ``GET /vcpcloud/api/padApi/getProxyRegion``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getProxyRegion", query=payload)

    def create_proxy_order(
        self,
        *,
        proxy_good_id: Optional[int] = None,
        region: Optional[str] = None,
        num: Optional[int] = None,
        country: Optional[str] = None,
        proxy_address: Optional[str] = None,
        auto_renew: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Purchase Static Residential Product.

        ``POST /vcpcloud/api/padApi/createProxyOrder``

        Args:
            proxy_good_id: Unique ID of the corresponding static residential product (API: ``proxyGoodId``)
            region: Region of static residential proxy-country (API: ``region``)
            num: Purchase quantity (API: ``num``)
            country: Country of static residential proxy-country (API: ``country``)
            proxy_address: Address of static residential proxy-countryZh (API: ``proxyAddress``)
            auto_renew: Enable auto-renew false-off true-on (API: ``autoRenew``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"proxyGoodId": proxy_good_id, "region": region, "num": num, "country": country, "proxyAddress": proxy_address, "autoRenew": auto_renew}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createProxyOrder", json_body=payload)

    def select_proxy_order_list(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Static Residential Proxy Order Details.

        ``POST /vcpcloud/api/padApi/selectProxyOrderList``

        Args:
            page: Page number (API: ``page``)
            rows: Items per page (API: ``rows``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/selectProxyOrderList", json_body=payload)

    def create_renew_proxy_order(
        self,
        *,
        proxy_good_id: Optional[int] = None,
        proxy_ips: Optional[str] = None,
        auto_renew: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Static Residential Proxy Renewal.

        ``POST /vcpcloud/api/padApi/createRenewProxyOrder``

        Args:
            proxy_good_id: Unique ID of the corresponding static residential product (API: ``proxyGoodId``)
            proxy_ips: IPs to renew, separated by commas (API: ``proxyIps``)
            auto_renew: Enable auto-renew false-off true-on (API: ``autoRenew``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"proxyGoodId": proxy_good_id, "proxyIps": proxy_ips, "autoRenew": auto_renew}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createRenewProxyOrder", json_body=payload)

    def query_proxy_list(
        self,
        *,
        current: Optional[int] = None,
        size: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query Static Residential Proxy List.

        ``POST /vcpcloud/api/padApi/queryProxyList``

        Args:
            current: Page number (API: ``current``)
            size: Items per page (API: ``size``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"current": current, "size": size}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/queryProxyList", json_body=payload)

    def del_proxy_by_host(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        account: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Delete Static Residential Proxy.

        Delete a static residential proxy under your own account by proxy address, port and username. Cloud phones currently using the proxy are automatically unbound from it. If several proxies share the same address, port and username, all of them are deleted. When no proxy matches, the request still succeeds and `data` is 0.

        ``POST /vcpcloud/api/padApi/delProxyByHost``

        Args:
            host: Proxy address (API: ``host``)
            port: Proxy port (API: ``port``)
            account: Proxy username (API: ``account``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"host": host, "port": port, "account": account}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/delProxyByHost", json_body=payload)


class AsyncStaticProxyAPI(AsyncAPIResource):
    """Async variant of :class:`StaticProxyAPI`."""

    async def proxy_good_list(
        self,
        **extra: Any,
    ) -> Any:
        """Get Static Residential Product List.

        ``GET /vcpcloud/api/padApi/proxyGoodList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/proxyGoodList", query=payload)

    async def get_proxy_region(
        self,
        **extra: Any,
    ) -> Any:
        """Get Supported Countries/Cities for Static Residential Products.

        ``GET /vcpcloud/api/padApi/getProxyRegion``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getProxyRegion", query=payload)

    async def create_proxy_order(
        self,
        *,
        proxy_good_id: Optional[int] = None,
        region: Optional[str] = None,
        num: Optional[int] = None,
        country: Optional[str] = None,
        proxy_address: Optional[str] = None,
        auto_renew: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Purchase Static Residential Product.

        ``POST /vcpcloud/api/padApi/createProxyOrder``

        Args:
            proxy_good_id: Unique ID of the corresponding static residential product (API: ``proxyGoodId``)
            region: Region of static residential proxy-country (API: ``region``)
            num: Purchase quantity (API: ``num``)
            country: Country of static residential proxy-country (API: ``country``)
            proxy_address: Address of static residential proxy-countryZh (API: ``proxyAddress``)
            auto_renew: Enable auto-renew false-off true-on (API: ``autoRenew``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"proxyGoodId": proxy_good_id, "region": region, "num": num, "country": country, "proxyAddress": proxy_address, "autoRenew": auto_renew}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createProxyOrder", json_body=payload)

    async def select_proxy_order_list(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Static Residential Proxy Order Details.

        ``POST /vcpcloud/api/padApi/selectProxyOrderList``

        Args:
            page: Page number (API: ``page``)
            rows: Items per page (API: ``rows``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/selectProxyOrderList", json_body=payload)

    async def create_renew_proxy_order(
        self,
        *,
        proxy_good_id: Optional[int] = None,
        proxy_ips: Optional[str] = None,
        auto_renew: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Static Residential Proxy Renewal.

        ``POST /vcpcloud/api/padApi/createRenewProxyOrder``

        Args:
            proxy_good_id: Unique ID of the corresponding static residential product (API: ``proxyGoodId``)
            proxy_ips: IPs to renew, separated by commas (API: ``proxyIps``)
            auto_renew: Enable auto-renew false-off true-on (API: ``autoRenew``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"proxyGoodId": proxy_good_id, "proxyIps": proxy_ips, "autoRenew": auto_renew}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createRenewProxyOrder", json_body=payload)

    async def query_proxy_list(
        self,
        *,
        current: Optional[int] = None,
        size: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query Static Residential Proxy List.

        ``POST /vcpcloud/api/padApi/queryProxyList``

        Args:
            current: Page number (API: ``current``)
            size: Items per page (API: ``size``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"current": current, "size": size}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/queryProxyList", json_body=payload)

    async def del_proxy_by_host(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        account: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Delete Static Residential Proxy.

        Delete a static residential proxy under your own account by proxy address, port and username. Cloud phones currently using the proxy are automatically unbound from it. If several proxies share the same address, port and username, all of them are deleted. When no proxy matches, the request still succeeds and `data` is 0.

        ``POST /vcpcloud/api/padApi/delProxyByHost``

        Args:
            host: Proxy address (API: ``host``)
            port: Proxy port (API: ``port``)
            account: Proxy username (API: ``account``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"host": host, "port": port, "account": account}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/delProxyByHost", json_body=payload)
