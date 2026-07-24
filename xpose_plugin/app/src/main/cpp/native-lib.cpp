// Native Hook Core (minimal) for the VMOS private XPose plugin.
//
// Goals of this minimal core (Roadmap item B):
//   1. the .so loads successfully (arm64-v8a first);
//   2. wraps Dobby (inline hook) + xDL (symbol resolver);
//   3. a **profile bridge that only READS** persist.vmos.spoof.* (no hard-coded
//      identity — every value comes from the Device Profile, same as Java);
//   4. reproduces the VMOS demo hook end-to-end (a Dobby inline hook on a libc
//      function, installed as a safe pass-through) to prove the toolchain works;
//   5. lifecycle logging + crash-guard (every step guarded; a failure logs and
//      returns — it never aborts the host process).
//
// It does NOT yet spoof any identity natively. Reaching real native identity
// sources (e.g. IMEI in com.android.phone) is Roadmap C: it must be traced and
// PoC'd per ROM before being trusted (see docs/en/device-profile-framework.md).
//
// Third-party: Dobby (MIT), xDL (MIT) — see THIRD_PARTY.md.

#include <jni.h>
#include <string>
#include <dlfcn.h>
#include <sys/system_properties.h>

#include "dobby.h"
#include "xdl.h"
#include "LogUtil.h"

// ---- Profile bridge: READ-ONLY access to persist.vmos.spoof.* -------------
static std::string profile_prop(const char *key) {
    char buf[PROP_VALUE_MAX] = {0};
    int n = __system_property_get(key, buf);
    return n > 0 ? std::string(buf, n) : std::string();
}

// ---- Optional: the framework's own native hook engine ---------------------
// libengcore.so (bundled by xscore) exports db_hk_wrapper(addr, replace, &orig).
// We resolve it if present, but default to Dobby directly.
typedef int (*engcore_hook_t)(void *address, void *replace_call, void **origin_call);
static engcore_hook_t g_engcore_hook = nullptr;

static void init_engcore() {
    void *eng = dlopen("libengcore.so", RTLD_NOW);
    if (eng == nullptr) {
        LOGI("libengcore.so not present — using Dobby directly (ok)");
        return;
    }
    g_engcore_hook = (engcore_hook_t) dlsym(eng, "db_hk_wrapper");
    LOGI("libengcore.so db_hk_wrapper=%p", (void *) g_engcore_hook);
}

// ---- Demo hook: libc open() as a SAFE pass-through ------------------------
// Proves the inline-hook toolchain works end-to-end without changing behavior.
static int (*open_backup)(const char *, int, mode_t) = nullptr;

static int fake_open(const char *pathname, int flags, mode_t mode) {
    // pass-through only (no behavior change) — this is a toolchain smoke test
    return open_backup ? open_backup(pathname, flags, mode) : -1;
}

static void install_demo_hook() {
    void *addr = DobbySymbolResolver("libc.so", "open");
    if (addr == nullptr) {
        LOGE("demo hook: could not resolve libc.so!open (skip)");
        return;
    }
    int rc = DobbyHook(addr, (dobby_dummy_func_t) fake_open,
                       (dobby_dummy_func_t *) &open_backup);
    LOGI("demo hook: DobbyHook(open)=%d (0=ok) backup=%p", rc, (void *) open_backup);
}

// ---- Entry: loaded from Entry.appMain via System.loadLibrary("vmosnative") -
extern "C" JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM *vm, void * /*reserved*/) {
    LOGI("[core] JNI_OnLoad begin (Native Hook Core minimal)");

    // (3) profile bridge — READ-ONLY proof: show a value sourced from the Profile
    std::string imei = profile_prop("persist.vmos.spoof.imei");
    std::string aid = profile_prop("persist.vmos.spoof.androidid");
    LOGI("[core] profile bridge: imei='%s' androidid='%s' (read-only)",
         imei.c_str(), aid.c_str());

    // (4) toolchain proof + (2) Dobby/xDL wrapper, each guarded (5)
    init_engcore();
    install_demo_hook();

    LOGI("[core] JNI_OnLoad done");
    return JNI_VERSION_1_6;
}
