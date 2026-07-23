# Private XPose hook — spoof IMEI / IMSI / ICCID / ANDROID_ID (`apmt`)

> Write your **own** framework hook against VMOS's **native XPose framework** —
> no LSPosed, no third-party module. This reaches the identity layer that
> `resetprop` alone cannot: the Java getters an app calls for IMEI / IMSI /
> ICCID / phone number / ANDROID_ID. Tiếng Việt: [xpose-custom-hook-vi.md](../vi/xpose-custom-hook-vi.md).

Project source lives in [`xpose_plugin/`](../../xpose_plugin) of this repo.

## Why a private XPose plugin (not an LSPosed module)

| | Private XPose plugin (`apmt`) | LSPosed module |
|---|---|---|
| Framework | VMOS **ships XPose in-image** (`/system/bin/apmt`, confirmed working) | Bundled `zygisk_lsposed` is **old**; new modules hit a libxposed API mismatch (`NoSuchMethodException`) |
| Compatibility | **Always compatible** — built against the image's own API | Must match the manager/module ABI; VMOS's bundled one lags |
| Privacy | **Your** APK, no known module signature | Well-known package/signature, easy to fingerprint |
| Fit | Hooks **exactly** the methods you choose | Whatever the third-party module decided |

This is the path to pick when you want IMEI/IMSI/ICCID/ANDROID_ID spoofing that
is private, tailored, and won't break on the next VMOS image.

## Confirmed framework facts (live on the test pad, 2026-07)

- `/system/bin/apmt` exists and runs: `apmt patch add|list|del`.
- Plugin = an APK whose entry class is `androidx.app.Entry` with:
  - `public static void appMain(ClassLoader loader, Context context, String appClass, String pkg, String process)` — runs **inside the target app** process.
  - `public static void systemMain(ClassLoader loader, String pkg, String processName)` — runs in **SystemServer** (`-p android`).
- API library: `net.armcloud.xscore:xscore:1.0.0`
  - `com.android.core.XSHelpers` — `findAndHookMethod(Class, "method", paramTypes…, XC_MethodHook)`
  - `com.android.core.XC_MethodHook` — `beforeHookedMethod` / `afterHookedMethod`, `param.setResult(...)`
  - `com.android.core.XSBridge`

## Design: build once, configure per device

The plugin **hard-codes nothing**. At hook time it reads spoof values from
`persist.vmos.spoof.*` system properties, so one APK serves every instance —
set values headlessly per device with Magisk `resetprop`. An empty/unset
property means "leave the real value untouched", so you spoof only what you need.

| Property | `set_identity_props` arg | Overrides (in scoped app) |
|---|---|---|
| `persist.vmos.spoof.imei` | `imei` | `TelephonyManager.getImei()` / `getDeviceId()` (+ per-slot) |
| `persist.vmos.spoof.meid` | `meid` | `getMeid()` |
| `persist.vmos.spoof.imsi` | `imsi` | `getSubscriberId()` |
| `persist.vmos.spoof.iccid` | `iccid` | `getSimSerialNumber()` |
| `persist.vmos.spoof.line1` | `line1` | `getLine1Number()` |
| `persist.vmos.spoof.androidid` | `android_id` | `Settings.Secure.getString(…, "android_id")` |
| `persist.vmos.spoof.gaid` | `gaid` | `AdvertisingIdClient$Info.getId()` (common GAID read path) |
| `persist.vmos.spoof.wifimac` | `wifi_mac` | `WifiInfo.getMacAddress()` |
| `persist.vmos.spoof.bssid` | `bssid` | `WifiInfo.getBSSID()` |
| `persist.vmos.spoof.serial` | `serial` | `Build.getSerial()` |
| `persist.vmos.spoof.drmid` | `drm_id` | `MediaDrm.getPropertyByteArray("deviceUniqueId")` getter (hex) |
| `persist.vmos.spoof.oaid` | `oaid` | MSA `IdSupplier.getOAID()` (best-effort per target) |

**Extensible by design:** you hook exactly the getters you want, and adding a
surface is one line in `xpose_plugin/`. Every extra hook is guarded — if a class
is absent in the target app it's skipped — so one APK loads safely into any app.
This significantly widens Java-layer coverage of common fingerprint APIs; it is
**not** a total device-identity replacement. See **Scope & limits** below.

## Deploy headless (VMOS SDK)

```python
from vmos import VMOSClient
from vmos.spoof import set_identity_props, load_xpose_plugin, list_xpose_plugins

with VMOSClient() as c:
    # 1) push the per-device identity values (resetprop + persist in Magisk module)
    set_identity_props(c, "ACP...",
                       imei="356789012345678", imsi="460110000000000",
                       iccid="8986000000000000000", android_id="a1b2c3d4e5f60718")

    # 2) load the plugin into the target app via apmt (build once, host the APK anywhere)
    load_xpose_plugin(c, "ACP...", name="vmosid",
                      target_pkg="com.example.targetapp",
                      apk_url="https://your-host/vmos-xpose-spoof.apk")

    print(list_xpose_plugins(c, "ACP..."))   # verify it's loaded
    # 3) restart the target app — it now reads the spoofed identity
```

Raw device equivalent (root shell):

```sh
apmt patch add -n vmosid -p com.example.targetapp -u https://your-host/plugin.apk
apmt patch list
apmt patch del -n vmosid
```

Helpers: `set_identity_props`, `load_xpose_plugin`, `list_xpose_plugins`,
`remove_xpose_plugin` (all in `vmos.spoof`).

## Build the APK

Not buildable inside the VMOS shell — use a normal Android toolchain (Android
Studio, or `gradle :app:assembleRelease` with Android SDK + JDK 17). If the
`net.armcloud.xscore` artifact isn't on public Maven, take it from the official
demo (`ArmCloudXposed.zip`) or drop a compile-time **stub** jar exposing
`com.android.core.{XSHelpers, XC_MethodHook, XSBridge}` into `app/libs/` — the
real classes are provided by the framework at runtime; the stub only satisfies
`javac`. Full steps: [`xpose_plugin/README.md`](../../xpose_plugin/README.md).

## Verify with the CORRECT oracle

XPose/LSPosed hooks live in the **app process**. So verify from a **scoped app**
that calls `TelephonyManager.getImei()` (e.g. a device-info APK added as the `-p`
target). Do **not** use `service call iphonesubinfo` or shell `getprop` — those
bypass the Java hook and will show the real value even when the spoof works.

## Scope & limits (what it does / doesn't do)

Be precise about this to avoid over-promising to customers:

- **App-process only.** Hooks are installed in the target app's process
  (`appMain`). `systemMain` (`-p android`) is currently a no-op stub — there is
  no system-wide hook yet.
- **Java layer only.** It hooks Java getters. It does **not** hook Binder/AIDL
  transactions, JNI, or native code. This is exactly why a shell `service call
  iphonesubinfo` (the Binder path) still returned the real IMEI in our live
  tests — expected: most apps use the Java `TelephonyManager` API, which *is*
  hooked.
- **Common access paths, not every overload.** GAID = `AdvertisingIdClient$Info.getId()`
  (the usual read path) — not App Set ID, Limit-Ad-Tracking state, or the GMS
  Binder route. MediaDrm = the `deviceUniqueId` getter only — it does **not**
  change Widevine provisioning, the DRM certificate, security level, or keybox.
- **Single class loader.** Classes are resolved via the loader passed to
  `appMain`; app code loaded in a separate `DexClassLoader` may not be covered.

**Ceilings:** hardware-backed attestation (TEE key attestation, Play Integrity
STRONG) is unbeatable by **any** software method. Native / Binder reads are out
of reach of **this Java plugin** — but other software approaches exist (Frida,
Zygisk-native, inline / PLT-GOT / JNI hooks, ROM or system-library patching);
they are simply out of scope here. To go deeper, extend the plugin
(Binder / `system_server` hooks) or pair it with a native (Zygisk) layer.

## Ethics

Use for legitimate device-variety reselling and comply with VMOS's ToS and the
target apps' terms.
