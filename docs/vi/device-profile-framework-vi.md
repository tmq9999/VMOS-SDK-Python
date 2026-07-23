# VMOS Real Device Profile Framework — Thiết kế

> Tài liệu thiết kế chính thức. Chuyển hướng từ "plugin spoof hook từng getter"
> sang **framework hướng-profile**: một **Device Profile** duy nhất là nguồn sự
> thật, mọi applier (system props, app hook, và system-server hook sau này) đều
> đọc từ nó. English: [device-profile-framework.md](../en/device-profile-framework.md).

## 1. Tầm nhìn & định vị

Bán một **VMOS Real Device Profile đã cấu hình** — môi trường Android dựng sẵn
cho app testing, QA, SDK/compatibility testing, automation, và đa dạng thiết bị —
trên nền một VMOS real device. Phần cứng nền (ADI) có thể là một model (vd Pixel 7
Pro); profile giao cho khách trình hiện một danh tính thiết bị đã chọn, **đáng
tin** (vd Pixel 10 Pro). Ta bán **profile**, không phải lớp vỏ giả tạo.

Ranh giới cứng: chỉ tầng phần mềm. Hardware attestation (Play Integrity STRONG /
TEE key attestation) không phần mềm nào vượt được — ngoài phạm vi.

## 2. Kiến trúc

```
VMOS Real Device
   → Base ADI (model đã thuê, vd Pixel 7 Pro)
      → Device Profile  (JSON chuẩn — nguồn sự thật duy nhất)
         → Profile Manager
              ├── System Applier      (Tầng 1: resetprop / Magisk / update_sim / settings)
              ├── App Hook            (Tầng 2: plugin XPose, getter Java theo app)
              ├── System-server Hook  (Tầng 3, tùy chọn: systemMain + tiến trình telephony)
              └── Verification        (đọc lại → so với profile → report)
```

**Nguyên tắc:** Profile là trung tâm; hook/applier chỉ là implementation. Không
applier nào hard-code dữ liệu danh tính — tất cả đọc từ Profile. Thêm backend mới
mà không phải sửa Profile.

## 3. Device Profile (JSON chuẩn)

Một tài liệu JSON trung lập ngôn ngữ, dùng chung cho phía Python (Tầng 1 +
provisioning) và plugin trên máy (Tầng 2). Các mục:

| Mục | Field ví dụ | Applier chính | Oracle verify |
|---|---|---|---|
| `meta` | name, version, baseAdi, createdAt, notes | — | — |
| `build` | brand, manufacturer, model, device, product, fingerprint, id, release, sdk, securityPatch, serial | Tầng 1 (resetprop); `serial` thêm Tầng 2 (`Build.getSerial`) | `getprop`; app device-info |
| `telephony` | imei[], meid, imsi, iccid, line1, mccMnc, operator, simCountryIso | Tầng 2 (app + phone process); operator/imsi/country thêm Tầng 1 (`update_sim`) | app device-info đã scope |
| `identity` | androidId, gaid, oaid, gsfId, mediaDrmId | Tầng 2 | app device-info đã scope |
| `network` | wifiMac, bssid, ssid | Tầng 2 (+ system) | app device-info |
| `display` | widthPx, heightPx, densityDpi, refreshRate | Tầng 1 (wm/props) / Tầng 3 | `wm size`; app |
| `locale` | language, country, timezone | Tầng 1 (settings) | `settings get`; app |
| `features` | cờ hasSystemFeature | Tầng 3 (system-server) | app |
| `runtime` | targetApps (scope hook), enabledSections | Profile Manager | — |

Mỗi field ghi rõ **tầng nào áp** và **verify ra sao**.

### Hợp đồng phân phối profile
- **Python**: `DeviceProfile` (mở rộng dataclass sẵn có) → `validate()` →
  serialize ra `vmos_profile.json` chuẩn.
- **Trên máy**: đẩy JSON lên pad (một bản trong Magisk module để dính reboot).
  Plugin **đọc profile JSON** thay cho hàng chục prop `persist.vmos.spoof.*` rời
  rạc. Một profile → mọi hook. (Prop vẫn là fallback cho scalar đơn giản.)

## 4. Các applier (ba tầng)

- **Tầng 1 — System Applier** (xong): `resetprop` + Magisk module cho `build.*`;
  `update_sim` cho SIM/IMSI/operator; `settings` cho locale/timezone; ADI
  template cho model nền. Dính reboot, revert được.
- **Tầng 2 — App Hook** (đang làm): plugin XPose nạp theo app qua `apmt`; ghi đè
  getter Java trong tiến trình **app đã scope**. Đây là tầng **duy nhất** đổi
  được IMEI/GAID/Android-ID... theo cách một app cụ thể đọc.
- **Tầng 3 — System-server Hook** (tùy chọn, sau): `systemMain` cho **nhất quán**
  `build`/display/feature toàn hệ. Hai lưu ý:
  - IMEI/IMSI **không** nằm ở `system_server`; chúng ở **tiến trình telephony**
    (`com.android.phone`). Hook tiến trình đó (một target Tầng 2, không phải
    system-server) mới làm cả đường Binder (`service call iphonesubinfo`) nhất
    quán — chính là bản vá cho "lỗ hổng Binder" trước đây.
  - Hook `system_server` rủi ro hơn (crash có thể bootloop máy), nên opt-in và
    scope hẹp.

## 5. Bộ máy nhất quán (giá trị sản phẩm thật sự)

Hook thì dễ; một profile **đáng tin, nhất quán nội bộ** mới khó và giá trị.
Generator/validator phải bảo đảm:
- `model ↔ fingerprint ↔ build.id` khớp (từ bộ Pixel-Props chuẩn).
- **IMEI** hợp Luhn với TAC hợp lý cho hãng.
- **IMSI/ICCID** có MCC/MNC khớp nhà mạng/quốc gia của SIM.
- **GAID** đúng dạng UUID; **MAC** dùng OUI hợp lý / locally-administered.
- `locale`/`timezone` khớp quốc gia SIM; `display` khớp model.
`validate()` từ chối profile không nhất quán trước khi áp.

## 6. Verification

- **Bây giờ**: app device-info đã cài (`com.liuzh.deviceinfo`,
  `ru.andr7e.deviceinfohw`, `com.ytheekshana.deviceinfo`) + screenshot pad +
  logcat `hooked …` của plugin.
- **Đích đến**: bước Verification đọc lại mọi field danh tính (từ app scope + hệ
  thống) ra JSON và **so với profile**, xuất report `Passed / Cần cải thiện` theo
  từng mục. Có thể là một verify APK nhỏ hoặc lấy từ output device-info.
- Field Tầng 2 **không bao giờ** verify bằng `service call` / `getprop` / Play
  Integrity (bỏ qua hook Java hoặc dựa hardware attestation).

## 7. Vòng đời

Profile là **JSON có version** (thân thiện git): tạo, validate, áp, export,
import, rollback. Mỗi pad ghi lại profile+version đang áp để cả fleet audit được.

## 8. Lộ trình

| Pha | Sản phẩm |
|---|---|
| **P1 — Profile core** | Schema JSON; mở rộng `DeviceProfile` + `validate()` + serialize; generator/validator nhất quán; plugin đọc `vmos_profile.json`; một lệnh `apply_profile(pad, profile)` bao Tầng 1 + 2 |
| **P2 — App-layer bền hơn** | tiến trình phụ, `ClassLoader` động, hook theo signature, quản lý hook theo module |
| **P3 — Tầng hệ thống** | `systemMain` (nhất quán build/display/feature toàn hệ) + hook tiến trình telephony (IMEI nhất quán cả Binder), cùng đọc một profile |
| **P4 — Verification** | thành phần đọc-lại → so → report |
| **P5 — Vòng đời & catalog** | version profile, export/import/rollback, catalog profile dựng sẵn |

## 9. Trình tự (lưu ý rủi ro)

**Chứng minh Tầng 2 end-to-end trước** — một lần đổi IMEI/GAID thấy được trong app
device-info — **trước** khi refactor lớn. Profile core (P1) chủ yếu phía SDK nên
làm song song được, nhưng không xây framework trên một hook chưa kiểm chứng.

## Phụ lục — P1 trong code (đã có)

Profile core nằm ở `vmos.profile`:

```python
from vmos.profile import generate_profile, validate
p = generate_profile("pixel10pro", country="VN", operator="Viettel",
                     base_adi="Pixel 7 Pro", target_apps=["com.liuzh.deviceinfo"], seed=42)
issues = validate(p)              # [] hoặc [{level, field, message}, ...]
p.save("vmos_profile.json")       # JSON chuẩn — nguồn sự thật
dp = p.to_device_profile()        # đầu vào Tầng 1 cho apply_profile()
props = p.identity_props()        # map persist.vmos.spoof.* cho Tầng 2
```

- CLI: `python examples/14_generate_profile.py --model pixel10pro --country VN --operator Viettel --out vmos_profile.json`
- Mẫu: [`profiles/example-pixel10pro-vn.json`](../../profiles/example-pixel10pro-vn.json)
- Dữ liệu tham chiếu: model `pixel10pro | pixel10 | pixel10proxl`; quốc gia `VN | US | GB` (MCC/MNC chính xác).
- Trung thực: **TAC và display là mẫu chưa kiểm chứng** (thay bằng giá trị thật cho production); `validate()` cảnh báo TAC generic. Fingerprint đã vetted (Pixel-Props).
