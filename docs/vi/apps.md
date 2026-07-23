# `client.apps` — Quản lý ứng dụng

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Cài/gỡ, khởi chạy/dừng/khởi động lại ứng dụng, liệt kê ứng dụng, giữ ứng dụng chạy nền và ẩn ứng dụng.

## Danh sách phương thức

| Python | HTTP | Endpoint |
|---|---|---|
| [`update_sim`](#update-sim--modify-sim-card-information-based-on-country-code) | POST | `/vcpcloud/api/padApi/updateSIM` |
| [`upload_file_v3`](#upload-file-v3--file-upload-via-link-directly) | POST | `/vcpcloud/api/padApi/uploadFileV3` |
| [`batch_upload_file`](#batch-upload-file--batch-upload-files) | POST | `/vcpcloud/api/padApi/batchUploadFile` |
| [`list_installed_app`](#list-installed-app--real-time-query-installed-apps-list) | POST | `/vcpcloud/api/padApi/listInstalledApp` |
| [`set_keep_alive_app`](#set-keep-alive-app--set-app-keep-alive) | POST | `/vcpcloud/api/padApi/setKeepAliveApp` |
| [`add_user_rom`](#add-user-rom--upload-user-image) | POST | `/vcpcloud/api/padApi/addUserRom` |
| [`install_app`](#install-app--application-installation) | POST | `/vcpcloud/api/padApi/installApp` |
| [`start_app`](#start-app--app-start) | POST | `/vcpcloud/api/padApi/startApp` |
| [`stop_app`](#stop-app--stop-app) | POST | `/vcpcloud/api/padApi/stopApp` |
| [`restart_app`](#restart-app--application-restart) | POST | `/vcpcloud/api/padApi/restartApp` |

[Về trang chính](README.md)

---

### `update_sim` — Modify SIM Card Information Based on Country Code

Static setting of Android modification properties, requires instance restart to take effect, generally used for modifying device information. Same function as [Modify Instance Android Modification Properties], difference: randomly generates SIM info and always restarts. Properties persistently stored.

- **Endpoint**: `POST /vcpcloud/api/padApi/updateSIM`

**Chữ ký hàm**

```python
client.apps.update_sim(pad_code, *, country_code=None, props=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance ID |
| `country_code` | `countryCode` | String | không | Country code |
| `props` | `props` | Object | không | System properties (key-value) |

**Các trường con của `props`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `ro.product.vendor.name` | String | Property setting |

**Ví dụ** (JSON payload)

```json
{
    "padCode": "AC32010250001",
    "props": {
        "persist.sys.cloud.phonenum": "1234578998"
    },
    "countryCode": "US"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `upload_file_v3` — File Upload via Link Directly

Push file from file management center to cloud phone instance (async task). If file found by md5 or file ID, directly use OSS path for download. If not in OSS, send URL for download and upload content to OSS. If auto install app, check package name; if empty, throw exception. (Auto install grants all permissions by default; use isAuthorization to disable).

- **Endpoint**: `POST /vcpcloud/api/padApi/uploadFileV3`

**Chữ ký hàm**

```python
client.apps.upload_file_v3(pad_codes, *, auto_install=None, file_unique_id=None, customize_file_path=None, file_name=None, package_name=None, url=None, md5=None, is_authorization=None, icon_path=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | có |  |
| `auto_install` | `autoInstall` | Integer | không | Auto install: 1-yes, 0-no (default no). Only for APK |
| `file_unique_id` | `fileUniqueId` | String | không | File unique ID |
| `customize_file_path` | `customizeFilePath` | String | không | Custom path (start with /, e.g. "/DCIM/", "/Documents/" etc.) |
| `file_name` | `fileName` | String | không | File name |
| `package_name` | `packageName` | String | không | Package name |
| `url` | `url` | String | không | File URL |
| `md5` | `md5` | String | không | File MD5 |
| `is_authorization` | `isAuthorization` | Boolean | không | Grant permissions (default all) |
| `icon_path` | `iconPath` | String | không | Icon for install |

**Các trường con của `padCodes`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `padCode` | String | Instance code |

**Ví dụ** (JSON payload)

```json
{
    "padCodes": [
        "AC32010250022"
    ],
    "customizeFilePath": "/DCIM/",
    "md5": "d97fb05b3a07d8werw2341f10212sdfs3sdfs24",
    "url": "https://file.vmoscloud.com/appMarket/2/apk/fe1f75df23e6fe3fd3b31c0f7f60c0af.apk",
    "autoInstall": 1,
    "packageName": "com.zhiliaoapp.musically",
    "fileName": "market",
    "isAuthorization": false
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `batch_upload_file` — Batch Upload Files

Push different files to multiple cloud phone instances in a single call (e.g. different videos to different instances). Each item in `list` specifies a group of instances and its file. Items are processed independently; a failure of one item does not affect the others. Up to 100 items per call.

- **Endpoint**: `POST /vcpcloud/api/padApi/batchUploadFile`

**Chữ ký hàm**

```python
client.apps.batch_upload_file(list, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `list` | `list` | Object[] | có | Upload item list, up to 100 items per call |

**Các trường con của `list`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `padCodes` | String[] | Target instance codes, multiple allowed |
| `url` | String | File download URL |
| `autoInstall` | Integer | Auto install: 1-yes, 0-no, apk only |
| `customizeFilePath` | String | Custom path, must start with / |
| `fileName` | String | File name |
| `md5` | String | File unique identifier |

**Ví dụ** (JSON payload)

```json
{
    "list": [
        {
            "padCodes": ["AC32010250011"],
            "url": "https://file.vmoscloud.com/userFile/video1.mp4",
            "customizeFilePath": "/Movies/",
            "fileName": "video1"
        },
        {
            "padCodes": ["AC32010250022"],
            "url": "https://file.vmoscloud.com/userFile/video2.mp4",
            "customizeFilePath": "/Movies/",
            "fileName": "video2"
        }
    ]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `list_installed_app` — Real-Time Query Installed Apps List

- **Endpoint**: `POST /vcpcloud/api/padApi/listInstalledApp`

**Chữ ký hàm**

```python
client.apps.list_installed_app(pad_codes, *, app_name=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | có | Instance codes |
| `app_name` | `appName` | String | không | App name |

**Ví dụ** (JSON payload)

```json
{
 "padCodes": ["AC32010250001"],
 "appName": ""
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `set_keep_alive_app` — Set App Keep-Alive

Currently supports Android 13,14,15 only.

- **Endpoint**: `POST /vcpcloud/api/padApi/setKeepAliveApp`

**Chữ ký hàm**

```python
client.apps.set_keep_alive_app(apply_all_instances, *, pad_codes=None, app_infos=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | không | Instance codes |
| `apply_all_instances` | `applyAllInstances` | Boolean | có | Apply to all instances mode |
| `app_infos` | `appInfos` | Object[] | không |  |

**Các trường con của `appInfos`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `serverName` | String | com.xxx.xxx (package)/com.xxx.xxx.service.DomeService (full service path) |

**Ví dụ** (JSON payload)

```json
{
 "padCodes": [
  "AC002",
  "AC001"
 ],
 "appInfos": [{
   "serverName": "com.example/com.example.service.TaskService"
  }
 ],
 "applyAllInstances": false
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `add_user_rom` — Upload User Image

- **Endpoint**: `POST /vcpcloud/api/padApi/addUserRom`

**Chữ ký hàm**

```python
client.apps.add_user_rom(name, update_log, android_version, version, download_url, package_size, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `name` | `name` | String | có | ROM name |
| `update_log` | `updateLog` | String | có | Update log |
| `android_version` | `androidVersion` | String | có | Android version |
| `version` | `version` | String | có | Version |
| `download_url` | `downloadUrl` | String | có | Download URL |
| `package_size` | `packageSize` | String | có | Size (bytes) |

**Ví dụ** (JSON payload)

```json
{
    "name": "CloudROM-13-11",
    "updateLog": "更新日志",
    "androidVersion": "13",
    "version": "v1.0.0",
    "downloadUrl": "https://file.vmoscloud.com/userFile/userRom/d281d848eff49adee2dda2475235b80b2.tar",
    "packageSize": 236978175,
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `install_app` — Application Installation

Install one or more apps on one or more instances at once. This API is asynchronous and supports allowlist/blocklist logic.

- **Endpoint**: `POST /vcpcloud/api/padApi/installApp`

**Chữ ký hàm**

```python
client.apps.install_app(apps, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `apps` | `apps` | Object[] | có | Application list |

**Các trường con của `apps`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `appId` | Integer | Application ID |
| `appName` | String | Application name |
| `pkgName` | String | Package name |
| `isGrantAllPerm` | Boolean | Grant all permissions (default true) |
| `padCodes` | String[] |  |
| `` | String | Instance code |

**Ví dụ** (JSON payload)

```json
{
 "apps":[
  {
   "appId":124,
   "appName":"AppName",
   "pkgName":"com.huluxia.gametools",
   "isGrantAllPerm":false,
   "padCodes":["AC22010020062"]
  }
 ]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `start_app` — App Start

Start an app on an instance based on the instance ID and app package name.

- **Endpoint**: `POST /vcpcloud/api/padApi/startApp`

**Chữ ký hàm**

```python
client.apps.start_app(pkg_name, pad_codes, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pkg_name` | `pkgName` | String | có | Package Name |
| `pad_codes` | `padCodes` | String[] | có |  |

**Các trường con của `padCodes`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | String | Instance Code |

**Ví dụ** (JSON payload)

```json
{
	"padCodes": [
		"AC22010020062"
	],
	"pkgName": "xxx.test.com"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `stop_app` — Stop App

Perform the operation of stopping an app on an instance based on the instance ID and app package name.

- **Endpoint**: `POST /vcpcloud/api/padApi/stopApp`

**Chữ ký hàm**

```python
client.apps.stop_app(pkg_name, pad_codes, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pkg_name` | `pkgName` | String | có | Package Name |
| `pad_codes` | `padCodes` | String[] | có | Instance IDs |

**Các trường con của `padCodes`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | String | Instance ID |

**Ví dụ** (JSON payload)

```json
{
	"padCodes": [
		"AC22010020062"
	],
	"pkgName": "xxx.test.com"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `restart_app` — Application Restart

Restart an application on an instance based on the instance ID and application package name.

- **Endpoint**: `POST /vcpcloud/api/padApi/restartApp`

**Chữ ký hàm**

```python
client.apps.restart_app(pkg_name, pad_codes, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pkg_name` | `pkgName` | String | có | Package name |
| `pad_codes` | `padCodes` | String[] | có | Instance IDs |

**Các trường con của `padCodes`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | String | Instance ID |

**Ví dụ** (JSON payload)

```json
{
	"padCodes": [
		"AC22010020062"
	],
	"pkgName": xxx.test.com
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
