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
    // VMOS/ArmCloud XPose SDK: com.android.core.{XSHelpers, XC_MethodHook, XSBridge}
    // + the native hook engine (libengcore.so). MUST be bundled (implementation,
    // NOT compileOnly): the framework does NOT expose these classes to the
    // plugin's classloader at runtime, so a plugin that fails to ship them throws
    // NoClassDefFoundError when it tries to hook. Resolved from https://maven.vmos.cn
    // (configured in settings.gradle.kts). This matches the official ArmCloudXposed demo.
    implementation("net.armcloud.xscore:xscore:1.0.0")
    // Makes reflective reads of hidden android.os.SystemProperties reliable on
    // Android 9+ (bundled into the APK; used by Entry.appMain).
    implementation("org.lsposed.hiddenapibypass:hiddenapibypass:4.3")
}
