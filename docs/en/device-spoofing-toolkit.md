# Device-Spoofing Toolkit (reseller) — `vmos.spoof`

> Turn one cloud **real device** into any device profile — including models VMOS does **not** offer (e.g. Pixel 10 Pro / Android 17 / SDK 37) — for resellers who want a differentiated product. Tiếng Việt: [toolkit-spoof-thiet-bi.md](../vi/toolkit-spoof-thiet-bi.md).

## Why it works (verified live on a Pixel 7 Pro, 2026-07)

1. The VMOS ADB shell (`instance.async_cmd`) runs **as root** (`uid=0`, SELinux `u:r:xu_daemon:s0`) — no `su` needed.
2. Kitsune Magisk (`io.github.huskydg.magisk`) ships `resetprop` (`/data/adb/magisk/magisk64 resetprop`), which rewrites the read-only `ro.*` build props that VMOS's per-key property API **cannot** change on a real device.
3. Persistence: a Magisk module `system.prop` + a `service.d` boot script re-apply at boot → the spoof **survives reboots** (verified with a real reboot: OK).

## Prerequisite
**Kitsune Magisk must be enabled** on the instance: Toolbox → Magisk (Mask) → ON. The toolkit can enable it headlessly via `enable_magisk_ui`.

## Quickstart (Python)

```python
from vmos import VMOSClient, DeviceProfile, apply_profile, verify_profile

with VMOSClient() as c:
    profile = DeviceProfile(
        model="Pixel 10 Pro", brand="google", manufacturer="Google",
        device="frankel",
        fingerprint="google/frankel/frankel:17/BP1A.250101.001/13000000:user/release-keys",
        release="17", sdk=37, android_id="0123456789abcdef",
    )
    apply_profile(c, "ACP...", profile, persist=True)    # resetprop + boot module + android_id
    print(verify_profile(c, "ACP...", profile)["ok"])     # getprop read-back + compare
```

## CLI

```bash
python examples/12_device_spoof_toolkit.py --pad ACP... --enable-magisk --preset pixel10pro --verify
python examples/12_device_spoof_toolkit.py --pad ACP... --model "Galaxy Z Fold7" --brand samsung --release 16 --sdk 36 --verify
python examples/12_device_spoof_toolkit.py --pad ACP... --remove
```

## Toolkit API

| Function | Role |
|---|---|
| `DeviceProfile(...)` | Declare model/brand/manufacturer/device/fingerprint/release/sdk/android_id (`deep` also writes per-partition props) |
| `apply_profile(client, pad, profile, persist=True)` | Verify root+Magisk → resetprop all props → android_id → install persistence |
| `verify_profile(client, pad, profile)` | `getprop` read-back + compare → `{ok, checks}` |
| `remove_spoof(client, pad)` | Remove module + service.d (runtime resets on next reboot) |
| `magisk_ready(shell)` | Check Kitsune Magisk is present |
| `enable_magisk_ui(client, pad)` | Headless enable via Toolbox UI (best-effort, ratio-based taps) |

## Verified result (live)

```
apply PIXEL_10_PRO_A17 (persist=True): 43 props
verify now:        model=Pixel 10 Pro | release=17 | sdk=37 | fingerprint=google/frankel/... OK
--- real REBOOT ---
verify after boot: model=Pixel 10 Pro | release=17 | sdk=37 | fingerprint=google/frankel/... OK  (PERSISTED)
remove_spoof + reboot → back to Pixel 7 Pro / 13 / 33  OK
```

## Reseller strategy (layered)

| Layer | Tool | For |
|---|---|---|
| Base | ADI template (`replace_real_adi_template`) | Models in VMOS's catalog |
| **Deep custom** | **`vmos.spoof` (resetprop)** | **Any model/Android/SDK beyond the catalog** |
| SIM/region | `update_sim` + `set_proxy`/`smart_ip` | Operator + IP matching the country |
| Framework | LSposed (toggle in Toolbox) | Deeper IMEI/OAID/AndroidID hooks |

## Deep identity: IMEI / OAID / Android ID (live-tested)

Verified directly on a real device — the actual matrix:

| Identity | Mechanism | Result |
|---|---|---|
| build.prop (model/brand/fingerprint/release/sdk) | `resetprop` (toolkit) | ✅ Changeable, persists across reboot |
| **IMEI** | held by RIL/telephony framework (not a prop) | ❌ `resetprop` has no effect; apps read via `service call iphonesubinfo` |
| **OAID** | no prop/settings lever | ❌ Not shell-changeable |
| **Android ID** | `settings put secure android_id` | ❌ **Ignored on VMOS** (tested incl. `--user 0`) |

➡️ **IMEI/OAID/Android ID require a framework hook** — i.e. LSposed **plus an Xposed spoofing module** (an APK hooking `TelephonyManager.getImei()`, the OAID SDK, `Settings.Secure` ANDROID_ID).

**LSposed (tested):** enable via Toolbox → Lsposed → ON (toolkit: `enable_lsposed_ui`). After reboot the `lspd` daemon runs and the `zygisk_lsposed` module loads ✅ — **framework active**. However VMOS ships **no** spoofing module and no easily-scriptable Manager UI, so installing + activating an Xposed spoofing module is **out of scope** for this toolkit (needs a specific module APK).

```python
from vmos.spoof import enable_lsposed_ui, lsposed_ready
enable_lsposed_ui(client, "ACP...")   # enable LSposed framework (Magisk required) + reboot
# then install an Xposed spoofing module via the LSposed Manager to hook IMEI/OAID/AndroidID
```

Alternative without an Xposed module: **IMEI/IMSI** can be regenerated (randomly) via VMOS's `update_sim` / ADI template — enough for region/operator variety, but you can't pick a specific IMEI.

## ⚠️ Limits (set customer expectations)
- Software/`build.prop`-level spoof only. Hardware-backed attestation (TEE key attestation, Play Integrity STRONG) cannot be spoofed by any software method.
- `android_id` via `settings put secure android_id` is the legacy value; modern apps may use per-app/signed IDs.
- For legitimate reselling; comply with VMOS's ToS and target apps' terms.
