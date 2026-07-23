# `client.static_proxy` — Proxy dân cư tĩnh

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Gói IP dân cư tĩnh, đơn hàng, tạo/gia hạn/quản lý proxy.

## Danh sách phương thức

| Python | HTTP | Endpoint |
|---|---|---|
| [`proxy_good_list`](#proxy-good-list--get-static-residential-product-list) | GET | `/vcpcloud/api/padApi/proxyGoodList` |
| [`get_proxy_region`](#get-proxy-region--get-supported-countries-cities-for-static-residential-products) | GET | `/vcpcloud/api/padApi/getProxyRegion` |
| [`create_proxy_order`](#create-proxy-order--purchase-static-residential-product) | POST | `/vcpcloud/api/padApi/createProxyOrder` |
| [`select_proxy_order_list`](#select-proxy-order-list--static-residential-proxy-order-details) | POST | `/vcpcloud/api/padApi/selectProxyOrderList` |
| [`create_renew_proxy_order`](#create-renew-proxy-order--static-residential-proxy-renewal) | POST | `/vcpcloud/api/padApi/createRenewProxyOrder` |
| [`query_proxy_list`](#query-proxy-list--query-static-residential-proxy-list) | POST | `/vcpcloud/api/padApi/queryProxyList` |
| [`del_proxy_by_host`](#del-proxy-by-host--delete-static-residential-proxy) | POST | `/vcpcloud/api/padApi/delProxyByHost` |

[Về trang chính](README.md)

---

### `proxy_good_list` — Get Static Residential Product List

- **Endpoint**: `GET /vcpcloud/api/padApi/proxyGoodList`

**Chữ ký hàm**

```python
client.static_proxy.proxy_good_list(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_proxy_region` — Get Supported Countries/Cities for Static Residential Products

- **Endpoint**: `GET /vcpcloud/api/padApi/getProxyRegion`

**Chữ ký hàm**

```python
client.static_proxy.get_proxy_region(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `create_proxy_order` — Purchase Static Residential Product

- **Endpoint**: `POST /vcpcloud/api/padApi/createProxyOrder`

**Chữ ký hàm**

```python
client.static_proxy.create_proxy_order(*, proxy_good_id=None, region=None, num=None, country=None, proxy_address=None, auto_renew=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `proxy_good_id` | `proxyGoodId` | Integer | không | Unique ID of the corresponding static residential product |
| `region` | `region` | String | không | Region of static residential proxy-country |
| `num` | `num` | Integer | không | Purchase quantity |
| `country` | `country` | String | không | Country of static residential proxy-country |
| `proxy_address` | `proxyAddress` | String | không | Address of static residential proxy-countryZh |
| `auto_renew` | `autoRenew` | Boolean | không | Enable auto-renew false-off true-on |

**Ví dụ** (JSON payload)

```json
{
    "proxyGoodId": 4,
    "region": "cn",
    "num": 1,
    "country": "cn",
    "proxyAddress": "China",
    "autoRenew": true
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `select_proxy_order_list` — Static Residential Proxy Order Details

- **Endpoint**: `POST /vcpcloud/api/padApi/selectProxyOrderList`

**Chữ ký hàm**

```python
client.static_proxy.select_proxy_order_list(*, page=None, rows=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `page` | `page` | Integer | không | Page number |
| `rows` | `rows` | Integer | không | Items per page |

**Ví dụ** (JSON payload)

```json
{
    "page": 1,
    "rows": 10
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `create_renew_proxy_order` — Static Residential Proxy Renewal

- **Endpoint**: `POST /vcpcloud/api/padApi/createRenewProxyOrder`

**Chữ ký hàm**

```python
client.static_proxy.create_renew_proxy_order(*, proxy_good_id=None, proxy_ips=None, auto_renew=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `proxy_good_id` | `proxyGoodId` | Integer | không | Unique ID of the corresponding static residential product |
| `proxy_ips` | `proxyIps` | String | không | IPs to renew, separated by commas |
| `auto_renew` | `autoRenew` | Boolean | không | Enable auto-renew false-off true-on |

**Ví dụ** (JSON payload)

```json
{
    "proxyGoodId": 4,
    "proxyIps": "154.81.41.161,154.81.41.162",
    "autoRenew": true
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `query_proxy_list` — Query Static Residential Proxy List

- **Endpoint**: `POST /vcpcloud/api/padApi/queryProxyList`

**Chữ ký hàm**

```python
client.static_proxy.query_proxy_list(*, current=None, size=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `current` | `current` | Integer | không | Page number |
| `size` | `size` | Integer | không | Items per page |

**Ví dụ** (JSON payload)

```json
{
    "current": 1,
    "size": 10
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `del_proxy_by_host` — Delete Static Residential Proxy

Delete a static residential proxy under your own account by proxy address, port and username. Cloud phones currently using the proxy are automatically unbound from it. If several proxies share the same address, port and username, all of them are deleted. When no proxy matches, the request still succeeds and `data` is 0.

- **Endpoint**: `POST /vcpcloud/api/padApi/delProxyByHost`

**Chữ ký hàm**

```python
client.static_proxy.del_proxy_by_host(*, host=None, port=None, account=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `host` | `host` | String | không | Proxy address |
| `port` | `port` | Integer | không | Proxy port |
| `account` | `account` | String | không | Proxy username |

**Ví dụ** (JSON payload)

```json
{
    "host": "154.81.40.200",
    "port": 63007,
    "account": "xxxxxx"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
