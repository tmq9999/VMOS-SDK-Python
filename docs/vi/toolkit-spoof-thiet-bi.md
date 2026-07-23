# Toolkit spoof thiết bị (reseller) — `vmos.spoof`

> Biến 1 cloud **real device** thành hồ sơ thiết bị bất kỳ — kể cả model VMOS **không có** trong catalog (vd Pixel 10 Pro / Android 17 / SDK 37) — cho mục đích reseller đa dạng sản phẩm. English: [device-spoofing-toolkit.md](../en/device-spoofing-toolkit.md).

## Vì sao làm được (đã kiểm chứng live trên Pixel 7 Pro, 2026-07)

1. Shell ADB của VMOS (`instance.async_cmd`) chạy **as root** (`uid=0`, context `u:r:xu_daemon:s0`) — **không cần su**.
2. Kitsune Magisk (`io.github.huskydg.magisk`) có `resetprop` (`/data/adb/magisk/magisk64 resetprop`) — ghi được các prop `ro.*` mà **API per-key của VMOS không đổi được** trên máy thật.
3. Persistence: Magisk module `system.prop` + script `service.d` chạy lúc boot → spoof **dính qua reboot** (đã test reboot thật: OK).

## Điều kiện tiên quyết
**Kitsune Magisk phải được BẬT** trên máy: Toolbox → Magisk (Mask) → ON. Toolkit tự bật được qua UI automation (`enable_magisk_ui`) nếu chưa bật.

## Dùng nhanh (Python)

```python
from vmos import VMOSClient, DeviceProfile, apply_profile, verify_profile

with VMOSClient() as c:
    # Hồ sơ tùy chỉnh — model VMOS không có
    profile = DeviceProfile(
        model="Pixel 10 Pro", brand="google", manufacturer="Google",
        device="frankel",
        fingerprint="google/frankel/frankel:17/BP1A.250101.001/13000000:user/release-keys",
        release="17", sdk=37, android_id="0123456789abcdef",
    )
    apply_profile(c, "ACP...", profile, persist=True)   # resetprop + boot module + android_id
    print(verify_profile(c, "ACP...", profile)["ok"])    # đọc lại getprop, so khớp
```

## Dùng qua CLI

```bash
# Bật Magisk (nếu chưa) rồi áp preset Pixel 10 Pro + verify
python examples/12_device_spoof_toolkit.py --pad ACP... --enable-magisk --preset pixel10pro --verify

# Hồ sơ tùy chỉnh
python examples/12_device_spoof_toolkit.py --pad ACP... \
    --model "Galaxy Z Fold7" --brand samsung --manufacturer samsung \
    --release 16 --sdk 36 --android-id 0123456789abcdef --verify

# Gỡ spoof (khôi phục sau reboot)
python examples/12_device_spoof_toolkit.py --pad ACP... --remove
```

## API toolkit

| Hàm | Vai trò |
|---|---|
| `DeviceProfile(...)` | Khai báo model/brand/manufacturer/device/fingerprint/release/sdk/android_id (+`deep` set cả prop theo partition) |
| `apply_profile(client, pad, profile, persist=True)` | Kiểm tra root+Magisk → resetprop toàn bộ → android_id → cài persistence |
| `verify_profile(client, pad, profile)` | Đọc `getprop` + so khớp → `{ok, checks}` |
| `remove_spoof(client, pad)` | Xoá module + service.d (runtime reset ở lần reboot sau) |
| `magisk_ready(shell)` | Kiểm tra Kitsune Magisk đã sẵn sàng |
| `enable_magisk_ui(client, pad)` | Bật Magisk headless qua Toolbox UI (best-effort, tọa độ theo tỉ lệ) |

## Kết quả kiểm chứng (live)

```
apply PIXEL_10_PRO_A17 (persist=True): 43 props
verify ngay:        model=Pixel 10 Pro | release=17 | sdk=37 | fingerprint=google/frankel/... ✅
--- REBOOT thật ---
verify sau reboot:  model=Pixel 10 Pro | release=17 | sdk=37 | fingerprint=google/frankel/... ✅ PERSISTED
remove_spoof + reboot → về Pixel 7 Pro / 13 / 33 ✅
```

## Chiến lược reseller (kết hợp)

| Tầng | Công cụ | Cho |
|---|---|---|
| Nền tảng | ADI template (`replace_real_adi_template`) | Model có sẵn trong catalog VMOS |
| **Tùy biến sâu** | **`vmos.spoof` (resetprop)** | **Model/Android/SDK tùy ý ngoài catalog** |
| SIM/vùng | `update_sim` + `set_proxy`/`smart_ip` | Nhà mạng + IP khớp quốc gia |
| Framework | LSposed (toggle trong Toolbox) | IMEI/OAID/AndroidID sâu hơn |

## Spoof sâu: IMEI / OAID / Android ID (đã test live)

Kiểm chứng trực tiếp trên máy thật — ma trận thực tế:

| Danh tính | Cơ chế | Kết quả |
|---|---|---|
| build.prop (model/brand/fingerprint/release/sdk) | `resetprop` (toolkit) | ✅ Đổi được, dính qua reboot |
| **IMEI** | RIL/telephony framework giữ (không phải prop) | ❌ `resetprop` vô tác dụng; app đọc qua `service call iphonesubinfo` |
| **OAID** | Không có prop/settings lever | ❌ Không đổi được qua shell |
| **Android ID** | `settings put secure android_id` | ❌ **Bị VMOS bỏ qua** (test cả `--user 0`) |

➡️ **IMEI/OAID/Android ID cần hook framework** — tức LSposed **+ một Xposed module spoof** (APK hook `TelephonyManager.getImei()`, OAID SDK, `Settings.Secure` ANDROID_ID).

**LSposed (đã test):** bật qua Toolbox → Lsposed → ON (toolkit: `enable_lsposed_ui`). Sau reboot: daemon `lspd` chạy, module `zygisk_lsposed` load ✅ — **framework active**. NHƯNG VMOS **không kèm** module spoof và không có Manager UI dễ script → bước cài + kích hoạt Xposed module spoof nằm **ngoài phạm vi** toolkit (cần APK module cụ thể).

```python
from vmos.spoof import enable_lsposed_ui, lsposed_ready
enable_lsposed_ui(client, "ACP...")   # bật framework LSposed (cần Magisk trước) + reboot
# → sau đó cài Xposed spoof module qua LSposed Manager để hook IMEI/OAID/AndroidID
```

Giải pháp thay thế (không cần Xposed module): **IMEI/IMSI** đổi được (ngẫu nhiên) bằng `update_sim` / ADI template của VMOS; đủ cho đa dạng vùng/nhà mạng nhưng không chọn IMEI cụ thể.

## Root hygiene / stealth (quan trọng cho reseller)

Global root là dấu hiệu dễ bị phát hiện nhất (SafetyNet, app ngân hàng, anti-fraud đều check). **Giữ "Global Root" của VMOS TẮT** trên máy bán ra — và tắt nó **không mất gì** về vận hành (đã kiểm chứng live 2026-07):

- Tắt global root (`client.instance.switch_root(pad_codes=[pad], global_root=True, root_status=0)` rồi reboot) → `persist.sys.device.root.global=0`, và gỡ `/system/xbin/su` + `/sbin/su`.
- **Shell quản lý của VMOS vẫn root** bất kể flag — `async_cmd` chạy dưới daemon VMOS (`u:r:xu_daemon:s0`, `uid=0`), độc lập với su app-facing — nên `resetprop`, persona CLI và mọi spoof vẫn chạy headless.

`/system/bin/su` còn lại khi **Kitsune Magisk** bật (Magisk cấp systemless su, mà bạn cần Magisk để spoof). Đừng gỡ Magisk để ẩn nó — dùng **Zygisk DenyList** của Magisk để ẩn root khỏi app đích (mặc định đang tắt). Tư thế khuyến nghị:

1. **Global Root: TẮT** (chỉ bật cho thao tác nhất thời rồi tắt lại).
2. **Magisk DenyList: BẬT** + thêm các app không được thấy root.
3. **LSPosed**: chỉ scope module vào app đích cụ thể, không lộ rộng.
4. Quản trị/spoof qua **shell API (root sẵn)** — không bao giờ để global su bật.

## ⚠️ Giới hạn (set kỳ vọng với khách)
- Chỉ spoof tầng phần mềm/`build.prop`. **Không** qua được hardware attestation (TEE key attestation, Play Integrity STRONG) — đó là chữ ký phần cứng thật.
- `android_id` set qua `settings put secure android_id` là giá trị legacy; app hiện đại có thể dùng ID theo app/ký khác.
- Dùng cho reseller hợp pháp; tuân thủ ToS của VMOS và của các app đích.
