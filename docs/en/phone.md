# `client.phone` — Cloud Phone Management

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Goods, orders, renewals, activation codes, authorization/transfer, backups, sharing, replacement.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`create_timing_share`](#create-timing-share--cloud-phone-management) | POST | `/vcpcloud/api/padApi/createTimingShare` |
| [`open_auto_renew`](#open-auto-renew--enable-cloud-phone-auto-renewal) | POST | `/vcpcloud/api/padApi/openAutoRenew` |
| [`close_auto_renew`](#close-auto-renew--disable-cloud-phone-auto-renewal) | POST | `/vcpcloud/api/padApi/closeAutoRenew` |
| [`close_all_auto_renew`](#close-all-auto-renew--batch-disable-cloud-phone-auto-renewal) | POST | `/vcpcloud/api/padApi/closeAllAutoRenew` |
| [`update_pad_name`](#update-pad-name--rename-cloud-phone) | POST | `/vcpcloud/api/padApi/updatePadName` |
| [`authorize_pad`](#authorize-pad--authorize-pad) | POST | `/vcpcloud/api/padApi/authorizePad` |
| [`replace_real_adi_template`](#replace-real-adi-template--modify-real-device-adi-template) | POST | `/vcpcloud/api/padApi/replaceRealAdiTemplate` |
| [`create_money_order`](#create-money-order--create-cloud-phone) | POST | `/vcpcloud/api/padApi/createMoneyOrder` |
| [`activate_by_code`](#activate-by-code--activate-cloud-phone-with-activation-code) | POST | `/vcpcloud/api/padApi/activateByCode` |
| [`query_activation_batch`](#query-activation-batch--query-batch-activation-progress) | POST | `/vcpcloud/api/padApi/queryActivationBatch` |
| [`user_pad_list`](#user-pad-list--cloud-phone-list) | POST | `/vcpcloud/api/padApi/userPadList` |
| [`pad_info`](#pad-info--cloud-phone-information-query) | POST | `/vcpcloud/api/padApi/padInfo` |
| [`get_cloud_good_list`](#get-cloud-good-list--sku-package-list) | GET | `/vcpcloud/api/padApi/getCloudGoodList` |
| [`image_version_list`](#image-version-list--android-image-version-collection) | POST | `/vcpcloud/api/padApi/imageVersionList` |
| [`create_money_pro_order`](#create-money-pro-order--equipment-pre-sale-purchase) | POST | `/vcpcloud/api/padApi/createMoneyProOrder` |
| [`query_pro_order_list`](#query-pro-order-list--query-pre-sale-order-result-details) | POST | `/vcpcloud/api/padApi/queryProOrderList` |
| [`query_pad_id_change_records`](#query-pad-id-change-records--query-padcode-change-records) | POST | `/vcpcloud/api/padApi/queryPadIdChangeRecords` |
| [`list_pad_backup_ids`](#list-pad-backup-ids--list-pad-backup-ids) | POST | `/vcpcloud/api/padApi/listPadBackupIds` |
| [`add_backup`](#add-backup--create-pad-backups) | POST | `/vcpcloud/api/padApi/addBackup` |
| [`clone_pad_backup`](#clone-pad-backup--clone-pad-backup-to-multiple-pads) | POST | `/vcpcloud/api/padApi/clonePadBackup` |
| [`query_backup_batch`](#query-backup-batch--query-backup-batch-progress) | POST | `/vcpcloud/api/padApi/queryBackupBatch` |

[Back to index](README.md)

---

### `create_timing_share` — Cloud Phone Management

Create a share token for one powered-on timing device. Sharing ends after the device is powered off.

- **Endpoint**: `POST /vcpcloud/api/padApi/createTimingShare`

**Signature**

```python
client.phone.create_timing_share(*, equipment_id=None, pad_code=None, permission=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `equipment_id` | `equipmentId` | Long | no | Device ID |
| `pad_code` | `padCode` | String | no | Timing device ID |
| `permission` | `permission` | String | no | Share permission |

**Example** (JSON payload)

```json
{
  "padCode": "AC32010601132",
  "permission": "default"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `open_auto_renew` — Enable Cloud Phone Auto-Renewal

Enable auto-renewal for a single cloud phone; it will be renewed automatically with the current package before expiration.

- **Endpoint**: `POST /vcpcloud/api/padApi/openAutoRenew`

**Signature**

```python
client.phone.open_auto_renew(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |

**Example** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `close_auto_renew` — Disable Cloud Phone Auto-Renewal

Disable auto-renewal for a single cloud phone; once disabled, it will no longer be renewed automatically upon expiration.

- **Endpoint**: `POST /vcpcloud/api/padApi/closeAutoRenew`

**Signature**

```python
client.phone.close_auto_renew(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |

**Example** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `close_all_auto_renew` — Batch Disable Cloud Phone Auto-Renewal

Disable auto-renewal for all cloud phones under the current account in a single call; once disabled, they will no longer be renewed automatically upon expiration.

- **Endpoint**: `POST /vcpcloud/api/padApi/closeAllAutoRenew`

**Signature**

```python
client.phone.close_all_auto_renew(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `update_pad_name` — Rename Cloud Phone

Rename a single cloud phone.

- **Endpoint**: `POST /vcpcloud/api/padApi/updatePadName`

**Signature**

```python
client.phone.update_pad_name(pad_code, pad_name, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |
| `pad_name` | `padName` | String | yes | New cloud phone name |

**Example** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S",
 "padName": "My Cloud Phone 01"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `authorize_pad` — Authorize Pad

Temporarily grant a single cloud phone to another account. During the authorization the granted account can access the cloud phone; device ownership does not change.

- **Endpoint**: `POST /vcpcloud/api/padApi/authorizePad`

**Signature**

```python
client.phone.authorize_pad(pad_code, authorized_account, *, minutes=None, equi_authorize=None, permission=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance code |
| `authorized_account` | `authorizedAccount` | String | yes | Granted account (registered phone number or email) |
| `minutes` | `minutes` | Integer | no | Authorization duration in minutes; required when equiAuthorize=false |
| `equi_authorize` | `equiAuthorize` | Boolean | no | Authorize for the device's remaining validity; default false |
| `permission` | `permission` | String | no | Allowed-operation list, comma-separated; empty means all |

**Example** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S",
 "authorizedAccount": "13800000000",
 "minutes": 60,
 "equiAuthorize": false,
 "permission": "restartPad,adb"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `replace_real_adi_template` — Modify Real Device ADI Template

Modify cloud real device ADI template with provided template ID. Conditions: 1. Instance created as cloud real device type 2. Instance Android version matches target ADI version

- **Endpoint**: `POST /vcpcloud/api/padApi/replaceRealAdiTemplate`

**Signature**

```python
client.phone.replace_real_adi_template(pad_codes, wipe_data, real_phone_template_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | yes |  |
| `wipe_data` | `wipeData` | Boolean | yes | Clear data |
| `real_phone_template_id` | `realPhoneTemplateId` | Long | yes | Real device template ID |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Instance code |

**Example** (JSON payload)

```json
{
 "padCodes": ["AC32010250011"],
 "wipeData": true,
 "realPhoneTemplateId": 186
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `create_money_order` — Create Cloud Phone

Create a new cloud phone. (Note that the purchased product package must be available on the web platform, otherwise the purchase will fail.)

- **Endpoint**: `POST /vcpcloud/api/padApi/createMoneyOrder`

**Signature**

```python
client.phone.create_money_order(android_version_name, good_id, good_num, auto_renew, equipment_id, *, country_code=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `android_version_name` | `androidVersionName` | String | yes | Android version: Android10、Android13, Android14 |
| `good_id` | `goodId` | Integer | yes | Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) |
| `good_num` | `goodNum` | Integer | yes | Product quantity |
| `auto_renew` | `autoRenew` | Boolean | yes | Whether to auto-renew (enabled by default) |
| `equipment_id` | `equipmentId` | String | yes | Renewal device IDs (comma separated for multiple devices) |
| `country_code` | `countryCode` | String | no | Country code, used to specify the region of the cloud phone |

**Example** (JSON payload)

```json
{
    "androidVersionName": "Android13",
    "goodId": 1,
    "goodNum": 1,
    "autoRenew": true,
    "countryCode": "US"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `activate_by_code` — Activate Cloud Phone with Activation Code

Batch-activate cloud phones using activation codes. Submit a list of activation codes and immediately get a batch number (batchId); cloud phones are created asynchronously in the background and belong to the caller's account once activated. Activation codes that cannot be used are returned in failCodes. (The product package corresponding to the activation code must exist and be valid on the web platform, otherwise activation will fail.)

- **Endpoint**: `POST /vcpcloud/api/padApi/activateByCode`

**Signature**

```python
client.phone.activate_by_code(active_code_list, *, country_code=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `active_code_list` | `activeCodeList` | String[] | yes | List of activation codes, multiple allowed |
| `country_code` | `countryCode` | String | no | Country/region code. Defaults to HK if not provided |

**Example** (JSON payload)

```json
{
    "activeCodeList": ["ABCD-1234-EFGH-5678"],
    "countryCode": "HK"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `query_activation_batch` — Query Batch Activation Progress

Query the progress of a batch activation task submitted via activateByCode. Returns the overall status, the number of activation codes succeeded/failed/in progress, the number of activated devices, and per-code details.

- **Endpoint**: `POST /vcpcloud/api/padApi/queryActivationBatch`

**Signature**

```python
client.phone.query_activation_batch(batch_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `batch_id` | `batchId` | String | yes | Batch number returned by activateByCode |

**Example** (JSON payload)

```json
{
    "batchId": "100001_1736306672346"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `user_pad_list` — Cloud Phone List

Cloud phone list.

- **Endpoint**: `POST /vcpcloud/api/padApi/userPadList`

**Signature**

```python
client.phone.user_pad_list(*, pad_code=None, equipment_ids=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | no | Instance code |
| `equipment_ids` | `equipmentIds` | Integer[] | no | Array of equipment IDs |

**Example** (JSON payload)

```json
{
    "padCode": null,
    "equipmentIds": [
        106626
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `pad_info` — Cloud Phone Information Query

Query cloud phone information.

- **Endpoint**: `POST /vcpcloud/api/padApi/padInfo`

**Signature**

```python
client.phone.pad_info(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance ID |

**Example** (JSON payload)

```json
{
    "padCode": null
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_cloud_good_list` — SKU Package List

Get the SKU package list.

- **Endpoint**: `GET /vcpcloud/api/padApi/getCloudGoodList`

**Signature**

```python
client.phone.get_cloud_good_list(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `image_version_list` — Android image version collection

Get the image set that can be upgraded on the current device

- **Endpoint**: `POST /vcpcloud/api/padApi/imageVersionList`

**Signature**

```python
client.phone.image_version_list(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | PadCode |

**Example** (JSON payload)

```json
{
    "padCode": "ACP250329MMRFCCT"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `create_money_pro_order` — Equipment Pre-sale Purchase

When stock is insufficient, you can use this API to pre-order a device (only applicable to cloud phone products with a rental period of 30 days or more). Once stock is replenished, the system will prioritize fulfilling pre-sale orders and automatically dispatch the devices. After the order is shipped, users will receive an email notification and an additional one-day usage bonus.

- **Endpoint**: `POST /vcpcloud/api/padApi/createMoneyProOrder`

**Signature**

```python
client.phone.create_money_pro_order(*, android_version_name=None, good_id=None, good_num=None, auto_renew=None, country_code=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `android_version_name` | `androidVersionName` | String | no | Android Version：Android10、Android13、Android14 |
| `good_id` | `goodId` | Integer | no | Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) |
| `good_num` | `goodNum` | Integer | no | Product Number |
| `auto_renew` | `autoRenew` | Boolean | no | Whether to automatically renew (default closed) true-on, false-off |
| `country_code` | `countryCode` | String | no | Country code, used to specify the region of the cloud phone |

**Example** (JSON payload)

```json
{
    "androidVersionName": "Android13",
    "goodId": 75,
    "goodNum": 1,
    "autoRenew": true,
    "countryCode": "US"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `query_pro_order_list` — Query pre-sale order result details

Query the details of pre-sale order results. You can query by pre-sale order number, order status (1-to be shipped 2-shipped, empty default all)

- **Endpoint**: `POST /vcpcloud/api/padApi/queryProOrderList`

**Signature**

```python
client.phone.query_pro_order_list(*, pro_buy_status=None, order_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pro_buy_status` | `proBuyStatus` | Integer | no | 1-To be shipped 2-Shipment If empty, default to all |
| `order_id` | `orderId` | Integer | no | Pre-sale order number |

**Example** (JSON payload)

```json
{
    "proBuyStatus": "2",
    "orderId": "VMOS-CLOUD174290228048631464"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `query_pad_id_change_records` — Query padCode Change Records**

Query padCode change records for devices owned by the current user

- **Endpoint**: `POST /vcpcloud/api/padApi/queryPadIdChangeRecords`

**Signature**

```python
client.phone.query_pad_id_change_records(*, query_date=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `query_date` | `queryDate` | String | no | Calendar day to query (format `yyyy-MM-dd`, Asia/Shanghai). If omitted, the last 3 calendar days (inclusive of today) are returned. Future dates are rejected |

**Example** (JSON payload)

```json
{
    "queryDate": "2026-04-15"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `list_pad_backup_ids` — List Pad Backup IDs**

List all available cloud-disk backup IDs owned by the current OpenAPI user, ordered by create time descending. The returned IDs can be fed into the batch clone endpoint below.

- **Endpoint**: `POST /vcpcloud/api/padApi/listPadBackupIds`

**Signature**

```python
client.phone.list_pad_backup_ids(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `add_backup` — Create Pad Backups**

Batch create cloud-disk backups for the given cloud phones. The call is asynchronous and returns immediately; use the `batchId` in the response to track task progress. Constraints: * Up to 50 cloud phones per call. * Only one in-flight backup task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Remaining storage quota must be at least 16GB × backup pad count.

- **Endpoint**: `POST /vcpcloud/api/padApi/addBackup`

**Signature**

```python
client.phone.add_backup(vc_pad_backup_list, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `vc_pad_backup_list` | `vcPadBackupList` | Object[] | yes | Cloud phones to back up (1 to 50 entries) |

**Nested fields of `vcPadBackupList`:**

| API name | Type | Description |
|---|---|---|
| `padCode` | String | Pad code |

**Example** (JSON payload)

```json
{
    "vcPadBackupList": [
        { "padCode": "AC32010601132" },
        { "padCode": "AC32010601133" }
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `clone_pad_backup` — Clone Pad Backup to Multiple Pads**

Batch clone a cloud-disk backup onto multiple cloud phones. The call is asynchronous and returns immediately. Constraints: * Only one in-flight clone task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Source backup and target cloud phone product specs must match.

- **Endpoint**: `POST /vcpcloud/api/padApi/clonePadBackup`

**Signature**

```python
client.phone.clone_pad_backup(vc_pad_backup_list, pads, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `vc_pad_backup_list` | `vcPadBackupList` | Object[] | yes | Source backup list (at least 1 item) |
| `pads` | `pads` | Object[] | yes | Target cloud phone list (at least 1 item) |

**Nested fields of `vcPadBackupList`:**

| API name | Type | Description |
|---|---|---|
| `backupId` | String | Cloud-disk backup ID (from `listPadBackupIds`) |

**Nested fields of `pads`:**

| API name | Type | Description |
|---|---|---|
| `padCode` | String | Cloud phone padCode |

**Example** (JSON payload)

```json
{
    "vcPadBackupList": [
        { "backupId": "bkp-AAA-1" }
    ],
    "pads": [
        { "padCode": "AC32010601132" },
        { "padCode": "AC32010601133" }
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `query_backup_batch` — Query Backup Batch Progress**

Query backup progress by `batchId`. Returns per-pad status and `backupId` (available once status ≥ 1). Use the `batchId` returned by `addBackup` to poll this endpoint.

- **Endpoint**: `POST /vcpcloud/api/padApi/queryBackupBatch`

**Signature**

```python
client.phone.query_backup_batch(batch_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `batch_id` | `batchId` | String | yes | Batch ID returned by `addBackup` |

**Example** (JSON payload)

```json
{
    "batchId": "100001_1762424603654"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
