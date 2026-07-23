# `client.dynamic_proxy` — Dynamic Proxy

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Dynamic proxy regions, goods, orders, traffic balance, per-pad proxy config.

## Methods

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

[Back to index](README.md)

---

### `get_dynamic_good_service` — Query Dynamic Proxy Product List

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicGoodService`

**Signature**

```python
client.dynamic_proxy.get_dynamic_good_service(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_dynamic_proxy_region` — Query Dynamic Proxy Region List

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicProxyRegion`

**Signature**

```python
client.dynamic_proxy.get_dynamic_proxy_region(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `query_current_traffic_balance` — Get Dynamic Proxy Current Balance

- **Endpoint**: `GET /vcpcloud/api/padApi/queryCurrentTrafficBalance`

**Signature**

```python
client.dynamic_proxy.query_current_traffic_balance(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_dynamic_proxy_host` — Query Supported Server Regions

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicProxyHost`

**Signature**

```python
client.dynamic_proxy.get_dynamic_proxy_host(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `buy_dynamic_proxy` — Purchase Dynamic Proxy Traffic Package

- **Endpoint**: `POST /vcpcloud/api/padApi/buyDynamicProxy`

**Signature**

```python
client.dynamic_proxy.buy_dynamic_proxy(*, good_id=None, good_num=None, auto_renew_order=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `good_id` | `goodId` | Integer | no | Unique ID of the corresponding dynamic traffic package |
| `good_num` | `goodNum` | Integer | no | Purchase quantity |
| `auto_renew_order` | `autoRenewOrder` | Integer | no | Enable auto-renew 0-off 1-on. When remaining traffic is less than 50MB, auto-renew is triggered |

**Example** (JSON payload)

```json
{
    "goodId": 1,
    "goodNum": 1,
    "autoRenewOrder": 0
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `create_proxy` — Create Dynamic Proxy

- **Endpoint**: `POST /vcpcloud/api/padApi/createProxy`

**Signature**

```python
client.dynamic_proxy.create_proxy(*, city=None, country_code=None, good_num=None, proxy_host=None, proxy_type=None, proxy_use_type=None, state=None, time=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `city` | `city` | String | no | City, pass "" if not selected |
| `country_code` | `countryCode` | String | no | Country Code |
| `good_num` | `goodNum` | Integer | no | Purchase quantity |
| `proxy_host` | `proxyHost` | String | no | Continent website |
| `proxy_type` | `proxyType` | String | no | Proxy type socks5 / http / https |
| `proxy_use_type` | `proxyUseType` | String | no | Mount type proxy / vpm |
| `state` | `state` | String | no | Region, pass "" if not selected |
| `time` | `time` | String | no | Auto change ip frequency (minutes) Options: 5, 10, 15, 30, 45, 60, 90 |

**Example** (JSON payload)

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

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_proxys` — Get Proxys

- **Endpoint**: `GET /vcpcloud/api/padApi/getProxys`

**Signature**

```python
client.dynamic_proxy.get_proxys(*, page=None, rows=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Current page |
| `rows` | `rows` | Integer | no | Items per page |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_dynamic_proxy_orders` — Get Dynamic Proxy Orders

- **Endpoint**: `POST /vcpcloud/api/padApi/getDynamicProxyOrders`

**Signature**

```python
client.dynamic_proxy.get_dynamic_proxy_orders(*, page=None, rows=None, complete_start_time=None, complete_end_time=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Current page |
| `rows` | `rows` | Integer | no | Items per page |
| `complete_start_time` | `completeStartTime` | String | no | Payment start time |
| `complete_end_time` | `completeEndTime` | String | no | Payment end time |

**Example** (JSON payload)

```json
{
   "page": 1,
   "rows": 10,
   "completeStartTime": "2025-02-27 23:20:36",
   "completeEndTime": "2025-02-28 23:20:36"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `batch_pad_config_proxy` — Configure Dynamic Proxy for Cloud Phone

- **Endpoint**: `POST /vcpcloud/api/padApi/batchPadConfigProxy`

**Signature**

```python
client.dynamic_proxy.batch_pad_config_proxy(*, pad_codes=None, set_proxy_flag=None, proxy_ids=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | no | Cloud phone collection |
| `set_proxy_flag` | `setProxyFlag` | Boolean | no | Whether device proxies to cloud phone |
| `proxy_ids` | `proxyIds` | Array | no | Dynamic Proxy unique ID |

**Nested fields of `padCodes`:**

| API name | Type | Description |
|---|---|---|
| `` | String | Cloud phone number |

**Example** (JSON payload)

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

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `select_batch_pad_proxy_task` — Query Batch Cloud Phone Proxy Setting Task

- **Endpoint**: `POST /vcpcloud/api/padApi/selectBatchPadProxyTask`

**Signature**

```python
client.dynamic_proxy.select_batch_pad_proxy_task(*, task_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Integer | no | Batch ID, mounting proxy is an asynchronous operation, so need to wait 5s or loop query |

**Example** (JSON payload)

```json
{
    "taskId": "1cb0ba24-cdc2-47d3-909d-d7ea2ab10576"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_dynamic_proxy_automatic_renewal` — Query Dynamic Proxy Auto-Renew Information

- **Endpoint**: `GET /vcpcloud/api/padApi/getDynamicProxyAutomaticRenewal`

**Signature**

```python
client.dynamic_proxy.get_dynamic_proxy_automatic_renewal(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `set_auto_renew_switch` — Set Dynamic Proxy Auto-Renew Switch

- **Endpoint**: `POST /vcpcloud/api/padApi/setAutoRenewSwitch`

**Signature**

```python
client.dynamic_proxy.set_auto_renew_switch(*, auto_renew_order=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `auto_renew_order` | `autoRenewOrder` | Integer | no | Auto-renew switch 0-off 1-on |

**Example** (JSON payload)

```json
{
    "autoRenewOrder": 0
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `del_proxy_by_ids` — Delete Dynamic Proxy

- **Endpoint**: `POST /vcpcloud/api/padApi/delProxyByIds`

**Signature**

```python
client.dynamic_proxy.del_proxy_by_ids(*, ids=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `ids` | Integer[] | no | Collection of dynamic proxy IDs to delete |

**Nested fields of `ids`:**

| API name | Type | Description |
|---|---|---|
| `` | Integer | Dynamic proxy unique ID |

**Example** (JSON payload)

```json
{
    "ids": [
        1
    ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
