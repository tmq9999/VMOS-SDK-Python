// Compile-only STUB of the VMOS/ArmCloud XPose API (com.android.core.*).
// Produces a plain jar used with `compileOnly(project(":xscore-stub"))` so the
// plugin builds even when the real `net.armcloud.xscore` artifact isn't on a
// public Maven repo. These classes are NOT packaged into the plugin APK — the
// framework supplies the real implementations at runtime.
plugins { id("java-library") }

java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}
