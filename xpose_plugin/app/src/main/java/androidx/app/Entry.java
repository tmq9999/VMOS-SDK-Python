package androidx.app;

import android.content.Context;
import android.util.Log;

import com.android.core.XC_MethodHook;
import com.android.core.XSHelpers;

/**
 * VMOS private device-identity spoof plugin for the ArmCloud/VMOS XPose framework.
 *
 * <p>Loaded per target app with:
 * <pre>apmt patch add -n vmosid -p &lt;target.pkg&gt; -f /sdcard/vmos-xpose-spoof.apk</pre>
 *
 * <p><b>Build once, configure per device.</b> The hook does not hard-code any
 * identity. Instead it reads spoof values from {@code persist.vmos.spoof.*}
 * system properties, which you set headlessly with Magisk {@code resetprop}
 * (and persist via a Magisk module) — no rebuild per device:
 * <pre>
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.imei      356789012345678
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.meid      A0000012345678
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.imsi      460110000000000
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.iccid     8986000000000000000
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.line1     84987654321
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.androidid a1b2c3d4e5f60718
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.gaid      38400000-8cf0-11bd-b23e-10b96e40000d
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.wifimac   02:00:00:11:22:33
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.serial    1A2B3C4D5E6F
 *   /data/adb/magisk/magisk64 resetprop -n persist.vmos.spoof.drmid     deadbeefcafe0011  (hex)
 * </pre>
 * An empty / unset property means "leave the real value untouched", so you can
 * spoof only what you need. The VMOS SDK helper {@code vmos.spoof.set_identity_props}
 * sets these props for you.
 *
 * <p>Because this hooks the app-side Java getters it changes what the scoped app
 * actually reads — the layer {@code resetprop} alone cannot reach. Coverage:
 * {@code TelephonyManager} (IMEI/MEID/IMSI/ICCID/line1), {@code Settings.Secure}
 * (ANDROID_ID), {@code AdvertisingIdClient$Info.getId} (common GAID path),
 * {@code WifiInfo} (MAC/BSSID), {@code Build.getSerial()}, {@code MediaDrm}
 * deviceUniqueId getter, and the MSA OAID supplier. Every extra hook is
 * guarded — absent classes are skipped — so one APK is safe to load into any
 * target, and you extend it by adding a hook for whatever getter a specific app
 * uses.
 *
 * <p><b>Scope/limits:</b> this is an <i>app-process, Java-layer</i> hook. It does
 * not hook Binder/AIDL, JNI, or native code (so a shell {@code service call
 * iphonesubinfo} still returns the real IMEI), does not cover every method
 * overload or a separate {@code DexClassLoader}, and does not alter Widevine
 * provisioning/attestation. {@link #systemMain} is a no-op stub today.
 */
public class Entry {

    private static final String TAG = "VMOSSpoof";

    /** Read a system property (via the hidden android.os.SystemProperties). "" if unset. */
    private static String prop(String key) {
        try {
            Class<?> sp = Class.forName("android.os.SystemProperties");
            Object v = sp.getMethod("get", String.class, String.class).invoke(null, key, "");
            return v == null ? "" : (String) v;
        } catch (Throwable t) {
            return "";
        }
    }

    /** XPose app entry point (must be exactly this signature). */
    public static void appMain(ClassLoader loader, Context context, String appClass, String pkg, String process) {
        if (process != null && process.contains("sandboxed_process")) return; // skip webview procs
        Log.d(TAG, "appMain pkg=" + pkg + " process=" + process);
        try {
            // Allow reflective reads of the hidden android.os.SystemProperties on Android 9+.
            org.lsposed.hiddenapibypass.HiddenApiBypass.addHiddenApiExemptions("Landroid/os/SystemProperties;");
        } catch (Throwable ignored) { /* class absent / older API — plain reflection still works */ }
        try {
            hookTelephony(loader);
        } catch (Throwable t) {
            Log.e(TAG, "hookTelephony failed: " + Log.getStackTraceString(t));
        }
        try {
            hookAndroidId(loader);
        } catch (Throwable t) {
            Log.e(TAG, "hookAndroidId failed: " + Log.getStackTraceString(t));
        }
        try {
            hookExtras(loader);
        } catch (Throwable t) {
            Log.e(TAG, "hookExtras failed: " + Log.getStackTraceString(t));
        }
    }

    /** Force a method's return value to the given property, when that property is set. */
    private static void forceReturnFromProp(Class<?> cls, String method, final String propKey, Class<?>... paramTypes) {
        try {
            Object[] args = new Object[paramTypes.length + 2];
            args[0] = method;
            System.arraycopy(paramTypes, 0, args, 1, paramTypes.length);
            args[args.length - 1] = new XC_MethodHook() {
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    String v = prop(propKey);
                    if (v != null && !v.isEmpty()) {
                        param.setResult(v);
                    }
                }
            };
            XSHelpers.findAndHookMethod(cls, args);
            Log.d(TAG, "hooked " + cls.getSimpleName() + "." + method + " <- " + propKey);
        } catch (Throwable t) {
            Log.d(TAG, "skip " + method + ": " + t);
        }
    }

    private static void hookTelephony(ClassLoader loader) throws Exception {
        Class<?> tm = loader.loadClass("android.telephony.TelephonyManager");
        // IMEI (API 26+): no-arg + per-slot
        forceReturnFromProp(tm, "getImei", "persist.vmos.spoof.imei");
        forceReturnFromProp(tm, "getImei", "persist.vmos.spoof.imei", int.class);
        // Legacy device id (== IMEI on GSM / MEID on CDMA)
        forceReturnFromProp(tm, "getDeviceId", "persist.vmos.spoof.imei");
        forceReturnFromProp(tm, "getDeviceId", "persist.vmos.spoof.imei", int.class);
        forceReturnFromProp(tm, "getMeid", "persist.vmos.spoof.meid");
        forceReturnFromProp(tm, "getMeid", "persist.vmos.spoof.meid", int.class);
        // IMSI / ICCID / phone number
        forceReturnFromProp(tm, "getSubscriberId", "persist.vmos.spoof.imsi");
        forceReturnFromProp(tm, "getSubscriberId", "persist.vmos.spoof.imsi", int.class);
        forceReturnFromProp(tm, "getSimSerialNumber", "persist.vmos.spoof.iccid");
        forceReturnFromProp(tm, "getSimSerialNumber", "persist.vmos.spoof.iccid", int.class);
        forceReturnFromProp(tm, "getLine1Number", "persist.vmos.spoof.line1");
    }

    /** Hook Settings.Secure.getString(...) to override ANDROID_ID for the scoped app. */
    private static void hookAndroidId(ClassLoader loader) throws Exception {
        Class<?> secure = loader.loadClass("android.provider.Settings$Secure");
        Class<?> cr = loader.loadClass("android.content.ContentResolver");
        XSHelpers.findAndHookMethod(secure, "getString", cr, String.class, new XC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                if (param.args.length >= 2 && "android_id".equals(param.args[1])) {
                    String v = prop("persist.vmos.spoof.androidid");
                    if (v != null && !v.isEmpty()) param.setResult(v);
                }
            }
        });
        Log.d(TAG, "hooked Settings.Secure.getString(android_id)");
    }

    /**
     * Extra identity surfaces beyond telephony / ANDROID_ID. Each block is fully
     * guarded: if the class/method isn't present in this app it is silently
     * skipped (so the same APK is safe to load into any target). This is what
     * makes the private plugin "deeper" than a fixed third-party module — add a
     * hook for any getter a target app uses to fingerprint the device.
     */
    private static void hookExtras(ClassLoader loader) {
        // Google Advertising ID (GAID) — present when the app links Play Services ads.
        try {
            Class<?> info = loader.loadClass("com.google.android.gms.ads.identifier.AdvertisingIdClient$Info");
            forceReturnFromProp(info, "getId", "persist.vmos.spoof.gaid");
        } catch (Throwable t) {
            Log.d(TAG, "gaid skip: " + t);
        }
        // Wi-Fi MAC (getMacAddress + getBSSID) — WifiInfo.
        try {
            Class<?> wi = loader.loadClass("android.net.wifi.WifiInfo");
            forceReturnFromProp(wi, "getMacAddress", "persist.vmos.spoof.wifimac");
            forceReturnFromProp(wi, "getBSSID", "persist.vmos.spoof.bssid");
        } catch (Throwable t) {
            Log.d(TAG, "wifi skip: " + t);
        }
        // Hardware serial — Build.getSerial() (static). Build.SERIAL static field
        // comes from ro.serialno, which resetprop already covers.
        try {
            Class<?> build = loader.loadClass("android.os.Build");
            forceReturnFromProp(build, "getSerial", "persist.vmos.spoof.serial");
        } catch (Throwable t) {
            Log.d(TAG, "serial skip: " + t);
        }
        // MediaDrm / Widevine device-unique-id (byte[]) — used by DRM/streaming apps.
        try {
            hookMediaDrm(loader);
        } catch (Throwable t) {
            Log.d(TAG, "mediadrm skip: " + t);
        }
        // OAID (MSA SDK). The concrete supplier class varies per integration; this
        // overrides the common interface getter when a concrete impl exposes it.
        try {
            Class<?> supplier = loader.loadClass("com.bun.miitmdid.interfaces.IdSupplier");
            forceReturnFromProp(supplier, "getOAID", "persist.vmos.spoof.oaid");
        } catch (Throwable t) {
            Log.d(TAG, "oaid skip (add the concrete supplier class for your target): " + t);
        }
    }

    /** Hook {@code MediaDrm.getPropertyByteArray("deviceUniqueId")} (Widevine ID). */
    private static void hookMediaDrm(ClassLoader loader) throws Exception {
        Class<?> drm = loader.loadClass("android.media.MediaDrm");
        XSHelpers.findAndHookMethod(drm, "getPropertyByteArray", String.class, new XC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                if (param.args.length >= 1 && "deviceUniqueId".equals(param.args[0])) {
                    String hex = prop("persist.vmos.spoof.drmid");
                    if (hex != null && !hex.isEmpty()) param.setResult(hexToBytes(hex));
                }
            }
        });
        Log.d(TAG, "hooked MediaDrm.getPropertyByteArray(deviceUniqueId)");
    }

    /** Parse a hex string (e.g. "deadbeef…") into bytes for byte[]-returning hooks. */
    private static byte[] hexToBytes(String s) {
        int n = s.length() & ~1;              // ignore a trailing odd nibble
        byte[] out = new byte[n / 2];
        for (int i = 0; i < n; i += 2) {
            out[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i + 1), 16));
        }
        return out;
    }

    /**
     * XPose SystemServer entry point (load with {@code -p android}). Hooking
     * build props here is optional — {@code resetprop} + a Magisk module already
     * cover {@code ro.*} build identity system-wide.
     */
    public static void systemMain(ClassLoader classLoader, String pkg, String processName) {
        Log.d(TAG, "systemMain pkg=" + pkg + " process=" + processName);
    }
}
