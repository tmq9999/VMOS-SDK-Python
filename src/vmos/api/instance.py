"""Instance management: restart/reset, properties, SIM/GPS/WiFi, ADB, screenshots, previews, image upgrade, one-click new device, root, network tools, media injection and more.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["InstanceAPI", "AsyncInstanceAPI"]


class InstanceAPI(SyncAPIResource):
    """Instance management: restart/reset, properties, SIM/GPS/WiFi, ADB, screenshots, previews, image upgrade, one-click new device, root, network tools, media injection and more."""

    def set_wifi_list(
        self,
        pad_codes: Sequence[str],
        wifi_json_list: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Modify Instance WIFI Properties.

        Modify the WIFI list properties of the specified instance (this interface and one-key new device WIFI setup are mutually exclusive, otherwise overwriting issues may occur)

        ``POST /vcpcloud/api/padApi/setWifiList``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            wifi_json_list: WIFI properties list (API: ``wifiJsonList``, required) Nested fields: ``SSID``, ``BSSID``, ``MAC``, ``IP``, ``gateway``, ``DNS1``, ``DNS2``, ``hessid``, ``anqpDomainId``, ``capabilities``, ``level``, ``linkSpeed``, ``txLinkSpeed``, ``rxLinkSpeed``, ``frequency``, ``distance``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "wifiJsonList": wifi_json_list}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/setWifiList", json_body=payload)

    def pad_detail(
        self,
        *,
        last_id: Optional[int] = None,
        rows: Optional[int] = None,
        pad_codes: Optional[Sequence[str]] = None,
        pad_ips: Optional[Sequence[str]] = None,
        online: Optional[int] = None,
        pad_status: Optional[int] = None,
        compute_occupied: Optional[bool] = None,
        net_storage_res_flag: Optional[int] = None,
        brand: Optional[str] = None,
        brand_model: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Query Cloud Phone Base Info List.

        Support paginated query of cloud phone base information including running status, online status, compute occupation, etc.

        ``POST /vcpcloud/api/padApi/padDetail``

        Args:
            last_id: Last query returned lastId; null for first query (API: ``lastId``)
            rows: Records per page, max 1000 per page (API: ``rows``)
            pad_codes: (API: ``padCodes``)
            pad_ips: (API: ``padIps``)
            online: Instance online status: 0-offline, 1-online (API: ``online``)
            pad_status: Instance running status: 14-abnormal, others-normal (API: ``padStatus``)
            compute_occupied: Filter compute occupation: true-occupied, false-not occupied (API: ``computeOccupied``)
            net_storage_res_flag: Net storage flag: 1-net storage instance, 0-local instance (API: ``netStorageResFlag``)
            brand: Instance brand (exact match) (API: ``brand``)
            brand_model: Brand model (exact match) (API: ``brandModel``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"lastId": last_id, "rows": rows, "padCodes": pad_codes, "padIps": pad_ips, "online": online, "padStatus": pad_status, "computeOccupied": compute_occupied, "netStorageResFlag": net_storage_res_flag, "brand": brand, "brandModel": brand_model}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/padDetail", json_body=payload)

    def restart(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Instance Restart.

        Perform restart operation on the specified instance to resolve issues like system unresponsiveness or freezing.

        ``POST /vcpcloud/api/padApi/restart``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/restart", json_body=payload)

    def reset(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Instance Reset.

        ``POST /vcpcloud/api/padApi/reset``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/reset", json_body=payload)

    def pad_properties(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Query Instance Properties.

        Query the property information of the specified instance, including system properties and settings.

        ``POST /vcpcloud/api/padApi/padProperties``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/padProperties", json_body=payload)

    def batch_pad_properties(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Batch Query Instance Properties.

        Batch query the property information of specified instances, including system properties and settings.

        ``POST /vcpcloud/api/padApi/batchPadProperties``

        Args:
            pad_codes: Instance count not exceeding 200 (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/batchPadProperties", json_body=payload)

    def update_pad_properties(
        self,
        pad_codes: Sequence[str],
        *,
        modem_persist_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        modem_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        system_persist_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        system_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        setting_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        oaid_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Modify Instance Properties.

        Dynamically modify instance properties, including system and settings. Instance must be powered on; this interface takes effect immediately. Refer to [Instance Properties List](https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/InstanceList.html#modem-properties-%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8)

        ``POST /vcpcloud/api/padApi/updatePadProperties``

        Args:
            pad_codes: (API: ``padCodes``, required)
            modem_persist_properties_list: Modem persistent properties list (API: ``modemPersistPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            modem_properties_list: Modem non-persistent properties list (API: ``modemPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            system_persist_properties_list: System persistent properties list (API: ``systemPersistPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            system_properties_list: System non-persistent properties list (API: ``systemPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            setting_properties_list: Setting properties list (API: ``settingPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            oaid_properties_list: OAID properties list (API: ``oaidPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "modemPersistPropertiesList": modem_persist_properties_list, "modemPropertiesList": modem_properties_list, "systemPersistPropertiesList": system_persist_properties_list, "systemPropertiesList": system_properties_list, "settingPropertiesList": setting_properties_list, "oaidPropertiesList": oaid_properties_list}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/updatePadProperties", json_body=payload)

    def update_pad_android_prop(
        self,
        props: Mapping[str, Any],
        *,
        pad_code: Optional[str] = None,
        restart: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Modify Instance Android Modification Properties.

        ``POST /vcpcloud/api/padApi/updatePadAndroidProp``

        Args:
            props: System properties (key-value) (API: ``props``, required) Nested fields: ``ro.product.vendor.name``.
            pad_code: Instance ID (API: ``padCode``)
            restart: Auto restart after setting (default false) (API: ``restart``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"props": props, "padCode": pad_code, "restart": restart}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/updatePadAndroidProp", json_body=payload)

    def get_update_sim_task_status(
        self,
        task_id: str,
        **extra: Any,
    ) -> Any:
        """Query SIM Modification Task Status.

        Query the execution status of a task by the taskId returned from [Modify SIM Card Information Based on Country Code](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#modify-sim-card-information-based-on-country-code). Only tasks created by the current account can be queried.

        ``POST /vcpcloud/api/padApi/getUpdateSIMTaskStatus``

        Args:
            task_id: Task ID returned by updateSIM (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/getUpdateSIMTaskStatus", json_body=payload)

    def dissolve_room(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Stop Streaming.

        Stop streaming for specified instance, disconnect connection.

        ``POST /vcpcloud/api/padApi/dissolveRoom``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/dissolveRoom", json_body=payload)

    def check_ip(
        self,
        host: str,
        port: int,
        account: str,
        password: str,
        type: str,
        *,
        country: Optional[str] = None,
        ip: Optional[str] = None,
        loc: Optional[str] = None,
        city: Optional[str] = None,
        region: Optional[str] = None,
        timezone: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Smart IP Proxy Detection.

        Detect if proxy IP is available and if location information is correct.

        ``POST /vcpcloud/api/padApi/checkIP``

        Args:
            host: Proxy info (IP or host) (API: ``host``, required)
            port: Proxy port (numeric) (API: ``port``, required)
            account: Proxy username (API: ``account``, required)
            password: Proxy password (API: ``password``, required)
            type: Proxy protocol: Socks5, http, https (API: ``type``, required)
            country: Country - required when forcing specification (API: ``country``)
            ip: IP - required when forcing (API: ``ip``)
            loc: Latitude, longitude - required when forcing (API: ``loc``)
            city: City - required when forcing (API: ``city``)
            region: Region - required when forcing (API: ``region``)
            timezone: Timezone - required when forcing (API: ``timezone``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"host": host, "port": port, "account": account, "password": password, "type": type, "country": country, "ip": ip, "loc": loc, "city": city, "region": region, "timezone": timezone}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/checkIP", json_body=payload)

    def smart_ip(
        self,
        pad_codes: Sequence[str],
        host: str,
        port: int,
        account: str,
        password: str,
        type: str,
        mode: str,
        *,
        bypass_package_list: Optional[Sequence[Any]] = None,
        bypass_ip_list: Optional[Sequence[Any]] = None,
        bypass_domain_list: Optional[Sequence[Any]] = None,
        follow_language: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Set Smart IP.

        ``POST /vcpcloud/api/padApi/smartIp``

        Args:
            pad_codes: (API: ``padCodes``, required)
            host: Proxy info (IP or host) (API: ``host``, required)
            port: Proxy port (API: ``port``, required)
            account: Proxy username (API: ``account``, required)
            password: Proxy password (API: ``password``, required)
            type: Proxy protocol: socks5, http, https (API: ``type``, required)
            mode: Proxy mode: vpn / proxy (API: ``mode``, required)
            bypass_package_list: Bypass packages (API: ``bypassPackageList``)
            bypass_ip_list: Bypass IPs (API: ``bypassIpList``)
            bypass_domain_list: Bypass domains (API: ``bypassDomainList``)
            follow_language: Whether device language follows the proxy IP (API: ``followLanguage``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "host": host, "port": port, "account": account, "password": password, "type": type, "mode": mode, "bypassPackageList": bypass_package_list, "bypassIpList": bypass_ip_list, "bypassDomainList": bypass_domain_list, "followLanguage": follow_language}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/smartIp", json_body=payload)

    def not_smart_ip(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Cancel Smart IP.

        Cancel smart IP, restore exit IP, SIM info, GPS, timezone (device restarts, takes effect within 1 minute; status 119-initializing; returns to 100-normal on success/failure/timeout; timeout 5 minutes).

        ``POST /vcpcloud/api/padApi/notSmartIp``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/notSmartIp", json_body=payload)

    def get_list_installed_app(
        self,
        pad_code_list: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Get All Installed Apps in Specified Cloud Instance List.

        ``POST /vcpcloud/api/padApi/getListInstalledApp``

        Args:
            pad_code_list: (API: ``padCodeList``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodeList": pad_code_list}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/getListInstalledApp", json_body=payload)

    def update_time_zone(
        self,
        time_zone: str,
        pad_codes: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Modify Instance Timezone.

        ``POST /vcpcloud/api/padApi/updateTimeZone``

        Args:
            time_zone: UTC standard timezone (API: ``timeZone``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"timeZone": time_zone, "padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/updateTimeZone", json_body=payload)

    def update_language(
        self,
        language: str,
        pad_codes: Sequence[Any],
        *,
        country: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Modify Instance Language.

        ``POST /vcpcloud/api/padApi/updateLanguage``

        Args:
            language: Language (API: ``language``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            country: Country (API: ``country``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"language": language, "padCodes": pad_codes, "country": country}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/updateLanguage", json_body=payload)

    def gps_inject_info(
        self,
        longitude: float,
        latitude: float,
        pad_codes: Sequence[Any],
        *,
        altitude: Optional[float] = None,
        speed: Optional[float] = None,
        bearing: Optional[float] = None,
        horizontal_accuracy_meters: Optional[float] = None,
        **extra: Any,
    ) -> Any:
        """Set Instance Latitude and Longitude.

        ``POST /vcpcloud/api/padApi/gpsInjectInfo``

        Args:
            longitude: Longitude (API: ``longitude``, required)
            latitude: Latitude (API: ``latitude``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            altitude: Altitude (requires latest image) (API: ``altitude``)
            speed: Speed m/s (images after 20251024) (API: ``speed``)
            bearing: Bearing ° (images after 20251024) (API: ``bearing``)
            horizontal_accuracy_meters: Horizontal accuracy (images after 20251024) (API: ``horizontalAccuracyMeters``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"longitude": longitude, "latitude": latitude, "padCodes": pad_codes, "altitude": altitude, "speed": speed, "bearing": bearing, "horizontalAccuracyMeters": horizontal_accuracy_meters}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/gpsInjectInfo", json_body=payload)

    def info(
        self,
        pad_codes: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Query Instance Proxy Information.

        ``POST /vcpcloud/open/network/proxy/info``

        Args:
            pad_codes: Instance list (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/open/network/proxy/info", json_body=payload)

    def replace_pad(
        self,
        pad_codes: Sequence[Any],
        *,
        country_code: Optional[str] = None,
        real_phone_template_id: Optional[int] = None,
        android_prop: Optional[Mapping[str, Any]] = None,
        replacement_real_adi_flag: Optional[bool] = None,
        exclude_real_phone_template_ids: Optional[Sequence[Any]] = None,
        certificate: Optional[str] = None,
        wipe_data: Optional[bool] = None,
        wipe_specific_data: Optional[Sequence[str]] = None,
        keep_specific_data: Optional[Sequence[str]] = None,
        enable_cpu_core_config: Optional[bool] = None,
        webview_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """One-Key New Device** ⭐.

        * Virtual machine: directly set Android properties, clear all data * Cloud real device: clear all data (equivalent to reset), add SIM info; if template ID provided, replace ADI template. If no template and replacementRealAdiFlag true, randomly select template. * Note: If no country info or unsupported, default Singapore SIM. * Unsupported country returns 500 error: Currently not supporting country code XX * Path Format Conversion Rules: /data/system/... -> /system/... /data/misc/... -> /misc/..…

        ``POST /vcpcloud/api/padApi/replacePad``

        Args:
            pad_codes: Instance ID list (API: ``padCodes``, required)
            country_code: Country code (see: https://chahuo.com/country-code-lookup.html) (API: ``countryCode``)
            real_phone_template_id: Template ID (refer to [Paginated Get Real Device Templates]) (API: ``realPhoneTemplateId``)
            android_prop: Refer to [Android Modification Properties List] (API: ``androidProp``)
            replacement_real_adi_flag: Whether random ADI template for real device (false-no, true-yes) (API: ``replacementRealAdiFlag``)
            exclude_real_phone_template_ids: Exclude template IDs when random (API: ``excludeRealPhoneTemplateIds``)
            certificate: Phone root certificate (API: ``certificate``)
            wipe_data: Clear user data (default true, CBS2.4.4+ support) (API: ``wipeData``)
            wipe_specific_data: Effective when wipeData false; specify data to clear (API: ``wipeSpecificData``)
            keep_specific_data: Effective when wipeData is false; specifies which data should be preserved (mutually exclusive with wipeSpecificData) (API: ``keepSpecificData``)
            enable_cpu_core_config: Enable CPU core config (based on Android cpuset for performance stability) (API: ``enableCpuCoreConfig``)
            webview_id: WebView version ID, see [Query Available WebView Versions](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#query-available-webview-versions) (API: ``webviewId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "countryCode": country_code, "realPhoneTemplateId": real_phone_template_id, "androidProp": android_prop, "replacementRealAdiFlag": replacement_real_adi_flag, "excludeRealPhoneTemplateIds": exclude_real_phone_template_ids, "certificate": certificate, "wipeData": wipe_data, "wipeSpecificData": wipe_specific_data, "keepSpecificData": keep_specific_data, "enableCpuCoreConfig": enable_cpu_core_config, "webviewId": webview_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/replacePad", json_body=payload)

    def pad_replace_new(
        self,
        pad_codes: Sequence[str],
        set_proxy_flag: bool,
        *,
        wipe_data: Optional[bool] = None,
        keep_lang_timezone: Optional[bool] = None,
        android_prop: Optional[Mapping[str, Any]] = None,
        webview_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """One-Key New Device (Auto SIM/GPS/Timezone)** ⭐.

        ``POST /vcpcloud/api/padApi/padReplaceNew``

        Args:
            pad_codes: Instance codes (does not support `ACN` prefix) (API: ``padCodes``, required)
            set_proxy_flag: Set to `true` to write SIM based on deployment location (API: ``setProxyFlag``, required)
            wipe_data: Whether to clear data; default `true` (API: ``wipeData``)
            keep_lang_timezone: Whether to keep old language/timezone; default `false` (API: ``keepLangTimezone``)
            android_prop: Custom Android system properties as key-value pairs. Examples: `persist.sys.locale`, `persist.sys.timezone`, etc. Higher priority than auto-generated properties (API: ``androidProp``)
            webview_id: WebView version ID, see [Query Available WebView Versions](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#query-available-webview-versions) (API: ``webviewId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "setProxyFlag": set_proxy_flag, "wipeData": wipe_data, "keepLangTimezone": keep_lang_timezone, "androidProp": android_prop, "webviewId": webview_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/padReplaceNew", json_body=payload)

    def country(
        self,
        **extra: Any,
    ) -> Any:
        """Query One-Key New Device Supported Countries List.

        ``GET /vcpcloud/api/padApi/country``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("GET", "/vcpcloud/api/padApi/country", query=payload)

    def webview_version_list(
        self,
        **extra: Any,
    ) -> Any:
        """Query Available WebView Versions.

        ``POST /vcpcloud/api/padApi/webview/version/list``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/webview/version/list", json_body=payload)

    def replacement(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Device Replacement.

        ``POST /vcpcloud/api/padApi/replacement``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/replacement", json_body=payload)

    def get_long_generate_url(
        self,
        pad_codes: Sequence[Any],
        *,
        format: Optional[str] = None,
        height: Optional[str] = None,
        width: Optional[str] = None,
        quality: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get Instance Real-Time Preview Image.

        Get current screen screenshot for specified instance. Returns URL and expiration; access URL for real-time screenshot. Supports batch.

        ``POST /vcpcloud/api/padApi/getLongGenerateUrl``

        Args:
            pad_codes: Instance list (API: ``padCodes``, required)
            format: Image format: png, jpg (default png; png no compression) (API: ``format``)
            height: Scaled height (pixels; default original) (API: ``height``)
            width: Scaled width (pixels; default original) (API: ``width``)
            quality: Image quality (0-100; default 50%; below 60 blurry) (API: ``quality``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "format": format, "height": height, "width": width, "quality": quality}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/getLongGenerateUrl", json_body=payload)

    def set_proxy(
        self,
        enable: bool,
        pad_codes: Sequence[Any],
        *,
        account: Optional[str] = None,
        password: Optional[str] = None,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        proxy_type: Optional[str] = None,
        proxy_name: Optional[str] = None,
        model: Optional[str] = None,
        bypass_package_list: Optional[Sequence[Any]] = None,
        bypass_ip_list: Optional[Sequence[Any]] = None,
        bypass_domain_list: Optional[Sequence[Any]] = None,
        limit_package_list: Optional[Sequence[Any]] = None,
        limit_ip_list: Optional[Sequence[Any]] = None,
        limit_domain_list: Optional[Sequence[Any]] = None,
        s_uo_t: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Instance Set Proxy.

        ``POST /vcpcloud/api/padApi/setProxy``

        Args:
            enable: Enable (API: ``enable``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            account: Username (API: ``account``)
            password: Password (API: ``password``)
            ip: IP (API: ``ip``)
            port: Port (API: ``port``)
            proxy_type: Supported: proxy, vpn (API: ``proxyType``)
            proxy_name: Supported: socks5, http-relay (includes http/https) (API: ``proxyName``)
            model: List mode: bypass(default)/limit (API: ``model``)
            bypass_package_list: Packages bypassing proxy (model=bypass) (API: ``bypassPackageList``)
            bypass_ip_list: IPs bypassing proxy (model=bypass) (API: ``bypassIpList``)
            bypass_domain_list: Domains bypassing proxy (model=bypass) (API: ``bypassDomainList``)
            limit_package_list: Only these packages use proxy (model=limit) (API: ``limitPackageList``)
            limit_ip_list: Only these IPs use proxy (model=limit) (API: ``limitIpList``)
            limit_domain_list: Only these domains use proxy (model=limit) (API: ``limitDomainList``)
            s_uo_t: Enable UDP (default false) (API: ``sUoT``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"enable": enable, "padCodes": pad_codes, "account": account, "password": password, "ip": ip, "port": port, "proxyType": proxy_type, "proxyName": proxy_name, "model": model, "bypassPackageList": bypass_package_list, "bypassIpList": bypass_ip_list, "bypassDomainList": bypass_domain_list, "limitPackageList": limit_package_list, "limitIpList": limit_ip_list, "limitDomainList": limit_domain_list, "sUoT": s_uo_t}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/setProxy", json_body=payload)

    def async_cmd(
        self,
        pad_codes: Sequence[str],
        script_content: str,
        **extra: Any,
    ) -> Any:
        """Async Execute ADB Commands.

        Async execute commands in one or more cloud instances.

        ``POST /vcpcloud/api/padApi/asyncCmd``

        Args:
            pad_codes: (API: ``padCodes``, required)
            script_content: ADB commands (multiple separated by “;” ) (API: ``scriptContent``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "scriptContent": script_content}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/asyncCmd", json_body=payload)

    def switch_root(
        self,
        pad_codes: Sequence[str],
        root_status: int,
        *,
        global_root: Optional[bool] = None,
        package_name: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Switch Root Permissions.

        Switch root permissions in one or more cloud instances. For single app root, specify package name (cloud real device: not recommended global root due to detection risk).

        ``POST /vcpcloud/api/padApi/switchRoot``

        Args:
            pad_codes: (API: ``padCodes``, required)
            root_status: Root status: 0-off, 1-on (API: ``rootStatus``, required)
            global_root: Global root (default no) (API: ``globalRoot``)
            package_name: Package name (required for non-global; multiple comma separated) (API: ``packageName``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "rootStatus": root_status, "globalRoot": global_root, "packageName": package_name}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/switchRoot", json_body=payload)

    def screenshot(
        self,
        pad_codes: Sequence[str],
        rotation: int,
        *,
        broadcast: Optional[bool] = None,
        definition: Optional[int] = None,
        resolution_height: Optional[int] = None,
        resolution_width: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Local Screenshot.

        Instance screenshot.

        ``POST /vcpcloud/api/padApi/screenshot``

        Args:
            pad_codes: (API: ``padCodes``, required)
            rotation: Screenshot orientation: 0-default, 1-rotate to portrait (API: ``rotation``, required)
            broadcast: Broadcast event (default false) (API: ``broadcast``)
            definition: Clarity 0-100 (API: ``definition``)
            resolution_height: Height >1 (API: ``resolutionHeight``)
            resolution_width: Width >1 (API: ``resolutionWidth``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "rotation": rotation, "broadcast": broadcast, "definition": definition, "resolutionHeight": resolution_height, "resolutionWidth": resolution_width}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/screenshot", json_body=payload)

    def generate_preview(
        self,
        pad_codes: Sequence[str],
        rotation: int,
        *,
        broadcast: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Generate Preview Image.

        Get preview image for specified instance.

        ``POST /vcpcloud/api/padApi/generatePreview``

        Args:
            pad_codes: (API: ``padCodes``, required)
            rotation: Screenshot orientation: 0-default, 1-rotate to portrait (API: ``rotation``, required)
            broadcast: Broadcast event (default false) (API: ``broadcast``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "rotation": rotation, "broadcast": broadcast}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/generatePreview", json_body=payload)

    def upgrade_image(
        self,
        pad_codes: Sequence[str],
        image_id: str,
        wipe_data: bool,
        *,
        enable_cpu_core_config: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Upgrade Image.

        Batch instance image upgrade.

        ``POST /vcpcloud/api/padApi/upgradeImage``

        Args:
            pad_codes: (API: ``padCodes``, required)
            image_id: Image ID (API: ``imageId``, required)
            wipe_data: Clear data partition: true-yes, false-no (API: ``wipeData``, required)
            enable_cpu_core_config: Enable CPU core config (API: ``enableCpuCoreConfig``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "imageId": image_id, "wipeData": wipe_data, "enableCpuCoreConfig": enable_cpu_core_config}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/upgradeImage", json_body=payload)

    def set_hide_accessibility_app_list(
        self,
        pad_codes: Sequence[str],
        app_infos: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Hide Accessibility Service.

        1. The specified app itself can still detect that it has enabled accessibility service. 2. Third-party apps cannot detect that the specified app has enabled accessibility service. 3. The specified app will not appear in the accessibility service list.

        ``POST /vcpcloud/api/padApi/setHideAccessibilityAppList``

        Args:
            pad_codes: Array of instance codes (maximum 200) (API: ``padCodes``, required)
            app_infos: Array of hidden app list objects; pass empty array [] to clear (0–200 items) (API: ``appInfos``, required) Nested fields: ``packageName``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "appInfos": app_infos}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/setHideAccessibilityAppList", json_body=payload)

    def virtual_real_switch(
        self,
        pad_codes: Sequence[str],
        image_id: str,
        wipe_data: bool,
        upgrade_image_convert_type: str,
        *,
        real_phone_template_id: Optional[int] = None,
        screen_layout_id: Optional[int] = None,
        certificate: Optional[str] = None,
        device_android_props: Optional[Mapping[str, Any]] = None,
        enable_cpu_core_config: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Upgrade Real Device Image.

        Batch real device image upgrade.

        ``POST /vcpcloud/api/padApi/virtualRealSwitch``

        Args:
            pad_codes: (API: ``padCodes``, required)
            image_id: Image ID (API: ``imageId``, required)
            wipe_data: Clear data: true-yes, false-no (API: ``wipeData``, required)
            upgrade_image_convert_type: Convert type: virtual / real (API: ``upgradeImageConvertType``, required)
            real_phone_template_id: Real device template ID (required for real) (API: ``realPhoneTemplateId``)
            screen_layout_id: Screen layout ID (required for virtual) (API: ``screenLayoutId``)
            certificate: Custom root certificate (API: ``certificate``)
            device_android_props: Android props (CBS <2.4.4 not support) (API: ``deviceAndroidProps``)
            enable_cpu_core_config: Enable CPU core config (API: ``enableCpuCoreConfig``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "imageId": image_id, "wipeData": wipe_data, "upgradeImageConvertType": upgrade_image_convert_type, "realPhoneTemplateId": real_phone_template_id, "screenLayoutId": screen_layout_id, "certificate": certificate, "deviceAndroidProps": device_android_props, "enableCpuCoreConfig": enable_cpu_core_config}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/virtualRealSwitch", json_body=payload)

    def template_list(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Paginated Get Real Device Templates.

        Paginated retrieval of real device templates.

        ``POST /vcpcloud/api/padApi/templateList``

        Args:
            page: Page number, default 1 (API: ``page``)
            rows: Number of items per page, default 10, range 1-100 (API: ``rows``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/templateList", json_body=payload)

    def model_info(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Batch Get Instance Device Model Information.

        Batch get device model information for corresponding instances based on instance codes.

        ``POST /vcpcloud/api/padApi/modelInfo``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/modelInfo", json_body=payload)

    def set_speed(
        self,
        pad_codes: Sequence[str],
        up_bandwidth: float,
        down_bandwidth: float,
        **extra: Any,
    ) -> Any:
        """Set Instance Bandwidth.

        Set instance bandwidth based on instance code.

        ``POST /vcpcloud/api/padApi/setSpeed``

        Args:
            pad_codes: (API: ``padCodes``, required)
            up_bandwidth: Upload bandwidth Mbps (0: unlimited; -1: block internet) (API: ``upBandwidth``, required)
            down_bandwidth: Download bandwidth Mbps (0: unlimited; -1: block internet) (API: ``downBandwidth``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "upBandwidth": up_bandwidth, "downBandwidth": down_bandwidth}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/setSpeed", json_body=payload)

    def open_online_adb(
        self,
        pad_codes: Sequence[str],
        open_status: int,
        **extra: Any,
    ) -> Any:
        """Enable/Disable ADB.

        Enable or disable ADB for instance based on instance code.

        ``POST /vcpcloud/api/padApi/openOnlineAdb``

        Args:
            pad_codes: Instance list (1-200 instances) (API: ``padCodes``, required)
            open_status: ADB status (1: enable; 0 or omit: disable) (API: ``openStatus``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "openStatus": open_status}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/openOnlineAdb", json_body=payload)

    def adb(
        self,
        pad_code: str,
        enable: bool,
        *,
        expire_minutes: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get ADB Connection Information.

        Get ADB connection information based on instance code. If response data (key, adb) incomplete, call [Enable/Disable ADB] to enable ADB first.

        ``POST /vcpcloud/api/padApi/adb``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            enable: ADB status: true-enable, false-disable (API: ``enable``, required)
            expire_minutes: ADB validity period in minutes (1–7 days, i.e. 1440–10080), default 1440 (API: ``expireMinutes``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "enable": enable, "expireMinutes": expire_minutes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/adb", json_body=payload)

    def batch_adb(
        self,
        pad_codes: Sequence[str],
        enable: bool,
        **extra: Any,
    ) -> Any:
        """Batch Get ADB Connection Information.

        Batch get or disable ADB connection information based on instance code list. If enable success but connection info incomplete, call [Enable/Disable ADB] to re-enable first. Max 10 instances per call.

        ``POST /vcpcloud/api/padApi/batch/adb``

        Args:
            pad_codes: Instance code list (max 10) (API: ``padCodes``, required)
            enable: Enable ADB: true-enable and return info, false-disable (API: ``enable``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "enable": enable}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/batch/adb", json_body=payload)

    def confirm_transfer(
        self,
        pad_codes: Sequence[str],
        make_over_mobile_phone: str,
        **extra: Any,
    ) -> Any:
        """Transfer Cloud Phone.

        Transfer specified cloud phone instances to another account (via the recipient account's email).

        ``POST /vcpcloud/api/padApi/confirmTransfer``

        Args:
            pad_codes: List of instance codes to transfer (API: ``padCodes``, required)
            make_over_mobile_phone: Recipient account email (API: ``makeOverMobilePhone``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "makeOverMobilePhone": make_over_mobile_phone}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/confirmTransfer", json_body=payload)

    def execute_script_info(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Get Instance Script Execution Result.

        Get script execution result for instance via script task ID.

        ``POST /vcpcloud/api/padApi/executeScriptInfo``

        Args:
            task_ids: Array length 1-100 (API: ``taskIds``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/executeScriptInfo", json_body=payload)

    def screenshot_info(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Get Instance Screenshot Result.

        Get instance screenshot result via screenshot task ID.

        ``POST /vcpcloud/api/padApi/screenshotInfo``

        Args:
            task_ids: (API: ``taskIds``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/screenshotInfo", json_body=payload)

    def infos(
        self,
        page: int,
        rows: int,
        *,
        pad_type: Optional[str] = None,
        pad_codes: Optional[Sequence[str]] = None,
        **extra: Any,
    ) -> Any:
        """Instance List Information.

        Paginated get instance list information based on query conditions.

        ``POST /vcpcloud/api/padApi/infos``

        Args:
            page: Page number (API: ``page``, required)
            rows: Records per page (API: ``rows``, required)
            pad_type: Instance type (virtual: virtual; real: real) (API: ``padType``)
            pad_codes: (API: ``padCodes``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows, "padType": pad_type, "padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/infos", json_body=payload)

    def add_phone_record(
        self,
        pad_codes: Sequence[str],
        call_records: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Import Call Logs.

        This interface imports call log data into cloud phone. During import, it automatically detects saved contacts and displays corresponding names in call logs for quick identification.

        ``POST /vcpcloud/api/padApi/addPhoneRecord``

        Args:
            pad_codes: Instances to edit call logs (API: ``padCodes``, required)
            call_records: Call logs (API: ``callRecords``, required) Nested fields: ``number``, ``inputType``, ``duration``, ``timeString``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "callRecords": call_records}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/addPhoneRecord", json_body=payload)

    def input_text(
        self,
        pad_codes: Sequence[str],
        text: str,
        **extra: Any,
    ) -> Any:
        """Cloud Phone Text Input.

        Focus input box in cloud phone first, call this interface with text to display at specified position.

        ``POST /vcpcloud/api/padApi/inputText``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            text: Input text (API: ``text``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "text": text}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/inputText", json_body=payload)

    def simulate_send_sms(
        self,
        pad_codes: Sequence[str],
        sender_number: str,
        sms_content: str,
        **extra: Any,
    ) -> Any:
        """Simulate Send SMS.

        Simulate sending SMS to instance (supports batch). Limited to AOSP13/14.

        ``POST /vcpcloud/api/padApi/simulateSendSms``

        Args:
            pad_codes: Instance list (1-100) (API: ``padCodes``, required)
            sender_number: Sender number (no mainland; max 16 chars, digits/letters/space/+-) (API: ``senderNumber``, required)
            sms_content: SMS content (max 127 chars) (API: ``smsContent``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "senderNumber": sender_number, "smsContent": sms_content}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/simulateSendSms", json_body=payload)

    def reset_gaid(
        self,
        pad_codes: Sequence[str],
        reset_gms_type: str,
        task_source: str,
        *,
        opr_by: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Reset GAID.

        Reset advertising ID (GAID) in cloud phone via instance code or group.

        ``POST /vcpcloud/api/padApi/resetGAID``

        Args:
            pad_codes: (API: ``padCodes``, required)
            reset_gms_type: Reset type: GAID (API: ``resetGmsType``, required)
            task_source: Task source: OPEN_PLATFORM (API: ``taskSource``, required)
            opr_by: Operator (API: ``oprBy``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "resetGmsType": reset_gms_type, "taskSource": task_source, "oprBy": opr_by}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/resetGAID", json_body=payload)

    def inject_audio_to_mic(
        self,
        pad_codes: Sequence[str],
        enable: bool,
        *,
        url: Optional[str] = None,
        file_unique_id: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Inject Audio to Instance Microphone.

        Inject audio file to instance microphone (PCM format only; convert first).

        ``POST /vcpcloud/api/padApi/injectAudioToMic``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            enable: Inject switch (API: ``enable``, required)
            url: Audio download URL (one of url/fileUniqueId) (API: ``url``)
            file_unique_id: File unique ID (one of url/fileUniqueId) (API: ``fileUniqueId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "enable": enable, "url": url, "fileUniqueId": file_unique_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/injectAudioToMic", json_body=payload)

    def clean_app_home(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Clear Processes and Return to Desktop.

        Clear all processes except system and return to desktop.

        ``POST /vcpcloud/api/padApi/cleanAppHome``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/cleanAppHome", json_body=payload)

    def unmanned_live(
        self,
        pad_codes: Sequence[str],
        *,
        inject_switch: Optional[bool] = None,
        inject_loop: Optional[bool] = None,
        inject_url: Optional[str] = None,
        inject_urls: Optional[Sequence[str]] = None,
        **extra: Any,
    ) -> Any:
        """Unmanned Live Streaming.

        Instance video injection (only img-25092692759 image supported currently). Use injectUrl or injectUrls (at least one, not both; max 5 for injectUrls).

        ``POST /vcpcloud/api/padApi/unmannedLive``

        Args:
            pad_codes: Instances (1-100) (API: ``padCodes``, required)
            inject_switch: Enable injection (true: on; false: off; default false) (API: ``injectSwitch``)
            inject_loop: Loop playback (default false) (API: ``injectLoop``)
            inject_url: Single video URL (http/https/rtmp:// or local; one with injectUrls) (API: ``injectUrl``)
            inject_urls: Video URL list (max 5; one with injectUrl) (API: ``injectUrls``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "injectSwitch": inject_switch, "injectLoop": inject_loop, "injectUrl": inject_url, "injectUrls": inject_urls}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/unmannedLive", json_body=payload)

    def inject_picture(
        self,
        pad_codes: Sequence[str],
        inject_url: str,
        *,
        inject_switch: Optional[bool] = None,
        inject_loop: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Image Injection.

        Instance image injection.

        ``POST /vcpcloud/api/padApi/injectPicture``

        Args:
            pad_codes: Instances (1-100) (API: ``padCodes``, required)
            inject_url: Image URL (http/https/rtmp://) (API: ``injectUrl``, required)
            inject_switch: Enable (true: on; false: off; default false) (API: ``injectSwitch``)
            inject_loop: Loop (default false) (API: ``injectLoop``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "injectUrl": inject_url, "injectSwitch": inject_switch, "injectLoop": inject_loop}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/injectPicture", json_body=payload)


class AsyncInstanceAPI(AsyncAPIResource):
    """Async variant of :class:`InstanceAPI`."""

    async def set_wifi_list(
        self,
        pad_codes: Sequence[str],
        wifi_json_list: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Modify Instance WIFI Properties.

        Modify the WIFI list properties of the specified instance (this interface and one-key new device WIFI setup are mutually exclusive, otherwise overwriting issues may occur)

        ``POST /vcpcloud/api/padApi/setWifiList``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            wifi_json_list: WIFI properties list (API: ``wifiJsonList``, required) Nested fields: ``SSID``, ``BSSID``, ``MAC``, ``IP``, ``gateway``, ``DNS1``, ``DNS2``, ``hessid``, ``anqpDomainId``, ``capabilities``, ``level``, ``linkSpeed``, ``txLinkSpeed``, ``rxLinkSpeed``, ``frequency``, ``distance``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "wifiJsonList": wifi_json_list}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/setWifiList", json_body=payload)

    async def pad_detail(
        self,
        *,
        last_id: Optional[int] = None,
        rows: Optional[int] = None,
        pad_codes: Optional[Sequence[str]] = None,
        pad_ips: Optional[Sequence[str]] = None,
        online: Optional[int] = None,
        pad_status: Optional[int] = None,
        compute_occupied: Optional[bool] = None,
        net_storage_res_flag: Optional[int] = None,
        brand: Optional[str] = None,
        brand_model: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Query Cloud Phone Base Info List.

        Support paginated query of cloud phone base information including running status, online status, compute occupation, etc.

        ``POST /vcpcloud/api/padApi/padDetail``

        Args:
            last_id: Last query returned lastId; null for first query (API: ``lastId``)
            rows: Records per page, max 1000 per page (API: ``rows``)
            pad_codes: (API: ``padCodes``)
            pad_ips: (API: ``padIps``)
            online: Instance online status: 0-offline, 1-online (API: ``online``)
            pad_status: Instance running status: 14-abnormal, others-normal (API: ``padStatus``)
            compute_occupied: Filter compute occupation: true-occupied, false-not occupied (API: ``computeOccupied``)
            net_storage_res_flag: Net storage flag: 1-net storage instance, 0-local instance (API: ``netStorageResFlag``)
            brand: Instance brand (exact match) (API: ``brand``)
            brand_model: Brand model (exact match) (API: ``brandModel``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"lastId": last_id, "rows": rows, "padCodes": pad_codes, "padIps": pad_ips, "online": online, "padStatus": pad_status, "computeOccupied": compute_occupied, "netStorageResFlag": net_storage_res_flag, "brand": brand, "brandModel": brand_model}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/padDetail", json_body=payload)

    async def restart(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Instance Restart.

        Perform restart operation on the specified instance to resolve issues like system unresponsiveness or freezing.

        ``POST /vcpcloud/api/padApi/restart``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/restart", json_body=payload)

    async def reset(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Instance Reset.

        ``POST /vcpcloud/api/padApi/reset``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/reset", json_body=payload)

    async def pad_properties(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Query Instance Properties.

        Query the property information of the specified instance, including system properties and settings.

        ``POST /vcpcloud/api/padApi/padProperties``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/padProperties", json_body=payload)

    async def batch_pad_properties(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Batch Query Instance Properties.

        Batch query the property information of specified instances, including system properties and settings.

        ``POST /vcpcloud/api/padApi/batchPadProperties``

        Args:
            pad_codes: Instance count not exceeding 200 (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/batchPadProperties", json_body=payload)

    async def update_pad_properties(
        self,
        pad_codes: Sequence[str],
        *,
        modem_persist_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        modem_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        system_persist_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        system_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        setting_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        oaid_properties_list: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Modify Instance Properties.

        Dynamically modify instance properties, including system and settings. Instance must be powered on; this interface takes effect immediately. Refer to [Instance Properties List](https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/InstanceList.html#modem-properties-%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8)

        ``POST /vcpcloud/api/padApi/updatePadProperties``

        Args:
            pad_codes: (API: ``padCodes``, required)
            modem_persist_properties_list: Modem persistent properties list (API: ``modemPersistPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            modem_properties_list: Modem non-persistent properties list (API: ``modemPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            system_persist_properties_list: System persistent properties list (API: ``systemPersistPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            system_properties_list: System non-persistent properties list (API: ``systemPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            setting_properties_list: Setting properties list (API: ``settingPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            oaid_properties_list: OAID properties list (API: ``oaidPropertiesList``) Nested fields: ``propertiesName``, ``propertiesValue``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "modemPersistPropertiesList": modem_persist_properties_list, "modemPropertiesList": modem_properties_list, "systemPersistPropertiesList": system_persist_properties_list, "systemPropertiesList": system_properties_list, "settingPropertiesList": setting_properties_list, "oaidPropertiesList": oaid_properties_list}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/updatePadProperties", json_body=payload)

    async def update_pad_android_prop(
        self,
        props: Mapping[str, Any],
        *,
        pad_code: Optional[str] = None,
        restart: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Modify Instance Android Modification Properties.

        ``POST /vcpcloud/api/padApi/updatePadAndroidProp``

        Args:
            props: System properties (key-value) (API: ``props``, required) Nested fields: ``ro.product.vendor.name``.
            pad_code: Instance ID (API: ``padCode``)
            restart: Auto restart after setting (default false) (API: ``restart``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"props": props, "padCode": pad_code, "restart": restart}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/updatePadAndroidProp", json_body=payload)

    async def get_update_sim_task_status(
        self,
        task_id: str,
        **extra: Any,
    ) -> Any:
        """Query SIM Modification Task Status.

        Query the execution status of a task by the taskId returned from [Modify SIM Card Information Based on Country Code](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#modify-sim-card-information-based-on-country-code). Only tasks created by the current account can be queried.

        ``POST /vcpcloud/api/padApi/getUpdateSIMTaskStatus``

        Args:
            task_id: Task ID returned by updateSIM (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/getUpdateSIMTaskStatus", json_body=payload)

    async def dissolve_room(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Stop Streaming.

        Stop streaming for specified instance, disconnect connection.

        ``POST /vcpcloud/api/padApi/dissolveRoom``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/dissolveRoom", json_body=payload)

    async def check_ip(
        self,
        host: str,
        port: int,
        account: str,
        password: str,
        type: str,
        *,
        country: Optional[str] = None,
        ip: Optional[str] = None,
        loc: Optional[str] = None,
        city: Optional[str] = None,
        region: Optional[str] = None,
        timezone: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Smart IP Proxy Detection.

        Detect if proxy IP is available and if location information is correct.

        ``POST /vcpcloud/api/padApi/checkIP``

        Args:
            host: Proxy info (IP or host) (API: ``host``, required)
            port: Proxy port (numeric) (API: ``port``, required)
            account: Proxy username (API: ``account``, required)
            password: Proxy password (API: ``password``, required)
            type: Proxy protocol: Socks5, http, https (API: ``type``, required)
            country: Country - required when forcing specification (API: ``country``)
            ip: IP - required when forcing (API: ``ip``)
            loc: Latitude, longitude - required when forcing (API: ``loc``)
            city: City - required when forcing (API: ``city``)
            region: Region - required when forcing (API: ``region``)
            timezone: Timezone - required when forcing (API: ``timezone``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"host": host, "port": port, "account": account, "password": password, "type": type, "country": country, "ip": ip, "loc": loc, "city": city, "region": region, "timezone": timezone}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/checkIP", json_body=payload)

    async def smart_ip(
        self,
        pad_codes: Sequence[str],
        host: str,
        port: int,
        account: str,
        password: str,
        type: str,
        mode: str,
        *,
        bypass_package_list: Optional[Sequence[Any]] = None,
        bypass_ip_list: Optional[Sequence[Any]] = None,
        bypass_domain_list: Optional[Sequence[Any]] = None,
        follow_language: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Set Smart IP.

        ``POST /vcpcloud/api/padApi/smartIp``

        Args:
            pad_codes: (API: ``padCodes``, required)
            host: Proxy info (IP or host) (API: ``host``, required)
            port: Proxy port (API: ``port``, required)
            account: Proxy username (API: ``account``, required)
            password: Proxy password (API: ``password``, required)
            type: Proxy protocol: socks5, http, https (API: ``type``, required)
            mode: Proxy mode: vpn / proxy (API: ``mode``, required)
            bypass_package_list: Bypass packages (API: ``bypassPackageList``)
            bypass_ip_list: Bypass IPs (API: ``bypassIpList``)
            bypass_domain_list: Bypass domains (API: ``bypassDomainList``)
            follow_language: Whether device language follows the proxy IP (API: ``followLanguage``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "host": host, "port": port, "account": account, "password": password, "type": type, "mode": mode, "bypassPackageList": bypass_package_list, "bypassIpList": bypass_ip_list, "bypassDomainList": bypass_domain_list, "followLanguage": follow_language}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/smartIp", json_body=payload)

    async def not_smart_ip(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Cancel Smart IP.

        Cancel smart IP, restore exit IP, SIM info, GPS, timezone (device restarts, takes effect within 1 minute; status 119-initializing; returns to 100-normal on success/failure/timeout; timeout 5 minutes).

        ``POST /vcpcloud/api/padApi/notSmartIp``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/notSmartIp", json_body=payload)

    async def get_list_installed_app(
        self,
        pad_code_list: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Get All Installed Apps in Specified Cloud Instance List.

        ``POST /vcpcloud/api/padApi/getListInstalledApp``

        Args:
            pad_code_list: (API: ``padCodeList``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodeList": pad_code_list}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/getListInstalledApp", json_body=payload)

    async def update_time_zone(
        self,
        time_zone: str,
        pad_codes: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Modify Instance Timezone.

        ``POST /vcpcloud/api/padApi/updateTimeZone``

        Args:
            time_zone: UTC standard timezone (API: ``timeZone``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"timeZone": time_zone, "padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/updateTimeZone", json_body=payload)

    async def update_language(
        self,
        language: str,
        pad_codes: Sequence[Any],
        *,
        country: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Modify Instance Language.

        ``POST /vcpcloud/api/padApi/updateLanguage``

        Args:
            language: Language (API: ``language``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            country: Country (API: ``country``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"language": language, "padCodes": pad_codes, "country": country}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/updateLanguage", json_body=payload)

    async def gps_inject_info(
        self,
        longitude: float,
        latitude: float,
        pad_codes: Sequence[Any],
        *,
        altitude: Optional[float] = None,
        speed: Optional[float] = None,
        bearing: Optional[float] = None,
        horizontal_accuracy_meters: Optional[float] = None,
        **extra: Any,
    ) -> Any:
        """Set Instance Latitude and Longitude.

        ``POST /vcpcloud/api/padApi/gpsInjectInfo``

        Args:
            longitude: Longitude (API: ``longitude``, required)
            latitude: Latitude (API: ``latitude``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            altitude: Altitude (requires latest image) (API: ``altitude``)
            speed: Speed m/s (images after 20251024) (API: ``speed``)
            bearing: Bearing ° (images after 20251024) (API: ``bearing``)
            horizontal_accuracy_meters: Horizontal accuracy (images after 20251024) (API: ``horizontalAccuracyMeters``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"longitude": longitude, "latitude": latitude, "padCodes": pad_codes, "altitude": altitude, "speed": speed, "bearing": bearing, "horizontalAccuracyMeters": horizontal_accuracy_meters}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/gpsInjectInfo", json_body=payload)

    async def info(
        self,
        pad_codes: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Query Instance Proxy Information.

        ``POST /vcpcloud/open/network/proxy/info``

        Args:
            pad_codes: Instance list (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/open/network/proxy/info", json_body=payload)

    async def replace_pad(
        self,
        pad_codes: Sequence[Any],
        *,
        country_code: Optional[str] = None,
        real_phone_template_id: Optional[int] = None,
        android_prop: Optional[Mapping[str, Any]] = None,
        replacement_real_adi_flag: Optional[bool] = None,
        exclude_real_phone_template_ids: Optional[Sequence[Any]] = None,
        certificate: Optional[str] = None,
        wipe_data: Optional[bool] = None,
        wipe_specific_data: Optional[Sequence[str]] = None,
        keep_specific_data: Optional[Sequence[str]] = None,
        enable_cpu_core_config: Optional[bool] = None,
        webview_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """One-Key New Device** ⭐.

        * Virtual machine: directly set Android properties, clear all data * Cloud real device: clear all data (equivalent to reset), add SIM info; if template ID provided, replace ADI template. If no template and replacementRealAdiFlag true, randomly select template. * Note: If no country info or unsupported, default Singapore SIM. * Unsupported country returns 500 error: Currently not supporting country code XX * Path Format Conversion Rules: /data/system/... -> /system/... /data/misc/... -> /misc/..…

        ``POST /vcpcloud/api/padApi/replacePad``

        Args:
            pad_codes: Instance ID list (API: ``padCodes``, required)
            country_code: Country code (see: https://chahuo.com/country-code-lookup.html) (API: ``countryCode``)
            real_phone_template_id: Template ID (refer to [Paginated Get Real Device Templates]) (API: ``realPhoneTemplateId``)
            android_prop: Refer to [Android Modification Properties List] (API: ``androidProp``)
            replacement_real_adi_flag: Whether random ADI template for real device (false-no, true-yes) (API: ``replacementRealAdiFlag``)
            exclude_real_phone_template_ids: Exclude template IDs when random (API: ``excludeRealPhoneTemplateIds``)
            certificate: Phone root certificate (API: ``certificate``)
            wipe_data: Clear user data (default true, CBS2.4.4+ support) (API: ``wipeData``)
            wipe_specific_data: Effective when wipeData false; specify data to clear (API: ``wipeSpecificData``)
            keep_specific_data: Effective when wipeData is false; specifies which data should be preserved (mutually exclusive with wipeSpecificData) (API: ``keepSpecificData``)
            enable_cpu_core_config: Enable CPU core config (based on Android cpuset for performance stability) (API: ``enableCpuCoreConfig``)
            webview_id: WebView version ID, see [Query Available WebView Versions](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#query-available-webview-versions) (API: ``webviewId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "countryCode": country_code, "realPhoneTemplateId": real_phone_template_id, "androidProp": android_prop, "replacementRealAdiFlag": replacement_real_adi_flag, "excludeRealPhoneTemplateIds": exclude_real_phone_template_ids, "certificate": certificate, "wipeData": wipe_data, "wipeSpecificData": wipe_specific_data, "keepSpecificData": keep_specific_data, "enableCpuCoreConfig": enable_cpu_core_config, "webviewId": webview_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/replacePad", json_body=payload)

    async def pad_replace_new(
        self,
        pad_codes: Sequence[str],
        set_proxy_flag: bool,
        *,
        wipe_data: Optional[bool] = None,
        keep_lang_timezone: Optional[bool] = None,
        android_prop: Optional[Mapping[str, Any]] = None,
        webview_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """One-Key New Device (Auto SIM/GPS/Timezone)** ⭐.

        ``POST /vcpcloud/api/padApi/padReplaceNew``

        Args:
            pad_codes: Instance codes (does not support `ACN` prefix) (API: ``padCodes``, required)
            set_proxy_flag: Set to `true` to write SIM based on deployment location (API: ``setProxyFlag``, required)
            wipe_data: Whether to clear data; default `true` (API: ``wipeData``)
            keep_lang_timezone: Whether to keep old language/timezone; default `false` (API: ``keepLangTimezone``)
            android_prop: Custom Android system properties as key-value pairs. Examples: `persist.sys.locale`, `persist.sys.timezone`, etc. Higher priority than auto-generated properties (API: ``androidProp``)
            webview_id: WebView version ID, see [Query Available WebView Versions](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#query-available-webview-versions) (API: ``webviewId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "setProxyFlag": set_proxy_flag, "wipeData": wipe_data, "keepLangTimezone": keep_lang_timezone, "androidProp": android_prop, "webviewId": webview_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/padReplaceNew", json_body=payload)

    async def country(
        self,
        **extra: Any,
    ) -> Any:
        """Query One-Key New Device Supported Countries List.

        ``GET /vcpcloud/api/padApi/country``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("GET", "/vcpcloud/api/padApi/country", query=payload)

    async def webview_version_list(
        self,
        **extra: Any,
    ) -> Any:
        """Query Available WebView Versions.

        ``POST /vcpcloud/api/padApi/webview/version/list``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/webview/version/list", json_body=payload)

    async def replacement(
        self,
        pad_code: str,
        **extra: Any,
    ) -> Any:
        """Device Replacement.

        ``POST /vcpcloud/api/padApi/replacement``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/replacement", json_body=payload)

    async def get_long_generate_url(
        self,
        pad_codes: Sequence[Any],
        *,
        format: Optional[str] = None,
        height: Optional[str] = None,
        width: Optional[str] = None,
        quality: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get Instance Real-Time Preview Image.

        Get current screen screenshot for specified instance. Returns URL and expiration; access URL for real-time screenshot. Supports batch.

        ``POST /vcpcloud/api/padApi/getLongGenerateUrl``

        Args:
            pad_codes: Instance list (API: ``padCodes``, required)
            format: Image format: png, jpg (default png; png no compression) (API: ``format``)
            height: Scaled height (pixels; default original) (API: ``height``)
            width: Scaled width (pixels; default original) (API: ``width``)
            quality: Image quality (0-100; default 50%; below 60 blurry) (API: ``quality``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "format": format, "height": height, "width": width, "quality": quality}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/getLongGenerateUrl", json_body=payload)

    async def set_proxy(
        self,
        enable: bool,
        pad_codes: Sequence[Any],
        *,
        account: Optional[str] = None,
        password: Optional[str] = None,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        proxy_type: Optional[str] = None,
        proxy_name: Optional[str] = None,
        model: Optional[str] = None,
        bypass_package_list: Optional[Sequence[Any]] = None,
        bypass_ip_list: Optional[Sequence[Any]] = None,
        bypass_domain_list: Optional[Sequence[Any]] = None,
        limit_package_list: Optional[Sequence[Any]] = None,
        limit_ip_list: Optional[Sequence[Any]] = None,
        limit_domain_list: Optional[Sequence[Any]] = None,
        s_uo_t: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Instance Set Proxy.

        ``POST /vcpcloud/api/padApi/setProxy``

        Args:
            enable: Enable (API: ``enable``, required)
            pad_codes: Instance list (API: ``padCodes``, required)
            account: Username (API: ``account``)
            password: Password (API: ``password``)
            ip: IP (API: ``ip``)
            port: Port (API: ``port``)
            proxy_type: Supported: proxy, vpn (API: ``proxyType``)
            proxy_name: Supported: socks5, http-relay (includes http/https) (API: ``proxyName``)
            model: List mode: bypass(default)/limit (API: ``model``)
            bypass_package_list: Packages bypassing proxy (model=bypass) (API: ``bypassPackageList``)
            bypass_ip_list: IPs bypassing proxy (model=bypass) (API: ``bypassIpList``)
            bypass_domain_list: Domains bypassing proxy (model=bypass) (API: ``bypassDomainList``)
            limit_package_list: Only these packages use proxy (model=limit) (API: ``limitPackageList``)
            limit_ip_list: Only these IPs use proxy (model=limit) (API: ``limitIpList``)
            limit_domain_list: Only these domains use proxy (model=limit) (API: ``limitDomainList``)
            s_uo_t: Enable UDP (default false) (API: ``sUoT``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"enable": enable, "padCodes": pad_codes, "account": account, "password": password, "ip": ip, "port": port, "proxyType": proxy_type, "proxyName": proxy_name, "model": model, "bypassPackageList": bypass_package_list, "bypassIpList": bypass_ip_list, "bypassDomainList": bypass_domain_list, "limitPackageList": limit_package_list, "limitIpList": limit_ip_list, "limitDomainList": limit_domain_list, "sUoT": s_uo_t}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/setProxy", json_body=payload)

    async def async_cmd(
        self,
        pad_codes: Sequence[str],
        script_content: str,
        **extra: Any,
    ) -> Any:
        """Async Execute ADB Commands.

        Async execute commands in one or more cloud instances.

        ``POST /vcpcloud/api/padApi/asyncCmd``

        Args:
            pad_codes: (API: ``padCodes``, required)
            script_content: ADB commands (multiple separated by “;” ) (API: ``scriptContent``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "scriptContent": script_content}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/asyncCmd", json_body=payload)

    async def switch_root(
        self,
        pad_codes: Sequence[str],
        root_status: int,
        *,
        global_root: Optional[bool] = None,
        package_name: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Switch Root Permissions.

        Switch root permissions in one or more cloud instances. For single app root, specify package name (cloud real device: not recommended global root due to detection risk).

        ``POST /vcpcloud/api/padApi/switchRoot``

        Args:
            pad_codes: (API: ``padCodes``, required)
            root_status: Root status: 0-off, 1-on (API: ``rootStatus``, required)
            global_root: Global root (default no) (API: ``globalRoot``)
            package_name: Package name (required for non-global; multiple comma separated) (API: ``packageName``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "rootStatus": root_status, "globalRoot": global_root, "packageName": package_name}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/switchRoot", json_body=payload)

    async def screenshot(
        self,
        pad_codes: Sequence[str],
        rotation: int,
        *,
        broadcast: Optional[bool] = None,
        definition: Optional[int] = None,
        resolution_height: Optional[int] = None,
        resolution_width: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Local Screenshot.

        Instance screenshot.

        ``POST /vcpcloud/api/padApi/screenshot``

        Args:
            pad_codes: (API: ``padCodes``, required)
            rotation: Screenshot orientation: 0-default, 1-rotate to portrait (API: ``rotation``, required)
            broadcast: Broadcast event (default false) (API: ``broadcast``)
            definition: Clarity 0-100 (API: ``definition``)
            resolution_height: Height >1 (API: ``resolutionHeight``)
            resolution_width: Width >1 (API: ``resolutionWidth``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "rotation": rotation, "broadcast": broadcast, "definition": definition, "resolutionHeight": resolution_height, "resolutionWidth": resolution_width}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/screenshot", json_body=payload)

    async def generate_preview(
        self,
        pad_codes: Sequence[str],
        rotation: int,
        *,
        broadcast: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Generate Preview Image.

        Get preview image for specified instance.

        ``POST /vcpcloud/api/padApi/generatePreview``

        Args:
            pad_codes: (API: ``padCodes``, required)
            rotation: Screenshot orientation: 0-default, 1-rotate to portrait (API: ``rotation``, required)
            broadcast: Broadcast event (default false) (API: ``broadcast``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "rotation": rotation, "broadcast": broadcast}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/generatePreview", json_body=payload)

    async def upgrade_image(
        self,
        pad_codes: Sequence[str],
        image_id: str,
        wipe_data: bool,
        *,
        enable_cpu_core_config: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Upgrade Image.

        Batch instance image upgrade.

        ``POST /vcpcloud/api/padApi/upgradeImage``

        Args:
            pad_codes: (API: ``padCodes``, required)
            image_id: Image ID (API: ``imageId``, required)
            wipe_data: Clear data partition: true-yes, false-no (API: ``wipeData``, required)
            enable_cpu_core_config: Enable CPU core config (API: ``enableCpuCoreConfig``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "imageId": image_id, "wipeData": wipe_data, "enableCpuCoreConfig": enable_cpu_core_config}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/upgradeImage", json_body=payload)

    async def set_hide_accessibility_app_list(
        self,
        pad_codes: Sequence[str],
        app_infos: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Hide Accessibility Service.

        1. The specified app itself can still detect that it has enabled accessibility service. 2. Third-party apps cannot detect that the specified app has enabled accessibility service. 3. The specified app will not appear in the accessibility service list.

        ``POST /vcpcloud/api/padApi/setHideAccessibilityAppList``

        Args:
            pad_codes: Array of instance codes (maximum 200) (API: ``padCodes``, required)
            app_infos: Array of hidden app list objects; pass empty array [] to clear (0–200 items) (API: ``appInfos``, required) Nested fields: ``packageName``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "appInfos": app_infos}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/setHideAccessibilityAppList", json_body=payload)

    async def virtual_real_switch(
        self,
        pad_codes: Sequence[str],
        image_id: str,
        wipe_data: bool,
        upgrade_image_convert_type: str,
        *,
        real_phone_template_id: Optional[int] = None,
        screen_layout_id: Optional[int] = None,
        certificate: Optional[str] = None,
        device_android_props: Optional[Mapping[str, Any]] = None,
        enable_cpu_core_config: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Upgrade Real Device Image.

        Batch real device image upgrade.

        ``POST /vcpcloud/api/padApi/virtualRealSwitch``

        Args:
            pad_codes: (API: ``padCodes``, required)
            image_id: Image ID (API: ``imageId``, required)
            wipe_data: Clear data: true-yes, false-no (API: ``wipeData``, required)
            upgrade_image_convert_type: Convert type: virtual / real (API: ``upgradeImageConvertType``, required)
            real_phone_template_id: Real device template ID (required for real) (API: ``realPhoneTemplateId``)
            screen_layout_id: Screen layout ID (required for virtual) (API: ``screenLayoutId``)
            certificate: Custom root certificate (API: ``certificate``)
            device_android_props: Android props (CBS <2.4.4 not support) (API: ``deviceAndroidProps``)
            enable_cpu_core_config: Enable CPU core config (API: ``enableCpuCoreConfig``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "imageId": image_id, "wipeData": wipe_data, "upgradeImageConvertType": upgrade_image_convert_type, "realPhoneTemplateId": real_phone_template_id, "screenLayoutId": screen_layout_id, "certificate": certificate, "deviceAndroidProps": device_android_props, "enableCpuCoreConfig": enable_cpu_core_config}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/virtualRealSwitch", json_body=payload)

    async def template_list(
        self,
        *,
        page: Optional[int] = None,
        rows: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Paginated Get Real Device Templates.

        Paginated retrieval of real device templates.

        ``POST /vcpcloud/api/padApi/templateList``

        Args:
            page: Page number, default 1 (API: ``page``)
            rows: Number of items per page, default 10, range 1-100 (API: ``rows``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/templateList", json_body=payload)

    async def model_info(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Batch Get Instance Device Model Information.

        Batch get device model information for corresponding instances based on instance codes.

        ``POST /vcpcloud/api/padApi/modelInfo``

        Args:
            pad_codes: (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/modelInfo", json_body=payload)

    async def set_speed(
        self,
        pad_codes: Sequence[str],
        up_bandwidth: float,
        down_bandwidth: float,
        **extra: Any,
    ) -> Any:
        """Set Instance Bandwidth.

        Set instance bandwidth based on instance code.

        ``POST /vcpcloud/api/padApi/setSpeed``

        Args:
            pad_codes: (API: ``padCodes``, required)
            up_bandwidth: Upload bandwidth Mbps (0: unlimited; -1: block internet) (API: ``upBandwidth``, required)
            down_bandwidth: Download bandwidth Mbps (0: unlimited; -1: block internet) (API: ``downBandwidth``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "upBandwidth": up_bandwidth, "downBandwidth": down_bandwidth}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/setSpeed", json_body=payload)

    async def open_online_adb(
        self,
        pad_codes: Sequence[str],
        open_status: int,
        **extra: Any,
    ) -> Any:
        """Enable/Disable ADB.

        Enable or disable ADB for instance based on instance code.

        ``POST /vcpcloud/api/padApi/openOnlineAdb``

        Args:
            pad_codes: Instance list (1-200 instances) (API: ``padCodes``, required)
            open_status: ADB status (1: enable; 0 or omit: disable) (API: ``openStatus``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "openStatus": open_status}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/openOnlineAdb", json_body=payload)

    async def adb(
        self,
        pad_code: str,
        enable: bool,
        *,
        expire_minutes: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Get ADB Connection Information.

        Get ADB connection information based on instance code. If response data (key, adb) incomplete, call [Enable/Disable ADB] to enable ADB first.

        ``POST /vcpcloud/api/padApi/adb``

        Args:
            pad_code: Instance code (API: ``padCode``, required)
            enable: ADB status: true-enable, false-disable (API: ``enable``, required)
            expire_minutes: ADB validity period in minutes (1–7 days, i.e. 1440–10080), default 1440 (API: ``expireMinutes``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCode": pad_code, "enable": enable, "expireMinutes": expire_minutes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/adb", json_body=payload)

    async def batch_adb(
        self,
        pad_codes: Sequence[str],
        enable: bool,
        **extra: Any,
    ) -> Any:
        """Batch Get ADB Connection Information.

        Batch get or disable ADB connection information based on instance code list. If enable success but connection info incomplete, call [Enable/Disable ADB] to re-enable first. Max 10 instances per call.

        ``POST /vcpcloud/api/padApi/batch/adb``

        Args:
            pad_codes: Instance code list (max 10) (API: ``padCodes``, required)
            enable: Enable ADB: true-enable and return info, false-disable (API: ``enable``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "enable": enable}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/batch/adb", json_body=payload)

    async def confirm_transfer(
        self,
        pad_codes: Sequence[str],
        make_over_mobile_phone: str,
        **extra: Any,
    ) -> Any:
        """Transfer Cloud Phone.

        Transfer specified cloud phone instances to another account (via the recipient account's email).

        ``POST /vcpcloud/api/padApi/confirmTransfer``

        Args:
            pad_codes: List of instance codes to transfer (API: ``padCodes``, required)
            make_over_mobile_phone: Recipient account email (API: ``makeOverMobilePhone``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "makeOverMobilePhone": make_over_mobile_phone}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/confirmTransfer", json_body=payload)

    async def execute_script_info(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Get Instance Script Execution Result.

        Get script execution result for instance via script task ID.

        ``POST /vcpcloud/api/padApi/executeScriptInfo``

        Args:
            task_ids: Array length 1-100 (API: ``taskIds``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/executeScriptInfo", json_body=payload)

    async def screenshot_info(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Get Instance Screenshot Result.

        Get instance screenshot result via screenshot task ID.

        ``POST /vcpcloud/api/padApi/screenshotInfo``

        Args:
            task_ids: (API: ``taskIds``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/screenshotInfo", json_body=payload)

    async def infos(
        self,
        page: int,
        rows: int,
        *,
        pad_type: Optional[str] = None,
        pad_codes: Optional[Sequence[str]] = None,
        **extra: Any,
    ) -> Any:
        """Instance List Information.

        Paginated get instance list information based on query conditions.

        ``POST /vcpcloud/api/padApi/infos``

        Args:
            page: Page number (API: ``page``, required)
            rows: Records per page (API: ``rows``, required)
            pad_type: Instance type (virtual: virtual; real: real) (API: ``padType``)
            pad_codes: (API: ``padCodes``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "rows": rows, "padType": pad_type, "padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/infos", json_body=payload)

    async def add_phone_record(
        self,
        pad_codes: Sequence[str],
        call_records: Sequence[Mapping[str, Any]],
        **extra: Any,
    ) -> Any:
        """Import Call Logs.

        This interface imports call log data into cloud phone. During import, it automatically detects saved contacts and displays corresponding names in call logs for quick identification.

        ``POST /vcpcloud/api/padApi/addPhoneRecord``

        Args:
            pad_codes: Instances to edit call logs (API: ``padCodes``, required)
            call_records: Call logs (API: ``callRecords``, required) Nested fields: ``number``, ``inputType``, ``duration``, ``timeString``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "callRecords": call_records}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/addPhoneRecord", json_body=payload)

    async def input_text(
        self,
        pad_codes: Sequence[str],
        text: str,
        **extra: Any,
    ) -> Any:
        """Cloud Phone Text Input.

        Focus input box in cloud phone first, call this interface with text to display at specified position.

        ``POST /vcpcloud/api/padApi/inputText``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            text: Input text (API: ``text``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "text": text}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/inputText", json_body=payload)

    async def simulate_send_sms(
        self,
        pad_codes: Sequence[str],
        sender_number: str,
        sms_content: str,
        **extra: Any,
    ) -> Any:
        """Simulate Send SMS.

        Simulate sending SMS to instance (supports batch). Limited to AOSP13/14.

        ``POST /vcpcloud/api/padApi/simulateSendSms``

        Args:
            pad_codes: Instance list (1-100) (API: ``padCodes``, required)
            sender_number: Sender number (no mainland; max 16 chars, digits/letters/space/+-) (API: ``senderNumber``, required)
            sms_content: SMS content (max 127 chars) (API: ``smsContent``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "senderNumber": sender_number, "smsContent": sms_content}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/simulateSendSms", json_body=payload)

    async def reset_gaid(
        self,
        pad_codes: Sequence[str],
        reset_gms_type: str,
        task_source: str,
        *,
        opr_by: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Reset GAID.

        Reset advertising ID (GAID) in cloud phone via instance code or group.

        ``POST /vcpcloud/api/padApi/resetGAID``

        Args:
            pad_codes: (API: ``padCodes``, required)
            reset_gms_type: Reset type: GAID (API: ``resetGmsType``, required)
            task_source: Task source: OPEN_PLATFORM (API: ``taskSource``, required)
            opr_by: Operator (API: ``oprBy``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "resetGmsType": reset_gms_type, "taskSource": task_source, "oprBy": opr_by}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/resetGAID", json_body=payload)

    async def inject_audio_to_mic(
        self,
        pad_codes: Sequence[str],
        enable: bool,
        *,
        url: Optional[str] = None,
        file_unique_id: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Inject Audio to Instance Microphone.

        Inject audio file to instance microphone (PCM format only; convert first).

        ``POST /vcpcloud/api/padApi/injectAudioToMic``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            enable: Inject switch (API: ``enable``, required)
            url: Audio download URL (one of url/fileUniqueId) (API: ``url``)
            file_unique_id: File unique ID (one of url/fileUniqueId) (API: ``fileUniqueId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "enable": enable, "url": url, "fileUniqueId": file_unique_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/injectAudioToMic", json_body=payload)

    async def clean_app_home(
        self,
        pad_codes: Sequence[str],
        **extra: Any,
    ) -> Any:
        """Clear Processes and Return to Desktop.

        Clear all processes except system and return to desktop.

        ``POST /vcpcloud/api/padApi/cleanAppHome``

        Args:
            pad_codes: Instance codes (API: ``padCodes``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/cleanAppHome", json_body=payload)

    async def unmanned_live(
        self,
        pad_codes: Sequence[str],
        *,
        inject_switch: Optional[bool] = None,
        inject_loop: Optional[bool] = None,
        inject_url: Optional[str] = None,
        inject_urls: Optional[Sequence[str]] = None,
        **extra: Any,
    ) -> Any:
        """Unmanned Live Streaming.

        Instance video injection (only img-25092692759 image supported currently). Use injectUrl or injectUrls (at least one, not both; max 5 for injectUrls).

        ``POST /vcpcloud/api/padApi/unmannedLive``

        Args:
            pad_codes: Instances (1-100) (API: ``padCodes``, required)
            inject_switch: Enable injection (true: on; false: off; default false) (API: ``injectSwitch``)
            inject_loop: Loop playback (default false) (API: ``injectLoop``)
            inject_url: Single video URL (http/https/rtmp:// or local; one with injectUrls) (API: ``injectUrl``)
            inject_urls: Video URL list (max 5; one with injectUrl) (API: ``injectUrls``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "injectSwitch": inject_switch, "injectLoop": inject_loop, "injectUrl": inject_url, "injectUrls": inject_urls}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/unmannedLive", json_body=payload)

    async def inject_picture(
        self,
        pad_codes: Sequence[str],
        inject_url: str,
        *,
        inject_switch: Optional[bool] = None,
        inject_loop: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Image Injection.

        Instance image injection.

        ``POST /vcpcloud/api/padApi/injectPicture``

        Args:
            pad_codes: Instances (1-100) (API: ``padCodes``, required)
            inject_url: Image URL (http/https/rtmp://) (API: ``injectUrl``, required)
            inject_switch: Enable (true: on; false: off; default false) (API: ``injectSwitch``)
            inject_loop: Loop (default false) (API: ``injectLoop``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "injectUrl": inject_url, "injectSwitch": inject_switch, "injectLoop": inject_loop}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/injectPicture", json_body=payload)
