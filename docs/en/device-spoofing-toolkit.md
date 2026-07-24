# Device-Spoofing Toolkit (reseller) — `vmos.spoof`

> Turn one cloud **real device** into any device profile — including models VMOS does **not** offer (e.g. Pixel 10 Pro / Android 17 / SDK 37) — for resellers who want a differentiated product. Tiếng Việt: [toolkit-spoof-thiet-bi.md](../vi/toolkit-spoof-thiet-bi.md).

## Why it works (verified live on a Pixel 7 Pro, 2026-07)

1. The VMOS ADB shell (`instance.async_cmd`) runs **as root** (`uid=0`, SELinux `u:r:xu_daemon:s0`) — no `su` needed.
2. Kitsune Magisk (`io.github.huskydg.magisk`) ships `resetprop` (`/data/adb/magisk/magisk64 resetprop`), which rewrites the read-only `ro.*` build props that VMOS's per-key property API **cannot** change on a real device.
3. Persistence: a Magisk module `system.prop` + a `service.d` boot script re-apply at boot → the spoof **survives reboots** (verified with a real reboot: OK).

## Prerequisite — Magisk (with `resetprop`)

**Magisk must be present** on the instance (it provides `resetprop`). Two ways:

1. **Headless install (recommended, no Toolbox UI, no `switchRoot`)** —
   `enable_magisk_headless(client, pad)`. The VMOS async shell already runs as
   `uid=0` (`u:r:xu_daemon:s0`), which is enough to drop ArmCloud's cloud-Magisk
   payload into `/debug_ramdisk` and run its `install.sh`. Flow: query the OSS
   payload record (no auth) → `curl` the `.gz` onto the pad → `tar -xf` into
   `/debug_ramdisk` → run `magisk_env/install.sh`.
2. **Toolbox UI (fallback)** — Toolbox → Magisk (Mask) → ON, or `enable_magisk_ui`
   (best-effort, ratio-based taps).

**Live-verified 2026-07** (genuine Pixel 7 Pro pad): 27 MB payload,
`install.sh` → `Magisk安装成功`, `ro.sys.cloud.magisk=1`, and **`resetprop` works
immediately** — no reboot needed for build-prop spoofing. The Magisk
**daemon/Zygisk** (needed for modules/LSPosed) activate only after a reboot, so
pass `restart=True` if you need those.

```python
from vmos.spoof import enable_magisk_headless, magisk_ready
res = enable_magisk_headless(client, "ACP...")          # no UI, no switchRoot
# res["installed"] is True; resetprop is usable now (daemon needs restart=True)
```

## Quickstart (Python)

```python
from vmos import VMOSClient, DeviceProfile, apply_profile, verify_profile

with VMOSClient() as c:
    profile = DeviceProfile(
        model="Pixel 10 Pro", brand="google", manufacturer="Google",
        device="blazer",   # Pixel 10 Pro = blazer (frankel = Pixel 10, mustang = Pixel 10 Pro XL)
        fingerprint="google/blazer/blazer:17/CP2A.260705.006/15641320:user/release-keys",
        release="17", sdk=37, android_id="0123456789abcdef",
    )
    apply_profile(c, "ACP...", profile, persist=True)    # resetprop + boot module + android_id
    print(verify_profile(c, "ACP...", profile)["ok"])     # getprop read-back + compare
```

> **Use REAL fingerprints.** Codenames matter: **blazer = Pixel 10 Pro**,
> frankel = Pixel 10, mustang = Pixel 10 Pro XL. Pull authentic, current
> per-device build props from [Pixel-Props/build.prop](https://github.com/Pixel-Props/build.prop)
> (built-in presets `PIXEL_10_PRO_A17`, `PIXEL_10_A17`, `PIXEL_10_PRO_XL_A17`
> use these real values). A fabricated/mismatched fingerprint is an easy
> detection signal.

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
| `magisk_ready(shell)` | Check Magisk (`resetprop`) is present |
| `enable_magisk_headless(client, pad, restart=False)` | **Install cloud Magisk with no UI / no switchRoot** (OSS payload → `/debug_ramdisk` → `install.sh`); `resetprop` usable immediately |
| `query_magisk_payload_url(shell, pad)` | Get the cloud-Magisk `.gz` payload URL (on-pad OSS query, no auth) |
| `enable_magisk_ui(client, pad)` | Fallback: enable via Toolbox UI (best-effort, ratio-based taps) |

## Verified result (live)

```
apply PIXEL_10_PRO_A17 (persist=True): 43 props
verify now:        model=Pixel 10 Pro | release=17 | sdk=37 | fingerprint=google/blazer/blazer:17/... OK
--- real REBOOT ---
verify after boot: model=Pixel 10 Pro | release=17 | sdk=37 | fingerprint=google/blazer/blazer:17/... OK  (PERSISTED)
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

➡️ **IMEI/OAID/Android ID require a framework hook** — an APK that hooks `TelephonyManager.getImei()`/`getSubscriberId()`/… and `Settings.Secure` ANDROID_ID inside the target app. Two supported paths:

**Path 1 — Private XPose plugin (recommended).** VMOS ships its **native XPose framework** in-image (`/system/bin/apmt`, confirmed working), so a plugin built against its API is **always compatible** and fully **private**. Build once from [`xpose_plugin/`](../../xpose_plugin), then load headlessly:

```python
from vmos.spoof import set_identity_props, load_xpose_plugin
set_identity_props(client, "ACP...", imei="356789012345678", android_id="a1b2c3d4e5f60718")
load_xpose_plugin(client, "ACP...", name="vmosid",
                  target_pkg="com.example.targetapp", apk_url="https://your-host/plugin.apk")
```
Full guide: [xpose-custom-hook.md](xpose-custom-hook.md).

**Path 2 — LSposed module.** Enable via Toolbox → Lsposed → ON (`enable_lsposed_ui`); after reboot the `lspd` daemon runs and `zygisk_lsposed` loads ✅. **But** the framework bundled with VMOS's Kitsune is **old** (new modules hit a libxposed API mismatch, `NoSuchMethodException`), so a fresh LSPosed manager APK must replace it first, then scope the module with `scope_lsposed_module()`. Path 1 avoids this entirely.

Simplest alternative (no hook): **IMEI/IMSI** can be regenerated (randomly) via VMOS's `update_sim` / ADI template — enough for region/operator variety, but you can't pick a specific IMEI.

## Root hygiene / stealth (important for resellers)

Global root is the single most detectable signal (SafetyNet, banking, anti-fraud
apps all check for it). **Keep VMOS "Global Root" OFF** on shipped devices — and
it costs you nothing operationally (live-verified 2026-07):

- Turning global root off (`client.instance.switch_root(pad_codes=[pad],
  global_root=True, root_status=0)`, then reboot) sets
  `persist.sys.device.root.global=0` and removes `/system/xbin/su` + `/sbin/su`.
- The **VMOS management shell stays root regardless** — `async_cmd` runs as the
  VMOS daemon (`u:r:xu_daemon:s0`, `uid=0`), independent of the app-facing su
  flag — so `resetprop`, the persona CLI, and all spoofing still work headlessly.

`/system/bin/su` remains while **Kitsune Magisk** is enabled (Magisk provides a
systemless su, and you need Magisk for spoofing). Don't uninstall Magisk to hide
it — use Magisk's **Zygisk DenyList** to hide root from your target apps instead
(it's off by default). Recommended posture:

1. **Global Root: OFF** (enable only for a one-off op, then turn back off).
2. **Magisk DenyList: ON** + add the apps that must not see root.
3. **LSPosed**: scope modules only to the specific target apps, never broadly.
4. Administer/spoof through the **root API shell** — never leave global su on.

## ⚠️ Limits (set customer expectations)
- Software/`build.prop`-level spoof only. Hardware-backed attestation (TEE key attestation, Play Integrity STRONG) cannot be spoofed by any software method.
- `android_id` via `settings put secure android_id` is the legacy value; modern apps may use per-app/signed IDs.
- For legitimate reselling; comply with VMOS's ToS and target apps' terms.
