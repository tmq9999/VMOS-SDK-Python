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
 * </pre>
 * An empty / unset property means "leave the real value untouched", so you can
 * spoof only what you need. The VMOS SDK helper {@code vmos.spoof.set_identity_props}
 * sets these props for you.
 *
 * <p>Because this hooks the app-side Java getters ({@code TelephonyManager},
 * {@code Settings.Secure}) it changes what the scoped app actually reads — the
 * layer {@code resetprop} alone cannot reach for IMEI/IMSI/ICCID/ANDROID_ID.
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
            hookTelephony(loader);
        } catch (Throwable t) {
            Log.e(TAG, "hookTelephony failed: " + Log.getStackTraceString(t));
        }
        try {
            hookAndroidId(loader);
        } catch (Throwable t) {
            Log.e(TAG, "hookAndroidId failed: " + Log.getStackTraceString(t));
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
     * XPose SystemServer entry point (load with {@code -p android}). Hooking
     * build props here is optional — {@code resetprop} + a Magisk module already
     * cover {@code ro.*} build identity system-wide.
     */
    public static void systemMain(ClassLoader classLoader, String pkg, String processName) {
        Log.d(TAG, "systemMain pkg=" + pkg + " process=" + processName);
    }
}
