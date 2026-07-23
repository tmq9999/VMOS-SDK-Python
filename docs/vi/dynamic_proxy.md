# `client.dynamic_proxy` — Proxy động

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Khu vực proxy động, gói, đơn hàng, số dư lưu lượng, cấu hình proxy cho từng máy.

## Danh sách phương thức

| Python | HTTP | Endpoint |
|---|---|---|
| [`get_dynamic_good_service`](#get-dynamic-good-service--query-dynamic-proxy-product-list) | GET | `/vcpcloud/api/padApi/getDynamicGoodService` |
| [`get_dynamic_proxy_region`](#get-dynamic-proxy-region--query-dynamic-proxy-region-list) | GET | `/vcpcloud/api/padApi/getDynamicProxyRegion` |
| [`query_current_traffic_balance`](#query-current-traffic-balance--get-dynamic-proxy-current-balance) | GET | `/vcpcloud/api/padApi/queryCurrentTrafficBalance` |
| [`get_dynamic_proxy_host`](#get-dynamic-proxy-host--query-supported-server-regions) | GET | `/vcpcloud/api/padApi/getDynamicProxyHost` |
| [`buy_dynamic_proxy`](#buy-dynamic-proxy--purchase-dynamic-proxy-traffic-package) | POST | `/vcpcloud/api/padApi/buyDynamicProxy` |
| [`create_proxy`](#create-proxy--create-dynamic-proxy) | POST | `/vcpcloud/api/padApi/createProxy` |
| [`get_proxys`](#get-proxys--get-proxys) | GET | `/vcpcloud/api/padApi/getProxys` |
| [`get_dynamic_proxy_orders`](#get-dynamic-proxy-orders--get-dynamic-proxy-orders) | POST | `/vcpcloud/api/padApi/getDynamicProxyOrders` |
| [`batch_pad_config_proxy`](#batch-pad-config-proxy--configure-dynamic-proxy-for-cloud-phone) | POST | `/vcpcloud/api/padApi/batchPadConfigProxy` |
| [`select_batch_pad_proxy_task`](#select-batch-pad-proxy-task--query-batch-cloud-phone-proxy-setting-task) | POST | `/vcpcloud/api/padApi/selectBatchPadProxyTask` |
| [`get_dynamic_proxy_automatic_renewal`](#get-dynamic-proxy-automatic-renewal--query-dynamic-proxy-auto-renew-information) | GET | `/vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal` |
| [`set_auto_renew_switch`](#set-auto-renew-switch--set-dynamic-proxy-auto-renew-switch) | POST | `/vcpcloud/api/padApi/setAutoRenewSwitch` |
| [`del_proxy_by_ids`](#del-proxy-by-ids--delete-dynamic-proxy) | POST | `/vcpcloud/api/padApi/delProxyByIds` |

[Về trang chính](README.md)

---

### `get_dynamic_good_service` — Query Dynamic Proxy Product List

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicGoodService`

**Chữ ký hàm**

```python
client.dynamic_proxy.get_dynamic_good_service(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_dynamic_proxy_region` — Query Dynamic Proxy Region List

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicProxyRegion`

**Chữ ký hàm**

```python
client.dynamic_proxy.get_dynamic_proxy_region(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `query_current_traffic_balance` — Get Dynamic Proxy Current Balance

- **Endpoint**: `GET /vcpcloud/api/padApi/queryCurrentTrafficBalance`

**Chữ ký hàm**

```python
client.dynamic_proxy.query_current_traffic_balance(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_dynamic_proxy_host` — Query Supported Server Regions

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicProxyHost`

**Chữ ký hàm**

```python
client.dynamic_proxy.get_dynamic_proxy_host(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `buy_dynamic_proxy` — Purchase Dynamic Proxy Traffic Package

- **Endpoint**: `POST /vcpcloud/api/padApi/buyDynamicProxy`

**Chữ ký hàm**

```python
client.dynamic_proxy.buy_dynamic_proxy(*, good_id=None, good_num=None, auto_renew_order=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `good_id` | `goodId` | Integer | không | Unique ID of the corresponding dynamic traffic package |
| `good_num` | `goodNum` | Integer | không | Purchase quantity |
| `auto_renew_order` | `autoRenewOrder` | Integer | không | Enable auto-renew 0-off 1-on. When remaining traffic is less than 50MB, auto-renew is triggered |

**Ví dụ** (JSON payload)

```json
{
    "goodId": 1,
    "goodNum": 1,
    "autoRenewOrder": 0
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `create_proxy` — Create Dynamic Proxy

- **Endpoint**: `POST /vcpcloud/api/padApi/createProxy`

**Chữ ký hàm**

```python
client.dynamic_proxy.create_proxy(*, city=None, country_code=None, good_num=None, proxy_host=None, proxy_type=None, proxy_use_type=None, state=None, time=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `city` | `city` | String | không | City, pass "" if not selected |
| `country_code` | `countryCode` | String | không | Country Code |
| `good_num` | `goodNum` | Integer | không | Purchase quantity |
| `proxy_host` | `proxyHost` | String | không | Continent website |
| `proxy_type` | `proxyType` | String | không | Proxy type socks5 / http / https |
| `proxy_use_type` | `proxyUseType` | String | không | Mount type proxy / vpm |
| `state` | `state` | String | không | Region, pass "" if not selected |
| `time` | `time` | String | không | Auto change ip frequency (minutes) Options: 5, 10, 15, 30, 45, 60, 90 |

**Ví dụ** (JSON payload)

```json
{
    "proxyHost": "xxxxx:7778",
    "countryCode": "CN",
    "state": "Sichuan",
    "city": "Sichuan",
    "time": 5,
    "proxyType": "socks5",
    "proxyUseType": "vpn"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_proxys` — Get Proxys

- **Endpoint**: `GET /vcpcloud/api/padApi/getProxys`

**Chữ ký hàm**

```python
client.dynamic_proxy.get_proxys(*, page=None, rows=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `page` | `page` | Integer | không | Current page |
| `rows` | `rows` | Integer | không | Items per page |

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_dynamic_proxy_orders` — Get Dynamic Proxy Orders

- **Endpoint**: `POST /vcpcloud/api/padApi/getDynamicProxyOrders`

**Chữ ký hàm**

```python
client.dynamic_proxy.get_dynamic_proxy_orders(*, page=None, rows=None, complete_start_time=None, complete_end_time=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `page` | `page` | Integer | không | Current page |
| `rows` | `rows` | Integer | không | Items per page |
| `complete_start_time` | `completeStartTime` | String | không | Payment start time |
| `complete_end_time` | `completeEndTime` | String | không | Payment end time |

**Ví dụ** (JSON payload)

```json
{
   "page": 1,
   "rows": 10,
   "completeStartTime": "2025-02-27 23:20:36",
   "completeEndTime": "2025-02-28 23:20:36"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `batch_pad_config_proxy` — Configure Dynamic Proxy for Cloud Phone

- **Endpoint**: `POST /vcpcloud/api/padApi/batchPadConfigProxy`

**Chữ ký hàm**

```python
client.dynamic_proxy.batch_pad_config_proxy(*, pad_codes=None, set_proxy_flag=None, proxy_ids=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | không | Cloud phone collection |
| `set_proxy_flag` | `setProxyFlag` | Boolean | không | Whether device proxies to cloud phone |
| `proxy_ids` | `proxyIds` | Array | không | Dynamic Proxy unique ID |

**Các trường con của `padCodes`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | String | Cloud phone number |

**Ví dụ** (JSON payload)

```json
{
    "padCodes": [
        "AC32010921223"
    ],
    "setProxyFlag": true,
    "proxyIds":  [
        82750
    ]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `select_batch_pad_proxy_task` — Query Batch Cloud Phone Proxy Setting Task

- **Endpoint**: `POST /vcpcloud/api/padApi/selectBatchPadProxyTask`

**Chữ ký hàm**

```python
client.dynamic_proxy.select_batch_pad_proxy_task(*, task_id=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `task_id` | `taskId` | Integer | không | Batch ID, mounting proxy is an asynchronous operation, so need to wait 5s or loop query |

**Ví dụ** (JSON payload)

```json
{
    "taskId": "1cb0ba24-cdc2-47d3-909d-d7ea2ab10576"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_dynamic_proxy_automatic_renewal` — Query Dynamic Proxy Auto-Renew Information

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal`

**Chữ ký hàm**

```python
client.dynamic_proxy.get_dynamic_proxy_automatic_renewal(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `set_auto_renew_switch` — Set Dynamic Proxy Auto-Renew Switch

- **Endpoint**: `POST /vcpcloud/api/padApi/setAutoRenewSwitch`

**Chữ ký hàm**

```python
client.dynamic_proxy.set_auto_renew_switch(*, auto_renew_order=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `auto_renew_order` | `autoRenewOrder` | Integer | không | Auto-renew switch 0-off 1-on |

**Ví dụ** (JSON payload)

```json
{
    "autoRenewOrder": 0
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `del_proxy_by_ids` — Delete Dynamic Proxy

- **Endpoint**: `POST /vcpcloud/api/padApi/delProxyByIds`

**Chữ ký hàm**

```python
client.dynamic_proxy.del_proxy_by_ids(*, ids=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `ids` | `ids` | Integer[] | không | Collection of dynamic proxy IDs to delete |

**Các trường con của `ids`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | Integer | Dynamic proxy unique ID |

**Ví dụ** (JSON payload)

```json
{
    "ids": [
        1
    ]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
