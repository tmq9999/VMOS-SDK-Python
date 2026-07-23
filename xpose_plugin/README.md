# VMOS private device-spoof plugin (XPose / `apmt`)

A **private, self-written** hook plugin for VMOS's **native XPose framework** —
no LSPosed, no third-party module. It hooks the app-side Java getters
(`TelephonyManager`, `Settings.Secure`) so a target app reads the IMEI / IMSI /
ICCID / phone-number / ANDROID_ID **you** choose — the layer `resetprop` alone
cannot reach.

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

| Property | Overrides |
|---|---|
| `persist.vmos.spoof.imei` | `TelephonyManager.getImei()/getDeviceId()` (+ per-slot) |
| `persist.vmos.spoof.meid` | `getMeid()` |
| `persist.vmos.spoof.imsi` | `getSubscriberId()` |
| `persist.vmos.spoof.iccid` | `getSimSerialNumber()` |
| `persist.vmos.spoof.line1` | `getLine1Number()` |
| `persist.vmos.spoof.androidid` | `Settings.Secure.getString(..., "android_id")` |

The VMOS SDK helper `vmos.spoof.set_identity_props(...)` sets these for you, and
`vmos.spoof.load_xpose_plugin(...)` runs the `apmt` load.

## Build (needs a normal Android toolchain — not buildable inside the VMOS shell)

```bash
# Android Studio: open this folder and Build > APK, or CLI with Android SDK + JDK 17:
gradle :app:assembleRelease        # → app/build/outputs/apk/release/app-release.apk
```
If the `net.armcloud.xscore:xscore:1.0.0` artifact isn't reachable from public
Maven, get it from the official demo (`ArmCloudXposed.zip` → its module depends
on the same lib) or drop a compile-time **stub** jar exposing
`com.android.core.{XSHelpers, XC_MethodHook, XSBridge}` into `app/libs/` and
switch the dependency to `compileOnly(files("libs/xscore-stub.jar"))`. The real
classes are provided by the framework at runtime; the stub only satisfies
`javac`.

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

## Scope & ethics

Software/Java-layer spoof only; hardware-backed attestation (TEE key
attestation, Play Integrity STRONG) is out of reach of any software method. Use
for legitimate device-variety reselling and comply with VMOS's ToS and target
apps' terms.
