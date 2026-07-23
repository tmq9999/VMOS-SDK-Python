pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositories {
        google(); mavenCentral()
        // VMOS/ArmCloud XPose SDK (com.android.core.* + native libengcore.so):
        maven(url = "https://maven.vmos.cn")
    }
}
rootProject.name = "vmos-xpose-spoof"
include(":app")
