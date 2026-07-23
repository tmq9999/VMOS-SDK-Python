package com.android.core;

/**
 * Compile-time STUB of {@code com.android.core.XSBridge} (VMOS/ArmCloud XPose API).
 *
 * <p>Not referenced by {@code androidx.app.Entry} today — included so the stub
 * mirrors the documented API surface and future hooks can call it. Declared
 * {@code compileOnly}; the real class is provided by the framework at runtime.
 */
public class XSBridge {

    public static void log(String message) {
    }

    public static void log(Throwable throwable) {
    }

    /** Invoke the original (un-hooked) implementation of a method. */
    public static Object invokeOriginalMethod(Object method, Object thisObject, Object[] args) throws Throwable {
        return null;
    }
}
