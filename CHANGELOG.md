# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **App-scoped `Build.*` identity spoof — GMS-safe (keeps Google Play Services /
  Play Store GENUINE).** The XPose plugin (`androidx.app.Entry`) now spoofs the
  static `Build.MODEL` / `MANUFACTURER` / `BRAND` / `DEVICE` / `PRODUCT` /
  `FINGERPRINT` and `Build.VERSION.RELEASE` fields **per app**, read from
  `persist.vmos.spoof.build.*` (only when a prop is set). `appMain` gained a
  **denylist guard** that returns early for `com.google.android.gms` (and its
  process packages), `com.android.vending` and `com.google.android.gsf`, so those
  keep their real A13/SDK33 identity — a *system-wide* Pixel/Android-16/SDK-36
  spoof crash-loops `com.google.android.gms.persistent`, so spoofing every app
  *except* GMS/Play is the GMS-safe design (a denylist, the opposite of injecting
  into GMS). `Build.VERSION.SDK_INT` spoofing is included but **disabled by
  default** (app-scoped SDK skew can crash the target app; enable per-app after
  testing). **The plugin APK must be rebuilt** (`./gradlew :app:assembleRelease`)
  after this `Entry.java` change.
- `vmos.spoof.set_build_props()` — set the `persist.vmos.spoof.build.*` props the
  plugin reads (the `Build.*` counterpart of `set_identity_props`). Only non-empty
  fields are written; `sdk_int` is accepted but a no-op until the plugin's SDK_INT
  line is manually enabled.
- **Denylist scoping helpers** (`vmos.spoof`): `GMS_DENYLIST` constant,
  `list_installed_packages()` (parses `pm list packages -3` / `-s`) and
  `app_scoped_targets()` — "all installed apps **EXCEPT** GMS/Play" (extend via
  `extra_denylist`). `apmt` is **per-package (no wildcard)**, so each target needs
  its own patch and **newly-installed apps require a re-run**.
- `JavaHookBackend` now spoofs `Build.*` too (`spoof_build=True`, on by default)
  and can auto-scope every installed app minus the denylist onto
  `profile.runtime.target_apps` (`auto_scope_all=True`, also on `standard_manager`).
  `Profile.build_hook_props()` / `Profile.build_hook_kwargs()` bridge the `build`
  section to the plugin / `set_build_props`.
- **Headless root stack — Magisk + Zygisk-Next + LSPosed, one pass**
  (`vmos.spoof.install_root_stack_headless`) — encodes the real-device-verified
  sequence (Pixel 9 Pro / Android 13; no Toolbox UI, no `switchRoot`, no `su`):
  `uploadFileV3` → md5/size download wait **on the device** → `install.sh &&
  install_modules.sh` (logs redirected) → `restart` → reboot-readiness wait
  (tolerating code `110031`) → active-state verification. Ships reusable building
  blocks, each independently testable: `wait_for_file_download`,
  `stage_root_stack_install`, `verify_root_stack`, `wait_for_pad_ready`,
  `pad_online` / `wait_for_pad_online`, `resolve_pad_code`, `coerce_task_ids`, plus
  the `PAD_NOT_READY_CODE` and `ROOT_STACK_MODULES` constants.
- **Headless Magisk install** (`vmos.spoof.enable_magisk_headless`) — installs
  ArmCloud's cloud-Magisk with **no Toolbox UI and no `switchRoot`**: queries the
  OSS payload record (no auth), `curl`s the `.gz` onto the pad, extracts to
  `/debug_ramdisk`, runs `magisk_env/install.sh`. `resetprop` works immediately;
  the daemon/Zygisk activate after a reboot (`restart=True`). Helper
  `query_magisk_payload_url` + constant `MAGISK_OSS_QUERY_URL`. **Live-verified**
  on a genuine Pixel 7 Pro pad (27 MB payload, `ro.sys.cloud.magisk=1`,
  `resetprop` functional pre-reboot). Docs updated (en+vi).
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

- `vmos.spoof.enable_magisk_headless` now also runs `install_modules.sh` (stages
  **Zygisk-Next + LSPosed** — previously it installed Magisk only) and verifies
  success by an on-device **state check** rather than a truncatable output marker.
  New `install_modules=True` toggle; the download step reports a compact return
  code + size, and the result dict gains `install_rc` / `modules_rc` / `binaries`
  / `modules`.
- **Credential env-var aliases** — `VMOSClient` / `AsyncVMOSClient` now also accept
  `VMOS_ACCESS_KEY_ID` / `VMOS_SECRET_ACCESS_KEY` (the canonical `VMOS_ACCESS_KEY`
  / `VMOS_SECRET_KEY` still take precedence), and `vmos.spoof.resolve_pad_code`
  accepts `VMOS_PAD_CODE` / `VMOS_PADCODE` / `PADCODE`. This reconciles the SDK
  with credential stores that inject the `*_ID` / `*_ACCESS_` / `VMOS_PADCODE`
  names. No breaking change to existing behavior.
- `docs/{en,vi}/device-profile-framework.md` — Roadmap item **A** marked done
  (now codified as `ProfileManager`); added a *Profile Manager in code* appendix.

### Fixed

- **Prop-key mismatch: phone number spoof never reached the plugin** — the SDK
  wrote `persist.vmos.spoof.line1`, but the compiled plugin reads
  `persist.vmos.spoof.line`, so `getLine1Number()` spoofing silently did nothing.
  `vmos.spoof._IDENTITY_PROPS` and `Profile.identity_props()` now write
  `persist.vmos.spoof.line` (the public `line1` kwarg/`telephony.line1` field are
  unchanged), and the plugin's `getLine1Number` hook reads the same `.line` key so
  a rebuild stays consistent. The rest of the map was audited against the plugin's
  reads: `android_id`/`wifi_mac`/`drm_id` already map correctly to
  `.androidid`/`.wifimac`/`.drmid`. A test asserts the exact prop-key set.
- **Async task-detail body format (`code=100013`)** — `padTaskDetail` /
  `fileTaskDetail` must be called with the integer-array body
  `{"taskIds":[<int>, ...]}`; the object form `{"taskIds":[{"taskId":N}]}` is
  rejected. `PadRootShell` now normalizes ids through `coerce_task_ids`, and
  terminal-status handling recognizes the documented failure codes
  (`-1`/`-2`/`-3`/`-4`).
- **`uploadFileV3` download-completion detection** — `fileTaskDetail` returns
  `data: null` for these tasks on this tenant, so it cannot signal completion.
  Completion is now detected by polling the file's md5/size **on the device**
  (`wait_for_file_download`), not via `fileTaskDetail`.
- **Truncated `taskResult` false-failures** — VMOS truncates async task output, so
  scanning verbose installer output for an `INSTALL_COMPLETE` marker produced false
  failures. Install and verification now redirect verbose logs to on-device files
  and confirm success by a separate compact **state** check (`ro.sys.cloud.magisk`,
  the five Magisk binaries, the `zygisksu` / `zygisk_lsposed` module dirs, and the
  running `lspd` daemon).
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
