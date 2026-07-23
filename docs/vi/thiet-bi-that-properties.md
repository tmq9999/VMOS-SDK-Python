# Thiết bị thật (Cloud Real Device) — Những thuộc tính có thể thay đổi

> Tổng hợp từ [tài liệu chính thức VMOS](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html) và trang [Instance Property List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/InstanceList.html). English version: [real-device-properties.md](../en/real-device-properties.md).

## TL;DR

VMOS thay đổi thuộc tính thiết bị theo **2 cơ chế**:

1. **Sửa từng thuộc tính (per-key)** qua `updatePadProperties` (động, hiệu lực ngay) và `updatePadAndroidProp` (tĩnh, lưu bền, hiệu lực sau khi khởi động lại).
2. **ADI template** — gói định danh (fingerprint) dựng sẵn, áp cho **thiết bị thật** qua `replaceRealAdiTemplate` hoặc qua "One-Key New Device".

**Điểm mấu chốt về thiết bị thật** (docs ghi rõ ở mục *One-Key New Device*):

| Loại instance | Cách đổi định danh thiết bị |
|---|---|
| **Máy ảo (virtual)** | Ghi trực tiếp các thuộc tính Android (per-key), xoá toàn bộ dữ liệu |
| **Thiết bị thật (cloud real device)** | Xoá dữ liệu (= reset) + nạp SIM; **fingerprint đến từ ADI template** (chỉ định `realPhoneTemplateId` hoặc random). Không phải ghi tay từng key. |

Nói cách khác: trên **thiết bị thật**, phần **model/fingerprint** (ro.product.\*, ro.build.\*) được đổi bằng cách **chọn/thay ADI template**, không phải ghi tay từng khoá như máy ảo.

---

## 1. Định danh / fingerprint thiết bị (real device → dùng ADI template)

| Việc muốn làm | Endpoint | SDK | Điều kiện / lưu ý |
|---|---|---|---|
| Thay ADI template (đổi cả bộ model/fingerprint) | `replaceRealAdiTemplate` | `client.phone.replace_real_adi_template(pad_codes, wipe_data, real_phone_template_id)` | Instance phải là **loại real device**; phiên bản Android phải khớp phiên bản ADI |
| Liệt kê template real device | `templateList` | `client.instance.template_list(...)` | Lấy `realPhoneTemplateId` hợp lệ |
| Máy mới một chạm (xoá data + SIM + ADI) | `replacePad` | `client.instance.replace_pad(..., real_phone_template_id=?, replacement_real_adi_flag=?)` | Real device: nếu có template → thay; nếu `replacementRealAdiFlag=true` và không có template → chọn ngẫu nhiên |
| Máy mới + tự động SIM/GPS/timezone theo vị trí | `padReplaceNew` | `client.instance.pad_replace_new(...)` | Tự ghi SIM/GPS/timezone theo nơi triển khai |
| Nâng cấp image real device | `virtualRealSwitch` | `client.instance.virtual_real_switch(...)` | Nâng cấp/đổi image cho real device |

> ⚠️ Các trường fingerprint trong bảng dưới (mục 2, nhóm *System*) là **nội dung mà một ADI template gói lại**. Với thiết bị thật, cách được VMOS thiết kế để đổi chúng là **thay template**, không ghi tay từng key.

## 2. Danh mục thuộc tính per-key (updatePadProperties / updatePadAndroidProp)

`updatePadProperties` nhận 6 nhóm; mỗi phần tử là `{"propertiesName": key, "propertiesValue": value}`:

### a) Modem / SIM — viễn thông
`modemPropertiesList` (tạm thời, mất sau restart) · `modemPersistPropertiesList` (bền, hiệu lực sau restart)

| Key | Ý nghĩa |
|---|---|
| `IMEI` | IMEI |
| `ICCID` | Số SIM (ICCID) |
| `IMSI` | IMSI |
| `MCCMNC` | Mã mạng (vd `461,01`) |
| `OpName` | Tên nhà mạng |
| `PhoneNum` | Số điện thoại |
| `aic.sim.state` / `aic.operator.shortname` / `aic.operator.numeric` / `aic.spn` / `aic.iccid` / `aic.imsi` / `aic.phonenum` / `aic.net.country` / `aic.sim.country` / `aic.signal.strength` / `aic.deviceid` / `aic.cellinfo` / `aic.net.type` / `aic.radio.type` / `aic.gid1` / `aic.alphatag` / `aic.nai` | Trạng thái SIM, nhà mạng, tín hiệu, thông tin trạm (cell), loại mạng dữ liệu/thoại (LTE/GSM/CDMA/NR)… |

### b) System — build/fingerprint
`systemPropertiesList` (tạm thời) · `systemPersistPropertiesList` (bền)

| Key | Ý nghĩa |
|---|---|
| `ro.product.manufacturer` / `ro.product.brand` / `ro.product.model` / `ro.product.name` / `ro.product.device` / `ro.product.board` | Hãng, thương hiệu, model, tên sản phẩm, device, board |
| `ro.build.id` / `ro.build.display.id` / `ro.build.tags` / `ro.build.fingerprint` / `ro.build.date.utc` / `ro.build.user` / `ro.build.host` / `ro.build.description` / `ro.build.version.incremental` / `ro.build.version.codename` | Thông tin/fingerprint bản build |

### c) Setting — cấu hình hệ thống
`settingPropertiesList`

| Key | Ý nghĩa |
|---|---|
| `ssaid/<package>` | Android ID theo từng app (vd `ssaid/com.demo`) |
| `bt/mac` | Địa chỉ MAC Bluetooth |
| `language` | Ngôn ngữ hệ thống (vd `zh-CN`) |
| `timezone` | Múi giờ (vd `Asia/Shanghai`) |
| `systemvolume` | Âm lượng media cố định (0–15) |

### d) OAID — định danh quảng cáo
`oaidPropertiesList`

| Key | Ý nghĩa |
|---|---|
| `UDID` | Định danh kiểu iOS |
| `OAID` | Anonymous ID Android (CCIA) |
| `VAID` | ID quảng cáo theo hãng |
| `AAID` | ID quảng cáo Google Play Services |

### e) Field quan sát được từ máy thật (không có trong tài liệu chính thức)

> ⚠️ **Observed live, not in official docs.** Đọc `padProperties` trên một **thiết bị thật** (Pixel 7 Pro, Android 13) vào 2026-07-24 cho thấy nhóm `systemPropertiesList` còn trả về các key **ngoài** danh mục tài liệu. Chúng phản ánh phần cứng/định danh do ADI template nạp; hãy coi là chỉ-đọc trừ khi VMOS xác nhận cho ghi.

| Key | Ví dụ giá trị (máy thật) | Ý nghĩa |
|---|---|---|
| `ro.build.version.release` | `13` | Phiên bản Android (docs chỉ liệt kê `version.codename` / `version.incremental`) |
| `wifiMac` | `00:02:00:00:00:00` | Địa chỉ MAC WiFi (khác `bt/mac` ở nhóm Setting) |
| `bluetoothaddr` | `02:00:00:00:00:00` | Địa chỉ Bluetooth (dạng đọc-ra; docs dùng `bt/mac` khi ghi) |
| `gpuVendor` | `ARM` | Hãng GPU |
| `gpuRenderer` | `Mali-G710` | Bộ render GPU |
| `gpuVersion` | `OpenGL ES 3.2 v1.g18p0-...` | Phiên bản OpenGL/GPU |

> 📌 Lưu ý casing khi **đọc ra** trên máy thật: nhóm modem trả `imei` / `phonenum` / `SimOperatorName` / `simCountryIso` (khác các key `IMEI` / `PhoneNum` / `OpName` mà tài liệu dùng để **ghi vào**).

**Khác biệt hai endpoint per-key:**
- `updatePadProperties` — **động**, máy phải đang bật, **hiệu lực ngay**; nhóm `*PropertiesList` (không bền) mất sau restart, `*PersistPropertiesList` giữ lại.
- `updatePadAndroidProp` — **tĩnh**, lưu **bền**, khởi tạo lại mỗi lần boot, hiệu lực **sau khi khởi động lại** (không cần gọi lại sau reset/restart).

## 3. Các thuộc tính khác đổi được bằng endpoint chuyên dụng (áp dụng chung, gồm real device)

| Thuộc tính | Endpoint | SDK |
|---|---|---|
| SIM theo mã quốc gia (random + restart) | `updateSIM` | `client.apps.update_sim(pad_code, country_code=?, props=?)` |
| Vị trí GPS | `gpsInjectInfo` | `client.instance.gps_inject_info(longitude, latitude, pad_codes, ...)` |
| Múi giờ | `updateTimeZone` | `client.instance.update_time_zone(...)` |
| Ngôn ngữ | `updateLanguage` | `client.instance.update_language(...)` |
| Danh sách WiFi | `setWifiList` | `client.instance.set_wifi_list(pad_codes, wifi_json_list)` |
| Proxy | `setProxy` | `client.instance.set_proxy(pad_codes, ...)` |
| Smart IP (tự đổi IP/SIM/GPS/timezone theo quốc gia của proxy) | `smartIp` / `notSmartIp` | `client.instance.smart_ip(...)` / `client.instance.not_smart_ip(...)` |
| Reset GAID (ID quảng cáo Google) | `resetGAID` | `client.instance.reset_gaid(...)` |
| Nhập SMS mô phỏng | `simulateSendSms` | `client.instance.simulate_send_sms(...)` |
| Nhập nhật ký cuộc gọi | `addPhoneRecord` | `client.instance.add_phone_record(...)` |
| Danh bạ | `updateContacts` | `client.request("POST", "/vcpcloud/api/padApi/updateContacts", json_body={...})` |
| Tên thiết bị (hiển thị) | `updatePadName` | `client.phone.update_pad_name(...)` |
| Root | `switchRoot` | `client.instance.switch_root(...)` — ⚠️ real device: **không khuyến nghị** global root vì dễ bị phát hiện |

> 💡 **Smart IP** (`smartIp`) là cách nhanh nhất để đồng bộ hoá "danh tính vùng": nó tự đổi IP ra, thông tin SIM, toạ độ GPS và múi giờ theo quốc gia của proxy (máy khởi động lại, hiệu lực trong ~1 phút).

---

## Lưu ý trung thực về giới hạn tài liệu

- Tài liệu VMOS **không công bố một danh sách riêng "các key chỉ được đổi trên thiết bị thật"**. Danh mục key ở mục 2 là **dùng chung** cho instance.
- Chỗ **duy nhất** tài liệu phân biệt rõ hành vi virtual vs real là mục **One-Key New Device**: real device lấy fingerprint từ **ADI template**, không ghi tay từng key như máy ảo.
- Vì vậy: với thiết bị thật, hãy **ưu tiên ADI template** cho phần model/fingerprint; còn SIM/GPS/timezone/ngôn ngữ/proxy/WiFi/OAID/GAID dùng các endpoint chuyên dụng ở mục 3.
- Việc `updatePadProperties`/`updatePadAndroidProp` ghi per-key có được thiết bị thật chấp nhận hay không thì tài liệu **không nói tường minh** — nên **kiểm thử trực tiếp** trên pad thật của bạn trước khi dùng cho sản xuất.

## Ví dụ nhanh

```python
from vmos import VMOSClient

with VMOSClient() as c:
    # 1) Thiết bị thật: đổi cả bộ fingerprint bằng ADI template
    templates = c.instance.template_list(page=1, size=20)           # tìm realPhoneTemplateId
    c.phone.replace_real_adi_template(
        pad_codes=["ACP..."], wipe_data=False, real_phone_template_id=186,
    )

    # 2) Đồng bộ danh tính vùng (IP + SIM + GPS + timezone) theo proxy
    c.instance.smart_ip(pad_codes=["ACP..."])   # tham số proxy: xem docs/en/instance.md

    # 3) Sửa per-key (nếu real device chấp nhận) — SIM + ngôn ngữ, hiệu lực ngay
    c.instance.update_pad_properties(pad_codes=["ACP..."], **{
        "modemPersistPropertiesList": [
            {"propertiesName": "PhoneNum", "propertiesValue": "84987654321"},
        ],
        "settingPropertiesList": [
            {"propertiesName": "language", "propertiesValue": "vi-VN"},
            {"propertiesName": "timezone", "propertiesValue": "Asia/Ho_Chi_Minh"},
        ],
    })
```
