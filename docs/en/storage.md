# `client.storage` — Cloud Space / Storage

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Storage goods, cloud-space backups, file upload/query/delete, storage renewal.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`select_files`](#select-files--query-user-file-list) | POST | `/vcpcloud/api/padApi/selectFiles` |
| [`delete_oss_files`](#delete-oss-files--delete-cloud-space-files) | POST | `/vcpcloud/api/padApi/deleteOssFiles` |
| [`upload_file`](#upload-file--upload-file-to-cloud-space) | POST | `/vcpcloud/api/padApi/uploadFile` |
| [`buy_storage_goods`](#buy-storage-goods--purchase-cloud-space-expansion) | POST | `/vcpcloud/api/padApi/buyStorageGoods` |
| [`vc_timing_backup_list`](#vc-timing-backup-list--storage-resource-package-list) | GET | `/vcpcloud/api/padApi/vcTimingBackupList` |
| [`get_vc_storage_goods`](#get-vc-storage-goods--cloud-space-product-list) | GET | `/vcpcloud/api/padApi/getVcStorageGoods` |
| [`renews_storage_goods`](#renews-storage-goods--aggregate-renewal-of-cloud-space-products) | POST | `/vcpcloud/api/padApi/renewsStorageGoods` |
| [`delete_upload_files`](#delete-upload-files--delete-backup-resource-package-data) | POST | `/vcpcloud/api/padApi/deleteUploadFiles` |
| [`update_renew_storage_status`](#update-renew-storage-status--cloud-space-auto-renew-aggregate-product-switch) | GET | `/vcpcloud/api/padApi/updateRenewStorageStatus` |
| [`select_auto_renew`](#select-auto-renew--query-cloud-space-renewal-details) | GET | `/vcpcloud/api/padApi/selectAutoRenew` |
| [`get_renew_storage_info`](#get-renew-storage-info--cloud-space-remaining-storage-capacity) | GET | `/vcpcloud/api/padApi/getRenewStorageInfo` |

[Back to index](README.md)

---

### `select_files` — Query User File List

- **Endpoint**: `POST /vcpcloud/api/padApi/selectFiles`

**Signature**

```python
client.storage.select_files(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `delete_oss_files` — Delete Cloud Space Files

- **Endpoint**: `POST /vcpcloud/api/padApi/deleteOssFiles`

**Signature**

```python
client.storage.delete_oss_files(files, *, urls=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `files` | `files` | Integer[] | yes | Collection of unique cloud space file IDs |
| `urls` | `urls` | String[] | no | Collection of cloud space file download links |

**Nested fields of `files`:**

| API name | Type | Description |
|---|---|---|
| `` | Integer | Unique cloud space file ID |

**Nested fields of `urls`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Cloud space file download link |

**Example** (JSON payload)

```json
{
    "files": [479452]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `upload_file` — Upload File to Cloud Space

Upload file to cloud space and get download link

- **Endpoint**: `POST /vcpcloud/api/padApi/uploadFile`

**Signature**

```python
client.storage.upload_file(file, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `file` | `file` | File | yes | File to upload |

**Example** (JSON payload)

```json
curl --request POST \
  --url /vcpcloud/api/padApi/uploadFile \
  --header 'accept-language: zh' \
  --header 'content-type: multipart/form-data' \
  --form 'file=@C:\FourSeasonsPhilly.webp'
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `buy_storage_goods` — Purchase Cloud Space Expansion

Purchase cloud space expansion

- **Endpoint**: `POST /vcpcloud/api/padApi/buyStorageGoods`

**Signature**

```python
client.storage.buy_storage_goods(storage_id, auto_renew_order, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `storage_id` | `storageId` | Integer | yes | Unique ID of cloud space expansion product |
| `auto_renew_order` | `autoRenewOrder` | Integer | yes | Auto-renew? 0-No 1-Yes |

**Example** (JSON payload)

```json
{
    "storageId": 1,
    "autoRenewOrder": 0
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `vc_timing_backup_list` — Storage Resource Package List

List of storage resource packages after shutdown backup

- **Endpoint**: `GET /vcpcloud/api/padApi/vcTimingBackupList`

**Signature**

```python
client.storage.vc_timing_backup_list(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_vc_storage_goods` — Cloud Space Product List

Cloud space product list

- **Endpoint**: `GET /vcpcloud/api/padApi/getVcStorageGoods`

**Signature**

```python
client.storage.get_vc_storage_goods(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `renews_storage_goods` — Aggregate Renewal of Cloud Space Products

Aggregate renewal of cloud space products

- **Endpoint**: `POST /vcpcloud/api/padApi/renewsStorageGoods`

**Signature**

```python
client.storage.renews_storage_goods(auto_renew_order, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `auto_renew_order` | `autoRenewOrder` | Integer | yes | Auto-renew? 0-No 1-Yes |

**Example** (JSON payload)

```json
{
    "autoRenewOrder": 0
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `delete_upload_files` — Delete Backup Resource Package Data

Delete backup resource package data

- **Endpoint**: `POST /vcpcloud/api/padApi/deleteUploadFiles`

**Signature**

```python
client.storage.delete_upload_files(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `update_renew_storage_status` — Cloud Space Auto-renew Aggregate Product Switch

Cloud space auto-renew aggregate product switch

- **Endpoint**: `GET /vcpcloud/api/padApi/updateRenewStorageStatus`

**Signature**

```python
client.storage.update_renew_storage_status(renew_storage_status, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `renew_storage_status` | `renewStorageStatus` | String | yes | Auto-renew? false-No true-Yes |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `select_auto_renew` — Query Cloud Space Renewal Details

Query cloud space renewal details

- **Endpoint**: `GET /vcpcloud/api/padApi/selectAutoRenew`

**Signature**

```python
client.storage.select_auto_renew(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_renew_storage_info` — Cloud Space Remaining Storage Capacity

Cloud space remaining storage capacity

- **Endpoint**: `GET /vcpcloud/api/padApi/getRenewStorageInfo`

**Signature**

```python
client.storage.get_renew_storage_info(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
