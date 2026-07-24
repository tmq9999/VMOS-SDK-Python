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
              ├── System Applier      (Layer 1: resetprop / Magisk / update_sim / settings)
              ├── App Hook            (Layer 2: XPose plugin, per-app Java getters)
              ├── System-server Hook  (Layer 3, optional: systemMain + telephony process)
              └── Verification        (read back → diff vs profile → report)
```

**Principle:** the Profile is the center; hooks/appliers are just
implementations. No applier hard-codes identity data — they all read the Profile.
New backends can be added without changing the Profile.

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

## 4. Appliers (the three layers)

- **Layer 1 — System Applier** (done): `resetprop` + Magisk module for `build.*`;
  `update_sim` for SIM/IMSI/operator; `settings` for locale/timezone; ADI
  template for the base model. Reboot-persistent, reversible.
- **Layer 2 — App Hook** (in progress): the XPose plugin loaded per app via
  `apmt`; overrides Java getters in the **scoped app's** process. This is the
  only layer that can change IMEI/GAID/Android-ID/etc. as a specific app reads
  them.
- **Layer 3 — System-server Hook** (optional, later): `systemMain` for
  system-wide `build`/display/feature **consistency**. Note two realities:
  - IMEI/IMSI are **not** in `system_server`; they live in the **telephony
    process** (`com.android.phone`). Hooking that process (a Layer-2 target, not
    system-server) is what makes even the Binder path (`service call
    iphonesubinfo`) consistent — the fix for the earlier "Binder bypass" gap.
  - Hooking `system_server` is higher-risk (a crash there can bootloop the
    instance), so it is opt-in and narrowly scoped.
- **Native hooks are framework-supported** (a distinct capability, not yet built
  here): VMOS's XPose ships **Dobby** (inline hook) + **xDL** (symbol resolver)
  and the `libengcore.so` engine, demonstrated in the ArmCloudXposed demo
  (hooking libc `open`/`openat` and the linker's `do_dlopen`). A plugin can add a
  native `.so` (loaded from `appMain`) to intercept **native/JNI/Binder reads,
  Cronet, and native OAID SDKs** — the lever for identity that never surfaces in
  Java. Only hardware attestation (TEE) stays out of reach.

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

## 8. Roadmap

| Phase | Deliverable |
|---|---|
| **P1 — Profile core** | Profile JSON schema; extend `DeviceProfile` + `validate()` + serialize; consistency generator/validator; plugin reads `vmos_profile.json`; one-call `apply_profile(pad, profile)` spanning Layer 1 + 2 |
| **P2 — App-layer robustness** | secondary processes, dynamic `ClassLoader`, hook-by-signature, per-module hook management |
| **P3 — System layer** | `systemMain` (system-wide build/display/feature consistency) + telephony-process hook (Binder-consistent IMEI), all reading the same profile |
| **P4 — Verification** | read-back → diff → report component |
| **P5 — Lifecycle & catalog** | profile versioning, export/import/rollback, a catalog of ready-made profiles |

## 9. Sequencing (risk note)

**Prove Layer 2 end-to-end first** — one live IMEI/GAID change visible in a
device-info app — *before* the big refactor. The Profile core (P1) is mostly
SDK-side and can proceed in parallel, but the framework should not be built on an
unverified hook.

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
