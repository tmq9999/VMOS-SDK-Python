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

## ⚠️ Lưu ý

- **Bị phát hiện**: mọi hook mức Java đều có thể bị app cứng phát hiện (đọc native `__system_property_get`, Cronet, thư viện integrity). Lớp Magisk boot của DeviceSpoofLab giảm rủi ro đọc native; khi bị phát hiện có thể dùng LSPosed fork ẩn hơn (vd "Vector").
- **Hardware attestation** (TEE key attestation, Play Integrity STRONG) **không** module nào qua được — chữ ký phần cứng, ngoài tầm phần mềm.
- Đây là dự án bên thứ ba; kiểm tra APK, ghim version, test 1 instance trước khi triển khai hàng loạt. Dùng cho reseller đa dạng thiết bị hợp pháp; tuân thủ ToS VMOS và app đích.
