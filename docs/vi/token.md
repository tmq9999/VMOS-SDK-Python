# `client.token` — SDK Token

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Cấp & xóa token STS tạm thời cho SDK phía client.

## Danh sách phương thức

| Python | HTTP | Endpoint |
|---|---|---|
| [`sts_token_by_pad_code`](#sts-token-by-pad-code--get-sdk-temporary-token-by-padcode) | POST | `/vcpcloud/api/padApi/stsTokenByPadCode` |
| [`clear_sts_token`](#clear-sts-token--clear-sdk-authorization-token) | POST | `/vcpcloud/api/padApi/clearStsToken` |

[Về trang chính](README.md)

---

### `sts_token_by_pad_code` — Get SDK Temporary Token by padCode

- **Endpoint**: `POST /vcpcloud/api/padApi/stsTokenByPadCode`

**Chữ ký hàm**

```python
client.token.sts_token_by_pad_code(pad_code, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | có | Instance ID (padCode) |

**Ví dụ** (JSON payload)

```json
{"padCode":"AC32010230001"}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `clear_sts_token` — Clear SDK Authorization Token

- **Endpoint**: `POST /vcpcloud/api/padApi/clearStsToken`

**Chữ ký hàm**

```python
client.token.clear_sts_token(token, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `token` | `token` | String | có | The token to be cleared |

**Ví dụ** (JSON payload)

```json
{"token":1234}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
