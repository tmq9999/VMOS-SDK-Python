# VMOS Cloud Python SDK

**[English](#english)** | **[Tiếng Việt](#tiếng-việt)**

![tests](https://img.shields.io/badge/tests-182%20passed-brightgreen) ![endpoints](https://img.shields.io/badge/endpoints-152%2F152-blue) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green)

Complete, production-ready Python SDK for the [VMOS Cloud Server OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html) — cloud Android phone instances. Covers **all 152 documented endpoints** across 11 service areas, with V2 signed requests, sync **and** async clients, typed wrappers, webhook callback parsing, and a spec-driven test suite that verifies every endpoint against the official documentation.

---

## English

### Features

- ✅ **All 152 endpoints** from the official OpenAPI docs — instance management, apps, tasks, cloud phone commerce, cloud storage, static & dynamic proxies, email verification, RPA automation, SDK tokens, humanized touch simulation.
- 🔐 **V2 Simplified Signature** implemented exactly per spec (`SHA-256(SK + timestamp + path + body)`), verified against the official test vector. The SDK signs the *exact* bytes it sends — no re-ordering, no whitespace surprises.
- ⚡ **Sync + async**: `VMOSClient` and `AsyncVMOSClient` with identical APIs (httpx-based).
- 🧭 **Typed, documented wrappers**: every method has full docstrings with parameter descriptions from the official docs; `**extra` passes new/undocumented params without an SDK update.
- 🚨 **Clean error model**: `VMOSAPIError` (business errors), `VMOSAuthError` (signature/key issues 2019/2031/2032/2033), `VMOSRateLimitError`, `VMOSHTTPError`.
- 📥 **Webhook callbacks**: `vmos.callbacks.parse_callback()` parses all documented callback payloads (ADB results, file uploads, app operations, status changes...).
- 🧪 **182 tests**: official signing vector + a spec-driven test for *every single endpoint* (path, HTTP method, parameter names, signature over exact bytes).
- ✅ **Live-verified**: POST & GET signing confirmed against the production API across multiple namespaces (`phone`, `instance`, `apps`).
- 🤖 **AI-ready**: [`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md) and a machine-readable endpoint manifest ([`tests/data/endpoints_manifest.json`](tests/data/endpoints_manifest.json)) so Claude, Codex, Cursor & friends can use the SDK at full fidelity.

### Installation

```bash
pip install httpx
pip install git+https://github.com/tmq9999/VMOS-SDK-Python.git
# or, from a clone:
git clone https://github.com/tmq9999/VMOS-SDK-Python.git && cd VMOS-SDK-Python && pip install .
```

Requires Python **3.9+**. Single runtime dependency: `httpx`.

### Authentication

Get your **AccessKey ID** and **SecretAccessKey** from the VMOS console → **Developer → API**, then either pass them explicitly or export them:

```bash
export VMOS_ACCESS_KEY="ak_xxxxxxxx"
export VMOS_SECRET_KEY="sk_xxxxxxxx"
```

```python
from vmos import VMOSClient

client = VMOSClient()                          # reads env vars
client = VMOSClient("ak_...", "sk_...")        # or explicit
```

### Quickstart

```python
from vmos import VMOSClient, VMOSAPIError

with VMOSClient() as client:
    # List your cloud phones (live-verified)
    pads = client.phone.user_pad_list()

    # Restart an instance → async task
    tasks = client.instance.restart(pad_codes=["AC32010180421"])
    print(tasks[0]["taskId"])

    # Query one phone
    info = client.phone.pad_info("AC32010180421")
    print(info["padType"], info["country"])

    # Humanized click
    client.touch.simulate_click(["AC32010180421"], 360, 640, width=720, height=1280)
```

Async — identical API, just `await`:

```python
import asyncio
from vmos import AsyncVMOSClient

async def main():
    async with AsyncVMOSClient() as client:
        pads = await client.phone.user_pad_list()
        print(pads)

asyncio.run(main())
```

### Client namespaces

| Namespace | Endpoints | What's inside |
|---|---|---|
| `client.instance` | 50 | Restart/reset, properties, SIM/GPS/WiFi, ADB & shell, screenshots, previews, image upgrade, one-click new device, root, media injection |
| `client.apps` | 10 | Install/uninstall, start/stop/restart, app lists, keep-alive, hidden apps, APK push by URL |
| `client.tasks` | 4 | Async task status & details |
| `client.phone` | 21 | Goods, orders, renewals, activation codes, authorization/transfer, backups, sharing, replacement |
| `client.storage` | 11 | Cloud Space: storage goods, backups, file upload/query/delete |
| `client.static_proxy` | 7 | Static residential IP service |
| `client.dynamic_proxy` | 13 | Dynamic proxy: regions, orders, traffic, per-pad config |
| `client.email` | 5 | Email verification service |
| `client.automation` | 25 | Flow Automation (RPA): scripts, dispatch, scheduling, account matrix, webview, unmanned live |
| `client.token` | 2 | SDK temporary (STS) tokens |
| `client.touch` | 4 | Humanized click/swipe/long-press + raw multi-touch |

Full per-method reference: **[docs/en/](docs/en/README.md)** · **[docs/vi/](docs/vi/README.md)**

### Return values & errors

Every wrapper returns the response **`data` field** directly and raises when the API answers `code != 200`:

```python
from vmos import VMOSAPIError, VMOSAuthError

try:
    data = client.phone.pad_info("BAD_CODE")
except VMOSAuthError as e:      # 2019/2031/2032/2033 — check your AK/SK & clock
    print("auth problem:", e.code, e.msg)
except VMOSAPIError as e:       # any other business error
    print("api error:", e.code, e.msg)
```

Need the raw envelope (`code`, `msg`, `ts`, `data`) without raising? Use `client.request_raw(...)`.

### Good to know

- **Signing is exact**: the client serializes JSON once (compact, UTF-8, no re-ordering) and signs those exact bytes. GET requests sign the exact query string; multipart uploads sign an empty string — all per the official V2 spec.
- **Async operations**: many endpoints (restart, screenshots, ADB, file push) return a `taskId`; poll `client.tasks.*` or receive webhook callbacks (`vmos.callbacks.parse_callback`).
- **Forward compatible**: any new parameter VMOS adds can be passed today via `**extra`.
- **Touch rate limit**: the humanized touch APIs reject repeat calls to the same device within 2 s (code 1218 → `VMOSRateLimitError`).
- **Production vs docs** (live-tested 2026-07): a few documented endpoints are not deployed yet and return HTTP 404: `padDetail`, `screenshotInfo`, `executeScriptInfo`, `padExecuteTaskInfo`. Working alternatives: list instances with `client.phone.user_pad_list()`; track any task with `client.tasks.pad_task_detail(task_ids=[...])` or `client.tasks.get_task_status(task_id=...)`.
- **Screenshots are synchronous in production**: `client.instance.screenshot(...)` returns `[{padCode, accessUrl, success, expireAt}]` — a signed, expiring URL you can download immediately (the docs describe an async task variant; production skips it).

### Examples

Runnable scripts in [`examples/`](examples): listing instances, restart + task polling, APK push & app lifecycle, screenshots & ADB, async fan-out, humanized touch, a webhook receiver, proxy & email services.

### Development

```bash
git clone https://github.com/tmq9999/VMOS-SDK-Python.git && cd VMOS-SDK-Python
pip install httpx pytest anyio
python -m pytest tests/ -q          # 182 tests
```

The SDK is **generated from the official docs** — see [`scripts/README.md`](scripts/README.md) to refresh it when VMOS ships new endpoints.

### Disclaimer

Unofficial SDK, not affiliated with VMOS. API behavior follows the official documentation; always verify billing-sensitive operations (orders, renewals) in a test environment first.

**License**: [MIT](LICENSE)

---

## Tiếng Việt

SDK Python **đầy đủ và sẵn sàng cho production** dành cho [VMOS Cloud Server OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html) — dịch vụ điện thoại Android đám mây. Bao phủ **toàn bộ 152 endpoint** trong tài liệu chính thức, chia thành 11 nhóm dịch vụ, với chữ ký V2, client đồng bộ **và** bất đồng bộ, wrapper có type + docstring, phân tích webhook callback, và bộ test kiểm chứng từng endpoint theo đúng tài liệu.

### Tính năng

- ✅ **Đủ 152 endpoint** chính thức — quản lý instance, ứng dụng, tác vụ, thương mại cloud phone, lưu trữ đám mây, proxy tĩnh & động, xác minh email, tự động hóa RPA, SDK token, mô phỏng cảm ứng giống người thật.
- 🔐 **Chữ ký V2 đơn giản hóa** đúng chuẩn spec (`SHA-256(SK + timestamp + path + body)`), đã xác minh với test vector chính thức. SDK ký *chính xác từng byte* gửi đi — không sắp xếp lại, không thay đổi khoảng trắng.
- ⚡ **Sync + async**: `VMOSClient` và `AsyncVMOSClient` có API giống hệt nhau (dựa trên httpx).
- 🧭 **Wrapper đầy đủ tài liệu**: mỗi phương thức có docstring với mô tả tham số lấy từ tài liệu chính thức; tham số mới/chưa có trong docs truyền qua `**extra` mà không cần chờ SDK cập nhật.
- 🚨 **Mô hình lỗi rõ ràng**: `VMOSAPIError` (lỗi nghiệp vụ), `VMOSAuthError` (lỗi chữ ký/khóa 2019/2031/2032/2033), `VMOSRateLimitError`, `VMOSHTTPError`.
- 📥 **Webhook callback**: `vmos.callbacks.parse_callback()` phân tích mọi payload callback trong tài liệu (kết quả ADB, tải file, thao tác ứng dụng, thay đổi trạng thái...).
- 🧪 **182 bài test**: test vector chữ ký chính thức + test tự động cho *từng endpoint một* (đường dẫn, HTTP method, tên tham số, chữ ký trên đúng byte gửi đi).
- ✅ **Đã kiểm chứng với API thật**: chữ ký POST & GET xác nhận hoạt động trên API production qua nhiều namespace (`phone`, `instance`, `apps`).
- 🤖 **Sẵn sàng cho AI**: [`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md) và manifest endpoint dạng máy-đọc-được ([`tests/data/endpoints_manifest.json`](tests/data/endpoints_manifest.json)) để Claude, Codex, Cursor... dùng SDK chính xác tối đa.

### Cài đặt

```bash
pip install httpx
pip install git+https://github.com/tmq9999/VMOS-SDK-Python.git
# hoặc từ bản clone:
git clone https://github.com/tmq9999/VMOS-SDK-Python.git && cd VMOS-SDK-Python && pip install .
```

Yêu cầu Python **3.9+**. Chỉ phụ thuộc duy nhất `httpx`.

### Xác thực

Lấy **AccessKey ID** và **SecretAccessKey** trong console VMOS → **Developer → API**, sau đó truyền trực tiếp hoặc export biến môi trường:

```bash
export VMOS_ACCESS_KEY="ak_xxxxxxxx"
export VMOS_SECRET_KEY="sk_xxxxxxxx"
```

```python
from vmos import VMOSClient

client = VMOSClient()                          # đọc biến môi trường
client = VMOSClient("ak_...", "sk_...")        # hoặc truyền trực tiếp
```

### Bắt đầu nhanh

```python
from vmos import VMOSClient, VMOSAPIError

with VMOSClient() as client:
    # Danh sách cloud phone của bạn (đã kiểm chứng live)
    pads = client.phone.user_pad_list()

    # Khởi động lại instance → tác vụ bất đồng bộ
    tasks = client.instance.restart(pad_codes=["AC32010180421"])
    print(tasks[0]["taskId"])

    # Truy vấn thông tin một máy
    info = client.phone.pad_info("AC32010180421")
    print(info["padType"], info["country"])

    # Click giống người thật
    client.touch.simulate_click(["AC32010180421"], 360, 640, width=720, height=1280)
```

Bất đồng bộ — API giống hệt, chỉ cần `await`:

```python
import asyncio
from vmos import AsyncVMOSClient

async def main():
    async with AsyncVMOSClient() as client:
        pads = await client.phone.user_pad_list()
        print(pads)

asyncio.run(main())
```

### Các namespace của client

| Namespace | Số endpoint | Chức năng |
|---|---|---|
| `client.instance` | 50 | Khởi động lại/reset, thuộc tính, SIM/GPS/WiFi, ADB & shell, chụp màn hình, xem trước, nâng cấp image, đổi máy một chạm, root, chèn media |
| `client.apps` | 10 | Cài/gỡ, chạy/dừng/khởi động lại ứng dụng, danh sách app, giữ app chạy, ẩn app, đẩy APK qua URL |
| `client.tasks` | 4 | Trạng thái & chi tiết tác vụ bất đồng bộ |
| `client.phone` | 21 | Gói dịch vụ, đơn hàng, gia hạn, mã kích hoạt, ủy quyền/chuyển giao, sao lưu, chia sẻ, thay thế |
| `client.storage` | 11 | Cloud Space: gói lưu trữ, sao lưu, tải/truy vấn/xóa file |
| `client.static_proxy` | 7 | Dịch vụ IP dân cư tĩnh |
| `client.dynamic_proxy` | 13 | Proxy động: khu vực, đơn hàng, lưu lượng, cấu hình từng máy |
| `client.email` | 5 | Dịch vụ xác minh email |
| `client.automation` | 25 | Tự động hóa luồng (RPA): kịch bản, điều phối, lập lịch, ma trận tài khoản, webview, live không người trực |
| `client.token` | 2 | Token tạm thời (STS) cho SDK |
| `client.touch` | 4 | Chạm/vuốt/nhấn giữ giống người thật + cảm ứng đa điểm |

Tài liệu chi tiết từng phương thức: **[docs/vi/](docs/vi/README.md)** · **[docs/en/](docs/en/README.md)**

### Giá trị trả về & xử lý lỗi

Mỗi wrapper trả về trực tiếp trường **`data`** của phản hồi và ném exception khi API trả `code != 200`:

```python
from vmos import VMOSAPIError, VMOSAuthError

try:
    data = client.phone.pad_info("BAD_CODE")
except VMOSAuthError as e:      # 2019/2031/2032/2033 — kiểm tra AK/SK & đồng hồ hệ thống
    print("lỗi xác thực:", e.code, e.msg)
except VMOSAPIError as e:       # các lỗi nghiệp vụ khác
    print("lỗi API:", e.code, e.msg)
```

Cần nguyên vẹn envelope (`code`, `msg`, `ts`, `data`) mà không ném lỗi? Dùng `client.request_raw(...)`.

### Lưu ý quan trọng

- **Chữ ký chính xác từng byte**: client serialize JSON một lần duy nhất (compact, UTF-8, không sắp xếp lại) và ký đúng chuỗi byte đó. GET ký đúng query string; upload multipart ký chuỗi rỗng — đúng theo spec V2 chính thức.
- **Thao tác bất đồng bộ**: nhiều endpoint (restart, chụp màn hình, ADB, đẩy file) trả về `taskId`; poll qua `client.tasks.*` hoặc nhận webhook callback (`vmos.callbacks.parse_callback`).
- **Tương thích tương lai**: tham số mới VMOS thêm sau này truyền ngay qua `**extra`.
- **Giới hạn tốc độ cảm ứng**: API touch giống người thật từ chối gọi lặp lại cùng thiết bị trong vòng 2 giây (code 1218 → `VMOSRateLimitError`).
- **Production vs tài liệu** (đã test live 2026-07): một số endpoint có trong docs nhưng chưa deploy, trả HTTP 404: `padDetail`, `screenshotInfo`, `executeScriptInfo`, `padExecuteTaskInfo`. Thay thế hoạt động tốt: liệt kê instance bằng `client.phone.user_pad_list()`; theo dõi mọi task bằng `client.tasks.pad_task_detail(task_ids=[...])` hoặc `client.tasks.get_task_status(task_id=...)`.
- **Screenshot là synchronous trên production**: `client.instance.screenshot(...)` trả về `[{padCode, accessUrl, success, expireAt}]` — URL có chữ ký, có hạn, tải được ngay (docs mô tả biến thể task bất đồng bộ; production bỏ qua bước đó).

### Ví dụ

Script chạy được trong [`examples/`](examples): liệt kê instance, restart + theo dõi tác vụ, đẩy APK & vòng đời ứng dụng, chụp màn hình & ADB, gọi song song async, cảm ứng giống người, webhook receiver, dịch vụ proxy & email.

### Phát triển

```bash
git clone https://github.com/tmq9999/VMOS-SDK-Python.git && cd VMOS-SDK-Python
pip install httpx pytest anyio
python -m pytest tests/ -q          # 182 bài test
```

SDK được **sinh từ tài liệu chính thức** — xem [`scripts/README.md`](scripts/README.md) để cập nhật khi VMOS phát hành endpoint mới.

### Miễn trừ trách nhiệm

SDK không chính thức, không liên kết với VMOS. Hành vi API tuân theo tài liệu chính thức; hãy kiểm tra các thao tác liên quan chi phí (đặt hàng, gia hạn) trong môi trường test trước.

**Giấy phép**: [MIT](LICENSE)
