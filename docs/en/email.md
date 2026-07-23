# `client.email` — Email Verification Service

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Email types & stock, purchase orders, verification-code retrieval.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`get_email_service_list`](#get-email-service-list--get-email-service-list) | GET | `/vcpcloud/api/padApi/getEmailServiceList` |
| [`get_email_type_list`](#get-email-type-list--get-email-type-and-remaining-stock) | GET | `/vcpcloud/api/padApi/getEmailTypeList` |
| [`create_email_order`](#create-email-order--create-email-purchase-order) | POST | `/vcpcloud/api/padApi/createEmailOrder` |
| [`get_email_order`](#get-email-order--query-purchased-email-list) | GET | `/vcpcloud/api/padApi/getEmailOrder` |
| [`get_email_code`](#get-email-code--refresh-to-get-email-verification-code) | GET | `/vcpcloud/api/padApi/getEmailCode` |

[Back to index](README.md)

---

### `get_email_service_list` — Get Email Service List

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailServiceList`

**Signature**

```python
client.email.get_email_service_list(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_email_type_list` — Get Email Type and Remaining Stock

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailTypeList`

**Signature**

```python
client.email.get_email_type_list(*, service_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `service_id` | `serviceId` | Integer | no | Corresponds to serviceItemId field |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `create_email_order` — Create Email Purchase Order

- **Endpoint**: `POST /vcpcloud/api/padApi/createEmailOrder`

**Signature**

```python
client.email.create_email_order(*, service_id=None, email_type_id=None, good_num=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `service_id` | `serviceId` | Integer | no | Corresponds to serviceItemId field |
| `email_type_id` | `emailTypeId` | Integer | no | Corresponds to ID field returned by /getEmailTypeList |
| `good_num` | `goodNum` | Integer | no | Purchase quantity |

**Example** (JSON payload)

```json
{
    "serviceId": 1,
    "emailTypeId": 1,
    "goodNum": 1
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_email_order` — Query Purchased Email List

When the verification code cannot be obtained through the refresh interface, you can query the result through: [https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=](https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=) + outOrderId (external order number)

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailOrder`

**Signature**

```python
client.email.get_email_order(*, page=None, size=None, service_id=None, email=None, status=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Required, pagination parameter, current page |
| `size` | `size` | Integer | no | Required, pagination parameter, items per page |
| `service_id` | `serviceId` | Integer | no | Optional, corresponds to serviceItemId field |
| `email` | `email` | String | no | Optional, email fuzzy query |
| `status` | `status` | Integer | no | Optional, email status 0-unused 1-receiving 2-used 3-expired |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `get_email_code` — Refresh to Get Email Verification Code

This interface refreshes the verification code list result, need to be used together with the [Query Purchased Email List] interface

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailCode`

**Signature**

```python
client.email.get_email_code(*, order_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `order_id` | `orderId` | String | no | Required, corresponds to outOrderId field |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
