package com.android.core;

/**
 * Compile-time STUB of the VMOS/ArmCloud XPose helper {@code com.android.core.XSHelpers}.
 *
 * <p>Only satisfies {@code javac}; declared {@code compileOnly} and never shipped
 * in the APK. The real implementation (which actually installs the hook) is
 * provided by the framework at runtime. The vararg forms below cover every call
 * shape used by {@code androidx.app.Entry}:
 * <pre>
 *   findAndHookMethod(Class, "method", paramType..., XC_MethodHook)
 *   findAndHookMethod(Class, Object[]{ "method", paramType..., XC_MethodHook })
 * </pre>
 */
public class XSHelpers {

    /** Hook a method on an already-loaded class. Returns an unhook handle at runtime (ignored here). */
    public static Object findAndHookMethod(Class<?> clazz, Object... args) {
        return null;
    }

    /** Hook a method on a class resolved by name via the given loader. */
    public static Object findAndHookMethod(String className, ClassLoader classLoader, Object... args) {
        return null;
    }
}
