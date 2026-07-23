# CLAUDE.md — Using the VMOS Cloud Python SDK

Guidance for Claude (and other AI coding assistants) writing code with this SDK.
For repo-contribution workflow (build/test/regen), see [AGENTS.md](AGENTS.md).

## What this library is

`vmos` is a complete Python SDK for the VMOS Cloud Server OpenAPI (cloud Android
phone instances). It wraps **all 152 documented endpoints** in 11 namespaces on
two clients: `VMOSClient` (sync) and `AsyncVMOSClient` (async, identical API).
Base URL: `https://api.vmoscloud.com`. Single dependency: `httpx`. Python ≥ 3.9.

```python
from vmos import VMOSClient          # sync
from vmos import AsyncVMOSClient     # async — same methods, await them
```

## Authentication

```python
client = VMOSClient(access_key="ak_...", secret_key="sk_...")
client = VMOSClient()   # falls back to env: VMOS_ACCESS_KEY / VMOS_SECRET_KEY
```

Never hardcode credentials in user code — prefer environment variables. The SDK
implements V2 signing internally (`X-Access-Key`, `X-Timestamp`, `X-Sign`); you
never construct auth headers yourself.

## Core semantics (memorize these)

1. **Return value**: every endpoint method returns the response `data` field
   directly. Non-200 business codes raise `VMOSAPIError` (subclasses:
   `VMOSAuthError` for 2019/2031/2032/2033, `VMOSRateLimitError` for throttling).
   Transport failures raise `VMOSHTTPError`. All inherit `VMOSError`.
2. **Raw envelope**: `client.request_raw(method, path, json_body=..., query=...)`
   returns an `APIResponse` (`.code`, `.msg`, `.ts`, `.data`, `.ok`) without raising
   on business errors.
3. **Naming rule**: Python arguments are `snake_case` conversions of the API's
   `camelCase` names — `padCodes` → `pad_codes`, `scriptContent` → `script_content`.
   The mapping is mechanical and documented in every docstring.
4. **Forward compatibility**: every method accepts `**extra` — those keys are sent
   verbatim in the payload. Use it for parameters newer than the SDK.
5. **`None` means "omit"**: optional arguments left as `None` are not sent at all.
6. **Escape hatch**: `client.request("POST", "/vcpcloud/api/padApi/anything",
   json_body={...})` performs a signed call to any path, wrapper or not.

## Finding the right method

- Human-readable reference: `docs/en/<namespace>.md` (also `docs/vi/`).
- **Machine-readable index**: `tests/data/endpoints_manifest.json` maps every
  endpoint path → `{module, method, http_method, params[{py, api, required, type}]}`.
  Parse it when you need exact signatures programmatically.

Namespaces: `instance` (50 — restart/reset, properties, SIM/GPS/WiFi, ADB,
screenshots, previews, image upgrade, new-device, root, media injection),
`apps` (10 — install/start/stop, APK push by URL, hidden/keep-alive lists),
`tasks` (4 — async task status), `phone` (21 — goods/orders/renewal/backup/
authorization/replacement), `storage` (11 — Cloud Space files & backups),
`static_proxy` (7), `dynamic_proxy` (13), `email` (5), `automation` (25 — RPA
scripts/dispatch/scheduling/account matrix/webview), `token` (2 — STS tokens),
`touch` (4 — humanized click/swipe/long-press + raw multi-touch).

### Placement surprises (check before guessing)

- `pad_info` and `user_pad_list` live in **`client.phone`**, not `client.instance`
  (follows the official docs' categorization). `pad_detail` is in `client.instance`.
- `upload_file_v3` (push APK/file by URL) is in **`client.apps`**;
  `upload_file` (multipart) is in **`client.storage`**; both create async tasks.
- Email endpoints exist in two API generations: `get_email_code` /
  `get_email_order` (padApi paths) and `get_email_code_vc` / `get_email_order_vc`
  (vcEmailService paths).
- Deep RPA paths keep their segments: `client.automation.scripts_list()` →
  `/vcpcloud/api/padApi/automation/scripts/list`; webview endpoints are
  `client.automation.webview_*`.

## Async-task pattern (very common)

Mutating operations (restart, reset, screenshots, ADB, file push, app install)
return task descriptors, not final results:

```python
tasks = client.instance.restart(pad_codes=["AC..."])   # -> [{"taskId": 123, ...}]
detail = client.tasks.pad_task_detail(task_ids=[tasks[0]["taskId"]])
# taskStatus: 3 = success; poll or subscribe to webhook callbacks instead of assuming completion
```

Webhooks: `vmos.callbacks.parse_callback(payload_dict)` → `CallbackEvent`
(`.kind`, `.pad_code`, `.task_id`, `.succeeded`, `.raw`). Kinds include
`app_install`, `app_uninstall`, `app_start`, `app_stop`, `app_restart`,
`file_upload`, `user_image_upload`, `adb_command`, `instance_status`.

## Gotchas that cause real bugs

- **Do not** pre-serialize JSON or set `Content-Type` yourself; the client signs
  the exact bytes it sends. Bypassing `client.request` breaks the signature.
- **Clock skew**: signatures embed unix-seconds timestamps valid ±5 minutes.
  `VMOSAuthError` with code 2033 → check the machine clock.
- **Touch rate limit**: same device within 2 s → code 1218
  (`VMOSRateLimitError`). Space out `client.touch.*` calls per device.
- **GET params**: passed via the documented keyword args; the SDK signs the exact
  query string it builds. Don't append query params to the path manually.
- **Multipart** (`client.storage.upload_file(file=...)`): pass httpx-style file
  tuples `("name.apk", b"...")`; the file body is intentionally not signed (per spec).
- Batch endpoints take plural args (`pad_codes: list`); single-target endpoints
  take `pad_code: str`. Docstrings and the manifest are authoritative.
- **`instance.pad_detail` is documented but NOT deployed** on the production
  gateway as of 2026-07 (HTTP 404 → `VMOSHTTPError`). List instances with
  `client.phone.user_pad_list()` instead.

## Cookbook

```python
# List all pads, then act on each (user_pad_list is live-verified)
pads = client.phone.user_pad_list()

# Set an HTTP/SOCKS proxy on pads
client.instance.set_proxy(pad_codes=["AC..."], **{...})   # see docs/en/instance.md

# Install & launch an app
client.apps.upload_file_v3(pad_codes=["AC..."], url="https://.../app.apk", auto_install=1)
client.apps.start_app(pad_codes=["AC..."], pkg_name="com.example.app")

# Humanized UI automation
client.touch.simulate_click(["AC..."], 360, 640, width=720, height=1280)
client.touch.simulate_swipe(["AC..."], start_x=360, start_y=1000, end_x=360, end_y=300)
client.instance.input_text(...)          # text entry — see docs/en/instance.md

# RPA flow dispatch
flows = client.automation.scripts_list(page=1, size=20)

# Issue an STS token for a client app
tok = client.token.sts_token_by_pad_code(pad_code="AC...")
```

Runnable end-to-end scripts: [`examples/`](examples).

## Testing code you write

Inject a mock transport — no network needed:

```python
import httpx
from vmos import VMOSClient

def handler(request):
    return httpx.Response(200, json={"code": 200, "msg": "success", "ts": 1, "data": {...}})

client = VMOSClient("ak", "sk", http_client=httpx.Client(transport=httpx.MockTransport(handler)))
```

Run the SDK's own suite with `python -m pytest tests/ -q` (182 tests; the
spec-driven test in `tests/test_all_endpoints.py` re-verifies signature and
payload shape for every endpoint).
