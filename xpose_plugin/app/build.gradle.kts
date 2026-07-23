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
    buildTypes { release { isMinifyEnabled = false } }
}

dependencies {
    // VMOS/ArmCloud XPose API: com.android.core.{XSHelpers, XC_MethodHook, XSBridge}
    // Provides the hook API at compile time; supplied by the framework at runtime.
    compileOnly("net.armcloud.xscore:xscore:1.0.0")
    // Fallback if the artifact is unavailable: drop a stub jar in app/libs/ (see README)
    // and use:  compileOnly(files("libs/xscore-stub.jar"))
    implementation("org.lsposed.hiddenapibypass:hiddenapibypass:4.3")
}
