"""Email verification service: email types/stock, purchase orders and verification-code retrieval.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["EmailAPI", "AsyncEmailAPI"]


class EmailAPI(SyncAPIResource):
    """Email verification service: email types/stock, purchase orders and verification-code retrieval."""

    def get_email_service_list(
        self,
        **extra: Any,
    ) -> Any:
        """Get Email Service List.

        ``GET /vcpcloud/api/padApi/getEmailServiceList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getEmailServiceList", query=payload)

    def get_email_type_list(
        self,
        *,
        service_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get Email Type and Remaining Stock.

        ``GET /vcpcloud/api/padApi/getEmailTypeList``

        Args:
            service_id: Corresponds to serviceItemId field (API: ``serviceId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"serviceId": service_id}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getEmailTypeList", query=payload)

    def create_email_order(
        self,
        *,
        service_id: Optional[int] = None,
        email_type_id: Optional[int] = None,
        good_num: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Create Email Purchase Order.

        ``POST /vcpcloud/api/padApi/createEmailOrder``

        Args:
            service_id: Corresponds to serviceItemId field (API: ``serviceId``)
            email_type_id: Corresponds to ID field returned by /getEmailTypeList (API: ``emailTypeId``)
            good_num: Purchase quantity (API: ``goodNum``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"serviceId": service_id, "emailTypeId": email_type_id, "goodNum": good_num}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createEmailOrder", json_body=payload)

    def get_email_order(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        service_id: Optional[int] = None,
        email: Optional[str] = None,
        status: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query Purchased Email List.

        When the verification code cannot be obtained through the refresh interface, you can query the result through: [https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=](https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=) + outOrderId (external order number)

        ``GET /vcpcloud/api/padApi/getEmailOrder``

        Args:
            page: Required, pagination parameter, current page (API: ``page``)
            size: Required, pagination parameter, items per page (API: ``size``)
            service_id: Optional, corresponds to serviceItemId field (API: ``serviceId``)
            email: Optional, email fuzzy query (API: ``email``)
            status: Optional, email status 0-unused 1-receiving 2-used 3-expired (API: ``status``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "serviceId": service_id, "email": email, "status": status}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getEmailOrder", query=payload)

    def get_email_code(
        self,
        *,
        order_id: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Refresh to Get Email Verification Code.

        This interface refreshes the verification code list result, need to be used together with the [Query Purchased Email List] interface

        ``GET /vcpcloud/api/padApi/getEmailCode``

        Args:
            order_id: Required, corresponds to outOrderId field (API: ``orderId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"orderId": order_id}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getEmailCode", query=payload)


class AsyncEmailAPI(AsyncAPIResource):
    """Async variant of :class:`EmailAPI`."""

    async def get_email_service_list(
        self,
        **extra: Any,
    ) -> Any:
        """Get Email Service List.

        ``GET /vcpcloud/api/padApi/getEmailServiceList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getEmailServiceList", query=payload)

    async def get_email_type_list(
        self,
        *,
        service_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get Email Type and Remaining Stock.

        ``GET /vcpcloud/api/padApi/getEmailTypeList``

        Args:
            service_id: Corresponds to serviceItemId field (API: ``serviceId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"serviceId": service_id}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getEmailTypeList", query=payload)

    async def create_email_order(
        self,
        *,
        service_id: Optional[int] = None,
        email_type_id: Optional[int] = None,
        good_num: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Create Email Purchase Order.

        ``POST /vcpcloud/api/padApi/createEmailOrder``

        Args:
            service_id: Corresponds to serviceItemId field (API: ``serviceId``)
            email_type_id: Corresponds to ID field returned by /getEmailTypeList (API: ``emailTypeId``)
            good_num: Purchase quantity (API: ``goodNum``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"serviceId": service_id, "emailTypeId": email_type_id, "goodNum": good_num}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createEmailOrder", json_body=payload)

    async def get_email_order(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        service_id: Optional[int] = None,
        email: Optional[str] = None,
        status: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query Purchased Email List.

        When the verification code cannot be obtained through the refresh interface, you can query the result through: [https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=](https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=) + outOrderId (external order number)

        ``GET /vcpcloud/api/padApi/getEmailOrder``

        Args:
            page: Required, pagination parameter, current page (API: ``page``)
            size: Required, pagination parameter, items per page (API: ``size``)
            service_id: Optional, corresponds to serviceItemId field (API: ``serviceId``)
            email: Optional, email fuzzy query (API: ``email``)
            status: Optional, email status 0-unused 1-receiving 2-used 3-expired (API: ``status``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "serviceId": service_id, "email": email, "status": status}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getEmailOrder", query=payload)

    async def get_email_code(
        self,
        *,
        order_id: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Refresh to Get Email Verification Code.

        This interface refreshes the verification code list result, need to be used together with the [Query Purchased Email List] interface

        ``GET /vcpcloud/api/padApi/getEmailCode``

        Args:
            order_id: Required, corresponds to outOrderId field (API: ``orderId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"orderId": order_id}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getEmailCode", query=payload)
