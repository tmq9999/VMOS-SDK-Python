plugins { id("com.android.application") }

android {
    namespace = "com.vmos.spoof.plugin"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.vmos.spoof.plugin"
        minSdk = 26          // Android 8.0+ (getImei introduced at API 26)
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            // Sign the release APK with the debug key so it is immediately
            // installable / loadable by `apmt`. Replace with your own keystore
            // for production if you want a stable signature.
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

dependencies {
    // VMOS/ArmCloud XPose API: com.android.core.{XSHelpers, XC_MethodHook, XSBridge}.
    // Default uses the in-repo compile-only STUB (:xscore-stub) so the plugin
    // builds even when the real artifact isn't on a public Maven repo. The real
    // classes are supplied by the framework at runtime (never packaged here).
    // If you HAVE the real artifact, swap the next line for:
    //     compileOnly("net.armcloud.xscore:xscore:1.0.0")
    compileOnly(project(":xscore-stub"))
    // Makes reflective reads of hidden android.os.SystemProperties reliable on
    // Android 9+ (bundled into the APK; used by Entry.appMain).
    implementation("org.lsposed.hiddenapibypass:hiddenapibypass:4.3")
}
