"""Cloud phone commerce & lifecycle: goods, orders, renewal, activation codes, authorization/transfer, backups, device sharing and replacement.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["PhoneAPI", "AsyncPhoneAPI"]


class PhoneAPI(SyncAPIResource):
    """Cloud phone commerce & lifecycle: goods, orders, renewal, activation codes, authorization/transfer, backups, device sharing and replacement."""

    def create_timing_share(
        self,
        *,
        equipment_id: Optional[int] = None,
        pad_code: Optional[str] = None,
        permission: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Cloud Phone Management.

        Create a share token for one powered-on timing device. Sharing ends after the device is powered off.

        ``POST /vcpcloud/api/padApi/createTimingShare``

        Args:
            equipment_id: Device ID (API: ``equipmentId``)
            pad_code: Timing device ID (API: ``padCode``)
            permission: Share permission (API: ``permission``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"equipmentId": equipment_id, "padCode": pad_code, "permission": permission}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createTimingShare", json_body=payload)

    def open_auto_renew(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Enable Cloud Phone Auto-Renewal.

        Enable auto-renewal for a single cloud phone; it will be renewed automatically with the current package before expiration.

        ``POST /vcpcloud/api/padApi/openAutoRenew``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/openAutoRenew", json_body=payload)

    def close_auto_renew(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Disable Cloud Phone Auto-Renewal.

        Disable auto-renewal for a single cloud phone; once disabled, it will no longer be renewed automatically upon expiration.

        ``POST /vcpcloud/api/padApi/closeAutoRenew``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/closeAutoRenew", json_body=payload)

    def close_all_auto_renew(
        self,
        **extra: Any,
    ) -> Any:
        """Batch Disable Cloud Phone Auto-Renewal.

        Disable auto-renewal for all cloud phones under the current account in a single call; once disabled, they will no longer be renewed automatically upon expiration.

        ``POST /vcpcloud/api/padApi/closeAllAutoRenew``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/closeAllAutoRenew", json_body=payload)

    def update_pad_name(
        self,
        pad_code: str,
        pad_name: str,
        **extra: Any,
    ) -> Any:
        """Rename Cloud Phone.

        Rename a single cloud phone.

        ``POST /vcpcloud/api/padApi/updatePadName``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            pad_name: New cloud phone name (API: ``padName``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "padName": pad_name}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/updatePadName", json_body=payload)

    def authorize_pad(
        self,
        pad_code: str,
        authorized_account: str,
        *,
        minutes: Optional[int] = None,
        equi_authorize: Optional[bool] = None,
        permission: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Authorize Pad.

        Temporarily grant a single cloud phone to another account. During the authorization the granted account can access the cloud phone; device ownership does not change.

        ``POST /vcpcloud/api/padApi/authorizePad``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            authorized_account: Granted account (registered phone number or email) (API: ``authorizedAccount``, required)
            minutes: Authorization duration in minutes; required when equiAuthorize=false (API: ``minutes``)
            equi_authorize: Authorize for the device's remaining validity; default false (API: ``equiAuthorize``)
            permission: Allowed-operation list, comma-separated; empty means all (API: ``permission``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "authorizedAccount": authorized_account, "minutes": minutes, "equiAuthorize": equi_authorize, "permission": permission}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/authorizePad", json_body=payload)

    def replace_real_adi_template(
        self,
        pad_codes: Sequence[str],
        wipe_data: bool,
        real_phone_template_id: int,
        **extra: Any,
    ) -> Any:
        """Modify Real Device ADI Template.

        Modify cloud real device ADI template with provided template ID. Conditions: 1. Instance created as cloud real device type 2. Instance Android version matches target ADI version

        ``POST /vcpcloud/api/padApi/replaceRealAdiTemplate``

        Args:
            pad_codes: (API: ``padCodes``, required)
            wipe_data: Clear data (API: ``wipeData``, required)
            real_phone_template_id: Real device template ID (API: ``realPhoneTemplateId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "wipeData": wipe_data, "realPhoneTemplateId": real_phone_template_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/replaceRealAdiTemplate", json_body=payload)

    def create_money_order(
        self,
        android_version_name: str,
        good_id: int,
        good_num: int,
        auto_renew: bool,
        equipment_id: str,
        *,
        country_code: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Create Cloud Phone.

        Create a new cloud phone. (Note that the purchased product package must be available on the web platform, otherwise the purchase will fail.)

        ``POST /vcpcloud/api/padApi/createMoneyOrder``

        Args:
            android_version_name: Android version: Android10、Android13, Android14 (API: ``androidVersionName``, required)
            good_id: Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) (API: ``goodId``, required)
            good_num: Product quantity (API: ``goodNum``, required)
            auto_renew: Whether to auto-renew (enabled by default) (API: ``autoRenew``, required)
            equipment_id: Renewal device IDs (comma separated for multiple devices) (API: ``equipmentId``, required)
            country_code: Country code, used to specify the region of the cloud phone (API: ``countryCode``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"androidVersionName": android_version_name, "goodId": good_id, "goodNum": good_num, "autoRenew": auto_renew, "equipmentId": equipment_id, "countryCode": country_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createMoneyOrder", json_body=payload)

    def activate_by_code(
        self,
        active_code_list: Sequence[str],
        *,
        country_code: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Activate Cloud Phone with Activation Code.

        Batch-activate cloud phones using activation codes. Submit a list of activation codes and immediately get a batch number (batchId); cloud phones are created asynchronously in the background and belong to the caller's account once activated. Activation codes that cannot be used are returned in failCodes. (The product package corresponding to the activation code must exist and be valid on the web platform, otherwise activation will fail.)

        ``POST /vcpcloud/api/padApi/activateByCode``

        Args:
            active_code_list: List of activation codes, multiple allowed (API: ``activeCodeList``, required)
            country_code: Country/region code. Defaults to HK if not provided (API: ``countryCode``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"activeCodeList": active_code_list, "countryCode": country_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/activateByCode", json_body=payload)

    def query_activation_batch(
        self,
        batch_id: str,
        **extra: Any,
    ) -> Any:
        """Query Batch Activation Progress.

        Query the progress of a batch activation task submitted via activateByCode. Returns the overall status, the number of activation codes succeeded/failed/in progress, the number of activated devices, and per-code details.

        ``POST /vcpcloud/api/padApi/queryActivationBatch``

        Args:
            batch_id: Batch number returned by activateByCode (API: ``batchId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"batchId": batch_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/queryActivationBatch", json_body=payload)

    def user_pad_list(
        self,
        *,
        pad_code: Optional[str] = None,
        equipment_ids: Optional[Sequence[Any]] = None,
        **extra: Any,
    ) -> Any:
        """Cloud Phone List.

        Cloud phone list.

        ``POST /vcpcloud/api/padApi/userPadList``

        Args:
            pad_code: Instance code (API: ``padCode``)
            equipment_ids: Array of equipment IDs (API: ``equipmentIds``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "equipmentIds": equipment_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/userPadList", json_body=payload)

    def pad_info(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Cloud Phone Information Query.

        Query cloud phone information.

        ``POST /vcpcloud/api/padApi/padInfo``

        Args:
            pad_code: Instance ID (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body=payload)

    def get_cloud_good_list(
        self,
        **extra: Any,
    ) -> Any:
        """SKU Package List.

        Get the SKU package list.

        ``GET /vcpcloud/api/padApi/getCloudGoodList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/getCloudGoodList", query=payload)

    def image_version_list(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Android image version collection.

        Get the image set that can be upgraded on the current device

        ``POST /vcpcloud/api/padApi/imageVersionList``

        Args:
            pad_code: PadCode (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/imageVersionList", json_body=payload)

    def create_money_pro_order(
        self,
        *,
        android_version_name: Optional[str] = None,
        good_id: Optional[int] = None,
        good_num: Optional[int] = None,
        auto_renew: Optional[bool] = None,
        country_code: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Equipment Pre-sale Purchase.

        When stock is insufficient, you can use this API to pre-order a device (only applicable to cloud phone products with a rental period of 30 days or more). Once stock is replenished, the system will prioritize fulfilling pre-sale orders and automatically dispatch the devices. After the order is shipped, users will receive an email notification and an additional one-day usage bonus.

        ``POST /vcpcloud/api/padApi/createMoneyProOrder``

        Args:
            android_version_name: Android Version：Android10、Android13、Android14 (API: ``androidVersionName``)
            good_id: Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) (API: ``goodId``)
            good_num: Product Number (API: ``goodNum``)
            auto_renew: Whether to automatically renew (default closed) true-on, false-off (API: ``autoRenew``)
            country_code: Country code, used to specify the region of the cloud phone (API: ``countryCode``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"androidVersionName": android_version_name, "goodId": good_id, "goodNum": good_num, "autoRenew": auto_renew, "countryCode": country_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/createMoneyProOrder", json_body=payload)

    def query_pro_order_list(
        self,
        *,
        pro_buy_status: Optional[int] = None,
        order_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query pre-sale order result details.

        Query the details of pre-sale order results. You can query by pre-sale order number, order status (1-to be shipped 2-shipped, empty default all)

        ``POST /vcpcloud/api/padApi/queryProOrderList``

        Args:
            pro_buy_status: 1-To be shipped 2-Shipment If empty, default to all (API: ``proBuyStatus``)
            order_id: Pre-sale order number (API: ``orderId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"proBuyStatus": pro_buy_status, "orderId": order_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/queryProOrderList", json_body=payload)

    def query_pad_id_change_records(
        self,
        *,
        query_date: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Query padCode Change Records**.

        Query padCode change records for devices owned by the current user

        ``POST /vcpcloud/api/padApi/queryPadIdChangeRecords``

        Args:
            query_date: Calendar day to query (format `yyyy-MM-dd`, Asia/Shanghai). If omitted, the last 3 calendar days (inclusive of today) are returned. Future dates are rejected (API: ``queryDate``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"queryDate": query_date}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/queryPadIdChangeRecords", json_body=payload)

    def list_pad_backup_ids(
        self,
        **extra: Any,
    ) -> Any:
        """List Pad Backup IDs**.

        List all available cloud-disk backup IDs owned by the current OpenAPI user, ordered by create time descending. The returned IDs can be fed into the batch clone endpoint below.

        ``POST /vcpcloud/api/padApi/listPadBackupIds``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/listPadBackupIds", json_body=payload)

    def add_backup(
        self,
        vc_pad_backup_list: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Create Pad Backups**.

        Batch create cloud-disk backups for the given cloud phones. The call is asynchronous and returns immediately; use the `batchId` in the response to track task progress. Constraints: * Up to 50 cloud phones per call. * Only one in-flight backup task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Remaining storage quota must be at least 16GB × backup pad count.

        ``POST /vcpcloud/api/padApi/addBackup``

        Args:
            vc_pad_backup_list: Cloud phones to back up (1 to 50 entries) (API: ``vcPadBackupList``, required) Nested fields: ``padCode``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"vcPadBackupList": vc_pad_backup_list}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/addBackup", json_body=payload)

    def clone_pad_backup(
        self,
        vc_pad_backup_list: Sequence[Mapping[str, Any]],
        pads: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Clone Pad Backup to Multiple Pads**.

        Batch clone a cloud-disk backup onto multiple cloud phones. The call is asynchronous and returns immediately. Constraints: * Only one in-flight clone task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Source backup and target cloud phone product specs must match.

        ``POST /vcpcloud/api/padApi/clonePadBackup``

        Args:
            vc_pad_backup_list: Source backup list (at least 1 item) (API: ``vcPadBackupList``, required) Nested fields: ``backupId``.
            pads: Target cloud phone list (at least 1 item) (API: ``pads``, required) Nested fields: ``padCode``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"vcPadBackupList": vc_pad_backup_list, "pads": pads}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/clonePadBackup", json_body=payload)

    def query_backup_batch(
        self,
        batch_id: str,
        **extra: Any,
    ) -> Any:
        """Query Backup Batch Progress**.

        Query backup progress by `batchId`. Returns per-pad status and `backupId` (available once status ≥ 1). Use the `batchId` returned by `addBackup` to poll this endpoint.

        ``POST /vcpcloud/api/padApi/queryBackupBatch``

        Args:
            batch_id: Batch ID returned by `addBackup` (API: ``batchId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"batchId": batch_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/queryBackupBatch", json_body=payload)


class AsyncPhoneAPI(AsyncAPIResource):
    """Async variant of :class:`PhoneAPI`."""

    async def create_timing_share(
        self,
        *,
        equipment_id: Optional[int] = None,
        pad_code: Optional[str] = None,
        permission: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Cloud Phone Management.

        Create a share token for one powered-on timing device. Sharing ends after the device is powered off.

        ``POST /vcpcloud/api/padApi/createTimingShare``

        Args:
            equipment_id: Device ID (API: ``equipmentId``)
            pad_code: Timing device ID (API: ``padCode``)
            permission: Share permission (API: ``permission``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"equipmentId": equipment_id, "padCode": pad_code, "permission": permission}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createTimingShare", json_body=payload)

    async def open_auto_renew(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Enable Cloud Phone Auto-Renewal.

        Enable auto-renewal for a single cloud phone; it will be renewed automatically with the current package before expiration.

        ``POST /vcpcloud/api/padApi/openAutoRenew``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/openAutoRenew", json_body=payload)

    async def close_auto_renew(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Disable Cloud Phone Auto-Renewal.

        Disable auto-renewal for a single cloud phone; once disabled, it will no longer be renewed automatically upon expiration.

        ``POST /vcpcloud/api/padApi/closeAutoRenew``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/closeAutoRenew", json_body=payload)

    async def close_all_auto_renew(
        self,
        **extra: Any,
    ) -> Any:
        """Batch Disable Cloud Phone Auto-Renewal.

        Disable auto-renewal for all cloud phones under the current account in a single call; once disabled, they will no longer be renewed automatically upon expiration.

        ``POST /vcpcloud/api/padApi/closeAllAutoRenew``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/closeAllAutoRenew", json_body=payload)

    async def update_pad_name(
        self,
        pad_code: str,
        pad_name: str,
        **extra: Any,
    ) -> Any:
        """Rename Cloud Phone.

        Rename a single cloud phone.

        ``POST /vcpcloud/api/padApi/updatePadName``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            pad_name: New cloud phone name (API: ``padName``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "padName": pad_name}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/updatePadName", json_body=payload)

    async def authorize_pad(
        self,
        pad_code: str,
        authorized_account: str,
        *,
        minutes: Optional[int] = None,
        equi_authorize: Optional[bool] = None,
        permission: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Authorize Pad.

        Temporarily grant a single cloud phone to another account. During the authorization the granted account can access the cloud phone; device ownership does not change.

        ``POST /vcpcloud/api/padApi/authorizePad``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            authorized_account: Granted account (registered phone number or email) (API: ``authorizedAccount``, required)
            minutes: Authorization duration in minutes; required when equiAuthorize=false (API: ``minutes``)
            equi_authorize: Authorize for the device's remaining validity; default false (API: ``equiAuthorize``)
            permission: Allowed-operation list, comma-separated; empty means all (API: ``permission``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "authorizedAccount": authorized_account, "minutes": minutes, "equiAuthorize": equi_authorize, "permission": permission}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/authorizePad", json_body=payload)

    async def replace_real_adi_template(
        self,
        pad_codes: Sequence[str],
        wipe_data: bool,
        real_phone_template_id: int,
        **extra: Any,
    ) -> Any:
        """Modify Real Device ADI Template.

        Modify cloud real device ADI template with provided template ID. Conditions: 1. Instance created as cloud real device type 2. Instance Android version matches target ADI version

        ``POST /vcpcloud/api/padApi/replaceRealAdiTemplate``

        Args:
            pad_codes: (API: ``padCodes``, required)
            wipe_data: Clear data (API: ``wipeData``, required)
            real_phone_template_id: Real device template ID (API: ``realPhoneTemplateId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "wipeData": wipe_data, "realPhoneTemplateId": real_phone_template_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/replaceRealAdiTemplate", json_body=payload)

    async def create_money_order(
        self,
        android_version_name: str,
        good_id: int,
        good_num: int,
        auto_renew: bool,
        equipment_id: str,
        *,
        country_code: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Create Cloud Phone.

        Create a new cloud phone. (Note that the purchased product package must be available on the web platform, otherwise the purchase will fail.)

        ``POST /vcpcloud/api/padApi/createMoneyOrder``

        Args:
            android_version_name: Android version: Android10、Android13, Android14 (API: ``androidVersionName``, required)
            good_id: Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) (API: ``goodId``, required)
            good_num: Product quantity (API: ``goodNum``, required)
            auto_renew: Whether to auto-renew (enabled by default) (API: ``autoRenew``, required)
            equipment_id: Renewal device IDs (comma separated for multiple devices) (API: ``equipmentId``, required)
            country_code: Country code, used to specify the region of the cloud phone (API: ``countryCode``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"androidVersionName": android_version_name, "goodId": good_id, "goodNum": good_num, "autoRenew": auto_renew, "equipmentId": equipment_id, "countryCode": country_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createMoneyOrder", json_body=payload)

    async def activate_by_code(
        self,
        active_code_list: Sequence[str],
        *,
        country_code: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Activate Cloud Phone with Activation Code.

        Batch-activate cloud phones using activation codes. Submit a list of activation codes and immediately get a batch number (batchId); cloud phones are created asynchronously in the background and belong to the caller's account once activated. Activation codes that cannot be used are returned in failCodes. (The product package corresponding to the activation code must exist and be valid on the web platform, otherwise activation will fail.)

        ``POST /vcpcloud/api/padApi/activateByCode``

        Args:
            active_code_list: List of activation codes, multiple allowed (API: ``activeCodeList``, required)
            country_code: Country/region code. Defaults to HK if not provided (API: ``countryCode``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"activeCodeList": active_code_list, "countryCode": country_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/activateByCode", json_body=payload)

    async def query_activation_batch(
        self,
        batch_id: str,
        **extra: Any,
    ) -> Any:
        """Query Batch Activation Progress.

        Query the progress of a batch activation task submitted via activateByCode. Returns the overall status, the number of activation codes succeeded/failed/in progress, the number of activated devices, and per-code details.

        ``POST /vcpcloud/api/padApi/queryActivationBatch``

        Args:
            batch_id: Batch number returned by activateByCode (API: ``batchId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"batchId": batch_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/queryActivationBatch", json_body=payload)

    async def user_pad_list(
        self,
        *,
        pad_code: Optional[str] = None,
        equipment_ids: Optional[Sequence[Any]] = None,
        **extra: Any,
    ) -> Any:
        """Cloud Phone List.

        Cloud phone list.

        ``POST /vcpcloud/api/padApi/userPadList``

        Args:
            pad_code: Instance code (API: ``padCode``)
            equipment_ids: Array of equipment IDs (API: ``equipmentIds``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "equipmentIds": equipment_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/userPadList", json_body=payload)

    async def pad_info(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Cloud Phone Information Query.

        Query cloud phone information.

        ``POST /vcpcloud/api/padApi/padInfo``

        Args:
            pad_code: Instance ID (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body=payload)

    async def get_cloud_good_list(
        self,
        **extra: Any,
    ) -> Any:
        """SKU Package List.

        Get the SKU package list.

        ``GET /vcpcloud/api/padApi/getCloudGoodList``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/getCloudGoodList", query=payload)

    async def image_version_list(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Android image version collection.

        Get the image set that can be upgraded on the current device

        ``POST /vcpcloud/api/padApi/imageVersionList``

        Args:
            pad_code: PadCode (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/imageVersionList", json_body=payload)

    async def create_money_pro_order(
        self,
        *,
        android_version_name: Optional[str] = None,
        good_id: Optional[int] = None,
        good_num: Optional[int] = None,
        auto_renew: Optional[bool] = None,
        country_code: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Equipment Pre-sale Purchase.

        When stock is insufficient, you can use this API to pre-order a device (only applicable to cloud phone products with a rental period of 30 days or more). Once stock is replenished, the system will prioritize fulfilling pre-sale orders and automatically dispatch the devices. After the order is shipped, users will receive an email notification and an additional one-day usage bonus.

        ``POST /vcpcloud/api/padApi/createMoneyProOrder``

        Args:
            android_version_name: Android Version：Android10、Android13、Android14 (API: ``androidVersionName``)
            good_id: Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) (API: ``goodId``)
            good_num: Product Number (API: ``goodNum``)
            auto_renew: Whether to automatically renew (default closed) true-on, false-off (API: ``autoRenew``)
            country_code: Country code, used to specify the region of the cloud phone (API: ``countryCode``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"androidVersionName": android_version_name, "goodId": good_id, "goodNum": good_num, "autoRenew": auto_renew, "countryCode": country_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/createMoneyProOrder", json_body=payload)

    async def query_pro_order_list(
        self,
        *,
        pro_buy_status: Optional[int] = None,
        order_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Query pre-sale order result details.

        Query the details of pre-sale order results. You can query by pre-sale order number, order status (1-to be shipped 2-shipped, empty default all)

        ``POST /vcpcloud/api/padApi/queryProOrderList``

        Args:
            pro_buy_status: 1-To be shipped 2-Shipment If empty, default to all (API: ``proBuyStatus``)
            order_id: Pre-sale order number (API: ``orderId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"proBuyStatus": pro_buy_status, "orderId": order_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/queryProOrderList", json_body=payload)

    async def query_pad_id_change_records(
        self,
        *,
        query_date: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Query padCode Change Records**.

        Query padCode change records for devices owned by the current user

        ``POST /vcpcloud/api/padApi/queryPadIdChangeRecords``

        Args:
            query_date: Calendar day to query (format `yyyy-MM-dd`, Asia/Shanghai). If omitted, the last 3 calendar days (inclusive of today) are returned. Future dates are rejected (API: ``queryDate``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"queryDate": query_date}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/queryPadIdChangeRecords", json_body=payload)

    async def list_pad_backup_ids(
        self,
        **extra: Any,
    ) -> Any:
        """List Pad Backup IDs**.

        List all available cloud-disk backup IDs owned by the current OpenAPI user, ordered by create time descending. The returned IDs can be fed into the batch clone endpoint below.

        ``POST /vcpcloud/api/padApi/listPadBackupIds``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/listPadBackupIds", json_body=payload)

    async def add_backup(
        self,
        vc_pad_backup_list: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Create Pad Backups**.

        Batch create cloud-disk backups for the given cloud phones. The call is asynchronous and returns immediately; use the `batchId` in the response to track task progress. Constraints: * Up to 50 cloud phones per call. * Only one in-flight backup task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Remaining storage quota must be at least 16GB × backup pad count.

        ``POST /vcpcloud/api/padApi/addBackup``

        Args:
            vc_pad_backup_list: Cloud phones to back up (1 to 50 entries) (API: ``vcPadBackupList``, required) Nested fields: ``padCode``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"vcPadBackupList": vc_pad_backup_list}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/addBackup", json_body=payload)

    async def clone_pad_backup(
        self,
        vc_pad_backup_list: Sequence[Mapping[str, Any]],
        pads: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Clone Pad Backup to Multiple Pads**.

        Batch clone a cloud-disk backup onto multiple cloud phones. The call is asynchronous and returns immediately. Constraints: * Only one in-flight clone task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Source backup and target cloud phone product specs must match.

        ``POST /vcpcloud/api/padApi/clonePadBackup``

        Args:
            vc_pad_backup_list: Source backup list (at least 1 item) (API: ``vcPadBackupList``, required) Nested fields: ``backupId``.
            pads: Target cloud phone list (at least 1 item) (API: ``pads``, required) Nested fields: ``padCode``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"vcPadBackupList": vc_pad_backup_list, "pads": pads}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/clonePadBackup", json_body=payload)

    async def query_backup_batch(
        self,
        batch_id: str,
        **extra: Any,
    ) -> Any:
        """Query Backup Batch Progress**.

        Query backup progress by `batchId`. Returns per-pad status and `backupId` (available once status ≥ 1). Use the `batchId` returned by `addBackup` to poll this endpoint.

        ``POST /vcpcloud/api/padApi/queryBackupBatch``

        Args:
            batch_id: Batch ID returned by `addBackup` (API: ``batchId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"batchId": batch_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/queryBackupBatch", json_body=payload)
