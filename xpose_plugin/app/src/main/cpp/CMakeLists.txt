# Native Hook Core for the VMOS private XPose plugin.
# Builds libvmosnative.so, loaded from androidx.app.Entry.appMain via
# System.loadLibrary("vmosnative"). Uses Dobby (inline hook, MIT) + xDL (symbol
# resolver, MIT) — see THIRD_PARTY.md. The framework's own engine libengcore.so
# is resolved at runtime (dlopen) when present.
cmake_minimum_required(VERSION 3.22.1)
project("vmosnative")

# xDL sources (symbol resolution across the process's loaded .so's)
aux_source_directory(third_party/xdl XDL_SRC)
include_directories(third_party/xdl dobby)

# Dobby prebuilt static lib, per ABI
set(LINK_DIR ${PROJECT_SOURCE_DIR}/dobby/libs/${ANDROID_ABI})
add_library(dobby STATIC IMPORTED)
set_target_properties(dobby PROPERTIES IMPORTED_LOCATION ${LINK_DIR}/libdobby.a)

add_library(${CMAKE_PROJECT_NAME} SHARED native-lib.cpp ${XDL_SRC})

target_link_libraries(${CMAKE_PROJECT_NAME} android log dobby)
