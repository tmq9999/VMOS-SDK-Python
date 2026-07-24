# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Profile Manager** (`vmos.manager`) — the profile-driven orchestrator. One
  canonical `Profile` is applied across independent, pluggable backends in a
  single call:
  - `ProfileManager` with `apply()` / `verify()` / `remove()`, and a
    `standard_manager(client, pad_code, ...)` factory that wires Layer 1 then
    Layer 2 (the combined provisioning proven live).
  - `Backend` base class + `SystemApplierBackend` (Layer 1 build props via
    resetprop/Magisk) and `JavaHookBackend` (Layer 2 `persist.vmos.spoof.*` +
    XPose plugin scoping). Register custom backends with
    `ProfileManager.register(...)` — the Profile schema never changes.
  - Validates the Profile first and raises `ProfileValidationError` on
    `error`-level issues (override with `validate_before_apply=False`).
- `Profile.identity_kwargs()` — the Layer-2 identity values keyed for
  `vmos.spoof.set_identity_props` (drives the Java Hook Backend from the Profile).
- `examples/15_profile_manager.py` — provision a whole device from one profile
  (`--dry-run` to preview offline, `--verify` to read back).

### Changed

- `docs/{en,vi}/device-profile-framework.md` — Roadmap item **A** marked done
  (now codified as `ProfileManager`); added a *Profile Manager in code* appendix.

### Fixed

- **Layer-1 build props silently not applied on real devices** — `apply_profile`
  sent the whole deep prop set (~50 props / ~4 KB) as a single `resetprop`
  command. The pad's `async_cmd` input is capped near 2 KB, so the command was
  truncated mid-quote and applied **nothing** (model/fingerprint stayed
  unchanged) while smaller Layer-2 batches worked — a confusing, device-only
  failure. `resetprop` and on-device file writes are now split into
  input-cap-safe batches (`resetprop_commands` + `_run_batched`;
  `ASYNC_CMD_MAX_BYTES`); `_write_file` streams payloads via chunked base64.
  **Live-verified** on the pad: `ProfileManager.apply` flips
  model→`Pixel 10 Pro XL`, device/board/hardware→`mustang`, fingerprint→mustang,
  confirmed in a device-info app.

## [1.0.0] - 2026-07-24

First stable release. 🎉

### Added

- **Complete API coverage** — all **152 endpoints** from the official VMOS Cloud
  Server OpenAPI documentation, organized into 11 client namespaces:
  `instance` (50), `apps` (10), `tasks` (4), `phone` (21), `storage` (11),
  `static_proxy` (7), `dynamic_proxy` (13), `email` (5), `automation` (25),
  `token` (2), `touch` (4).
- **V2 Simplified Signature** authentication
  (`X-Sign = SHA-256(SK + timestamp + path + bodyOrQuery)`), verified against
  the official documentation test vector. Exact-bytes signing: JSON bodies are
  serialized once and signed verbatim; GET requests sign the raw query string;
  multipart uploads sign an empty string.
- **Sync and async clients** — `VMOSClient` and `AsyncVMOSClient` (httpx),
  identical APIs, context-manager support, connection-error retries with
  exponential backoff, credentials via arguments or `VMOS_ACCESS_KEY` /
  `VMOS_SECRET_KEY` environment variables.
- **Error hierarchy** — `VMOSError` → `VMOSHTTPError` (transport),
  `VMOSAPIError` (business, with `.code`/`.msg`/`.ts`/`.data`),
  `VMOSAuthError` (2019/2031/2032/2033), `VMOSRateLimitError` (1218).
- **Webhook callback parsing** — `vmos.callbacks.parse_callback()` →
  `CallbackEvent` for all 12 documented callback types (ADB results, file
  uploads, app operations, image upload/upgrade, instance status).
- **Forward compatibility** — every method accepts `**extra`, sent verbatim,
  so new VMOS parameters work without an SDK update; `client.request()` is a
  signed escape hatch for any path.
- **Test suite (182 tests)** — official signing vector, client behavior
  (errors, GET/POST/multipart/unicode), callback parsing, and a spec-driven
  test that verifies path, HTTP method, parameter names, and signature for
  **every single endpoint**.
- **Bilingual documentation** — English + Vietnamese README, per-namespace API
  reference in `docs/en/` and `docs/vi/`, 8 runnable examples.
- **AI-assistant guides** — `CLAUDE.md` and `AGENTS.md` plus a
  machine-readable endpoint manifest (`tests/data/endpoints_manifest.json`).
- **Self-regenerating toolchain** — `scripts/` parses the official docs into a
  spec and regenerates API modules, manifest, and reference docs.
- **CI** — GitHub Actions workflow running the suite on Python 3.9–3.13.

### Production findings (live-verified 2026-07-24)

- POST & GET signing confirmed against the production API across `phone`,
  `instance`, `apps`, `tasks`, and `touch` namespaces — including a full
  UI-automation flow (humanized click → focused-field text input → screenshot
  confirmation) on a real instance.
- `instance.screenshot()` is **synchronous** in production and returns a
  signed, expiring `accessUrl` per pad (the docs describe an async variant).
- Task tracking that works in production: `tasks.pad_task_detail()` and
  `tasks.get_task_status()`; ADB stdout arrives in `taskResult`.
- Documented but not yet deployed on the production gateway (HTTP 404):
  `padDetail`, `screenshotInfo`, `executeScriptInfo`, `padExecuteTaskInfo` —
  the SDK keeps these wrappers for when VMOS ships them, and the docs point to
  the working alternatives.

[1.0.0]: https://github.com/tmq9999/VMOS-SDK-Python/releases/tag/v1.0.0
