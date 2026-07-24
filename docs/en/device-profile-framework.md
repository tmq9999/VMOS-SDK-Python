# VMOS Real Device Profile Framework — Design

> Design of record. Reframes the work from "a spoof plugin that hooks getters"
> into a **profile-driven framework**: a single **Device Profile** is the source
> of truth, and every applier (system props, app hook, future system-server hook)
> reads from it. Tiếng Việt: [device-profile-framework-vi.md](../vi/device-profile-framework-vi.md).

## 1. Vision & framing

Sell a **configured VMOS Real Device Profile** — a pre-provisioned Android
environment for app testing, QA, SDK/compatibility testing, automation, and
device diversity — on top of a VMOS real device. The base hardware (ADI) may be
one model (e.g. Pixel 7 Pro); the delivered profile presents a chosen, believable
device identity (e.g. Pixel 10 Pro). We sell the **profile**, not a deceptive
shell.

Hard boundary: software layer only. Hardware-backed attestation (Play Integrity
STRONG / TEE key attestation) is unbeatable by any software and is out of scope.

## 2. Architecture

```
VMOS Real Device
   → Base ADI (the rented model, e.g. Pixel 7 Pro)
      → Device Profile  (canonical JSON — the single source of truth)
         → Profile Manager
              ├── System Applier              (resetprop / Magisk / update_sim / settings)
              ├── Java Hook Backend           (XPose appMain — app-process Java getters)
              ├── Native Hook Backend         (XPose native .so — Dobby + xDL; native/JNI reads)
              ├── Service/System Hook Backend (systemMain + telephony process; higher-risk, PoC-gated)
              └── Verification                (read back → diff vs profile → report)
```

**Principle:** the Profile is the center; every backend is just an
implementation that **reads the same Profile** — none hard-codes identity data.
Backends are independent and can be added/removed without changing the Profile.
A field may be served by more than one backend (e.g. `serial` by System Applier
*and* Java Hook); the Profile stays the single source of truth for all of them.

## 3. The Device Profile (canonical JSON)

One language-neutral JSON document, consumed by both the Python side (Layer 1 +
provisioning) and the on-device plugin (Layer 2). Sections:

| Section | Example fields | Primary applier | Verify oracle |
|---|---|---|---|
| `meta` | name, version, baseAdi, createdAt, notes | — | — |
| `build` | brand, manufacturer, model, device, product, fingerprint, id, release, sdk, securityPatch, serial | Layer 1 (resetprop); `serial` also Layer 2 (`Build.getSerial`) | `getprop`; device-info app |
| `telephony` | imei[], meid, imsi, iccid, line1, mccMnc, operator, simCountryIso | Layer 2 (app + phone process); operator/imsi/country also Layer 1 (`update_sim`) | scoped device-info app |
| `identity` | androidId, gaid, oaid, gsfId, mediaDrmId | Layer 2 | scoped device-info app |
| `network` | wifiMac, bssid, ssid | Layer 2 (+ system) | device-info app |
| `display` | widthPx, heightPx, densityDpi, refreshRate | Layer 1 (wm/props) / Layer 3 | `wm size`; app |
| `locale` | language, country, timezone | Layer 1 (settings) | `settings get`; app |
| `features` | hasSystemFeature flags | Layer 3 (system-server) | app |
| `runtime` | targetApps (hook scope), enabledSections | Profile Manager | — |

Each field is annotated with **which layer applies it** and **how to verify it**.

### The profile-delivery contract
- **Python**: `DeviceProfile` (extend the existing dataclass) → `validate()` →
  serialize to canonical `vmos_profile.json`.
- **On device**: push the JSON to the pad (a Magisk module copy makes it
  reboot-persistent). The plugin **reads the profile JSON** instead of dozens of
  flat `persist.vmos.spoof.*` props. One profile → every hook. (Props remain a
  supported fallback for simple scalars.)

## 4. Backends (independent implementations, one shared Profile)

The orchestrator and the two verified backends are implemented in `vmos.manager`
(`ProfileManager`, `SystemApplierBackend`, `JavaHookBackend`, `standard_manager`).
Every backend subclasses `Backend` and reads the Profile through its bridge
methods — adding a new backend never touches the Profile schema (see the
*Profile Manager in code* appendix).

- **System Applier** (done): `resetprop` + Magisk module for `build.*`;
  `update_sim` for SIM/IMSI/operator; `settings` for locale/timezone; ADI
  template for the base model. Reboot-persistent, reversible.
  - **On-device input cap:** the pad's `async_cmd` truncates input near 2 KB, so
    `resetprop` sets and file writes are sent in batches under
    `ASYNC_CMD_MAX_BYTES` (a single ~4 KB command silently applies nothing).
- **Java Hook Backend** (done, verified): the XPose plugin (`appMain`) loaded per
  app via `apmt`; overrides Java getters in the **scoped app's** process. This is
  what changes IMEI/GAID/Android-ID/etc. as a specific app reads them via the Java
  API. Live-verified: Android ID read back matched the Profile value.
- **Native Hook Backend** (framework-supported; not built yet): a native `.so`
  loaded from `appMain`, using VMOS's shipped **Dobby** (inline hook) + **xDL**
  (symbol resolver) + `libengcore.so`. Reaches reads that never surface in Java:
  JNI/native SDKs, system properties read from native, `/proc` & `/sys` files,
  dynamically-loaded libraries, and logic living inside `.so`.
  - **Caveat (not absolute):** it hooks a native function only when the
    **address/symbol/signature is resolvable**, the **ABI matches** (arm64
    first), and the **process allows** loading the module. Symbols may be
    stripped, inlined, obfuscated, or shift between versions — each target needs
    verification, not assumption.
- **Service/System Hook Backend** (research/PoC-gated): `systemMain` for
  system-wide `build`/display/feature **consistency** (higher-risk — a crash in
  `system_server` can bootloop the instance, so opt-in and narrowly scoped), and
  the **telephony process** (`com.android.phone`) for values like IMEI/IMSI.
  - **Caveat:** hooking `com.android.phone` does **not** automatically make the
    Binder-returned IMEI change. It works only if we **trace the actual service
    implementation / data source** the Binder path returns and hook *that*
    (Java or native, or the source it reads) — a libc hook is **not** assumed
    sufficient. This backend enters the official roadmap **only after a
    proof-of-concept passes on a specific Android/ROM**.

Only hardware-backed attestation (TEE / Play Integrity STRONG) is out of reach of
every backend.

## 5. Consistency engine (the real product value)

The hooks are easy; a **believable, internally consistent** profile is the hard,
valuable part. The generator/validator must ensure:
- `model ↔ fingerprint ↔ build.id` match (from the authoritative Pixel-Props set).
- **IMEI** is Luhn-valid with a TAC plausible for the brand.
- **IMSI/ICCID** carry an MCC/MNC that matches the SIM operator/country.
- **GAID** is a UUID; **MAC** uses a plausible/locally-administered OUI.
- `locale`/`timezone` match the SIM country; `display` matches the model.
`validate()` rejects inconsistent profiles before apply.

## 6. Verification

- **Now**: installed device-info apps (`com.liuzh.deviceinfo`,
  `ru.andr7e.deviceinfohw`, `com.ytheekshana.deviceinfo`) + pad screenshot + the
  plugin's `hooked …` logcat.
- **Target**: a Verification step that reads back every identity field (from a
  scoped app and the system) to JSON and **diffs it against the profile**,
  emitting a per-section `Passed / Needs-improvement` report. May be a small
  verify APK or driven from device-info output.
- Layer-2 fields are **never** verified via `service call` / `getprop` / Play
  Integrity (they bypass the Java hook or rely on hardware attestation).

## 7. Lifecycle

Profiles are **versioned JSON** (git-friendly): create, validate, apply, export,
import, rollback. Each pad records which profile+version is applied so a fleet is
auditable.

## 8. Roadmap (agreed priority)

Done so far: **P1 Profile core** (schema, `Profile`, `validate()`, consistency
generator — SDK-side); **Java Hook Backend verified** (Android ID read back
matched the Profile live).

| Priority | Deliverable | Status |
|---|---|---|
| **A — Combined provisioning + verification** | one call applies the **System Applier** (Layer-1 build identity) **and** the **Java Hook Backend** (Layer-2 identity) from one Profile, then verifies model **and** Android ID together on a pad | **done** — live-verified; now codified as `ProfileManager` (`vmos.manager`) |
| **B — Native Hook Core (minimal), in parallel** | a native `.so` that (1) **loads successfully**, (2) **arm64 first**, (3) wraps **Dobby/xDL**, (4) **reads the Profile only** (no hard-coded identity), (5) reproduces the **VMOS demo hook end-to-end**, (6) has **lifecycle / logging / crash-guard** | parallel |
| **C — Research IMEI path in `com.android.phone`** | identify the process; **trace the Binder service implementation**; identify the Java/native **source** of the returned IMEI; build a **PoC on a specific Android/ROM** | after B |
| **D — Binder-consistent IMEI (gated)** | enters the official roadmap **only if the C PoC passes** | gated |

Later: P-lifecycle (profile versioning, export/import/rollback, ready-made
profile catalog); P-verification (read-back → diff → report component).

## 9. Sequencing (risk note)

Java Hook Backend is already **verified live** (Android ID). Proceed with **A**
(combine it with Layer 1) as the immediate milestone. Build **B** in parallel but
treat native reach as **conditional** (symbol/ABI/process — see the Native Hook
Backend caveat). Do **not** promise Binder-consistent IMEI until the **C** PoC
proves it on a real ROM (**D** is gated on that).

## Appendix — P1 in code (available now)

The Profile core ships in `vmos.profile`:

```python
from vmos.profile import generate_profile, validate
p = generate_profile("pixel10pro", country="VN", operator="Viettel",
                     base_adi="Pixel 7 Pro", target_apps=["com.liuzh.deviceinfo"], seed=42)
issues = validate(p)              # [] or [{level, field, message}, ...]
p.save("vmos_profile.json")       # canonical JSON — the source of truth
dp = p.to_device_profile()        # Layer-1 input for apply_profile()
props = p.identity_props()        # Layer-2 persist.vmos.spoof.* map
```

- CLI: `python examples/14_generate_profile.py --model pixel10pro --country VN --operator Viettel --out vmos_profile.json`
- Sample output: [`profiles/example-pixel10pro-vn.json`](../../profiles/example-pixel10pro-vn.json)
- Reference data: models `pixel10pro | pixel10 | pixel10proxl`; countries `VN | US | GB` (accurate MCC/MNC).
- Honesty: **TAC and display are unverified samples** (override for production); `validate()` warns on a generic TAC. Fingerprints are vetted (Pixel-Props).

## Appendix — Profile Manager in code (available now)

The orchestrator ships in `vmos.manager`. One Profile → every backend, one call:

```python
from vmos import VMOSClient, generate_profile, standard_manager

profile = generate_profile("pixel10pro", "VN", "Viettel",
                           target_apps=["com.liuzh.deviceinfo"], seed=42)

with VMOSClient() as client:                       # reads VMOS_ACCESS_KEY/SECRET_KEY
    mgr = standard_manager(client, "ACP...",       # Layer 1 + Layer 2, in order
                           apk_url="https://host/vmos-xpose-spoof.apk")
    mgr.apply(profile)      # validates, then drives System Applier + Java Hook
    mgr.verify(profile)     # reads back + diffs per backend
    # mgr.remove(profile)   # best-effort teardown (unloads named patches)
```

- **`ProfileManager`** validates the Profile first and refuses to apply one with
  `error`-level issues (raises `ProfileValidationError`); pass
  `validate_before_apply=False` to override.
- **Backends are independent and pluggable.** `SystemApplierBackend` (Layer 1)
  and `JavaHookBackend` (Layer 2) ship today; register your own `Backend`
  subclass (e.g. a future Native Hook) with `mgr.register(...)` — the Profile
  never changes.
- **No hard-coded identity.** Backends read the Profile via `to_device_profile()`
  (Layer 1) and `identity_kwargs()` / `identity_props()` (Layer 2).
- CLI: `python examples/15_profile_manager.py --pad ACP... --model pixel10pro --country VN --operator Viettel --target-app com.liuzh.deviceinfo --apk-url https://host/p.apk --verify`
  (add `--dry-run` to print the profile with no device).
- Honesty: Layer-2 `verify` confirms the `persist.vmos.spoof.*` props are set; the
  app-observed change is proven only by reading a **scoped device-info app**,
  never `service call` / `getprop` / Play Integrity.
