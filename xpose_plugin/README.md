# VMOS private device-spoof plugin (XPose / `apmt`)

A **private, self-written** hook plugin for VMOS's **native XPose framework** —
no LSPosed, no third-party module. It hooks the app-side Java getters so a target
app reads the identity **you** choose — the layer `resetprop` alone cannot reach.
Coverage (Java getters, app process): IMEI/MEID/IMSI/ICCID/phone
(`TelephonyManager`), ANDROID_ID (`Settings.Secure`), GAID
(`AdvertisingIdClient$Info.getId`), Wi-Fi MAC/BSSID (`WifiInfo`), hardware serial
(`Build.getSerial()`), `MediaDrm` deviceUniqueId, MSA OAID — and you extend it by
adding a hook for whatever getter a specific app reads. It does **not** reach
Binder/native (see Scope & limits).

Why this over LSPosed modules: VMOS ships the XPose framework in-image
(`/system/bin/apmt`, confirmed working), so a plugin built against its API is
**always compatible** (no "new libxposed API vs old bundled LSPosed" mismatch),
fully **private** (your APK, no known module signature), and **tailored** to
exactly the methods you want.

## Design: build once, configure per device

The plugin hard-codes **nothing**. It reads spoof values from
`persist.vmos.spoof.*` system properties at hook time, so one APK serves every
device — set the values headlessly per instance with Magisk `resetprop`
(persist them via a Magisk module). Empty/unset ⇒ that field is left real.

| Property | `set_identity_props` arg | Overrides |
|---|---|---|
| `persist.vmos.spoof.imei` | `imei` | `TelephonyManager.getImei()/getDeviceId()` (+ per-slot) |
| `persist.vmos.spoof.meid` | `meid` | `getMeid()` |
| `persist.vmos.spoof.imsi` | `imsi` | `getSubscriberId()` |
| `persist.vmos.spoof.iccid` | `iccid` | `getSimSerialNumber()` |
| `persist.vmos.spoof.line1` | `line1` | `getLine1Number()` |
| `persist.vmos.spoof.androidid` | `android_id` | `Settings.Secure.getString(..., "android_id")` |
| `persist.vmos.spoof.gaid` | `gaid` | `AdvertisingIdClient$Info.getId()` (Google Ad ID) |
| `persist.vmos.spoof.wifimac` | `wifi_mac` | `WifiInfo.getMacAddress()` |
| `persist.vmos.spoof.bssid` | `bssid` | `WifiInfo.getBSSID()` |
| `persist.vmos.spoof.serial` | `serial` | `Build.getSerial()` |
| `persist.vmos.spoof.drmid` | `drm_id` | `MediaDrm.getPropertyByteArray("deviceUniqueId")` — Widevine (hex) |
| `persist.vmos.spoof.oaid` | `oaid` | MSA `IdSupplier.getOAID()` (best-effort; add concrete supplier per target) |

The VMOS SDK helper `vmos.spoof.set_identity_props(...)` sets these for you, and
`vmos.spoof.load_xpose_plugin(...)` runs the `apmt` load. Every extra hook is
guarded: if a class isn't present in the target app it's skipped, so the same
APK is safe to load anywhere.

## Build (needs a normal Android toolchain — not buildable inside the VMOS shell)

Full step-by-step: **[BUILD.md](BUILD.md)**. In short — Gradle pulls the real
VMOS XPose SDK (`net.armcloud.xscore:xscore:1.0.0`) from `https://maven.vmos.cn`
and **bundles** it (classes + native `libengcore.so`) into the APK:

```bash
# Android Studio: open this folder → Build > APK. Or CLI (JDK 17 + Android SDK):
gradle :app:assembleRelease        # → app/build/outputs/apk/release/app-release.apk
```
The release APK is debug-signed (see `app/build.gradle.kts`) so it loads without
extra steps. Needs network to `maven.vmos.cn` at build time (offline option in BUILD.md).

## Deploy (headless, via the VMOS SDK / root shell)

```python
from vmos import VMOSClient
from vmos.spoof import load_xpose_plugin, set_identity_props

with VMOSClient() as c:
    # 1) push spoof values (persist props, applied by resetprop; persist via Magisk module)
    set_identity_props(c, "ACP...", imei="356789012345678",
                       imsi="460110000000000", iccid="8986000000000000000",
                       android_id="a1b2c3d4e5f60718")
    # 2) load the plugin into the target app via apmt
    load_xpose_plugin(c, "ACP...", name="vmosid",
                      target_pkg="com.example.targetapp",
                      apk_url="https://your-host/vmos-xpose-spoof.apk")
    # 3) (re)start the target app — it now reads the spoofed identity
```

Equivalent raw commands on the device (root shell):
```sh
apmt patch add -n vmosid -p com.example.targetapp -u https://your-host/plugin.apk
apmt patch list         # verify
apmt patch del -n vmosid  # remove
```

## Verify (correct oracle)

LSPosed/XPose hooks live in the **app process**, so verify from a **scoped app**
that calls `TelephonyManager.getImei()` — **not** `service call iphonesubinfo`
or shell `getprop` (those bypass the Java hook). A quick check is a device-info
app (e.g. an APK that shows IMEI) added as the target `-p` package.

## Scope & limits

Java-layer, **app-process** spoof: hooks are installed in the target app's
process; the `systemMain` path is a no-op stub. It does **not** hook
Binder/AIDL, JNI, or native — so a shell `service call iphonesubinfo` still shows
the real IMEI (most apps use the Java `TelephonyManager` API, which *is* hooked).
GAID = the common `AdvertisingIdClient$Info.getId()` path; MediaDrm = the
`deviceUniqueId` getter only (not Widevine provisioning / certificate /
security-level / keybox). Hardware attestation (TEE, Play Integrity STRONG) is
unbeatable by any software; native/Binder reads need a different software
approach (Frida, Zygisk-native, inline/JNI hooks) — out of scope here. Full
detail: [../docs/en/xpose-custom-hook.md](../docs/en/xpose-custom-hook.md).

Use for legitimate device-variety reselling; comply with VMOS's ToS and target
apps' terms.
