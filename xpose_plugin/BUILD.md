# Build the plugin APK — step by step

The plugin (`androidx.app.Entry`) can't be built inside the VMOS shell; you need
a normal Android toolchain **once**. After that, one APK serves every device —
you configure identities per device with `set_identity_props` (no rebuild).

Good news: the `com.android.core.*` XPose API is provided in this repo as a
**compile-only stub** (`xscore-stub/`), so you do **not** need the real
`net.armcloud.xscore` artifact to compile. The real classes are supplied by the
VMOS framework at runtime.

## 0. What you need

- **JDK 17** (Android Gradle Plugin 8.5 requires it).
- **Android SDK**: `platforms;android-35`, `build-tools;35.0.0`, `platform-tools`.
- Either **Android Studio** (easiest — bundles all of the above) or the
  command-line tools + Gradle 8.7+.

---

## Option A — Android Studio (simplest)

1. **File → Open…** and select the `xpose_plugin/` folder. Let Gradle sync finish
   (it downloads AGP, Gradle, and the `hiddenapibypass` dependency).
2. **Build → Build Bundle(s) / APK(s) → Build APK(s)** — or run the Gradle task
   `:app:assembleRelease` from the Gradle panel.
3. Grab the APK from:
   ```
   xpose_plugin/app/build/outputs/apk/release/app-release.apk
   ```
   It's signed with the debug key (see `app/build.gradle.kts`), so it installs and
   loads without extra steps.

---

## Option B — Command line (no IDE)

```bash
# 1) JDK 17 must be active
java -version        # -> 17.x

# 2) Install the Android SDK command-line tools, then:
export ANDROID_HOME="$HOME/Android/Sdk"
yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --licenses
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" \
    "platforms;android-35" "build-tools;35.0.0" "platform-tools"

# 3) Point the build at the SDK
cd xpose_plugin
echo "sdk.dir=$ANDROID_HOME" > local.properties

# 4) Build (Gradle 8.7+; or run `gradle wrapper` first to get ./gradlew)
gradle :app:assembleRelease        # -> app/build/outputs/apk/release/app-release.apk
```

> No system Gradle? Run `gradle wrapper --gradle-version 8.9` once (with any
> Gradle) to generate `./gradlew`, then use `./gradlew :app:assembleRelease`.

---

## About the `net.armcloud.xscore` library

You do **not** need it to build — `xscore-stub/` satisfies the compiler and is
never packaged into the APK. If you later obtain the real artifact (e.g. from the
official `ArmCloudXposed.zip` demo or a VMOS vendor Maven repo), you can switch
`app/build.gradle.kts` from:

```kotlin
compileOnly(project(":xscore-stub"))
```
to
```kotlin
compileOnly("net.armcloud.xscore:xscore:1.0.0")
```
(and add the vendor repo in `settings.gradle.kts`). Either way the runtime
behavior is identical — the framework provides the real classes.

---

## Host the APK so the pad can load it

`apmt` can pull the APK by URL (downloaded on the pad) or from a path already on
the pad:

- **Public URL** → use `--apk-url`. Any static host works (your server, an object
  store, a release asset). Make sure the pad can reach it over HTTPS.
- **Push to the pad first** → then use `--apk-path`. From the VMOS SDK root shell
  the pad has `curl`, so you can fetch it directly onto the device:
  ```python
  from vmos import VMOSClient
  from vmos.spoof import PadRootShell
  with VMOSClient() as c:
      PadRootShell(c, "ACP...").sh(
          "curl -L -o /sdcard/vmos-xpose-spoof.apk https://your-host/app-release.apk")
  ```

---

## Deploy + verify (ready to run)

Once you have the APK URL (or it's on the pad), the SDK does the rest — see
[`../examples/13_xpose_deploy.py`](../examples/13_xpose_deploy.py):

```bash
VMOS_ACCESS_KEY=... VMOS_SECRET_KEY=... \
python examples/13_xpose_deploy.py --pad ACP... \
    --target-pkg com.example.targetapp \
    --apk-url https://your-host/app-release.apk \
    --imei 356789012345678 \
    --gaid 38400000-8cf0-11bd-b23e-10b96e40000d \
    --android-id a1b2c3d4e5f60718
```

That sets the `persist.vmos.spoof.*` props, loads the plugin via `apmt`, restarts
the target app, prints `apmt patch list`, and tails the plugin's logcat
(`VMOSSpoof` tag) so you can see the `hooked …` confirmation lines.

**Verify with the correct oracle:** read the value from a **scoped app** that
calls the Java getter (e.g. a device-info app showing IMEI/GAID). Do **not** use
`service call iphonesubinfo` or shell `getprop` — those bypass the app-process
Java hook and will show the real value even when the spoof works.
