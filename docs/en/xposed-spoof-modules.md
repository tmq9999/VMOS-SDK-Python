# Xposed/LSPosed device-spoof modules for VMOS real devices — evaluation

> Research evaluation (2026-07) of LSPosed/Xposed modules that can spoof the
> **framework-held** identifiers VMOS's API + `resetprop` cannot change (IMEI,
> OAID/GAID, Android ID). Context: the VMOS real device already has **Kitsune
> Magisk + LSPosed framework + Zygisk** enabled (verified). Tiếng Việt:
> [xposed-spoof-modules-vi.md](../vi/xposed-spoof-modules-vi.md).

## Why a module is needed

`vmos.spoof` (Magisk `resetprop`) covers **build.prop identity** (model, brand,
fingerprint, SDK/release) — verified working. But **IMEI, OAID/GAID and
Android ID are held by the framework/RIL**, not system props, so they need a
**Java-level hook** inside each app process: an LSPosed module. Enabling the
LSPosed *framework* alone (done) hooks nothing — you must install a spoofing
**module APK** and scope it to the target apps.

## Candidates evaluated

| Module | Spoofs | Scope | A13 + Zygisk | Config / automatability | VMOS fit |
|---|---|---|---|---|---|
| **DeviceSpoofLab-Hooks** (yubunus, ~105★, Java) | IMEI/MEID, IMSI/ICCID (Luhn), phone #, **ANDROID_ID, GAID**, GSF ID, App Set ID, MediaDrm ID, + full build.prop | per-app (LSPosed scope) | ✅ tested A13/14/15 | app UI "randomize"; config in app private storage (root-writable → scriptable) | ★★★★★ best — hybrid **Magisk+LSPosed** matches VMOS; covers all 3 IDs + native/Cronet layer |
| **AndroidFaker** (Android1500, ~700★, GPL-3.0) | IMEI, MAC/BT MAC, **Android ID**, SIM serial/sub, mobile #, MediaDrm, SIM operator, App Set ID, IP | per-app profiles | ✅ Android 8.1+ | per-app profile system (create/switch via UI, long-press) | ★★★★ user-friendly, profile-based; UI-driven config |
| **Lsposed-SimSpoof** (K0rnhulio) | ICCID, IMSI, **IMEI**, phone #, carrier/country | **system framework (all apps)** | ✅ LSPosed 1.8+, A7+ | values **hardcoded → rebuild APK** per identity | ★★★ great "one device = one global identity" model, but rebuild-per-profile friction (or fork to read a config file) |
| **XPrivacyLua** (M66B) / **XPL-EX** (0bbedCode fork) | Android ID, GAID, GSF, serial, IMEI (`000…`), IMSI, ICCID, phone # | per-app scope | ✅ to A13 (community/LSPosed_mod) | privacy-masking (fake/blank, not chosen values); discontinued official | ★★ privacy masking, not believable *chosen* identity; XPL-EX fork more capable |
| **apps-matrix** (Bwijn) | SIM/network/locale/timezone only — **no IMEI/deviceID** | per-app (matrix.json) | ✅ | config baked in APK (rebuild) | ★★ good architecture reference; too narrow for IDs |

## Recommendation for the reseller pipeline

1. **Primary: DeviceSpoofLab-Hooks** — the only candidate covering **all three**
   missing IDs (IMEI + GAID + Android ID) plus build props, with a **hybrid
   Magisk + LSPosed** design that exactly matches what VMOS already has enabled.
   Its Magisk companion (`DeviceSpoofLab-Magisk`) boot-spoofs `Build.*` to beat
   native/Cronet reads that our current `resetprop`-only toolkit misses.
2. **Alternative: Lsposed-SimSpoof** if you prefer **one global identity per
   instance** (system-framework scope = every app, no per-app scoping) — a clean
   match for "1 cloud phone = 1 sold device". Cost: rebuild the APK per identity,
   or fork it to read values from a file (e.g. `/data/local/tmp/spoof.json`).
3. **AndroidFaker** as a friendlier profile-based option if you manage identities
   by hand rather than at scale.

## Fit / integration notes (VMOS-specific)

- Install path (headless, root shell we already have): push the module APK with
  `client.apps.upload_file_v3(url=...)` or `pm install`, then it appears in the
  LSPosed module list. **Scoping** a module to apps is stored in LSPosed's
  `modules_config.db` (`/data/adb/lspd/config/`), which is **root-writable** — so
  scope can be scripted instead of tapping the (widget-only) LSPosed Manager.
- Per-instance identity: for a reseller "1 device = 1 identity" model, a
  **system-framework-scoped** module (Lsposed-SimSpoof style) or writing
  DeviceSpoofLab's per-app config as root is the automatable route.
- Consistency: pair the module (IMEI/GAID/AndroidID) with `vmos.spoof`
  (build.prop) and `update_sim` + proxy (carrier/IP) for a coherent profile.

## ⚠️ Caveats

- **Detection**: all Java-level hooks can be detected by hardened apps
  (native `__system_property_get`, Cronet, integrity libs). DeviceSpoofLab's
  boot Magisk layer mitigates native reads; a stealth LSPosed fork (e.g.
  "Vector") is suggested when modules are detected.
- **Hardware attestation** (TEE key attestation, Play Integrity STRONG) is
  **not** defeated by any of these — hardware-signed, out of reach of software.
- These are third-party projects; vet the APK, pin a version, and test on one
  instance before fleet rollout. Use for legitimate device-variety reselling and
  comply with VMOS's ToS and target apps' terms.
