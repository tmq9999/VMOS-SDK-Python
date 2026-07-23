# `client.instance` — Instance Management

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Restart/reset, properties, SIM/GPS/WiFi, ADB & shell commands, screenshots, previews, image upgrades, one-click new device, root switching, network tools, media injection.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`set_wifi_list`](#set-wifi-list--modify-instance-wifi-properties) | POST | `/vcpcloud/api/padApi/setWifiList` |
| [`pad_detail`](#pad-detail--query-cloud-phone-base-info-list) | POST | `/vcpcloud/api/padApi/padDetail` |
| [`restart`](#restart--instance-restart) | POST | `/vcpcloud/api/padApi/restart` |
| [`reset`](#reset--instance-reset) | POST | `/vcpcloud/api/padApi/reset` |
| [`pad_properties`](#pad-properties--query-instance-properties) | POST | `/vcpcloud/api/padApi/padProperties` |
| [`batch_pad_properties`](#batch-pad-properties--batch-query-instance-properties) | POST | `/vcpcloud/api/padApi/batchPadProperties` |
| [`update_pad_properties`](#update-pad-properties--modify-instance-properties) | POST | `/vcpcloud/api/padApi/updatePadProperties` |
| [`update_pad_android_prop`](#update-pad-android-prop--modify-instance-android-modification-properties) | POST | `/vcpcloud/api/padApi/updatePadAndroidProp` |
| [`get_update_sim_task_status`](#get-update-sim-task-status--query-sim-modification-task-status) | POST | `/vcpcloud/api/padApi/getUpdateSIMTaskStatus` |
| [`dissolve_room`](#dissolve-room--stop-streaming) | POST | `/vcpcloud/api/padApi/dissolveRoom` |
| [`check_ip`](#check-ip--smart-ip-proxy-detection) | POST | `/vcpcloud/api/padApi/checkIP` |
| [`smart_ip`](#smart-ip--set-smart-ip) | POST | `/vcpcloud/api/padApi/smartIp` |
| [`not_smart_ip`](#not-smart-ip--cancel-smart-ip) | POST | `/vcpcloud/api/padApi/notSmartIp` |
| [`get_list_installed_app`](#get-list-installed-app--get-all-installed-apps-in-specified-cloud-instance-list) | POST | `/vcpcloud/api/padApi/getListInstalledApp` |
| [`update_time_zone`](#update-time-zone--modify-instance-timezone) | POST | `/vcpcloud/api/padApi/updateTimeZone` |
| [`update_language`](#update-language--modify-instance-language) | POST | `/vcpcloud/api/padApi/updateLanguage` |
| [`gps_inject_info`](#gps-inject-info--set-instance-latitude-and-longitude) | POST | `/vcpcloud/api/padApi/gpsInjectInfo` |
| [`info`](#info--query-instance-proxy-information) | POST | `/vcpcloud/open/network/proxy/info` |
| [`replace_pad`](#replace-pad--one-key-new-device) | POST | `/vcpcloud/api/padApi/replacePad` |
| [`pad_replace_new`](#pad-replace-new--one-key-new-device-auto-sim-gps-timezone) | POST | `/vcpcloud/api/padApi/padReplaceNew` |
| [`country`](#country--query-one-key-new-device-supported-countries-list) | GET | `/vcpcloud/api/padApi/country` |
| [`webview_version_list`](#webview-version-list--query-available-webview-versions) | POST | `/vcpcloud/api/padApi/webview/version/list` |
| [`replacement`](#replacement--device-replacement) | POST | `/vcpcloud/api/padApi/replacement` |
| [`get_long_generate_url`](#get-long-generate-url--get-instance-real-time-preview-image) | POST | `/vcpcloud/api/padApi/getLongGenerateUrl` |
| [`set_proxy`](#set-proxy--instance-set-proxy) | POST | `/vcpcloud/api/padApi/setProxy` |
| [`async_cmd`](#async-cmd--async-execute-adb-commands) | POST | `/vcpcloud/api/padApi/asyncCmd` |
| [`switch_root`](#switch-root--switch-root-permissions) | POST | `/vcpcloud/api/padApi/switchRoot` |
| [`screenshot`](#screenshot--local-screenshot) | POST | `/vcpcloud/api/padApi/screenshot` |
| [`generate_preview`](#generate-preview--generate-preview-image) | POST | `/vcpcloud/api/padApi/generatePreview` |
| [`upgrade_image`](#upgrade-image--upgrade-image) | POST | `/vcpcloud/api/padApi/upgradeImage` |
| [`set_hide_accessibility_app_list`](#set-hide-accessibility-app-list--hide-accessibility-service) | POST | `/vcpcloud/api/padApi/setHideAccessibilityAppList` |
| [`virtual_real_switch`](#virtual-real-switch--upgrade-real-device-image) | POST | `/vcpcloud/api/padApi/virtualRealSwitch` |
| [`template_list`](#template-list--paginated-get-real-device-templates) | POST | `/vcpcloud/api/padApi/templateList` |
| [`model_info`](#model-info--batch-get-instance-device-model-information) | POST | `/vcpcloud/api/padApi/modelInfo` |
| [`set_speed`](#set-speed--set-instance-bandwidth) | POST | `/vcpcloud/api/padApi/setSpeed` |
| [`open_online_adb`](#open-online-adb--enable-disable-adb) | POST | `/vcpcloud/api/padApi/openOnlineAdb` |
| [`adb`](#adb--get-adb-connection-information) | POST | `/vcpcloud/api/padApi/adb` |
| [`batch_adb`](#batch-adb--batch-get-adb-connection-information) | POST | `/vcpcloud/api/padApi/batch/adb` |
| [`confirm_transfer`](#confirm-transfer--transfer-cloud-phone) | POST | `/vcpcloud/api/padApi/confirmTransfer` |
| [`execute_script_info`](#execute-script-info--get-instance-script-execution-result) | POST | `/vcpcloud/api/padApi/executeScriptInfo` |
| [`screenshot_info`](#screenshot-info--get-instance-screenshot-result) | POST | `/vcpcloud/api/padApi/screenshotInfo` |
| [`infos`](#infos--instance-list-information) | POST | `/vcpcloud/api/padApi/infos` |
| [`add_phone_record`](#add-phone-record--import-call-logs) | POST | `/vcpcloud/api/padApi/addPhoneRecord` |
| [`input_text`](#input-text--cloud-phone-text-input) | POST | `/vcpcloud/api/padApi/inputText` |
| [`simulate_send_sms`](#simulate-send-sms--simulate-send-sms) | POST | `/vcpcloud/api/padApi/simulateSendSms` |
| [`reset_gaid`](#reset-gaid--reset-gaid) | POST | `/vcpcloud/api/padApi/resetGAID` |
| [`inject_audio_to_mic`](#inject-audio-to-mic--inject-audio-to-instance-microphone) | POST | `/vcpcloud/api/padApi/injectAudioToMic` |
| [`clean_app_home`](#clean-app-home--clear-processes-and-return-to-desktop) | POST | `/vcpcloud/api/padApi/cleanAppHome` |
| [`unmanned_live`](#unmanned-live--unmanned-live-streaming) | POST | `/vcpcloud/api/padApi/unmannedLive` |
| [`inject_picture`](#inject-picture--image-injection) | POST | `/vcpcloud/api/padApi/injectPicture` |

[Back to index](README.md)

---

### `set_wifi_list` — Modify Instance WIFI Properties

Modify the WIFI list properties of the specified instance (this interface and one-key new device WIFI setup are mutually exclusive, otherwise overwriting issues may occur)

- **Endpoint**: `POST /vcpcloud/api/padApi/setWifiList`

**Signature**

```python
client.instance.set_wifi_list(pad_codes, wifi_json_list, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance codes |
| `wifi_json_list` | `wifiJsonList` | String[] | yes | WIFI properties list |

**Nested fields of `wifiJsonList`:**

| API name | Type | Description |
|---|---|---|
| `SSID` | String | WIFI name (Chinese not supported) |
| `BSSID` | String | Access point MAC address |
| `MAC` | String | WIFI adapter MAC address |
| `IP` | String | WIFI network IP |
| `gateway` | String | WIFI gateway |
| `DNS1` | String | DNS1 |
| `DNS2` | String | DNS2 |
| `hessid` | Integer | Network identifier |
| `anqpDomainId` | Integer | ANQP (Access Network Query Protocol) domain ID |
| `capabilities` | String | WPA/WPA2 etc. information |
| `level` | Integer | Signal strength (RSSI) |
| `linkSpeed` | Integer | Current Wi-Fi connection speed |
| `txLinkSpeed` | Integer | Upload link speed |
| `rxLinkSpeed` | Integer | Download link speed |
| `frequency` | Integer | Wi-Fi channel frequency |
| `distance` | Integer | Estimated AP distance |
| `distanceSd` | Integer | Estimated distance standard deviation |
| `channelWidth` | Integer | Channel bandwidth |
| `centerFreq0` | Integer | Center frequency 0 |
| `centerFreq1` | Integer | Center frequency 1 |
| `is80211McRTTResponder` | Boolean | Whether supports 802.11mc (Wi-Fi RTT ranging technology) |

**Example** (JSON payload)

```json
{
    "padCodes":["AC2025030770R92X"],
    "wifiJsonList":[
        {
            "SSID": "110101",
            "BSSID": "02:31:00:00:00:01",
            "MAC": "02:00:10:00:00:00",
            "IP": "192.168.120.15",
            "gateway": "192.168.120.1",
            "DNS1": "1.1.1.1",
            "DNS2": "8.8.8.8",
            "hessid": 0,
            "anqpDomainId": 0,
            "capabilities": "",
            "level": 0,
            "linkSpeed": 500,
            "txLinkSpeed": 600,
            "rxLinkSpeed": 700,
            "frequency": 2413,
            "distance": -1,
            "distanceSd": -1,
            "channelWidth": 0,
            "centerFreq0": -1,
            "centerFreq1": -1,
            "is80211McRTTResponder": true
        }
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `pad_detail` — Query Cloud Phone Base Info List

Support paginated query of cloud phone base information including running status, online status, compute occupation, etc.

- **Endpoint**: `POST /vcpcloud/api/padApi/padDetail`

**Signature**

```python
client.instance.pad_detail(*, last_id=None, rows=None, pad_codes=None, pad_ips=None, online=None, pad_status=None, compute_occupied=None, net_storage_res_flag=None, brand=None, brand_model=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `last_id` | `lastId` | Long | no | Last query returned lastId; null for first query |
| `rows` | `rows` | Integer | no | Records per page, max 1000 per page |
| `pad_codes` | `padCodes` | String[] | no |  |
| `pad_ips` | `padIps` | String[] | no |  |
| `online` | `online` | Integer | no | Instance online status: 0-offline, 1-online |
| `pad_status` | `padStatus` | Integer | no | Instance running status: 14-abnormal, others-normal |
| `compute_occupied` | `computeOccupied` | Boolean | no | Filter compute occupation: true-occupied, false-not occupied |
| `net_storage_res_flag` | `netStorageResFlag` | Integer | no | Net storage flag: 1-net storage instance, 0-local instance |
| `brand` | `brand` | String | no | Instance brand (exact match) |
| `brand_model` | `brandModel` | String | no | Brand model (exact match) |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Nested fields of `padIps`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance IP |

**Example** (JSON payload)

```json
{
 "lastId": null,
 "rows": 10,
 "padCodes": ["ACP250331GLXXXXX"],
 "padIps":["192.168.1.1"],
 "online":1,
 "padStatus":10,
 "computeOccupied":true, 
 "netStorageResFlag":1
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `restart` — Instance Restart

Perform restart operation on the specified instance to resolve issues like system unresponsiveness or freezing.

- **Endpoint**: `POST /vcpcloud/api/padApi/restart`

**Signature**

```python
client.instance.restart(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC22030022693"
 ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `reset` — Instance Reset

- **Endpoint**: `POST /vcpcloud/api/padApi/reset`

**Signature**

```python
client.instance.reset(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC21020010001"
 ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `pad_properties` — Query Instance Properties

Query the property information of the specified instance, including system properties and settings.

- **Endpoint**: `POST /vcpcloud/api/padApi/padProperties`

**Signature**

```python
client.instance.pad_properties(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |

**Example** (JSON payload)

```json
{
 "padCode": "AC21020010001"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `batch_pad_properties` — Batch Query Instance Properties

Batch query the property information of specified instances, including system properties and settings.

- **Endpoint**: `POST /vcpcloud/api/padApi/batchPadProperties`

**Signature**

```python
client.instance.batch_pad_properties(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance count not exceeding 200 |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC21020010001",
        "AC21020010002"
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `update_pad_properties` — Modify Instance Properties

Dynamically modify instance properties, including system and settings. Instance must be powered on; this interface takes effect immediately. Refer to [Instance Properties List](https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/InstanceList.html#modem-properties-%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8)

- **Endpoint**: `POST /vcpcloud/api/padApi/updatePadProperties`

**Signature**

```python
client.instance.update_pad_properties(pad_codes, *, modem_persist_properties_list=None, modem_properties_list=None, system_persist_properties_list=None, system_properties_list=None, setting_properties_list=None, oaid_properties_list=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `modem_persist_properties_list` | `modemPersistPropertiesList` | Object[] | no | Modem persistent properties list |
| `modem_properties_list` | `modemPropertiesList` | Object[] | no | Modem non-persistent properties list |
| `system_persist_properties_list` | `systemPersistPropertiesList` | Object[] | no | System persistent properties list |
| `system_properties_list` | `systemPropertiesList` | Object[] | no | System non-persistent properties list |
| `setting_properties_list` | `settingPropertiesList` | Object[] | no | Setting properties list |
| `oaid_properties_list` | `oaidPropertiesList` | Object[] | no | OAID properties list |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Nested fields of `modemPersistPropertiesList`:**

| API name | Type | Description |
|---|---|---|
| `propertiesName` | String | Property name |
| `propertiesValue` | String | Property value |

**Nested fields of `modemPropertiesList`:**

| API name | Type | Description |
|---|---|---|
| `propertiesName` | String | Property name |
| `propertiesValue` | String | Property value |

**Nested fields of `systemPersistPropertiesList`:**

| API name | Type | Description |
|---|---|---|
| `propertiesName` | String | Property name |
| `propertiesValue` | String | Property value |

**Nested fields of `systemPropertiesList`:**

| API name | Type | Description |
|---|---|---|
| `propertiesName` | String | Property name |
| `propertiesValue` | String | Property value |

**Nested fields of `settingPropertiesList`:**

| API name | Type | Description |
|---|---|---|
| `propertiesName` | String | Property name |
| `propertiesValue` | String | Property value |

**Nested fields of `oaidPropertiesList`:**

| API name | Type | Description |
|---|---|---|
| `propertiesName` | String | Property name |
| `propertiesValue` | String | Property value |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC21020010001"
 ],
 "modemPersistPropertiesList": [
   {
    "propertiesName": "IMEI",
    "propertiesValue": "412327621057784"
   }
  ],
 "modemPropertiesList": [
   {
    "propertiesName": "IMEI",
    "propertiesValue": "412327621057784"
   }
  ],
  "systemPersistPropertiesList": [
   {
    "propertiesName": "ro.build.id",
    "propertiesValue": "QQ3A.200805.001"
   }
  ],
  "systemPropertiesList": [
   {
    "propertiesName": "ro.build.id",
    "propertiesValue": "QQ3A.200805.001"
   }
  ],
  "settingPropertiesList": [
   {
    "propertiesName": "ro.build.tags",
    "propertiesValue": "release-keys"
   }
  ],
  "oaidPropertiesList": [
   {
    "propertiesName": "oaid",
    "propertiesValue": "001"
   }
  ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `update_pad_android_prop` — Modify Instance Android Modification Properties

- **Endpoint**: `POST /vcpcloud/api/padApi/updatePadAndroidProp`

**Signature**

```python
client.instance.update_pad_android_prop(props, *, pad_code=None, restart=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | no | Instance ID |
| `restart` | `restart` | Boolean | no | Auto restart after setting (default false) |
| `props` | `props` | Object | yes | System properties (key-value) |

**Nested fields of `props`:**

| API name | Type | Description |
|---|---|---|
| `ro.product.vendor.name` | String | Property setting |

**Example** (JSON payload)

```json
{
 "padCode": "AC32010210001",
 "props": {
  "ro.product.vendor.name": "OP52D1L1"
 },
 "restart": false
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_update_sim_task_status` — Query SIM Modification Task Status

Query the execution status of a task by the taskId returned from [Modify SIM Card Information Based on Country Code](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#modify-sim-card-information-based-on-country-code). Only tasks created by the current account can be queried.

- **Endpoint**: `POST /vcpcloud/api/padApi/getUpdateSIMTaskStatus`

**Signature**

```python
client.instance.get_update_sim_task_status(task_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | String | yes | Task ID returned by updateSIM |

**Example** (JSON payload)

```json
{
    "taskId": "TASK-100000001"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `dissolve_room` — Stop Streaming

Stop streaming for specified instance, disconnect connection.

- **Endpoint**: `POST /vcpcloud/api/padApi/dissolveRoom`

**Signature**

```python
client.instance.dissolve_room(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": ["AC11010000031","AC22020020700"]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `check_ip` — Smart IP Proxy Detection

Detect if proxy IP is available and if location information is correct.

- **Endpoint**: `POST /vcpcloud/api/padApi/checkIP`

**Signature**

```python
client.instance.check_ip(host, port, account, password, type, *, country=None, ip=None, loc=None, city=None, region=None, timezone=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `host` | `host` | String | yes | Proxy info (IP or host) |
| `port` | `port` | Integer | yes | Proxy port (numeric) |
| `account` | `account` | String | yes | Proxy username |
| `password` | `password` | String | yes | Proxy password |
| `type` | `type` | String | yes | Proxy protocol: Socks5, http, https |
| `country` | `country` | String | no | Country - required when forcing specification |
| `ip` | `ip` | String | no | IP - required when forcing |
| `loc` | `loc` | String | no | Latitude, longitude - required when forcing |
| `city` | `city` | String | no | City - required when forcing |
| `region` | `region` | String | no | Region - required when forcing |
| `timezone` | `timezone` | String | no | Timezone - required when forcing |

**Example** (JSON payload)

```json
{
    "host": "62.112.132.92",
    "port": 45001,
    "account": "xxxxxxxxxx",
    "password": "xxxxxxxx",
    "type": "Socks5"
    // "country": "US"，
    // "ip": "156.228.84.62",
    // "loc": "39.0438,-77.4874",
    // "city": "Ashburn",
    // "region": "Virginia",
    // "timezone": "America/New_York"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `smart_ip` — Set Smart IP

- **Endpoint**: `POST /vcpcloud/api/padApi/smartIp`

**Signature**

```python
client.instance.smart_ip(pad_codes, host, port, account, password, type, mode, *, bypass_package_list=None, bypass_ip_list=None, bypass_domain_list=None, follow_language=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `host` | `host` | String | yes | Proxy info (IP or host) |
| `port` | `port` | Integer | yes | Proxy port |
| `account` | `account` | String | yes | Proxy username |
| `password` | `password` | String | yes | Proxy password |
| `type` | `type` | String | yes | Proxy protocol: socks5, http, https |
| `mode` | `mode` | String | yes | Proxy mode: vpn / proxy |
| `bypass_package_list` | `bypassPackageList` | Array | no | Bypass packages |
| `bypass_ip_list` | `bypassIpList` | Array | no | Bypass IPs |
| `bypass_domain_list` | `bypassDomainList` | Array | no | Bypass domains |
| `follow_language` | `followLanguage` | Boolean | no | Whether device language follows the proxy IP |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC32010160334"
    ],
    "host": "62.112.132.92",
    "port": 45001,
    "account": "xxxxxx",
    "password": "xxxxxxx",
    "type": "socks5",
    "mode": "vpn",
    "followLanguage": true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `not_smart_ip` — Cancel Smart IP

Cancel smart IP, restore exit IP, SIM info, GPS, timezone (device restarts, takes effect within 1 minute; status 119-initializing; returns to 100-normal on success/failure/timeout; timeout 5 minutes).

- **Endpoint**: `POST /vcpcloud/api/padApi/notSmartIp`

**Signature**

```python
client.instance.not_smart_ip(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC32010160334"
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_list_installed_app` — Get All Installed Apps in Specified Cloud Instance List

- **Endpoint**: `POST /vcpcloud/api/padApi/getListInstalledApp`

**Signature**

```python
client.instance.get_list_installed_app(pad_code_list, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code_list` | `padCodeList` | String[] | yes |  |

**Nested fields of `padCodeList`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodeList": ["AC32010601132"]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `update_time_zone` — Modify Instance Timezone

- **Endpoint**: `POST /vcpcloud/api/padApi/updateTimeZone`

**Signature**

```python
client.instance.update_time_zone(time_zone, pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `time_zone` | `timeZone` | String | yes | UTC standard timezone |
| `pad_codes` | `padCodes` | Array | yes | Instance list |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC32010140003"
 ],
 "timeZone": "Asia/Shanghai"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `update_language` — Modify Instance Language

- **Endpoint**: `POST /vcpcloud/api/padApi/updateLanguage`

**Signature**

```python
client.instance.update_language(language, pad_codes, *, country=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `language` | `language` | String | yes | Language |
| `country` | `country` | String | no | Country |
| `pad_codes` | `padCodes` | Array | yes | Instance list |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC32010140026"
 ],
 "language": "zh",
 "country": ""
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `gps_inject_info` — Set Instance Latitude and Longitude

- **Endpoint**: `POST /vcpcloud/api/padApi/gpsInjectInfo`

**Signature**

```python
client.instance.gps_inject_info(longitude, latitude, pad_codes, *, altitude=None, speed=None, bearing=None, horizontal_accuracy_meters=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `longitude` | `longitude` | Float | yes | Longitude |
| `latitude` | `latitude` | Float | yes | Latitude |
| `altitude` | `altitude` | Float | no | Altitude (requires latest image) |
| `speed` | `speed` | Float | no | Speed m/s (images after 20251024) |
| `bearing` | `bearing` | Float | no | Bearing ° (images after 20251024) |
| `horizontal_accuracy_meters` | `horizontalAccuracyMeters` | Float | no | Horizontal accuracy (images after 20251024) |
| `pad_codes` | `padCodes` | Array | yes | Instance list |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC32010030001"
 ],
 "longitude": 116.397455,
 "latitude": 39.909187,
 "altitude": 8
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `info` — Query Instance Proxy Information

- **Endpoint**: `POST /vcpcloud/open/network/proxy/info`

**Signature**

```python
client.instance.info(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | Array | yes | Instance list |

**Example** (JSON payload)

```json
{
  "padCodes": [
    "AC32010140012"
  ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `replace_pad` — One-Key New Device** ⭐

* Virtual machine: directly set Android properties, clear all data * Cloud real device: clear all data (equivalent to reset), add SIM info; if template ID provided, replace ADI template. If no template and replacementRealAdiFlag true, randomly select template. * Note: If no country info or unsupported, default Singapore SIM. * Unsupported country returns 500 error: Currently not supporting country code XX * Path Format Conversion Rules: /data/system/... -> /system/... /data/misc/... -> /misc/... /data/data/... -> /data/... （remove the second "data", for example /data/data/com.xx -> /data/com.x

- **Endpoint**: `POST /vcpcloud/api/padApi/replacePad`

**Signature**

```python
client.instance.replace_pad(pad_codes, *, country_code=None, real_phone_template_id=None, android_prop=None, replacement_real_adi_flag=None, exclude_real_phone_template_ids=None, certificate=None, wipe_data=None, wipe_specific_data=None, keep_specific_data=None, enable_cpu_core_config=None, webview_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | Array | yes | Instance ID list |
| `country_code` | `countryCode` | String | no | Country code (see: https://chahuo.com/country-code-lookup.html) |
| `real_phone_template_id` | `realPhoneTemplateId` | Long | no | Template ID (refer to [Paginated Get Real Device Templates]) |
| `android_prop` | `androidProp` | Object | no | Refer to [Android Modification Properties List] |
| `replacement_real_adi_flag` | `replacementRealAdiFlag` | Boolean | no | Whether random ADI template for real device (false-no, true-yes) |
| `exclude_real_phone_template_ids` | `excludeRealPhoneTemplateIds` | Long[] | no | Exclude template IDs when random |
| `certificate` | `certificate` | String | no | Phone root certificate |
| `wipe_data` | `wipeData` | Boolean | no | Clear user data (default true, CBS2.4.4+ support) |
| `wipe_specific_data` | `wipeSpecificData` | String[] | no | Effective when wipeData false; specify data to clear |
| `keep_specific_data` | `keepSpecificData` | String[] | no | Effective when wipeData is false; specifies which data should be preserved (mutually exclusive with wipeSpecificData) |
| `enable_cpu_core_config` | `enableCpuCoreConfig` | Boolean | no | Enable CPU core config (based on Android cpuset for performance stability) |
| `webview_id` | `webviewId` | Long | no | WebView version ID, see [Query Available WebView Versions](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#query-available-webview-versions) |

**Example** (JSON payload)

```json
{
  "padCodes": ["AC32010250031"],
  "countryCode": "SG",
  "realPhoneTemplateId": 210,
  "androidProp": {
    "persist.sys.cloud.battery.level": "67",
    "persist.sys.cloud.gps.lat": "1.3657",
    "persist.sys.cloud.gps.lon": "103.6464",
    "persist.sys.cloud.imsinum": "525050095718767"
  },
  "replacementRealAdiFlag": true,
  "excludeRealPhoneTemplateIds": [101, 102],
  "certificate": "手机根证书",
  "wipeData": false,
  "wipeSpecificData": ["/fonts", "/media"],
  "webviewId": 2066351288679604225
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `pad_replace_new` — One-Key New Device (Auto SIM/GPS/Timezone)** ⭐

- **Endpoint**: `POST /vcpcloud/api/padApi/padReplaceNew`

**Signature**

```python
client.instance.pad_replace_new(pad_codes, set_proxy_flag, *, wipe_data=None, keep_lang_timezone=None, android_prop=None, webview_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance codes (does not support `ACN` prefix) |
| `set_proxy_flag` | `setProxyFlag` | Boolean | yes | Set to `true` to write SIM based on deployment location |
| `wipe_data` | `wipeData` | Boolean | no | Whether to clear data; default `true` |
| `keep_lang_timezone` | `keepLangTimezone` | Boolean | no | Whether to keep old language/timezone; default `false` |
| `android_prop` | `androidProp` | Object | no | Custom Android system properties as key-value pairs. Examples: `persist.sys.locale`, `persist.sys.timezone`, etc. Higher priority than auto-generated properties |
| `webview_id` | `webviewId` | Long | no | WebView version ID, see [Query Available WebView Versions](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#query-available-webview-versions) |

**Example** (JSON payload)

```json
{
  "padCodes": ["ACP250328SSXVKN1"],
  "setProxyFlag": true,
  "wipeData": true,
  "keepLangTimezone": false,
  "androidProp": {
    "persist.sys.locale": "zh-CN",
    "persist.sys.timezone": "Asia/Shanghai"
  },
  "webviewId": 2066351288679604225
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `country` — Query One-Key New Device Supported Countries List

- **Endpoint**: `GET /vcpcloud/api/padApi/country`

**Signature**

```python
client.instance.country(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `webview_version_list` — Query Available WebView Versions

- **Endpoint**: `POST /vcpcloud/api/padApi/webview/version/list`

**Signature**

```python
client.instance.webview_version_list(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `replacement` — Device Replacement

- **Endpoint**: `POST /vcpcloud/api/padApi/replacement`

**Signature**

```python
client.instance.replacement(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |

**Example** (JSON payload)

```json
{
    "padCode": "AC32010030001"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_long_generate_url` — Get Instance Real-Time Preview Image

Get current screen screenshot for specified instance. Returns URL and expiration; access URL for real-time screenshot. Supports batch.

- **Endpoint**: `POST /vcpcloud/api/padApi/getLongGenerateUrl`

**Signature**

```python
client.instance.get_long_generate_url(pad_codes, *, format=None, height=None, width=None, quality=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | Array | yes | Instance list |
| `format` | `format` | String | no | Image format: png, jpg (default png; png no compression) |
| `height` | `height` | String | no | Scaled height (pixels; default original) |
| `width` | `width` | String | no | Scaled width (pixels; default original) |
| `quality` | `quality` | Integer | no | Image quality (0-100; default 50%; below 60 blurry) |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC11010000031",
        "AC11010000032"
    ],
    "format": "png"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `set_proxy` — Instance Set Proxy

- **Endpoint**: `POST /vcpcloud/api/padApi/setProxy`

**Signature**

```python
client.instance.set_proxy(enable, pad_codes, *, account=None, password=None, ip=None, port=None, proxy_type=None, proxy_name=None, model=None, bypass_package_list=None, bypass_ip_list=None, bypass_domain_list=None, limit_package_list=None, limit_ip_list=None, limit_domain_list=None, s_uo_t=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account` | `account` | String | no | Username |
| `password` | `password` | String | no | Password |
| `ip` | `ip` | String | no | IP |
| `port` | `port` | Integer | no | Port |
| `enable` | `enable` | Boolean | yes | Enable |
| `pad_codes` | `padCodes` | Array | yes | Instance list |
| `proxy_type` | `proxyType` | String | no | Supported: proxy, vpn |
| `proxy_name` | `proxyName` | String | no | Supported: socks5, http-relay (includes http/https) |
| `model` | `model` | String | no | List mode: bypass(default)/limit |
| `bypass_package_list` | `bypassPackageList` | Array | no | Packages bypassing proxy (model=bypass) |
| `bypass_ip_list` | `bypassIpList` | Array | no | IPs bypassing proxy (model=bypass) |
| `bypass_domain_list` | `bypassDomainList` | Array | no | Domains bypassing proxy (model=bypass) |
| `limit_package_list` | `limitPackageList` | Array | no | Only these packages use proxy (model=limit) |
| `limit_ip_list` | `limitIpList` | Array | no | Only these IPs use proxy (model=limit) |
| `limit_domain_list` | `limitDomainList` | Array | no | Only these domains use proxy (model=limit) |
| `s_uo_t` | `sUoT` | Boolean | no | Enable UDP (default false) |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC32010140023"
 ],
 "account": "2222",
 "password": "2222",
 "ip": "47.76.241.5",
 "port": 2222,
 "enable": true,
    "model": "bypass",
    "bypassPackageList":[],
    "bypassIpList":[],
    "bypassDomainList":[],
    "sUoT":true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `async_cmd` — Async Execute ADB Commands

Async execute commands in one or more cloud instances.

- **Endpoint**: `POST /vcpcloud/api/padApi/asyncCmd`

**Signature**

```python
client.instance.async_cmd(pad_codes, script_content, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `script_content` | `scriptContent` | String | yes | ADB commands (multiple separated by “;” ) |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC22020020793"
    ],
    "scriptContent": "cd /root;ls"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `switch_root` — Switch Root Permissions

Switch root permissions in one or more cloud instances. For single app root, specify package name (cloud real device: not recommended global root due to detection risk).

- **Endpoint**: `POST /vcpcloud/api/padApi/switchRoot`

**Signature**

```python
client.instance.switch_root(pad_codes, root_status, *, global_root=None, package_name=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `global_root` | `globalRoot` | Boolean | no | Global root (default no) |
| `package_name` | `packageName` | String | no | Package name (required for non-global; multiple comma separated) |
| `root_status` | `rootStatus` | Integer | yes | Root status: 0-off, 1-on |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
  "padCodes": [
    "AC32010250002"
  ],
  "globalRoot": false,
  "packageName": "com.android.ftpeasys",
  "rootStatus": 0
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `screenshot` — Local Screenshot

Instance screenshot.

- **Endpoint**: `POST /vcpcloud/api/padApi/screenshot`

**Signature**

```python
client.instance.screenshot(pad_codes, rotation, *, broadcast=None, definition=None, resolution_height=None, resolution_width=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `rotation` | `rotation` | Integer | yes | Screenshot orientation: 0-default, 1-rotate to portrait |
| `broadcast` | `broadcast` | Boolean | no | Broadcast event (default false) |
| `definition` | `definition` | Integer | no | Clarity 0-100 |
| `resolution_height` | `resolutionHeight` | Integer | no | Height >1 |
| `resolution_width` | `resolutionWidth` | Integer | no | Width >1 |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC21020010231"
 ],
 "rotation": 0,
 "broadcast": false,
    "definition": 50,
    "resolutionHeight": 1920,
    "resolutionWidth": 1080
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `generate_preview` — Generate Preview Image

Get preview image for specified instance.

- **Endpoint**: `POST /vcpcloud/api/padApi/generatePreview`

**Signature**

```python
client.instance.generate_preview(pad_codes, rotation, *, broadcast=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `rotation` | `rotation` | Integer | yes | Screenshot orientation: 0-default, 1-rotate to portrait |
| `broadcast` | `broadcast` | Boolean | no | Broadcast event (default false) |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC11010000031",
        "AC11010000032"
    ],
    "format": "png"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `upgrade_image` — Upgrade Image

Batch instance image upgrade.

- **Endpoint**: `POST /vcpcloud/api/padApi/upgradeImage`

**Signature**

```python
client.instance.upgrade_image(pad_codes, image_id, wipe_data, *, enable_cpu_core_config=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `image_id` | `imageId` | String | yes | Image ID |
| `wipe_data` | `wipeData` | Boolean | yes | Clear data partition: true-yes, false-no |
| `enable_cpu_core_config` | `enableCpuCoreConfig` | Boolean | no | Enable CPU core config |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC22030010182"
    ],
    "wipeData": false,
    "imageId": "mg-24061124017"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `set_hide_accessibility_app_list` — Hide Accessibility Service

1. The specified app itself can still detect that it has enabled accessibility service. 2. Third-party apps cannot detect that the specified app has enabled accessibility service. 3. The specified app will not appear in the accessibility service list.

- **Endpoint**: `POST /vcpcloud/api/padApi/setHideAccessibilityAppList`

**Signature**

```python
client.instance.set_hide_accessibility_app_list(pad_codes, app_infos, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Array of instance codes (maximum 200) |
| `app_infos` | `appInfos` | Object[] | yes | Array of hidden app list objects; pass empty array [] to clear (0–200 items) |

**Nested fields of `appInfos`:**

| API name | Type | Description |
|---|---|---|
| `packageName` | String | App package name. Special values: `*` or `ALL` means hide accessibility service permission for all apps |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC002",
  "AC001"
 ],
 "appInfos": [{
   "packageName": "com.tencent.mm"
  }]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `virtual_real_switch` — Upgrade Real Device Image

Batch real device image upgrade.

- **Endpoint**: `POST /vcpcloud/api/padApi/virtualRealSwitch`

**Signature**

```python
client.instance.virtual_real_switch(pad_codes, image_id, wipe_data, upgrade_image_convert_type, *, real_phone_template_id=None, screen_layout_id=None, certificate=None, device_android_props=None, enable_cpu_core_config=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `image_id` | `imageId` | String | yes | Image ID |
| `wipe_data` | `wipeData` | Boolean | yes | Clear data: true-yes, false-no |
| `real_phone_template_id` | `realPhoneTemplateId` | Integer | no | Real device template ID (required for real) |
| `upgrade_image_convert_type` | `upgradeImageConvertType` | String | yes | Convert type: virtual / real |
| `screen_layout_id` | `screenLayoutId` | Integer | no | Screen layout ID (required for virtual) |
| `certificate` | `certificate` | String | no | Custom root certificate |
| `device_android_props` | `deviceAndroidProps` | Object | no | Android props (CBS <2.4.4 not support) |
| `enable_cpu_core_config` | `enableCpuCoreConfig` | Boolean | no | Enable CPU core config |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC32010210023"
    ],
        "imageId": "img-24112653977",
        "wipeData": true,
        "realPhoneTemplateId": 178,
        "upgradeImageConvertType": "virtual",
        "screenLayoutId": 14
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `template_list` — Paginated Get Real Device Templates

Paginated retrieval of real device templates.

- **Endpoint**: `POST /vcpcloud/api/padApi/templateList`

**Signature**

```python
client.instance.template_list(*, page=None, rows=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Page number, default 1 |
| `rows` | `rows` | Integer | no | Number of items per page, default 10, range 1-100 |

**Example** (JSON payload)

```json
{
    "page": 1,
    "rows": 10
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `model_info` — Batch Get Instance Device Model Information

Batch get device model information for corresponding instances based on instance codes.

- **Endpoint**: `POST /vcpcloud/api/padApi/modelInfo`

**Signature**

```python
client.instance.model_info(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC22030010182"
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `set_speed` — Set Instance Bandwidth

Set instance bandwidth based on instance code.

- **Endpoint**: `POST /vcpcloud/api/padApi/setSpeed`

**Signature**

```python
client.instance.set_speed(pad_codes, up_bandwidth, down_bandwidth, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `up_bandwidth` | `upBandwidth` | float | yes | Upload bandwidth Mbps (0: unlimited; -1: block internet) |
| `down_bandwidth` | `downBandwidth` | float | yes | Download bandwidth Mbps (0: unlimited; -1: block internet) |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
 "padCodes": [
  "AC32010140011"
 ],
 "upBandwidth": 10.00,
 "downBandwidth": 10.00
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `open_online_adb` — Enable/Disable ADB

Enable or disable ADB for instance based on instance code.

- **Endpoint**: `POST /vcpcloud/api/padApi/openOnlineAdb`

**Signature**

```python
client.instance.open_online_adb(pad_codes, open_status, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance list (1-200 instances) |
| `open_status` | `openStatus` | Integer | yes | ADB status (1: enable; 0 or omit: disable) |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
    "padCodes":[
        "AC32010250032"
    ],
    "openStatus": 1
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `adb` — Get ADB Connection Information

Get ADB connection information based on instance code. If response data (key, adb) incomplete, call [Enable/Disable ADB] to enable ADB first.

- **Endpoint**: `POST /vcpcloud/api/padApi/adb`

**Signature**

```python
client.instance.adb(pad_code, enable, *, expire_minutes=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |
| `enable` | `enable` | Boolean | yes | ADB status: true-enable, false-disable |
| `expire_minutes` | `expireMinutes` | Integer | no | ADB validity period in minutes (1–7 days, i.e. 1440–10080), default 1440 |

**Example** (JSON payload)

```json
{
    "padCode": "AC32010250032",
    "enable": true,
    "expireMinutes": 2880
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `batch_adb` — Batch Get ADB Connection Information

Batch get or disable ADB connection information based on instance code list. If enable success but connection info incomplete, call [Enable/Disable ADB] to re-enable first. Max 10 instances per call.

- **Endpoint**: `POST /vcpcloud/api/padApi/batch/adb`

**Signature**

```python
client.instance.batch_adb(pad_codes, enable, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance code list (max 10) |
| `enable` | `enable` | Boolean | yes | Enable ADB: true-enable and return info, false-disable |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "AC32010250032",
        "AC32010250033"
    ],
    "enable": true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `confirm_transfer` — Transfer Cloud Phone

Transfer specified cloud phone instances to another account (via the recipient account's email).

- **Endpoint**: `POST /vcpcloud/api/padApi/confirmTransfer`

**Signature**

```python
client.instance.confirm_transfer(pad_codes, make_over_mobile_phone, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | List of instance codes to transfer |
| `make_over_mobile_phone` | `makeOverMobilePhone` | String | yes | Recipient account email |

**Example** (JSON payload)

```json
{
  "padCodes": [
    "ACXXXXXXXXX"
  ],
  "makeOverMobilePhone": "XXXX.gmail.com"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `execute_script_info` — Get Instance Script Execution Result

Get script execution result for instance via script task ID.

- **Endpoint**: `POST /vcpcloud/api/padApi/executeScriptInfo`

**Signature**

```python
client.instance.execute_script_info(task_ids, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | yes | Array length 1-100 |

**Nested fields of `taskIds`:**

| API name | Type | Description |
|---|---|---|
| `` | Integer | Task ID |

**Example** (JSON payload)

```json
{
 "taskIds": [1]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `screenshot_info` — Get Instance Screenshot Result

Get instance screenshot result via screenshot task ID.

- **Endpoint**: `POST /vcpcloud/api/padApi/screenshotInfo`

**Signature**

```python
client.instance.screenshot_info(task_ids, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | yes |  |

**Nested fields of `taskIds`:**

| API name | Type | Description |
|---|---|---|
| `` | Integer | Task ID |

**Example** (JSON payload)

```json
{
 "taskIds": [1]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `infos` — Instance List Information

Paginated get instance list information based on query conditions.

- **Endpoint**: `POST /vcpcloud/api/padApi/infos`

**Signature**

```python
client.instance.infos(page, rows, *, pad_type=None, pad_codes=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | yes | Page number |
| `rows` | `rows` | Integer | yes | Records per page |
| `pad_type` | `padType` | String | no | Instance type (virtual: virtual; real: real) |
| `pad_codes` | `padCodes` | String[] | no |  |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
"page": 1,
"rows": 10,
"padCodes": [
"AC21020010391"
]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `add_phone_record` — Import Call Logs

This interface imports call log data into cloud phone. During import, it automatically detects saved contacts and displays corresponding names in call logs for quick identification.

- **Endpoint**: `POST /vcpcloud/api/padApi/addPhoneRecord`

**Signature**

```python
client.instance.add_phone_record(pad_codes, call_records, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instances to edit call logs |
| `call_records` | `callRecords` | Object[] | yes | Call logs |

**Nested fields of `callRecords`:**

| API name | Type | Description |
|---|---|---|
| `number` | String | Phone number |
| `inputType` | int | Call type (1: outgoing; 2: incoming; 3: missed) |
| `duration` | int | Duration (seconds; 0 for missed) |
| `timeString` | String | Call time |

**Example** (JSON payload)

```json
{
  "padCodes": [
     "实例编号"
  ],
  "callRecords": [
    {
      "number": "18009781201",
      "inputType": 1,
      "duration": 30,
      "timeString": "2025-05-06 14:00:09"
    },
    {
      "number": "18009781202",
      "inputType": 2,
      "duration": 60,
      "timeString": "2025-05-07 14:00:09"
    },
    {
      "number": "18009781203",
      "inputType": 3,
      "duration": 0
    }
  ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `input_text` — Cloud Phone Text Input

Focus input box in cloud phone first, call this interface with text to display at specified position.

- **Endpoint**: `POST /vcpcloud/api/padApi/inputText`

**Signature**

```python
client.instance.input_text(pad_codes, text, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance codes |
| `text` | `text` | String | yes | Input text |

**Example** (JSON payload)

```json
{
   "padCodes": [
      "ACP250509FECQN33",
      "ACP250509T1VME44",
      "ACP25050917AYX11"
   ],
   "text": "12345678"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `simulate_send_sms` — Simulate Send SMS

Simulate sending SMS to instance (supports batch). Limited to AOSP13/14.

- **Endpoint**: `POST /vcpcloud/api/padApi/simulateSendSms`

**Signature**

```python
client.instance.simulate_send_sms(pad_codes, sender_number, sms_content, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance list (1-100) |
| `sender_number` | `senderNumber` | String | yes | Sender number (no mainland; max 16 chars, digits/letters/space/+-) |
| `sms_content` | `smsContent` | String | yes | SMS content (max 127 chars) |

**Example** (JSON payload)

```json
{
  "padCodes": ["ACN2505060777"],
  "senderNumber": "13800000000",
  "smsContent": "这是一条测试短信。"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `reset_gaid` — Reset GAID

Reset advertising ID (GAID) in cloud phone via instance code or group.

- **Endpoint**: `POST /vcpcloud/api/padApi/resetGAID`

**Signature**

```python
client.instance.reset_gaid(pad_codes, reset_gms_type, task_source, *, opr_by=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `reset_gms_type` | `resetGmsType` | String | yes | Reset type: GAID |
| `opr_by` | `oprBy` | String | no | Operator |
| `task_source` | `taskSource` | String | yes | Task source: OPEN_PLATFORM |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
   "padCodes": [
      "ACPXXXXXXXXXXXXXXX"
   ],
  "taskSource": "OPEN_PLATFORM",
  "oprBy": "admin",
  "resetGmsType": "GAID"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `inject_audio_to_mic` — Inject Audio to Instance Microphone

Inject audio file to instance microphone (PCM format only; convert first).

- **Endpoint**: `POST /vcpcloud/api/padApi/injectAudioToMic`

**Signature**

```python
client.instance.inject_audio_to_mic(pad_codes, enable, *, url=None, file_unique_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance codes |
| `url` | `url` | String | no | Audio download URL (one of url/fileUniqueId) |
| `file_unique_id` | `fileUniqueId` | String | no | File unique ID (one of url/fileUniqueId) |
| `enable` | `enable` | Boolean | yes | Inject switch |

**Example** (JSON payload)

```json
{
  "padCodes": [
    "ACP250509FECQN33","ACP250509T1VME44","ACP25050917AYX11
  ],
  "url":"http://localhost/abc ",
  "fileUniqueId":"8a6d0df189ef4b0e83858fd9eeb7620c",
  "enable":true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `clean_app_home` — Clear Processes and Return to Desktop

Clear all processes except system and return to desktop.

- **Endpoint**: `POST /vcpcloud/api/padApi/cleanAppHome`

**Signature**

```python
client.instance.clean_app_home(pad_codes, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instance codes |

**Example** (JSON payload)

```json
{
    "padCodes": [
        "ATP250814USYXXXX"
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `unmanned_live` — Unmanned Live Streaming

Instance video injection (only img-25092692759 image supported currently). Use injectUrl or injectUrls (at least one, not both; max 5 for injectUrls).

- **Endpoint**: `POST /vcpcloud/api/padApi/unmannedLive`

**Signature**

```python
client.instance.unmanned_live(pad_codes, *, inject_switch=None, inject_loop=None, inject_url=None, inject_urls=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instances (1-100) |
| `inject_switch` | `injectSwitch` | Boolean | no | Enable injection (true: on; false: off; default false) |
| `inject_loop` | `injectLoop` | Boolean | no | Loop playback (default false) |
| `inject_url` | `injectUrl` | String | no | Single video URL (http/https/rtmp:// or local; one with injectUrls) |
| `inject_urls` | `injectUrls` | String[] | no | Video URL list (max 5; one with injectUrl) |

**Example** (JSON payload)

```json
{
        "padCodes": ["ACN384345141346304"],
        "injectSwitch": true,
        "injectLoop": false,
        "injectUrl": "https://file.vmoscloud.com/userFile/1eea385b2a6ba3942ebf642badf39aa0.mp4",
        "injectUrls": [
          "https://file.vmoscloud.com/userFile/1eea385b2a6ba3942ebf642badf39aa0.mp4",
          "rtmp://example.com/live/unmanned01"
        ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `inject_picture` — Image Injection

Instance image injection.

- **Endpoint**: `POST /vcpcloud/api/padApi/injectPicture`

**Signature**

```python
client.instance.inject_picture(pad_codes, inject_url, *, inject_switch=None, inject_loop=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes | Instances (1-100) |
| `inject_switch` | `injectSwitch` | Boolean | no | Enable (true: on; false: off; default false) |
| `inject_loop` | `injectLoop` | Boolean | no | Loop (default false) |
| `inject_url` | `injectUrl` | String | yes | Image URL (http/https/rtmp://) |

**Example** (JSON payload)

```json
{
        "padCodes": ["ACN2510166WZUPCJ"],
        "injectSwitch": true,
        "injectLoop": false,
        "injectUrl": "https://file.vmoscloud.com/userFile/ac4e112d72f9ed724101f510e774001f.JPG"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
