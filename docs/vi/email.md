# `client.email` — Dịch vụ xác minh Email

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Loại email & tồn kho, đơn mua, lấy mã xác minh.

## Danh sách phương thức

| Python | HTTP | Endpoint |
|---|---|---|
| [`get_email_service_list`](#get-email-service-list--get-email-service-list) | GET | `/vcpcloud/api/padApi/getEmailServiceList` |
| [`get_email_type_list`](#get-email-type-list--get-email-type-and-remaining-stock) | GET | `/vcpcloud/api/padApi/getEmailTypeList` |
| [`create_email_order`](#create-email-order--create-email-purchase-order) | POST | `/vcpcloud/api/padApi/createEmailOrder` |
| [`get_email_order`](#get-email-order--query-purchased-email-list) | GET | `/vcpcloud/api/padApi/getEmailOrder` |
| [`get_email_code`](#get-email-code--refresh-to-get-email-verification-code) | GET | `/vcpcloud/api/padApi/getEmailCode` |

[Về trang chính](README.md)

---

### `get_email_service_list` — Get Email Service List

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailServiceList`

**Chữ ký hàm**

```python
client.email.get_email_service_list(**extra)
```

Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_email_type_list` — Get Email Type and Remaining Stock

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailTypeList`

**Chữ ký hàm**

```python
client.email.get_email_type_list(*, service_id=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `service_id` | `serviceId` | Integer | không | Corresponds to serviceItemId field |

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `create_email_order` — Create Email Purchase Order

- **Endpoint**: `POST /vcpcloud/api/padApi/createEmailOrder`

**Chữ ký hàm**

```python
client.email.create_email_order(*, service_id=None, email_type_id=None, good_num=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `service_id` | `serviceId` | Integer | không | Corresponds to serviceItemId field |
| `email_type_id` | `emailTypeId` | Integer | không | Corresponds to ID field returned by /getEmailTypeList |
| `good_num` | `goodNum` | Integer | không | Purchase quantity |

**Ví dụ** (JSON payload)

```json
{
    "serviceId": 1,
    "emailTypeId": 1,
    "goodNum": 1
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_email_order` — Query Purchased Email List

When the verification code cannot be obtained through the refresh interface, you can query the result through: [https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=](https://api.vmoscloud.com/vcpcloud/api/padApi/code?orderId=) + outOrderId (external order number)

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailOrder`

**Chữ ký hàm**

```python
client.email.get_email_order(*, page=None, size=None, service_id=None, email=None, status=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `page` | `page` | Integer | không | Required, pagination parameter, current page |
| `size` | `size` | Integer | không | Required, pagination parameter, items per page |
| `service_id` | `serviceId` | Integer | không | Optional, corresponds to serviceItemId field |
| `email` | `email` | String | không | Optional, email fuzzy query |
| `status` | `status` | Integer | không | Optional, email status 0-unused 1-receiving 2-used 3-expired |

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `get_email_code` — Refresh to Get Email Verification Code

This interface refreshes the verification code list result, need to be used together with the [Query Purchased Email List] interface

- **Endpoint**: `GET /vcpcloud/api/padApi/getEmailCode`

**Chữ ký hàm**

```python
client.email.get_email_code(*, order_id=None, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `order_id` | `orderId` | String | không | Required, corresponds to outOrderId field |

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
