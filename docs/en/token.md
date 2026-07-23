# `client.token` — SDK Token

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Issue & clear temporary STS tokens for the client-side SDK.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`sts_token_by_pad_code`](#sts-token-by-pad-code--get-sdk-temporary-token-by-padcode) | POST | `/vcpcloud/api/padApi/stsTokenByPadCode` |
| [`clear_sts_token`](#clear-sts-token--clear-sdk-authorization-token) | POST | `/vcpcloud/api/padApi/clearStsToken` |

[Back to index](README.md)

---

### `sts_token_by_pad_code` — Get SDK Temporary Token by padCode

- **Endpoint**: `POST /vcpcloud/api/padApi/stsTokenByPadCode`

**Signature**

```python
client.token.sts_token_by_pad_code(pad_code, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_code` | `padCode` | String | yes | Instance ID (padCode) |

**Example** (JSON payload)

```json
{"padCode":"AC32010230001"}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `clear_sts_token` — Clear SDK Authorization Token

- **Endpoint**: `POST /vcpcloud/api/padApi/clearStsToken`

**Signature**

```python
client.token.clear_sts_token(token, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `token` | `token` | String | yes | The token to be cleared |

**Example** (JSON payload)

```json
{"token":1234}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
