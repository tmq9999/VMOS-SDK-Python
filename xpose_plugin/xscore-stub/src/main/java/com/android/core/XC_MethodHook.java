package com.android.core;

/**
 * Compile-time STUB of the VMOS/ArmCloud XPose API class {@code com.android.core.XC_MethodHook}.
 *
 * <p>This exists only to satisfy {@code javac}. It is declared {@code compileOnly}
 * and is <b>never packaged into the APK</b>; the real implementation is provided
 * by the VMOS XPose framework at runtime. Keep the member signatures in sync with
 * what {@code androidx.app.Entry} uses ({@code args}, {@code setResult}).
 */
public abstract class XC_MethodHook {

    /** Per-invocation context passed to the hook callbacks. */
    public static class MethodHookParam {
        /** The hooked method's receiver ({@code null} for static methods). */
        public Object thisObject;
        /** The arguments the hooked method was called with. */
        public Object[] args;

        private Object result;

        public Object getResult() {
            return result;
        }

        /** Override the value the hooked method returns to its caller. */
        public void setResult(Object result) {
            this.result = result;
        }

        public Throwable getThrowable() {
            return null;
        }

        public void setThrowable(Throwable throwable) {
        }
    }

    /** Runs before the original method (override as needed). */
    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
    }

    /** Runs after the original method; use {@code param.setResult(...)} to override the return. */
    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
    }
}
