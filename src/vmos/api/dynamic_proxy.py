"""Dynamic proxy service: regions, goods, orders, traffic balance and per-pad proxy configuration.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["DynamicProxyAPI", "AsyncDynamicProxyAPI"]


class DynamicProxyAPI(SyncAPIResource):
    """Dynamic proxy service: regions, goods, orders, traffic balance and per-pad proxy configuration."""

    def get_dynamic_good_service(
        self,
        **extra: Any,
    ) -> Any:
        """Query Dynamic Proxy Product List.

        ``GET /vcpcloud/api/padApi/getDynamicGoodService``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getDynamicGoodService", query=payload)

    def get_dynamic_proxy_region(
        self,
        **extra: Any,
    ) -> Any:
        """Query Dynamic Proxy Region List.

        ``GET /vcpcloud/api/padApi/getDynamicProxyRegion``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getDynamicProxyRegion", query=payload)

    def query_current_traffic_balance(
        self,
        **extra: Any,
    ) -> Any:
        """Get Dynamic Proxy Current Balance.

        ``GET /vcpcloud/api/padApi/queryCurrentTrafficBalance``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/queryCurrentTrafficBalance", query=payload)

    def get_dynamic_proxy_host(
        self,
        **extra: Any,
    ) -> Any:
        """Query Supported Server Regions.

        ``GET /vcpcloud/api/padApi/getDynamicProxyHost``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getDynamicProxyHost", query=payload)

    def buy_dynamic_proxy(
        self,
        *,
        good_id: Optional[int] = None,
        good_num: Optional[int] = None,
        auto_renew_order: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Purchase Dynamic Proxy Traffic Package.

        ``POST /vcpcloud/api/padApi/buyDynamicProxy``

        Args:
            good_id: Unique ID of the corresponding dynamic traffic package (API: ``goodId``)
            good_num: Purchase quantity (API: ``goodNum``)
            auto_renew_order: Enable auto-renew 0-off 1-on. When remaining traffic is less than 50MB, auto-renew is triggered (API: ``autoRenewOrder``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"goodId": good_id, "goodNum": good_num, "autoRenewOrder": auto_renew_order}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/buyDynamicProxy", json_body=payload)

    def create_proxy(
        self,
        *,
        city: Optional[str] = None,
        country_code: Optional[str] = None,
        good_num: Optional[int] = None,
        proxy_host: Optional[str] = None,
        proxy_type: Optional[str] = None,
        proxy_use_type: Optional[str] = None,
        state: Optional[str] = None,
        time: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Create Dynamic Proxy.

        ``POST /vcpcloud/api/padApi/createProxy``

        Args:
            city: City, pass "" if not selected (API: ``city``)
            country_code: Country Code (API: ``countryCode``)
            good_num: Purchase quantity (API: ``goodNum``)
            proxy_host: Continent website (API: ``proxyHost``)
            proxy_type: Proxy type socks5 / http / https (API: ``proxyType``)
            proxy_use_type: Mount type proxy / vpm (API: ``proxyUseType``)
            state: Region, pass "" if not selected (API: ``state``)
            time: Auto change ip frequency (minutes) Options: 5, 10, 15, 30, 45, 60, 90 (API: ``time``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"city": city, "countryCode": country_code, "goodNum": good_num, "proxyHost": proxy_host, "proxyType": proxy_type, "proxyUseType": proxy_use_type, "state": state, "time": time}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createProxy", json_body=payload)

    def get_proxys(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get Proxys.

        ``GET /vcpcloud/api/padApi/getProxys``

        Args:
            page: Current page (API: ``page``)
            rows: Items per page (API: ``rows``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getProxys", query=payload)

    def get_dynamic_proxy_orders(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        complete_start_time: Optional[str] = None,
        complete_end_time: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Get Dynamic Proxy Orders.

        ``POST /vcpcloud/api/padApi/getDynamicProxyOrders``

        Args:
            page: Current page (API: ``page``)
            rows: Items per page (API: ``rows``)
            complete_start_time: Payment start time (API: ``completeStartTime``)
            complete_end_time: Payment end time (API: ``completeEndTime``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows, "completeStartTime": complete_start_time, "completeEndTime": complete_end_time}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/getDynamicProxyOrders", json_body=payload)

    def batch_pad_config_proxy(
        self,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        set_proxy_flag: Optional[bool] = None,
        proxy_ids: Optional[Sequence[Any]] = None,
        **extra: Any,
    ) -> Any:
        """Configure Dynamic Proxy for Cloud Phone.

        ``POST /vcpcloud/api/padApi/batchPadConfigProxy``

        Args:
            pad_codes: Cloud phone collection (API: ``padCodes``)
            set_proxy_flag: Whether device proxies to cloud phone (API: ``setProxyFlag``)
            proxy_ids: Dynamic Proxy unique ID (API: ``proxyIds``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "setProxyFlag": set_proxy_flag, "proxyIds": proxy_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/batchPadConfigProxy", json_body=payload)

    def select_batch_pad_proxy_task(
        self,
        *,
        task_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query Batch Cloud Phone Proxy Setting Task.

        ``POST /vcpcloud/api/padApi/selectBatchPadProxyTask``

        Args:
            task_id: Batch ID, mounting proxy is an asynchronous operation, so need to wait 5s or loop query (API: ``taskId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/selectBatchPadProxyTask", json_body=payload)

    def get_dynamic_proxy_automatic_renewal(
        self,
        **extra: Any,
    ) -> Any:
        """Query Dynamic Proxy Auto-Renew Information.

        ``GET /vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal", query=payload)

    def set_auto_renew_switch(
        self,
        *,
        auto_renew_order: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Set Dynamic Proxy Auto-Renew Switch.

        ``POST /vcpcloud/api/padApi/setAutoRenewSwitch``

        Args:
            auto_renew_order: Auto-renew switch 0-off 1-on (API: ``autoRenewOrder``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"autoRenewOrder": auto_renew_order}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/setAutoRenewSwitch", json_body=payload)

    def del_proxy_by_ids(
        self,
        *,
        ids: Optional[Sequence[Any]] = None,
        **extra: Any,
    ) -> Any:
        """Delete Dynamic Proxy.

        ``POST /vcpcloud/api/padApi/delProxyByIds``

        Args:
            ids: Collection of dynamic proxy IDs to delete (API: ``ids``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"ids": ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/delProxyByIds", json_body=payload)


class AsyncDynamicProxyAPI(AsyncAPIResource):
    """Async variant of :class:`DynamicProxyAPI`."""

    async def get_dynamic_good_service(
        self,
        **extra: Any,
    ) -> Any:
        """Query Dynamic Proxy Product List.

        ``GET /vcpcloud/api/padApi/getDynamicGoodService``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getDynamicGoodService", query=payload)

    async def get_dynamic_proxy_region(
        self,
        **extra: Any,
    ) -> Any:
        """Query Dynamic Proxy Region List.

        ``GET /vcpcloud/api/padApi/getDynamicProxyRegion``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getDynamicProxyRegion", query=payload)

    async def query_current_traffic_balance(
        self,
        **extra: Any,
    ) -> Any:
        """Get Dynamic Proxy Current Balance.

        ``GET /vcpcloud/api/padApi/queryCurrentTrafficBalance``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/queryCurrentTrafficBalance", query=payload)

    async def get_dynamic_proxy_host(
        self,
        **extra: Any,
    ) -> Any:
        """Query Supported Server Regions.

        ``GET /vcpcloud/api/padApi/getDynamicProxyHost``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getDynamicProxyHost", query=payload)

    async def buy_dynamic_proxy(
        self,
        *,
        good_id: Optional[int] = None,
        good_num: Optional[int] = None,
        auto_renew_order: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Purchase Dynamic Proxy Traffic Package.

        ``POST /vcpcloud/api/padApi/buyDynamicProxy``

        Args:
            good_id: Unique ID of the corresponding dynamic traffic package (API: ``goodId``)
            good_num: Purchase quantity (API: ``goodNum``)
            auto_renew_order: Enable auto-renew 0-off 1-on. When remaining traffic is less than 50MB, auto-renew is triggered (API: ``autoRenewOrder``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"goodId": good_id, "goodNum": good_num, "autoRenewOrder": auto_renew_order}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/buyDynamicProxy", json_body=payload)

    async def create_proxy(
        self,
        *,
        city: Optional[str] = None,
        country_code: Optional[str] = None,
        good_num: Optional[int] = None,
        proxy_host: Optional[str] = None,
        proxy_type: Optional[str] = None,
        proxy_use_type: Optional[str] = None,
        state: Optional[str] = None,
        time: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Create Dynamic Proxy.

        ``POST /vcpcloud/api/padApi/createProxy``

        Args:
            city: City, pass "" if not selected (API: ``city``)
            country_code: Country Code (API: ``countryCode``)
            good_num: Purchase quantity (API: ``goodNum``)
            proxy_host: Continent website (API: ``proxyHost``)
            proxy_type: Proxy type socks5 / http / https (API: ``proxyType``)
            proxy_use_type: Mount type proxy / vpm (API: ``proxyUseType``)
            state: Region, pass "" if not selected (API: ``state``)
            time: Auto change ip frequency (minutes) Options: 5, 10, 15, 30, 45, 60, 90 (API: ``time``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"city": city, "countryCode": country_code, "goodNum": good_num, "proxyHost": proxy_host, "proxyType": proxy_type, "proxyUseType": proxy_use_type, "state": state, "time": time}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createProxy", json_body=payload)

    async def get_proxys(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get Proxys.

        ``GET /vcpcloud/api/padApi/getProxys``

        Args:
            page: Current page (API: ``page``)
            rows: Items per page (API: ``rows``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getProxys", query=payload)

    async def get_dynamic_proxy_orders(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        complete_start_time: Optional[str] = None,
        complete_end_time: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Get Dynamic Proxy Orders.

        ``POST /vcpcloud/api/padApi/getDynamicProxyOrders``

        Args:
            page: Current page (API: ``page``)
            rows: Items per page (API: ``rows``)
            complete_start_time: Payment start time (API: ``completeStartTime``)
            complete_end_time: Payment end time (API: ``completeEndTime``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows, "completeStartTime": complete_start_time, "completeEndTime": complete_end_time}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/getDynamicProxyOrders", json_body=payload)

    async def batch_pad_config_proxy(
        self,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        set_proxy_flag: Optional[bool] = None,
        proxy_ids: Optional[Sequence[Any]] = None,
        **extra: Any,
    ) -> Any:
        """Configure Dynamic Proxy for Cloud Phone.

        ``POST /vcpcloud/api/padApi/batchPadConfigProxy``

        Args:
            pad_codes: Cloud phone collection (API: ``padCodes``)
            set_proxy_flag: Whether device proxies to cloud phone (API: ``setProxyFlag``)
            proxy_ids: Dynamic Proxy unique ID (API: ``proxyIds``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "setProxyFlag": set_proxy_flag, "proxyIds": proxy_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/batchPadConfigProxy", json_body=payload)

    async def select_batch_pad_proxy_task(
        self,
        *,
        task_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query Batch Cloud Phone Proxy Setting Task.

        ``POST /vcpcloud/api/padApi/selectBatchPadProxyTask``

        Args:
            task_id: Batch ID, mounting proxy is an asynchronous operation, so need to wait 5s or loop query (API: ``taskId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/selectBatchPadProxyTask", json_body=payload)

    async def get_dynamic_proxy_automatic_renewal(
        self,
        **extra: Any,
    ) -> Any:
        """Query Dynamic Proxy Auto-Renew Information.

        ``GET /vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal", query=payload)

    async def set_auto_renew_switch(
        self,
        *,
        auto_renew_order: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Set Dynamic Proxy Auto-Renew Switch.

        ``POST /vcpcloud/api/padApi/setAutoRenewSwitch``

        Args:
            auto_renew_order: Auto-renew switch 0-off 1-on (API: ``autoRenewOrder``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"autoRenewOrder": auto_renew_order}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/setAutoRenewSwitch", json_body=payload)

    async def del_proxy_by_ids(
        self,
        *,
        ids: Optional[Sequence[Any]] = None,
        **extra: Any,
    ) -> Any:
        """Delete Dynamic Proxy.

        ``POST /vcpcloud/api/padApi/delProxyByIds``

        Args:
            ids: Collection of dynamic proxy IDs to delete (API: ``ids``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"ids": ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/delProxyByIds", json_body=payload)
