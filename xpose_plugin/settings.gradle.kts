pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositories {
        google(); mavenCentral()
        // ArmCloud/VMOS xscore may live in a vendor maven repo; add it here if needed:
        // maven { url = uri("https://<vmos-maven-repo>/") }
    }
}
rootProject.name = "vmos-xpose-spoof"
include(":app")
