# `client.static_proxy` — Static Residential Proxy

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Static residential IP goods, orders, proxy create/renew/manage.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`proxy_good_list`](#proxy-good-list--get-static-residential-product-list) | GET | `/vcpcloud/api/padApi/proxyGoodList` |
| [`get_proxy_region`](#get-proxy-region--get-supported-countries-cities-for-static-residential-products) | GET | `/vcpcloud/api/padApi/getProxyRegion` |
| [`create_proxy_order`](#create-proxy-order--purchase-static-residential-product) | POST | `/vcpcloud/api/padApi/createProxyOrder` |
| [`select_proxy_order_list`](#select-proxy-order-list--static-residential-proxy-order-details) | POST | `/vcpcloud/api/padApi/selectProxyOrderList` |
| [`create_renew_proxy_order`](#create-renew-proxy-order--static-residential-proxy-renewal) | POST | `/vcpcloud/api/padApi/createRenewProxyOrder` |
| [`query_proxy_list`](#query-proxy-list--query-static-residential-proxy-list) | POST | `/vcpcloud/api/padApi/queryProxyList` |
| [`del_proxy_by_host`](#del-proxy-by-host--delete-static-residential-proxy) | POST | `/vcpcloud/api/padApi/delProxyByHost` |

[Back to index](README.md)

---

### `proxy_good_list` — Get Static Residential Product List

- **Endpoint**: `GET /vcpcloud/api/padApi/proxyGoodList`

**Signature**

```python
client.static_proxy.proxy_good_list(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_proxy_region` — Get Supported Countries/Cities for Static Residential Products

- **Endpoint**: `GET /vcpcloud/api/padApi/getProxyRegion`

**Signature**

```python
client.static_proxy.get_proxy_region(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `create_proxy_order` — Purchase Static Residential Product

- **Endpoint**: `POST /vcpcloud/api/padApi/createProxyOrder`

**Signature**

```python
client.static_proxy.create_proxy_order(*, proxy_good_id=None, region=None, num=None, country=None, proxy_address=None, auto_renew=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `proxy_good_id` | `proxyGoodId` | Integer | no | Unique ID of the corresponding static residential product |
| `region` | `region` | String | no | Region of static residential proxy-country |
| `num` | `num` | Integer | no | Purchase quantity |
| `country` | `country` | String | no | Country of static residential proxy-country |
| `proxy_address` | `proxyAddress` | String | no | Address of static residential proxy-countryZh |
| `auto_renew` | `autoRenew` | Boolean | no | Enable auto-renew false-off true-on |

**Example** (JSON payload)

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

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `select_proxy_order_list` — Static Residential Proxy Order Details

- **Endpoint**: `POST /vcpcloud/api/padApi/selectProxyOrderList`

**Signature**

```python
client.static_proxy.select_proxy_order_list(*, page=None, rows=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Page number |
| `rows` | `rows` | Integer | no | Items per page |

**Example** (JSON payload)

```json
{
    "page": 1,
    "rows": 10
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `create_renew_proxy_order` — Static Residential Proxy Renewal

- **Endpoint**: `POST /vcpcloud/api/padApi/createRenewProxyOrder`

**Signature**

```python
client.static_proxy.create_renew_proxy_order(*, proxy_good_id=None, proxy_ips=None, auto_renew=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `proxy_good_id` | `proxyGoodId` | Integer | no | Unique ID of the corresponding static residential product |
| `proxy_ips` | `proxyIps` | String | no | IPs to renew, separated by commas |
| `auto_renew` | `autoRenew` | Boolean | no | Enable auto-renew false-off true-on |

**Example** (JSON payload)

```json
{
    "proxyGoodId": 4,
    "proxyIps": "154.81.41.161,154.81.41.162",
    "autoRenew": true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `query_proxy_list` — Query Static Residential Proxy List

- **Endpoint**: `POST /vcpcloud/api/padApi/queryProxyList`

**Signature**

```python
client.static_proxy.query_proxy_list(*, current=None, size=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `current` | `current` | Integer | no | Page number |
| `size` | `size` | Integer | no | Items per page |

**Example** (JSON payload)

```json
{
    "current": 1,
    "size": 10
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `del_proxy_by_host` — Delete Static Residential Proxy

Delete a static residential proxy under your own account by proxy address, port and username. Cloud phones currently using the proxy are automatically unbound from it. If several proxies share the same address, port and username, all of them are deleted. When no proxy matches, the request still succeeds and `data` is 0.

- **Endpoint**: `POST /vcpcloud/api/padApi/delProxyByHost`

**Signature**

```python
client.static_proxy.del_proxy_by_host(*, host=None, port=None, account=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `host` | `host` | String | no | Proxy address |
| `port` | `port` | Integer | no | Proxy port |
| `account` | `account` | String | no | Proxy username |

**Example** (JSON payload)

```json
{
    "host": "154.81.40.200",
    "port": 63007,
    "account": "xxxxxx"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
