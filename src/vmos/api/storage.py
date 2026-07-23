"""Cloud Space: storage goods, backups, file management (upload/query/delete) and renewal of cloud storage.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["StorageAPI", "AsyncStorageAPI"]


class StorageAPI(SyncAPIResource):
    """Cloud Space: storage goods, backups, file management (upload/query/delete) and renewal of cloud storage."""

    def select_files(
        self,
        **extra: Any,
    ) -> Any:
        """Query User File List.

        ``POST /vcpcloud/api/padApi/selectFiles``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/selectFiles", json_body=payload)

    def delete_oss_files(
        self,
        files: Sequence[Any],
        *,
        urls: Optional[Sequence[str]] = None,
        **extra: Any,
    ) -> Any:
        """Delete Cloud Space Files.

        ``POST /vcpcloud/api/padApi/deleteOssFiles``

        Args:
            files: Collection of unique cloud space file IDs (API: ``files``, required)
            urls: Collection of cloud space file download links (API: ``urls``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"files": files, "urls": urls}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/deleteOssFiles", json_body=payload)

    def upload_file(
        self,
        file: Any,
        **extra: Any,
    ) -> Any:
        """Upload File to Cloud Space.

        Upload file to cloud space and get download link

        ``POST /vcpcloud/api/padApi/uploadFile``

        Args:
            file: File to upload (API: ``file``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/uploadFile", json_body=payload, files={"file": file})

    def buy_storage_goods(
        self,
        storage_id: int,
        auto_renew_order: int,
        **extra: Any,
    ) -> Any:
        """Purchase Cloud Space Expansion.

        Purchase cloud space expansion

        ``POST /vcpcloud/api/padApi/buyStorageGoods``

        Args:
            storage_id: Unique ID of cloud space expansion product (API: ``storageId``, required)
            auto_renew_order: Auto-renew? 0-No 1-Yes (API: ``autoRenewOrder``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"storageId": storage_id, "autoRenewOrder": auto_renew_order}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/buyStorageGoods", json_body=payload)

    def vc_timing_backup_list(
        self,
        **extra: Any,
    ) -> Any:
        """Storage Resource Package List.

        List of storage resource packages after shutdown backup

        ``GET /vcpcloud/api/padApi/vcTimingBackupList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/vcTimingBackupList", query=payload)

    def get_vc_storage_goods(
        self,
        **extra: Any,
    ) -> Any:
        """Cloud Space Product List.

        Cloud space product list

        ``GET /vcpcloud/api/padApi/getVcStorageGoods``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getVcStorageGoods", query=payload)

    def renews_storage_goods(
        self,
        auto_renew_order: int,
        **extra: Any,
    ) -> Any:
        """Aggregate Renewal of Cloud Space Products.

        Aggregate renewal of cloud space products

        ``POST /vcpcloud/api/padApi/renewsStorageGoods``

        Args:
            auto_renew_order: Auto-renew? 0-No 1-Yes (API: ``autoRenewOrder``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"autoRenewOrder": auto_renew_order}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/renewsStorageGoods", json_body=payload)

    def delete_upload_files(
        self,
        **extra: Any,
    ) -> Any:
        """Delete Backup Resource Package Data.

        Delete backup resource package data

        ``POST /vcpcloud/api/padApi/deleteUploadFiles``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/deleteUploadFiles", json_body=payload)

    def update_renew_storage_status(
        self,
        renew_storage_status: str,
        **extra: Any,
    ) -> Any:
        """Cloud Space Auto-renew Aggregate Product Switch.

        Cloud space auto-renew aggregate product switch

        ``GET /vcpcloud/api/padApi/updateRenewStorageStatus``

        Args:
            renew_storage_status: Auto-renew? false-No true-Yes (API: ``renewStorageStatus``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"renewStorageStatus": renew_storage_status}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/updateRenewStorageStatus", query=payload)

    def select_auto_renew(
        self,
        **extra: Any,
    ) -> Any:
        """Query Cloud Space Renewal Details.

        Query cloud space renewal details

        ``GET /vcpcloud/api/padApi/selectAutoRenew``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/selectAutoRenew", query=payload)

    def get_renew_storage_info(
        self,
        **extra: Any,
    ) -> Any:
        """Cloud Space Remaining Storage Capacity.

        Cloud space remaining storage capacity

        ``GET /vcpcloud/api/padApi/getRenewStorageInfo``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getRenewStorageInfo", query=payload)


class AsyncStorageAPI(AsyncAPIResource):
    """Async variant of :class:`StorageAPI`."""

    async def select_files(
        self,
        **extra: Any,
    ) -> Any:
        """Query User File List.

        ``POST /vcpcloud/api/padApi/selectFiles``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/selectFiles", json_body=payload)

    async def delete_oss_files(
        self,
        files: Sequence[Any],
        *,
        urls: Optional[Sequence[str]] = None,
        **extra: Any,
    ) -> Any:
        """Delete Cloud Space Files.

        ``POST /vcpcloud/api/padApi/deleteOssFiles``

        Args:
            files: Collection of unique cloud space file IDs (API: ``files``, required)
            urls: Collection of cloud space file download links (API: ``urls``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"files": files, "urls": urls}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/deleteOssFiles", json_body=payload)

    async def upload_file(
        self,
        file: Any,
        **extra: Any,
    ) -> Any:
        """Upload File to Cloud Space.

        Upload file to cloud space and get download link

        ``POST /vcpcloud/api/padApi/uploadFile``

        Args:
            file: File to upload (API: ``file``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/uploadFile", json_body=payload, files={"file": file})

    async def buy_storage_goods(
        self,
        storage_id: int,
        auto_renew_order: int,
        **extra: Any,
    ) -> Any:
        """Purchase Cloud Space Expansion.

        Purchase cloud space expansion

        ``POST /vcpcloud/api/padApi/buyStorageGoods``

        Args:
            storage_id: Unique ID of cloud space expansion product (API: ``storageId``, required)
            auto_renew_order: Auto-renew? 0-No 1-Yes (API: ``autoRenewOrder``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"storageId": storage_id, "autoRenewOrder": auto_renew_order}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/buyStorageGoods", json_body=payload)

    async def vc_timing_backup_list(
        self,
        **extra: Any,
    ) -> Any:
        """Storage Resource Package List.

        List of storage resource packages after shutdown backup

        ``GET /vcpcloud/api/padApi/vcTimingBackupList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/vcTimingBackupList", query=payload)

    async def get_vc_storage_goods(
        self,
        **extra: Any,
    ) -> Any:
        """Cloud Space Product List.

        Cloud space product list

        ``GET /vcpcloud/api/padApi/getVcStorageGoods``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getVcStorageGoods", query=payload)

    async def renews_storage_goods(
        self,
        auto_renew_order: int,
        **extra: Any,
    ) -> Any:
        """Aggregate Renewal of Cloud Space Products.

        Aggregate renewal of cloud space products

        ``POST /vcpcloud/api/padApi/renewsStorageGoods``

        Args:
            auto_renew_order: Auto-renew? 0-No 1-Yes (API: ``autoRenewOrder``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"autoRenewOrder": auto_renew_order}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/renewsStorageGoods", json_body=payload)

    async def delete_upload_files(
        self,
        **extra: Any,
    ) -> Any:
        """Delete Backup Resource Package Data.

        Delete backup resource package data

        ``POST /vcpcloud/api/padApi/deleteUploadFiles``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/deleteUploadFiles", json_body=payload)

    async def update_renew_storage_status(
        self,
        renew_storage_status: str,
        **extra: Any,
    ) -> Any:
        """Cloud Space Auto-renew Aggregate Product Switch.

        Cloud space auto-renew aggregate product switch

        ``GET /vcpcloud/api/padApi/updateRenewStorageStatus``

        Args:
            renew_storage_status: Auto-renew? false-No true-Yes (API: ``renewStorageStatus``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"renewStorageStatus": renew_storage_status}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/updateRenewStorageStatus", query=payload)

    async def select_auto_renew(
        self,
        **extra: Any,
    ) -> Any:
        """Query Cloud Space Renewal Details.

        Query cloud space renewal details

        ``GET /vcpcloud/api/padApi/selectAutoRenew``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/selectAutoRenew", query=payload)

    async def get_renew_storage_info(
        self,
        **extra: Any,
    ) -> Any:
        """Cloud Space Remaining Storage Capacity.

        Cloud space remaining storage capacity

        ``GET /vcpcloud/api/padApi/getRenewStorageInfo``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getRenewStorageInfo", query=payload)
