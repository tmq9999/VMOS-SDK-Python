# Third-party native components

The Native Hook Core vendors two open-source libraries (both MIT), consistent
with the official ArmCloudXposed demo:

| Component | Files | License | Purpose |
|---|---|---|---|
| **Dobby** | `dobby/` (headers + `libs/<abi>/libdobby.a`) | MIT | ARM/ARM64 inline hook engine (`DobbyHook`, `DobbySymbolResolver`) |
| **xDL** | `third_party/xdl/` (sources + `LICENSE`) | MIT | in-process dynamic-linker symbol resolver (`xdl_open`/`xdl_sym`/`xdl_dsym`) |

The framework's own native engine `libengcore.so` (from the proprietary
`net.armcloud.xscore` aar) is **not** vendored — it is resolved at runtime via
`dlopen` when present. `libdobby.a` is prebuilt for `arm64-v8a` and
`armeabi-v7a`; rebuild from the upstream Dobby project if you need other ABIs.
