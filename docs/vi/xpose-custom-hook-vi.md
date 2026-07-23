# Hook XPose riêng — spoof IMEI / IMSI / ICCID / ANDROID_ID (`apmt`)

> Tự viết hook framework của **riêng bạn** dựa trên **XPose framework native** của
> VMOS — không LSPosed, không module bên thứ ba. Đây là tầng mà `resetprop`
> **không** chạm tới được: các getter Java mà app gọi để lấy IMEI / IMSI / ICCID /
> số điện thoại / ANDROID_ID. English: [xpose-custom-hook.md](../en/xpose-custom-hook.md).

Mã nguồn project nằm ở [`xpose_plugin/`](../../xpose_plugin) trong repo.

## Vì sao chọn plugin XPose riêng (thay vì module LSPosed)

| | Plugin XPose riêng (`apmt`) | Module LSPosed |
|---|---|---|
| Framework | VMOS **có sẵn XPose trong image** (`/system/bin/apmt`, đã xác nhận chạy) | `zygisk_lsposed` kèm theo là bản **cũ**; module mới lệch API libxposed (`NoSuchMethodException`) |
| Tương thích | **Luôn tương thích** — build theo đúng API của image | Phải khớp ABI manager/module; bản kèm của VMOS lỗi thời |
| Riêng tư | APK của **bạn**, không có chữ ký module đã biết | Package/chữ ký nổi tiếng, dễ bị fingerprint |
| Độ khớp | Hook **đúng** các method bạn chọn | Tùy module bên thứ ba quyết định |

Đây là hướng nên chọn khi muốn spoof IMEI/IMSI/ICCID/ANDROID_ID **riêng tư, tùy
biến, và không vỡ** khi VMOS cập nhật image.

## Sự thật đã xác nhận về framework (live trên pad test, 2026-07)

- `/system/bin/apmt` tồn tại và chạy: `apmt patch add|list|del`.
- Plugin = một APK có class entry `androidx.app.Entry` với:
  - `public static void appMain(ClassLoader loader, Context context, String appClass, String pkg, String process)` — chạy **trong process app đích**.
  - `public static void systemMain(ClassLoader loader, String pkg, String processName)` — chạy trong **SystemServer** (`-p android`).
- Thư viện API: `net.armcloud.xscore:xscore:1.0.0`
  - `com.android.core.XSHelpers` — `findAndHookMethod(Class, "method", paramTypes…, XC_MethodHook)`
  - `com.android.core.XC_MethodHook` — `beforeHookedMethod` / `afterHookedMethod`, `param.setResult(...)`
  - `com.android.core.XSBridge`

## Thiết kế: build một lần, cấu hình theo từng máy

Plugin **không hard-code gì cả**. Lúc hook, nó đọc giá trị spoof từ các system
property `persist.vmos.spoof.*`, nên **một APK dùng cho mọi máy** — set giá trị
headless theo từng máy bằng Magisk `resetprop`. Property rỗng/chưa set nghĩa là
"giữ nguyên giá trị thật", nên bạn chỉ spoof phần cần thiết.

| Property | Tham số `set_identity_props` | Ghi đè (trong app được scope) |
|---|---|---|
| `persist.vmos.spoof.imei` | `imei` | `TelephonyManager.getImei()` / `getDeviceId()` (+ theo slot) |
| `persist.vmos.spoof.meid` | `meid` | `getMeid()` |
| `persist.vmos.spoof.imsi` | `imsi` | `getSubscriberId()` |
| `persist.vmos.spoof.iccid` | `iccid` | `getSimSerialNumber()` |
| `persist.vmos.spoof.line1` | `line1` | `getLine1Number()` |
| `persist.vmos.spoof.androidid` | `android_id` | `Settings.Secure.getString(…, "android_id")` |
| `persist.vmos.spoof.gaid` | `gaid` | `AdvertisingIdClient$Info.getId()` (Google Ad ID) |
| `persist.vmos.spoof.wifimac` | `wifi_mac` | `WifiInfo.getMacAddress()` |
| `persist.vmos.spoof.bssid` | `bssid` | `WifiInfo.getBSSID()` |
| `persist.vmos.spoof.serial` | `serial` | `Build.getSerial()` |
| `persist.vmos.spoof.drmid` | `drm_id` | `MediaDrm` Widevine device id (hex) |
| `persist.vmos.spoof.oaid` | `oaid` | MSA `IdSupplier.getOAID()` (best-effort theo target) |

**Đây chính là điểm "tùy biến sâu":** bạn hook đúng những getter mình muốn, và
thêm một bề mặt chỉ tốn một dòng trong `xpose_plugin/`. Mỗi hook thêm đều được
bọc guard — class không có trong app đích thì bỏ qua — nên một APK nạp an toàn
vào mọi app. Chỉ có đọc qua native (NDK/Cronet) và hardware attestation là trần
giới hạn; không phương pháp phần mềm nào vượt được hai cái đó.

## Triển khai headless (VMOS SDK)

```python
from vmos import VMOSClient
from vmos.spoof import set_identity_props, load_xpose_plugin, list_xpose_plugins

with VMOSClient() as c:
    # 1) đẩy giá trị danh tính theo máy (resetprop + persist trong Magisk module)
    set_identity_props(c, "ACP...",
                       imei="356789012345678", imsi="460110000000000",
                       iccid="8986000000000000000", android_id="a1b2c3d4e5f60718")

    # 2) nạp plugin vào app đích qua apmt (build 1 lần, host APK ở đâu cũng được)
    load_xpose_plugin(c, "ACP...", name="vmosid",
                      target_pkg="com.example.targetapp",
                      apk_url="https://your-host/vmos-xpose-spoof.apk")

    print(list_xpose_plugins(c, "ACP..."))   # kiểm tra đã nạp
    # 3) khởi động lại app đích — giờ nó đọc danh tính đã spoof
```

Lệnh raw tương đương trên máy (root shell):

```sh
apmt patch add -n vmosid -p com.example.targetapp -u https://your-host/plugin.apk
apmt patch list
apmt patch del -n vmosid
```

Helper: `set_identity_props`, `load_xpose_plugin`, `list_xpose_plugins`,
`remove_xpose_plugin` (đều trong `vmos.spoof`).

## Build APK

Không build được trong shell VMOS — dùng toolchain Android bình thường (Android
Studio, hoặc `gradle :app:assembleRelease` với Android SDK + JDK 17). Nếu artifact
`net.armcloud.xscore` không có trên public Maven, lấy từ demo chính thức
(`ArmCloudXposed.zip`) hoặc bỏ một **stub** jar compile-time expose
`com.android.core.{XSHelpers, XC_MethodHook, XSBridge}` vào `app/libs/` — class
thật do framework cung cấp lúc runtime; stub chỉ để `javac` qua. Chi tiết:
[`xpose_plugin/README.md`](../../xpose_plugin/README.md).

## Verify bằng ĐÚNG oracle

Hook XPose/LSPosed sống trong **process app**. Nên phải verify từ một **app đã
scope** có gọi `TelephonyManager.getImei()` (vd một APK device-info thêm làm target
`-p`). **Đừng** dùng `service call iphonesubinfo` hay `getprop` shell — chúng
**bỏ qua** hook Java và sẽ hiện giá trị thật ngay cả khi spoof đã chạy.

## Phạm vi & đạo đức

Chỉ spoof tầng phần mềm/Java. Hardware attestation (TEE key attestation, Play
Integrity STRONG) nằm ngoài tầm mọi phương pháp phần mềm. Dùng cho reseller đa
dạng thiết bị hợp pháp; tuân thủ ToS của VMOS và điều khoản của app đích.
