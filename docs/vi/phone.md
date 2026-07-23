# `client.phone` — Quản lý Cloud Phone

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Gói dịch vụ, đơn hàng, gia hạn, mã kích hoạt, ủy quyền/chuyển giao, sao lưu, chia sẻ, thay thế thiết bị.

## Danh sách phương thức

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

[Về trang chính](README.md)

---

### `create_timing_share` — Cloud Phone Management

Create a share token for one powered-on timing device. Sharing ends after the device is powered off.

- **Endpoint**: `POST /vcpcloud/api/padApi/createTimingShare`

**Chữ ký hàm**

```python
client.phone.create_timing_share(*, equipment_id=None, pad_code=None, permission=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `equipment_id` | `equipmentId` | Long | không | Device ID |
| `pad_code` | `padCode` | String | không | Timing device ID |
| `permission` | `permission` | String | không | Share permission |

**Ví dụ** (JSON payload)

```json
{
  "padCode": "AC32010601132",
  "permission": "default"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `open_auto_renew` — Enable Cloud Phone Auto-Renewal

Enable auto-renewal for a single cloud phone; it will be renewed automatically with the current package before expiration.

- **Endpoint**: `POST /vcpcloud/api/padApi/openAutoRenew`

**Chữ ký hàm**

```python
client.phone.open_auto_renew(pad_code, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance code |

**Ví dụ** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `close_auto_renew` — Disable Cloud Phone Auto-Renewal

Disable auto-renewal for a single cloud phone; once disabled, it will no longer be renewed automatically upon expiration.

- **Endpoint**: `POST /vcpcloud/api/padApi/closeAutoRenew`

**Chữ ký hàm**

```python
client.phone.close_auto_renew(pad_code, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance code |

**Ví dụ** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `close_all_auto_renew` — Batch Disable Cloud Phone Auto-Renewal

Disable auto-renewal for all cloud phones under the current account in a single call; once disabled, they will no longer be renewed automatically upon expiration.

- **Endpoint**: `POST /vcpcloud/api/padApi/closeAllAutoRenew`

**Chữ ký hàm**

```python
client.phone.close_all_auto_renew(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `update_pad_name` — Rename Cloud Phone

Rename a single cloud phone.

- **Endpoint**: `POST /vcpcloud/api/padApi/updatePadName`

**Chữ ký hàm**

```python
client.phone.update_pad_name(pad_code, pad_name, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance code |
| `pad_name` | `padName` | String | có | New cloud phone name |

**Ví dụ** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S",
 "padName": "My Cloud Phone 01"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `authorize_pad` — Authorize Pad

Temporarily grant a single cloud phone to another account. During the authorization the granted account can access the cloud phone; device ownership does not change.

- **Endpoint**: `POST /vcpcloud/api/padApi/authorizePad`

**Chữ ký hàm**

```python
client.phone.authorize_pad(pad_code, authorized_account, *, minutes=None, equi_authorize=None, permission=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance code |
| `authorized_account` | `authorizedAccount` | String | có | Granted account (registered phone number or email) |
| `minutes` | `minutes` | Integer | không | Authorization duration in minutes; required when equiAuthorize=false |
| `equi_authorize` | `equiAuthorize` | Boolean | không | Authorize for the device's remaining validity; default false |
| `permission` | `permission` | String | không | Allowed-operation list, comma-separated; empty means all |

**Ví dụ** (JSON payload)

```json
{
 "padCode": "ACP250417QAGGQ3S",
 "authorizedAccount": "13800000000",
 "minutes": 60,
 "equiAuthorize": false,
 "permission": "restartPad,adb"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `replace_real_adi_template` — Modify Real Device ADI Template

Modify cloud real device ADI template with provided template ID. Conditions: 1. Instance created as cloud real device type 2. Instance Android version matches target ADI version

- **Endpoint**: `POST /vcpcloud/api/padApi/replaceRealAdiTemplate`

**Chữ ký hàm**

```python
client.phone.replace_real_adi_template(pad_codes, wipe_data, real_phone_template_id, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | có |  |
| `wipe_data` | `wipeData` | Boolean | có | Clear data |
| `real_phone_template_id` | `realPhoneTemplateId` | Long | có | Real device template ID |

**Các trường con của `padCodes`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | String | Instance code |

**Ví dụ** (JSON payload)

```json
{
 "padCodes": ["AC32010250011"],
 "wipeData": true,
 "realPhoneTemplateId": 186
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `create_money_order` — Create Cloud Phone

Create a new cloud phone. (Note that the purchased product package must be available on the web platform, otherwise the purchase will fail.)

- **Endpoint**: `POST /vcpcloud/api/padApi/createMoneyOrder`

**Chữ ký hàm**

```python
client.phone.create_money_order(android_version_name, good_id, good_num, auto_renew, equipment_id, *, country_code=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `android_version_name` | `androidVersionName` | String | có | Android version: Android10、Android13, Android14 |
| `good_id` | `goodId` | Integer | có | Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) |
| `good_num` | `goodNum` | Integer | có | Product quantity |
| `auto_renew` | `autoRenew` | Boolean | có | Whether to auto-renew (enabled by default) |
| `equipment_id` | `equipmentId` | String | có | Renewal device IDs (comma separated for multiple devices) |
| `country_code` | `countryCode` | String | không | Country code, used to specify the region of the cloud phone |

**Ví dụ** (JSON payload)

```json
{
    "androidVersionName": "Android13",
    "goodId": 1,
    "goodNum": 1,
    "autoRenew": true,
    "countryCode": "US"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `activate_by_code` — Activate Cloud Phone with Activation Code

Batch-activate cloud phones using activation codes. Submit a list of activation codes and immediately get a batch number (batchId); cloud phones are created asynchronously in the background and belong to the caller's account once activated. Activation codes that cannot be used are returned in failCodes. (The product package corresponding to the activation code must exist and be valid on the web platform, otherwise activation will fail.)

- **Endpoint**: `POST /vcpcloud/api/padApi/activateByCode`

**Chữ ký hàm**

```python
client.phone.activate_by_code(active_code_list, *, country_code=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `active_code_list` | `activeCodeList` | String[] | có | List of activation codes, multiple allowed |
| `country_code` | `countryCode` | String | không | Country/region code. Defaults to HK if not provided |

**Ví dụ** (JSON payload)

```json
{
    "activeCodeList": ["ABCD-1234-EFGH-5678"],
    "countryCode": "HK"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `query_activation_batch` — Query Batch Activation Progress

Query the progress of a batch activation task submitted via activateByCode. Returns the overall status, the number of activation codes succeeded/failed/in progress, the number of activated devices, and per-code details.

- **Endpoint**: `POST /vcpcloud/api/padApi/queryActivationBatch`

**Chữ ký hàm**

```python
client.phone.query_activation_batch(batch_id, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `batch_id` | `batchId` | String | có | Batch number returned by activateByCode |

**Ví dụ** (JSON payload)

```json
{
    "batchId": "100001_1736306672346"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `user_pad_list` — Cloud Phone List

Cloud phone list.

- **Endpoint**: `POST /vcpcloud/api/padApi/userPadList`

**Chữ ký hàm**

```python
client.phone.user_pad_list(*, pad_code=None, equipment_ids=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | không | Instance code |
| `equipment_ids` | `equipmentIds` | Integer[] | không | Array of equipment IDs |

**Ví dụ** (JSON payload)

```json
{
    "padCode": null,
    "equipmentIds": [
        106626
    ]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `pad_info` — Cloud Phone Information Query

Query cloud phone information.

- **Endpoint**: `POST /vcpcloud/api/padApi/padInfo`

**Chữ ký hàm**

```python
client.phone.pad_info(pad_code, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance ID |

**Ví dụ** (JSON payload)

```json
{
    "padCode": null
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_cloud_good_list` — SKU Package List

Get the SKU package list.

- **Endpoint**: `GET /vcpcloud/api/padApi/getCloudGoodList`

**Chữ ký hàm**

```python
client.phone.get_cloud_good_list(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `image_version_list` — Android image version collection

Get the image set that can be upgraded on the current device

- **Endpoint**: `POST /vcpcloud/api/padApi/imageVersionList`

**Chữ ký hàm**

```python
client.phone.image_version_list(pad_code, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | PadCode |

**Ví dụ** (JSON payload)

```json
{
    "padCode": "ACP250329MMRFCCT"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `create_money_pro_order` — Equipment Pre-sale Purchase

When stock is insufficient, you can use this API to pre-order a device (only applicable to cloud phone products with a rental period of 30 days or more). Once stock is replenished, the system will prioritize fulfilling pre-sale orders and automatically dispatch the devices. After the order is shipped, users will receive an email notification and an additional one-day usage bonus.

- **Endpoint**: `POST /vcpcloud/api/padApi/createMoneyProOrder`

**Chữ ký hàm**

```python
client.phone.create_money_pro_order(*, android_version_name=None, good_id=None, good_num=None, auto_renew=None, country_code=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `android_version_name` | `androidVersionName` | String | không | Android Version：Android10、Android13、Android14 |
| `good_id` | `goodId` | Integer | không | Product ID (corresponding to the Product ID value of [SKU Package List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#sku-package-list)) |
| `good_num` | `goodNum` | Integer | không | Product Number |
| `auto_renew` | `autoRenew` | Boolean | không | Whether to automatically renew (default closed) true-on, false-off |
| `country_code` | `countryCode` | String | không | Country code, used to specify the region of the cloud phone |

**Ví dụ** (JSON payload)

```json
{
    "androidVersionName": "Android13",
    "goodId": 75,
    "goodNum": 1,
    "autoRenew": true,
    "countryCode": "US"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `query_pro_order_list` — Query pre-sale order result details

Query the details of pre-sale order results. You can query by pre-sale order number, order status (1-to be shipped 2-shipped, empty default all)

- **Endpoint**: `POST /vcpcloud/api/padApi/queryProOrderList`

**Chữ ký hàm**

```python
client.phone.query_pro_order_list(*, pro_buy_status=None, order_id=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pro_buy_status` | `proBuyStatus` | Integer | không | 1-To be shipped 2-Shipment If empty, default to all |
| `order_id` | `orderId` | Integer | không | Pre-sale order number |

**Ví dụ** (JSON payload)

```json
{
    "proBuyStatus": "2",
    "orderId": "VMOS-CLOUD174290228048631464"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `query_pad_id_change_records` — Query padCode Change Records**

Query padCode change records for devices owned by the current user

- **Endpoint**: `POST /vcpcloud/api/padApi/queryPadIdChangeRecords`

**Chữ ký hàm**

```python
client.phone.query_pad_id_change_records(*, query_date=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `query_date` | `queryDate` | String | không | Calendar day to query (format `yyyy-MM-dd`, Asia/Shanghai). If omitted, the last 3 calendar days (inclusive of today) are returned. Future dates are rejected |

**Ví dụ** (JSON payload)

```json
{
    "queryDate": "2026-04-15"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `list_pad_backup_ids` — List Pad Backup IDs**

List all available cloud-disk backup IDs owned by the current OpenAPI user, ordered by create time descending. The returned IDs can be fed into the batch clone endpoint below.

- **Endpoint**: `POST /vcpcloud/api/padApi/listPadBackupIds`

**Chữ ký hàm**

```python
client.phone.list_pad_backup_ids(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `add_backup` — Create Pad Backups**

Batch create cloud-disk backups for the given cloud phones. The call is asynchronous and returns immediately; use the `batchId` in the response to track task progress. Constraints: * Up to 50 cloud phones per call. * Only one in-flight backup task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Remaining storage quota must be at least 16GB × backup pad count.

- **Endpoint**: `POST /vcpcloud/api/padApi/addBackup`

**Chữ ký hàm**

```python
client.phone.add_backup(vc_pad_backup_list, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `vc_pad_backup_list` | `vcPadBackupList` | Object[] | có | Cloud phones to back up (1 to 50 entries) |

**Các trường con của `vcPadBackupList`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `padCode` | String | Pad code |

**Ví dụ** (JSON payload)

```json
{
    "vcPadBackupList": [
        { "padCode": "AC32010601132" },
        { "padCode": "AC32010601133" }
    ]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `clone_pad_backup` — Clone Pad Backup to Multiple Pads**

Batch clone a cloud-disk backup onto multiple cloud phones. The call is asynchronous and returns immediately. Constraints: * Only one in-flight clone task per user at a time. * Target cloud phones must be in a healthy running state. * Target devices must be owned or authorized by the caller. * Source backup and target cloud phone product specs must match.

- **Endpoint**: `POST /vcpcloud/api/padApi/clonePadBackup`

**Chữ ký hàm**

```python
client.phone.clone_pad_backup(vc_pad_backup_list, pads, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `vc_pad_backup_list` | `vcPadBackupList` | Object[] | có | Source backup list (at least 1 item) |
| `pads` | `pads` | Object[] | có | Target cloud phone list (at least 1 item) |

**Các trường con của `vcPadBackupList`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `backupId` | String | Cloud-disk backup ID (from `listPadBackupIds`) |

**Các trường con của `pads`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `padCode` | String | Cloud phone padCode |

**Ví dụ** (JSON payload)

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

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `query_backup_batch` — Query Backup Batch Progress**

Query backup progress by `batchId`. Returns per-pad status and `backupId` (available once status ≥ 1). Use the `batchId` returned by `addBackup` to poll this endpoint.

- **Endpoint**: `POST /vcpcloud/api/padApi/queryBackupBatch`

**Chữ ký hàm**

```python
client.phone.query_backup_batch(batch_id, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `batch_id` | `batchId` | String | có | Batch ID returned by `addBackup` |

**Ví dụ** (JSON payload)

```json
{
    "batchId": "100001_1762424603654"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
