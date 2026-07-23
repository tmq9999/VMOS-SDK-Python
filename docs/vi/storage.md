# `client.storage` — Cloud Space / Lưu trữ

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Gói lưu trữ, sao lưu cloud space, tải lên/truy vấn/xóa file, gia hạn lưu trữ.

## Danh sách phương thức

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

[Về trang chính](README.md)

---

### `select_files` — Query User File List

- **Endpoint**: `POST /vcpcloud/api/padApi/selectFiles`

**Chữ ký hàm**

```python
client.storage.select_files(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `delete_oss_files` — Delete Cloud Space Files

- **Endpoint**: `POST /vcpcloud/api/padApi/deleteOssFiles`

**Chữ ký hàm**

```python
client.storage.delete_oss_files(files, *, urls=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `files` | `files` | Integer[] | có | Collection of unique cloud space file IDs |
| `urls` | `urls` | String[] | không | Collection of cloud space file download links |

**Các trường con của `files`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | Integer | Unique cloud space file ID |

**Các trường con của `urls`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | String | Cloud space file download link |

**Ví dụ** (JSON payload)

```json
{
    "files": [479452]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `upload_file` — Upload File to Cloud Space

Upload file to cloud space and get download link

- **Endpoint**: `POST /vcpcloud/api/padApi/uploadFile`

**Chữ ký hàm**

```python
client.storage.upload_file(file, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `file` | `file` | File | có | File to upload |

**Ví dụ** (JSON payload)

```json
curl --request POST \
  --url /vcpcloud/api/padApi/uploadFile \
  --header 'accept-language: zh' \
  --header 'content-type: multipart/form-data' \
  --form 'file=@C:\FourSeasonsPhilly.webp'
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `buy_storage_goods` — Purchase Cloud Space Expansion

Purchase cloud space expansion

- **Endpoint**: `POST /vcpcloud/api/padApi/buyStorageGoods`

**Chữ ký hàm**

```python
client.storage.buy_storage_goods(storage_id, auto_renew_order, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `storage_id` | `storageId` | Integer | có | Unique ID of cloud space expansion product |
| `auto_renew_order` | `autoRenewOrder` | Integer | có | Auto-renew? 0-No 1-Yes |

**Ví dụ** (JSON payload)

```json
{
    "storageId": 1,
    "autoRenewOrder": 0
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `vc_timing_backup_list` — Storage Resource Package List

List of storage resource packages after shutdown backup

- **Endpoint**: `GET /vcpcloud/api/padApi/vcTimingBackupList`

**Chữ ký hàm**

```python
client.storage.vc_timing_backup_list(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_vc_storage_goods` — Cloud Space Product List

Cloud space product list

- **Endpoint**: `GET /vcpcloud/api/padApi/getVcStorageGoods`

**Chữ ký hàm**

```python
client.storage.get_vc_storage_goods(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `renews_storage_goods` — Aggregate Renewal of Cloud Space Products

Aggregate renewal of cloud space products

- **Endpoint**: `POST /vcpcloud/api/padApi/renewsStorageGoods`

**Chữ ký hàm**

```python
client.storage.renews_storage_goods(auto_renew_order, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `auto_renew_order` | `autoRenewOrder` | Integer | có | Auto-renew? 0-No 1-Yes |

**Ví dụ** (JSON payload)

```json
{
    "autoRenewOrder": 0
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `delete_upload_files` — Delete Backup Resource Package Data

Delete backup resource package data

- **Endpoint**: `POST /vcpcloud/api/padApi/deleteUploadFiles`

**Chữ ký hàm**

```python
client.storage.delete_upload_files(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `update_renew_storage_status` — Cloud Space Auto-renew Aggregate Product Switch

Cloud space auto-renew aggregate product switch

- **Endpoint**: `GET /vcpcloud/api/padApi/updateRenewStorageStatus`

**Chữ ký hàm**

```python
client.storage.update_renew_storage_status(renew_storage_status, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `renew_storage_status` | `renewStorageStatus` | String | có | Auto-renew? false-No true-Yes |

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `select_auto_renew` — Query Cloud Space Renewal Details

Query cloud space renewal details

- **Endpoint**: `GET /vcpcloud/api/padApi/selectAutoRenew`

**Chữ ký hàm**

```python
client.storage.select_auto_renew(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_renew_storage_info` — Cloud Space Remaining Storage Capacity

Cloud space remaining storage capacity

- **Endpoint**: `GET /vcpcloud/api/padApi/getRenewStorageInfo`

**Chữ ký hàm**

```python
client.storage.get_renew_storage_info(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
