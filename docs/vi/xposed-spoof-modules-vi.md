# Đánh giá module Xposed/LSPosed spoof thiết bị cho VMOS real device

> Nghiên cứu (2026-07) các module LSPosed/Xposed spoof được những định danh do **framework giữ** mà API VMOS + `resetprop` không đổi được (IMEI, OAID/GAID, Android ID). Bối cảnh: máy thật VMOS đã có sẵn **Kitsune Magisk + LSPosed framework + Zygisk** (đã kiểm chứng). English: [xposed-spoof-modules.md](../en/xposed-spoof-modules.md).

## Vì sao cần module

`vmos.spoof` (Magisk `resetprop`) lo được **build.prop** (model/brand/fingerprint/SDK/release) — đã chạy. Nhưng **IMEI, OAID/GAID, Android ID do framework/RIL giữ**, không phải system prop → cần **hook mức Java** trong tiến trình từng app, tức một LSPosed module. Bật *framework* LSPosed không (đã làm) — bản thân nó không hook gì; phải cài **module APK spoof** và gán scope cho app đích.

## Các ứng viên

| Module | Spoof được | Phạm vi | A13 + Zygisk | Config / tự động hoá | Phù hợp VMOS |
|---|---|---|---|---|---|
| **DeviceSpoofLab-Hooks** (yubunus, ~105★, Java) | IMEI/MEID, IMSI/ICCID (Luhn), số ĐT, **ANDROID_ID, GAID**, GSF ID, App Set ID, MediaDrm ID, + toàn bộ build.prop | theo app (LSPosed scope) | ✅ test A13/14/15 | "randomize" qua app UI; config trong bộ nhớ riêng app (root ghi được → script được) | ★★★★★ tốt nhất — kiến trúc **Magisk+LSPosed** khớp đúng VMOS; đủ cả 3 ID + lớp chống đọc native/Cronet |
| **AndroidFaker** (Android1500, ~700★, GPL-3.0) | IMEI, MAC/BT MAC, **Android ID**, SIM serial/sub, số ĐT, MediaDrm, SIM operator, App Set ID, IP | profile theo app | ✅ Android 8.1+ | hệ profile theo app (tạo/đổi qua UI, long-press) | ★★★★ thân thiện, theo profile; config qua UI |
| **Lsposed-SimSpoof** (K0rnhulio) | ICCID, IMSI, **IMEI**, số ĐT, nhà mạng/quốc gia | **system framework (mọi app)** | ✅ LSPosed 1.8+, A7+ | giá trị **hardcode → build lại APK** mỗi identity | ★★★ hợp mô hình "1 máy = 1 identity toàn cục", nhưng phải build lại (hoặc fork để đọc file config) |
| **XPrivacyLua** (M66B) / **XPL-EX** (0bbedCode) | Android ID, GAID, GSF, serial, IMEI (`000…`), IMSI, ICCID, số ĐT | theo app | ✅ tới A13 (cộng đồng/LSPosed_mod) | thiên về che (fake/blank, không phải giá trị chọn); bản gốc ngừng phát triển | ★★ che privacy, không tạo identity "chọn" đáng tin; fork XPL-EX mạnh hơn |
| **apps-matrix** (Bwijn) | chỉ SIM/network/locale/timezone — **không IMEI/deviceID** | theo app (matrix.json) | ✅ | config nhúng trong APK (build lại) | ★★ tham khảo kiến trúc tốt; quá hẹp cho ID |

## Khuyến nghị cho pipeline reseller

1. **Chính: DeviceSpoofLab-Hooks** — ứng viên duy nhất bao đủ **cả 3 ID còn thiếu** (IMEI + GAID + Android ID) + build props, kiến trúc **hybrid Magisk + LSPosed** khớp đúng thứ VMOS đã bật. Companion `DeviceSpoofLab-Magisk` spoof `Build.*` lúc boot để chống đọc native/Cronet — điều toolkit `resetprop`-only hiện tại chưa lo.
2. **Thay thế: Lsposed-SimSpoof** nếu muốn **1 identity toàn cục cho mỗi instance** (scope system-framework = mọi app, khỏi scope từng app) — hợp mô hình "1 cloud phone = 1 máy bán ra". Đổi lại: build APK lại mỗi identity, hoặc fork để đọc từ file (vd `/data/local/tmp/spoof.json`).
3. **AndroidFaker** khi quản identity thủ công theo profile thay vì quy mô lớn.

## Ghi chú tích hợp (riêng VMOS)

- Cài headless (đã có root shell): đẩy APK module bằng `client.apps.upload_file_v3(url=...)` hoặc `pm install`, module sẽ hiện trong danh sách LSPosed. **Scope** module cho app lưu ở `modules_config.db` của LSPosed (`/data/adb/lspd/config/`) — **root ghi được**, nên script scope được thay vì phải chạm Manager (vốn chỉ là widget).
- Identity theo instance: mô hình reseller "1 máy = 1 identity" → dùng module scope **system-framework** (kiểu Lsposed-SimSpoof) hoặc ghi config per-app của DeviceSpoofLab bằng root là hướng tự động hoá.
- Nhất quán: kết hợp module (IMEI/GAID/AndroidID) + `vmos.spoof` (build.prop) + `update_sim`/proxy (nhà mạng/IP) để có hồ sơ đồng bộ.

## Test thực tế — cài DeviceSpoofLab headless & kết quả (2026-07)

Đã cài **DeviceSpoofLab** end-to-end lên pad real-device, hoàn toàn headless qua root shell, và kiểm chứng:

**Cài (không UI):** pad có `curl` + `busybox` + `pm`:
```sh
curl -Lks -o /data/local/tmp/dsl.zip  <release .zip của DeviceSpoofLab-Magisk>
curl -Lks -o /data/local/tmp/dsl.apk  <release .apk của DeviceSpoofLab-Hooks>
mkdir -p /data/adb/modules/devicespooflab
cd /data/adb/modules/devicespooflab && busybox unzip -o -q /data/local/tmp/dsl.zip
pm install -r -g /data/local/tmp/dsl.apk        # APK LSPosed hooks (com.devicespooflab.hooks)
```
Copy tay thư mục module **được Magisk nhận lúc boot** (chạy `post-fs-data.sh`). Module theo cơ chế **persona**, script hoàn toàn qua CLI `common/webctl.sh`:
```sh
W=/data/adb/modules/devicespooflab/common/webctl.sh
sh $W generate-persona                          # tạo+activate persona (đọc config/*.conf), mark reboot
sh $W set-android-id "$(printf 'ENABLED\nVALUE=<16hex>\nUSER=0\nPKG=com.android.vending\n' | base64 -w0)"
sh $W apply-android-id                           # ghi lại SSAID store
sh $W status ; sh $W personas                    # trạng thái JSON
sh $W persona-delete <id>                        # revert về identity gốc
# rồi: reboot để áp dụng
```
Config là CSV thuần trong `config/*.conf` (`ENABLED,prop,value`, generator `${RANDOM_SERIAL}`, `${RANDOM_HEX:N}`) → chọn identity script được (vd `sed -i 's/Pixel 7 Pro/Pixel 10 Pro/g' config/device_identity.conf`).

**Kết quả sau reboot:**

| Mục tiêu | Cách | Kết quả |
|---|---|---|
| Build props (model → Pixel 10 Pro + partitions, serial) | Magisk `resetprop` lúc post-fs-data (persona) | ✅ `getprop ro.product.model` = Pixel 10 Pro; dính qua reboot |
| **Android ID** (vending, gms) | **ghi lại `/data/system/users/0/settings_ssaid.xml`** (ABX) — KHÔNG dùng `settings put` | ✅ đổi thành `00ddeeff11223344` (xác nhận trong ABX) — **đây là cách vượt được VMOS chặn `settings put`** |
| Đảo ngược | `persona-delete` khôi phục từ backup | ✅ về Pixel 7 Pro + SSAID gốc |

**IMEI / GAID (APK LSPosed) — chưa xong headless:** APK `com.devicespooflab.hooks` cài được, nhưng hook IMEI/GAID cần module **enabled + scoped** trong LSPosed. LSPosed lưu ở `/data/adb/lspd/config/modules_config.db` (root:root 600, context `u:object_r:system_file:s0`) — **root sửa được** NHƯNG pad **không có `sqlite3`** và DB dùng WAL (`modules_config.db-wal` ~120KB) quá lớn để pull qua kênh base64 của `async_cmd`. Nên muốn script scope cần: (a) đẩy binary `sqlite3` tĩnh lên pad để sửa on-device, (b) chuyển WAL theo chunk + checkpoint, hoặc (c) enable+scope 1 lần qua **LSPosed Manager UI** (có thể UI-automation bằng `simulate_click`). Phần build-prop + Android-ID ở trên KHÔNG cần bước này.

## Test thực tế — scope LSPosed headless qua SQLite (2026-07)

Đã hoàn tất phần scope automation headless bạn yêu cầu, và tìm ra blocker thật:

**sqlite3 trên máy** (pad không có `sqlite3`, và stdout `async_cmd` bị cắt ~2KB nên không pull được WAL): `curl` thẳng binary **sqlite3 static aarch64** lên pad (verify sha256), vd `bnsmb/binaries-for-Android/binaries/sqlite3.static` (ELF64 AArch64, chạy Android 13) → `/data/local/tmp/sqlite3`.

**Schema LSPosed** (`/data/adb/lspd/config/modules_config.db`):
```sql
modules(mid PK, module_pkg_name UNIQUE, apk_path, enabled 0/1, auto_include 0/1)
scope(mid, app_pkg_name, user_id)
```
LSPosed tự thêm 1 row `modules` (disabled) khi phát hiện APK module. Enable + scope headless (rồi reboot) — đóng gói thành `vmos.spoof.scope_lsposed_module(...)`:
```sql
UPDATE modules SET enabled=1, auto_include=1 WHERE module_pkg_name='com.devicespooflab.hooks';
INSERT OR IGNORE INTO scope(mid,app_pkg_name,user_id)
  VALUES((SELECT mid FROM modules WHERE module_pkg_name='com.devicespooflab.hooks'),'android',0), … ;
```
✅ Edit **giữ qua reboot** và LSPosed **load module vào tiến trình scoped** — xác nhận trong log: `I/LSPosed Loading xposed for com.android.vending/10034`.

**🚧 Blocker gốc — lệch API module/framework:** DeviceSpoofLab-Hooks v1.2 dùng **libxposed API MỚI** (`io.github.libxposed.api`), nhưng LSPosed bundled của VMOS (`zygisk_lsposed`) là bản **CŨ**, không khởi tạo được:
```
E/LSPosedContext Failed to load class com.devicespooflab.hooks.XposedModuleImpl
java.lang.NoSuchMethodException: XposedModuleImpl.<init>[XposedInterface, ModuleLoadedParam]
```
→ hook không init → IMEI/GAID/Android-ID **không** đổi được bằng module này trên LSPosed hiện tại của VMOS. Scope automation đúng; module chỉ đơn giản là không tương thích framework bundled.

**Lưu ý thêm:** `service call iphonesubinfo` / `getprop` từ shell **không** phải oracle đúng cho LSPosed hook — hook nằm ở **tầng Java app-side** (`TelephonyManager.getImei()`, `Settings.Secure`, `Build.*`), còn `service call` gọi thẳng binder service. Phải verify bằng **app được scope**, không phải shell.

**➡️ Khuyến nghị:** trên LSPosed bundled của VMOS, ưu tiên module viết cho **classic Xposed API** (`de.robv.android.xposed`) — vd **AndroidFaker** — khớp framework cũ, thay vì module libxposed mới. (Hoặc thay `zygisk_lsposed` bằng bản LSPosed mới hơn — nặng/rủi ro hơn.) Phần spoof **tầng Magisk** (build props + Android ID qua SSAID ở trên) KHÔNG cần LSPosed và đã chạy end-to-end.

## ⚠️ Lưu ý

- **Bị phát hiện**: mọi hook mức Java đều có thể bị app cứng phát hiện (đọc native `__system_property_get`, Cronet, thư viện integrity). Lớp Magisk boot của DeviceSpoofLab giảm rủi ro đọc native; khi bị phát hiện có thể dùng LSPosed fork ẩn hơn (vd "Vector").
- **Hardware attestation** (TEE key attestation, Play Integrity STRONG) **không** module nào qua được — chữ ký phần cứng, ngoài tầm phần mềm.
- Đây là dự án bên thứ ba; kiểm tra APK, ghim version, test 1 instance trước khi triển khai hàng loạt. Dùng cho reseller đa dạng thiết bị hợp pháp; tuân thủ ToS VMOS và app đích.
