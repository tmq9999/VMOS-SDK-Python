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
              ├── System Applier              (resetprop / Magisk / update_sim / settings)
              ├── Java Hook Backend           (XPose appMain — getter Java trong process app)
              ├── Native Hook Backend         (XPose .so native — Dobby + xDL; đọc native/JNI)
              ├── Service/System Hook Backend (systemMain + tiến trình telephony; rủi ro hơn, phải PoC)
              └── Verification                (đọc lại → so với profile → report)
```

**Nguyên tắc:** Profile là trung tâm; mỗi backend chỉ là implementation **đọc
cùng một Profile** — không backend nào hard-code dữ liệu danh tính. Các backend
độc lập, thêm/bớt mà không sửa Profile. Một field có thể do nhiều backend áp (vd
`serial` do System Applier *và* Java Hook) nhưng Profile vẫn là nguồn sự thật duy
nhất cho tất cả.

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

## 4. Các backend (implementation độc lập, chung một Profile)

- **System Applier** (xong): `resetprop` + Magisk module cho `build.*`;
  `update_sim` cho SIM/IMSI/operator; `settings` cho locale/timezone; ADI
  template cho model nền. Dính reboot, revert được.
- **Java Hook Backend** (xong, đã verify): plugin XPose (`appMain`) nạp theo app
  qua `apmt`; ghi đè getter Java trong tiến trình **app đã scope**. Đây là thứ
  đổi IMEI/GAID/Android-ID... theo cách app đọc qua API Java. Đã verify live:
  Android ID đọc lại khớp giá trị Profile.
- **Native Hook Backend** (framework hỗ trợ; chưa build): một `.so` native nạp từ
  `appMain`, dùng **Dobby** (inline hook) + **xDL** (resolver) + `libengcore.so`
  của VMOS. Với tới các đường đọc không lộ ở Java: SDK JNI/native, system
  property đọc từ native, file `/proc` & `/sys`, thư viện nạp động, và logic nằm
  trong `.so`.
  - **Lưu ý (không tuyệt đối):** chỉ hook được hàm native khi **địa chỉ/symbol/
    signature xác định được**, **ABI khớp** (arm64 trước), và **tiến trình cho
    phép** nạp module. Symbol có thể bị strip, inline, obfuscate hoặc đổi theo
    phiên bản — mỗi target phải kiểm chứng, không mặc định.
- **Service/System Hook Backend** (phải research/PoC trước): `systemMain` cho
  **nhất quán** `build`/display/feature toàn hệ (rủi ro hơn — crash
  `system_server` có thể bootloop máy, nên opt-in + scope hẹp), và **tiến trình
  telephony** (`com.android.phone`) cho các giá trị như IMEI/IMSI.
  - **Lưu ý:** hook `com.android.phone` **không** tự động làm IMEI qua Binder
    đổi. Chỉ khả thi nếu **trace đúng implementation/nguồn dữ liệu** mà Binder
    service trả rồi hook *đúng chỗ đó* (Java hoặc native, hoặc nguồn nó đọc) —
    hook `libc` **không** mặc định là đủ. Backend này chỉ vào roadmap chính thức
    **sau khi có PoC pass trên một Android/ROM cụ thể**.

Chỉ hardware attestation (TEE / Play Integrity STRONG) là ngoài tầm mọi backend.

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

## 8. Lộ trình (ưu tiên đã chốt)

Đã xong: **P1 Profile core** (schema, `Profile`, `validate()`, generator nhất
quán — phía SDK); **Java Hook Backend đã verify** (Android ID đọc lại khớp
Profile, live).

| Ưu tiên | Sản phẩm | Trạng thái |
|---|---|---|
| **A — Combined provisioning + verification** | một lệnh áp **System Applier** (danh tính build Tầng 1) **và** **Java Hook Backend** (danh tính Tầng 2) từ cùng một Profile, rồi verify **model** lẫn **Android ID** trên pad | kế tiếp |
| **B — Native Hook Core (tối thiểu), song song** | một `.so` native: (1) **nạp thành công**, (2) **arm64 trước**, (3) wrapper **Dobby/xDL**, (4) **chỉ đọc Profile** (không hard-code), (5) tái hiện **hook demo VMOS end-to-end**, (6) có **lifecycle / log / crash-guard** | song song |
| **C — Research đường IMEI trong `com.android.phone`** | xác định process; **trace implementation của Binder service**; xác định **nguồn** Java/native trả IMEI; **PoC trên một Android/ROM cụ thể** | sau B |
| **D — Binder-consistent IMEI (gated)** | chỉ vào roadmap chính thức **nếu PoC ở C pass** | gated |

Sau đó: vòng đời profile (version, export/import/rollback, catalog profile dựng
sẵn); thành phần verification (đọc-lại → so → report).

## 9. Trình tự (lưu ý rủi ro)

Java Hook Backend đã **verify live** (Android ID). Tiến hành **A** (gộp với Tầng
1) làm mốc kế tiếp. Dựng **B** song song nhưng coi khả năng native là **có điều
kiện** (symbol/ABI/process — xem lưu ý Native Hook Backend). **Đừng** hứa
Binder-consistent IMEI cho tới khi PoC **C** chứng minh trên ROM thật (**D** phụ
thuộc vào đó).

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
