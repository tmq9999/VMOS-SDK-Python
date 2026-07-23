"""Application management: install/uninstall, start/stop/restart apps, app lists, keep-alive and hidden-app configuration.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["AppsAPI", "AsyncAppsAPI"]


class AppsAPI(SyncAPIResource):
    """Application management: install/uninstall, start/stop/restart apps, app lists, keep-alive and hidden-app configuration."""

    def update_sim(
        self,
        pad_code: str,
        *,
        country_code: Optional[str] = None,
        props: Optional[Mapping[str, Any]] = None,
        **extra: Any,
    ) -> Any:
        """Modify SIM Card Information Based on Country Code.

        Static setting of Android modification properties, requires instance restart to take effect, generally used for modifying device information. Same function as [Modify Instance Android Modification Properties], difference: randomly generates SIM info and always restarts. Properties persistently stored.

        ``POST /vcpcloud/api/padApi/updateSIM``

        Args:
            pad_code: Instance ID (API: ``padCode``, required)
            country_code: Country code (API: ``countryCode``)
            props: System properties (key-value) (API: ``props``) Nested fields: ``ro.product.vendor.name``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "countryCode": country_code, "props": props}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/updateSIM", json_body=payload)

    def upload_file_v3(
        self,
        pad_codes: Sequence[str],
        *,
        auto_install: Optional[int] = None,
        file_unique_id: Optional[str] = None,
        customize_file_path: Optional[str] = None,
        file_name: Optional[str] = None,
        package_name: Optional[str] = None,
        url: Optional[str] = None,
        md5: Optional[str] = None,
        is_authorization: Optional[bool] = None,
        icon_path: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """File Upload via Link Directly.

        Push file from file management center to cloud phone instance (async task). If file found by md5 or file ID, directly use OSS path for download. If not in OSS, send URL for download and upload content to OSS. If auto install app, check package name; if empty, throw exception. (Auto install grants all permissions by default; use isAuthorization to disable).

        ``POST /vcpcloud/api/padApi/uploadFileV3``

        Args:
            pad_codes: (API: ``padCodes``, required) Nested fields: ``padCode``.
            auto_install: Auto install: 1-yes, 0-no (default no). Only for APK (API: ``autoInstall``)
            file_unique_id: File unique ID (API: ``fileUniqueId``)
            customize_file_path: Custom path (start with /, e.g. "/DCIM/", "/Documents/" etc.) (API: ``customizeFilePath``)
            file_name: File name (API: ``fileName``)
            package_name: Package name (API: ``packageName``)
            url: File URL (API: ``url``)
            md5: File MD5 (API: ``md5``)
            is_authorization: Grant permissions (default all) (API: ``isAuthorization``)
            icon_path: Icon for install (API: ``iconPath``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "autoInstall": auto_install, "fileUniqueId": file_unique_id, "customizeFilePath": customize_file_path, "fileName": file_name, "packageName": package_name, "url": url, "md5": md5, "isAuthorization": is_authorization, "iconPath": icon_path}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/uploadFileV3", json_body=payload)

    def batch_upload_file(
        self,
        list: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Batch Upload Files.

        Push different files to multiple cloud phone instances in a single call (e.g. different videos to different instances). Each item in `list` specifies a group of instances and its file. Items are processed independently; a failure of one item does not affect the others. Up to 100 items per call.

        ``POST /vcpcloud/api/padApi/batchUploadFile``

        Args:
            list: Upload item list, up to 100 items per call (API: ``list``, required) Nested fields: ``padCodes``, ``url``, ``autoInstall``, ``customizeFilePath``, ``fileName``, ``md5``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"list": list}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/batchUploadFile", json_body=payload)

    def list_installed_app(
        self,
        pad_codes: Sequence[str],
        *,
        app_name: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Real-Time Query Installed Apps List.

        ``POST /vcpcloud/api/padApi/listInstalledApp``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            app_name: App name (API: ``appName``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "appName": app_name}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/listInstalledApp", json_body=payload)

    def set_keep_alive_app(
        self,
        apply_all_instances: bool,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        app_infos: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Set App Keep-Alive.

        Currently supports Android 13,14,15 only.

        ``POST /vcpcloud/api/padApi/setKeepAliveApp``

        Args:
            apply_all_instances: Apply to all instances mode (API: ``applyAllInstances``, required)
            pad_codes: Instance codes (API: ``padCodes``)
            app_infos: (API: ``appInfos``) Nested fields: ``serverName``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"applyAllInstances": apply_all_instances, "padCodes": pad_codes, "appInfos": app_infos}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/setKeepAliveApp", json_body=payload)

    def add_user_rom(
        self,
        name: str,
        update_log: str,
        android_version: str,
        version: str,
        download_url: str,
        package_size: str,
        **extra: Any,
    ) -> Any:
        """Upload User Image.

        ``POST /vcpcloud/api/padApi/addUserRom``

        Args:
            name: ROM name (API: ``name``, required)
            update_log: Update log (API: ``updateLog``, required)
            android_version: Android version (API: ``androidVersion``, required)
            version: Version (API: ``version``, required)
            download_url: Download URL (API: ``downloadUrl``, required)
            package_size: Size (bytes) (API: ``packageSize``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"name": name, "updateLog": update_log, "androidVersion": android_version, "version": version, "downloadUrl": download_url, "packageSize": package_size}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/addUserRom", json_body=payload)

    def install_app(
        self,
        apps: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Application Installation.

        Install one or more apps on one or more instances at once. This API is asynchronous and supports allowlist/blocklist logic.

        ``POST /vcpcloud/api/padApi/installApp``

        Args:
            apps: Application list (API: ``apps``, required) Nested fields: ``appId``, ``appName``, ``pkgName``, ``isGrantAllPerm``, ``padCodes``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"apps": apps}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/installApp", json_body=payload)

    def start_app(
        self,
        pkg_name: str,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """App Start.

        Start an app on an instance based on the instance ID and app package name.

        ``POST /vcpcloud/api/padApi/startApp``

        Args:
            pkg_name: Package Name (API: ``pkgName``, required)
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"pkgName": pkg_name, "padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/startApp", json_body=payload)

    def stop_app(
        self,
        pkg_name: str,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Stop App.

        Perform the operation of stopping an app on an instance based on the instance ID and app package name.

        ``POST /vcpcloud/api/padApi/stopApp``

        Args:
            pkg_name: Package Name (API: ``pkgName``, required)
            pad_codes: Instance IDs (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"pkgName": pkg_name, "padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/stopApp", json_body=payload)

    def restart_app(
        self,
        pkg_name: str,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Application Restart.

        Restart an application on an instance based on the instance ID and application package name.

        ``POST /vcpcloud/api/padApi/restartApp``

        Args:
            pkg_name: Package name (API: ``pkgName``, required)
            pad_codes: Instance IDs (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"pkgName": pkg_name, "padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/restartApp", json_body=payload)


class AsyncAppsAPI(AsyncAPIResource):
    """Async variant of :class:`AppsAPI`."""

    async def update_sim(
        self,
        pad_code: str,
        *,
        country_code: Optional[str] = None,
        props: Optional[Mapping[str, Any]] = None,
        **extra: Any,
    ) -> Any:
        """Modify SIM Card Information Based on Country Code.

        Static setting of Android modification properties, requires instance restart to take effect, generally used for modifying device information. Same function as [Modify Instance Android Modification Properties], difference: randomly generates SIM info and always restarts. Properties persistently stored.

        ``POST /vcpcloud/api/padApi/updateSIM``

        Args:
            pad_code: Instance ID (API: ``padCode``, required)
            country_code: Country code (API: ``countryCode``)
            props: System properties (key-value) (API: ``props``) Nested fields: ``ro.product.vendor.name``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "countryCode": country_code, "props": props}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/updateSIM", json_body=payload)

    async def upload_file_v3(
        self,
        pad_codes: Sequence[str],
        *,
        auto_install: Optional[int] = None,
        file_unique_id: Optional[str] = None,
        customize_file_path: Optional[str] = None,
        file_name: Optional[str] = None,
        package_name: Optional[str] = None,
        url: Optional[str] = None,
        md5: Optional[str] = None,
        is_authorization: Optional[bool] = None,
        icon_path: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """File Upload via Link Directly.

        Push file from file management center to cloud phone instance (async task). If file found by md5 or file ID, directly use OSS path for download. If not in OSS, send URL for download and upload content to OSS. If auto install app, check package name; if empty, throw exception. (Auto install grants all permissions by default; use isAuthorization to disable).

        ``POST /vcpcloud/api/padApi/uploadFileV3``

        Args:
            pad_codes: (API: ``padCodes``, required) Nested fields: ``padCode``.
            auto_install: Auto install: 1-yes, 0-no (default no). Only for APK (API: ``autoInstall``)
            file_unique_id: File unique ID (API: ``fileUniqueId``)
            customize_file_path: Custom path (start with /, e.g. "/DCIM/", "/Documents/" etc.) (API: ``customizeFilePath``)
            file_name: File name (API: ``fileName``)
            package_name: Package name (API: ``packageName``)
            url: File URL (API: ``url``)
            md5: File MD5 (API: ``md5``)
            is_authorization: Grant permissions (default all) (API: ``isAuthorization``)
            icon_path: Icon for install (API: ``iconPath``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "autoInstall": auto_install, "fileUniqueId": file_unique_id, "customizeFilePath": customize_file_path, "fileName": file_name, "packageName": package_name, "url": url, "md5": md5, "isAuthorization": is_authorization, "iconPath": icon_path}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/uploadFileV3", json_body=payload)

    async def batch_upload_file(
        self,
        list: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Batch Upload Files.

        Push different files to multiple cloud phone instances in a single call (e.g. different videos to different instances). Each item in `list` specifies a group of instances and its file. Items are processed independently; a failure of one item does not affect the others. Up to 100 items per call.

        ``POST /vcpcloud/api/padApi/batchUploadFile``

        Args:
            list: Upload item list, up to 100 items per call (API: ``list``, required) Nested fields: ``padCodes``, ``url``, ``autoInstall``, ``customizeFilePath``, ``fileName``, ``md5``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"list": list}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/batchUploadFile", json_body=payload)

    async def list_installed_app(
        self,
        pad_codes: Sequence[str],
        *,
        app_name: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Real-Time Query Installed Apps List.

        ``POST /vcpcloud/api/padApi/listInstalledApp``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            app_name: App name (API: ``appName``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "appName": app_name}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/listInstalledApp", json_body=payload)

    async def set_keep_alive_app(
        self,
        apply_all_instances: bool,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        app_infos: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Set App Keep-Alive.

        Currently supports Android 13,14,15 only.

        ``POST /vcpcloud/api/padApi/setKeepAliveApp``

        Args:
            apply_all_instances: Apply to all instances mode (API: ``applyAllInstances``, required)
            pad_codes: Instance codes (API: ``padCodes``)
            app_infos: (API: ``appInfos``) Nested fields: ``serverName``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"applyAllInstances": apply_all_instances, "padCodes": pad_codes, "appInfos": app_infos}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/setKeepAliveApp", json_body=payload)

    async def add_user_rom(
        self,
        name: str,
        update_log: str,
        android_version: str,
        version: str,
        download_url: str,
        package_size: str,
        **extra: Any,
    ) -> Any:
        """Upload User Image.

        ``POST /vcpcloud/api/padApi/addUserRom``

        Args:
            name: ROM name (API: ``name``, required)
            update_log: Update log (API: ``updateLog``, required)
            android_version: Android version (API: ``androidVersion``, required)
            version: Version (API: ``version``, required)
            download_url: Download URL (API: ``downloadUrl``, required)
            package_size: Size (bytes) (API: ``packageSize``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"name": name, "updateLog": update_log, "androidVersion": android_version, "version": version, "downloadUrl": download_url, "packageSize": package_size}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/addUserRom", json_body=payload)

    async def install_app(
        self,
        apps: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Application Installation.

        Install one or more apps on one or more instances at once. This API is asynchronous and supports allowlist/blocklist logic.

        ``POST /vcpcloud/api/padApi/installApp``

        Args:
            apps: Application list (API: ``apps``, required) Nested fields: ``appId``, ``appName``, ``pkgName``, ``isGrantAllPerm``, ``padCodes``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"apps": apps}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/installApp", json_body=payload)

    async def start_app(
        self,
        pkg_name: str,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """App Start.

        Start an app on an instance based on the instance ID and app package name.

        ``POST /vcpcloud/api/padApi/startApp``

        Args:
            pkg_name: Package Name (API: ``pkgName``, required)
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"pkgName": pkg_name, "padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/startApp", json_body=payload)

    async def stop_app(
        self,
        pkg_name: str,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Stop App.

        Perform the operation of stopping an app on an instance based on the instance ID and app package name.

        ``POST /vcpcloud/api/padApi/stopApp``

        Args:
            pkg_name: Package Name (API: ``pkgName``, required)
            pad_codes: Instance IDs (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"pkgName": pkg_name, "padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/stopApp", json_body=payload)

    async def restart_app(
        self,
        pkg_name: str,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Application Restart.

        Restart an application on an instance based on the instance ID and application package name.

        ``POST /vcpcloud/api/padApi/restartApp``

        Args:
            pkg_name: Package name (API: ``pkgName``, required)
            pad_codes: Instance IDs (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"pkgName": pkg_name, "padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/restartApp", json_body=payload)
