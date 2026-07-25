# AGENTS.md — VMOS Cloud Python SDK

Instructions for AI coding agents (Codex, Cursor, Copilot Workspace, Claude
Code, Windsurf, ...) working **in this repository** or **with this SDK**.

## Project overview

Complete Python SDK for the VMOS Cloud Server OpenAPI (cloud Android phones).
All **152 documented endpoints**, 11 namespaces, sync + async clients, V2
request signing, webhook callback parsing. Python ≥ 3.9, single runtime
dependency `httpx`, MIT license.

```
src/vmos/
  __init__.py        public exports (VMOSClient, AsyncVMOSClient, errors, ...)
  client.py          request pipeline: serialize once → sign exact bytes → send
  auth.py            V2Signer (SHA-256(SK + ts + path + bodyOrQuery))
  exceptions.py      VMOSError / VMOSHTTPError / VMOSAPIError / VMOSAuthError / VMOSRateLimitError
  models.py          APIResponse envelope
  callbacks.py       webhook payload parsing (CallbackEvent, parse_callback)
  api/_base.py       resource base classes + build_payload (hand-written)
  api/*.py           GENERATED endpoint wrappers — do not edit by hand
scripts/             generator toolchain (parse docs → spec → code + docs)
scripts/data/endpoints.json          parsed spec snapshot (source of truth)
tests/               245 tests; test_all_endpoints.py covers every endpoint
tests/data/endpoints_manifest.json   machine-readable endpoint→method index
docs/en/, docs/vi/   GENERATED per-namespace API reference
examples/            runnable usage scripts
```

## Setup & commands

```bash
pip install httpx pytest anyio     # runtime + test deps
python -m pytest tests/ -q         # run the full suite (must stay green)
```

No install step is needed to run tests (`tests/conftest.py` adds `src/` to the
path). CI (`.github/workflows/ci.yml`) runs the suite on Python 3.9–3.13.

## Editing rules

1. **Never hand-edit generated files** (`src/vmos/api/*.py` except `_base.py`,
   `docs/en|vi/*.md`, `tests/data/endpoints_manifest.json`). Change the
   generators in `scripts/` (or the spec) and regenerate:
   ```bash
   python3 scripts/gen_sdk.py && python3 scripts/gen_docs.py && python -m pytest tests/ -q
   ```
2. To sync with new VMOS docs: dump the official docs page to markdown, then
   `python3 scripts/parse_spec.py OpenAPI.md` → regenerate (see `scripts/README.md`).
3. Hand-written core (`client.py`, `auth.py`, `exceptions.py`, `models.py`,
   `callbacks.py`, `api/_base.py`, tests) is edited normally — keep the test
   suite green and add tests for new behavior.
4. **Signing invariant** (do not break): the string that is signed must be the
   exact bytes/query sent on the wire. JSON is serialized exactly once in
   `client.py::_encode_json` (compact separators, `ensure_ascii=False`);
   GET signs the exact query string; multipart signs `""`.
5. Style: 4-space indent, double quotes, type hints, Google-style docstrings.
   Keep Python 3.9 compatibility (no `match`, no `X | Y` unions at runtime).

## Using the SDK (agent cheat sheet)

```python
from vmos import VMOSClient, AsyncVMOSClient, VMOSAPIError

client = VMOSClient()  # or VMOSClient("ak", "sk"); env: VMOS_ACCESS_KEY/VMOS_SECRET_KEY
data = client.phone.user_pad_list()             # returns response `data`; raises on code != 200
```

- Namespaces: `instance`, `apps`, `tasks`, `phone`, `storage`, `static_proxy`,
  `dynamic_proxy`, `email`, `automation`, `token`, `touch`.
- Exact signatures for any endpoint: parse `tests/data/endpoints_manifest.json`
  (path → module/method/params) or read `docs/en/<namespace>.md`.
- Python args are snake_case of the API's camelCase (`padCodes` → `pad_codes`);
  unknown/new API params go through `**extra`; `None` values are omitted.
- Mutating ops return async **tasks** (`taskId`) — poll `client.tasks.*` or
  parse webhooks with `vmos.callbacks.parse_callback`.
- Documented but 404 on current production gateway: `pad_detail`,
  `screenshot_info`, `execute_script_info`, `pad_execute_task_info`. List
  instances via `phone.user_pad_list()`; track tasks via
  `tasks.pad_task_detail(task_ids=[...])`. `instance.screenshot()` is
  synchronous in production and returns a signed `accessUrl` per pad.
- Known placements: `pad_info`/`user_pad_list` → `client.phone`;
  `upload_file_v3` (URL push) → `client.apps`; `upload_file` (multipart) →
  `client.storage`; RPA deep paths → `client.automation.scripts_list()` etc.
- Errors: catch `VMOSAPIError` (`.code`, `.msg`); `VMOSAuthError` = bad AK/SK,
  missing headers, or >5 min clock skew; `VMOSRateLimitError` = throttled
  (touch APIs: 2 s per device).
- Mock for tests: `VMOSClient("ak", "sk", http_client=httpx.Client(transport=httpx.MockTransport(handler)))`.

## PR / commit expectations

- Run `python -m pytest tests/ -q` before committing; all 245+ tests must pass.
- If you regenerate code, commit spec + generated files + manifest together so
  the suite stays consistent.
- Conventional, descriptive commit messages (e.g. `feat: add X endpoint group`,
  `fix: sign GET query in sent order`).
