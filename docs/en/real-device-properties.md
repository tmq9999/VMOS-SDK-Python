# Cloud Real Device — Which Properties Can Be Changed

> Compiled from the [official VMOS docs](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html) and the [Instance Property List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/InstanceList.html) page. Phiên bản tiếng Việt: [thiet-bi-that-properties.md](../vi/thiet-bi-that-properties.md).

## TL;DR

VMOS changes device properties through **two mechanisms**:

1. **Per-key editing** via `updatePadProperties` (dynamic, takes effect immediately) and `updatePadAndroidProp` (static, persistent, takes effect after restart).
2. **ADI template** — a pre-built device-identity (fingerprint) bundle applied to **real devices** via `replaceRealAdiTemplate` or through "One-Key New Device".

**The key real-device distinction** (stated explicitly in the *One-Key New Device* note):

| Instance type | How device identity is changed |
|---|---|
| **Virtual machine** | Directly set Android properties (per-key), clear all data |
| **Cloud real device** | Clear data (= reset) + add SIM info; **fingerprint comes from an ADI template** (specify `realPhoneTemplateId` or random). Not per-key writes. |

In short: on a **real device**, the **model/fingerprint** (ro.product.\*, ro.build.\*) is changed by **selecting/replacing an ADI template**, not by writing individual keys like a virtual machine.

---

## 1. Device identity / fingerprint (real device → use ADI templates)

| Goal | Endpoint | SDK | Conditions / notes |
|---|---|---|---|
| Replace ADI template (swap the whole model/fingerprint bundle) | `replaceRealAdiTemplate` | `client.phone.replace_real_adi_template(pad_codes, wipe_data, real_phone_template_id)` | Instance must be **real-device type**; Android version must match the ADI version |
| List real-device templates | `templateList` | `client.instance.template_list(...)` | Get a valid `realPhoneTemplateId` |
| One-Key New Device (clear data + SIM + ADI) | `replacePad` | `client.instance.replace_pad(..., real_phone_template_id=?, replacement_real_adi_flag=?)` | Real device: template provided → replace; `replacementRealAdiFlag=true` with no template → random |
| New device + auto SIM/GPS/timezone by location | `padReplaceNew` | `client.instance.pad_replace_new(...)` | Writes SIM/GPS/timezone based on deployment location |
| Upgrade real-device image | `virtualRealSwitch` | `client.instance.virtual_real_switch(...)` | Real-device image upgrade/switch |

> ⚠️ The fingerprint fields in section 2 (the *System* group) are **exactly what an ADI template bundles**. On a real device, the VMOS-designed way to change them is to **swap the template**, not to write each key.

## 2. Per-key property catalog (updatePadProperties / updatePadAndroidProp)

`updatePadProperties` accepts 6 groups; each element is `{"propertiesName": key, "propertiesValue": value}`:

### a) Modem / SIM — telephony
`modemPropertiesList` (non-persistent, lost after restart) · `modemPersistPropertiesList` (persistent, after restart)

`IMEI`, `ICCID`, `IMSI`, `MCCMNC`, `OpName`, `PhoneNum`, and the `aic.*` family — `aic.sim.state`, `aic.operator.shortname`, `aic.operator.numeric`, `aic.spn`, `aic.iccid`, `aic.imsi`, `aic.phonenum`, `aic.net.country`, `aic.sim.country`, `aic.signal.strength`, `aic.deviceid`, `aic.cellinfo`, `aic.net.type`, `aic.radio.type`, `aic.gid1`, `aic.alphatag`, `aic.nai` (SIM state, operator, signal strength, cell info, data/voice network type LTE/GSM/CDMA/NR…).

### b) System — build/fingerprint
`systemPropertiesList` (non-persistent) · `systemPersistPropertiesList` (persistent)

`ro.product.manufacturer`, `ro.product.brand`, `ro.product.model`, `ro.product.name`, `ro.product.device`, `ro.product.board`, `ro.build.id`, `ro.build.display.id`, `ro.build.tags`, `ro.build.fingerprint`, `ro.build.date.utc`, `ro.build.user`, `ro.build.host`, `ro.build.description`, `ro.build.version.incremental`, `ro.build.version.codename`.

### c) Setting — system config
`settingPropertiesList`

| Key | Meaning |
|---|---|
| `ssaid/<package>` | Per-app Android ID (e.g. `ssaid/com.demo`) |
| `bt/mac` | Bluetooth MAC |
| `language` | System language (e.g. `zh-CN`) |
| `timezone` | Time zone (e.g. `Asia/Shanghai`) |
| `systemvolume` | Fixed media volume (0–15) |

### d) OAID — advertising identifiers
`oaidPropertiesList` — `UDID`, `OAID`, `VAID`, `AAID`.

### e) Fields observed live (not in official docs)

> ⚠️ **Observed live, not in official docs.** Reading `padProperties` on a **real device** (Pixel 7 Pro, Android 13) on 2026-07-24 showed the `systemPropertiesList` group also returns keys **beyond** the documented catalog. They reflect hardware/identity bundled by the ADI template; treat them as read-only unless VMOS confirms they're writable.

| Key | Example value (real device) | Meaning |
|---|---|---|
| `ro.build.version.release` | `13` | Android version (docs only list `version.codename` / `version.incremental`) |
| `wifiMac` | `00:02:00:00:00:00` | WiFi MAC address (distinct from `bt/mac` in the Setting group) |
| `bluetoothaddr` | `02:00:00:00:00:00` | Bluetooth address (read-out form; docs use `bt/mac` for writes) |
| `gpuVendor` | `ARM` | GPU vendor |
| `gpuRenderer` | `Mali-G710` | GPU renderer |
| `gpuVersion` | `OpenGL ES 3.2 v1.g18p0-...` | OpenGL/GPU version |

> 📌 Read-out casing on a real device: the modem group returns `imei` / `phonenum` / `SimOperatorName` / `simCountryIso` (different from the `IMEI` / `PhoneNum` / `OpName` keys the docs use for **writing**).

**Difference between the two per-key endpoints:**
- `updatePadProperties` — **dynamic**, instance must be powered on, **effective immediately**; `*PropertiesList` (non-persistent) is lost after restart, `*PersistPropertiesList` survives.
- `updatePadAndroidProp` — **static**, **persistent**, re-initialized on each boot, effective **after restart** (no need to call again after reset/restart).

## 3. Other changeable properties via dedicated endpoints (apply generally, incl. real device)

| Property | Endpoint | SDK |
|---|---|---|
| SIM by country code (random + restart) | `updateSIM` | `client.apps.update_sim(pad_code, country_code=?, props=?)` |
| GPS location | `gpsInjectInfo` | `client.instance.gps_inject_info(longitude, latitude, pad_codes, ...)` |
| Time zone | `updateTimeZone` | `client.instance.update_time_zone(...)` |
| Language | `updateLanguage` | `client.instance.update_language(...)` |
| WiFi list | `setWifiList` | `client.instance.set_wifi_list(pad_codes, wifi_json_list)` |
| Proxy | `setProxy` | `client.instance.set_proxy(pad_codes, ...)` |
| Smart IP (auto IP/SIM/GPS/timezone to proxy country) | `smartIp` / `notSmartIp` | `client.instance.smart_ip(...)` / `client.instance.not_smart_ip(...)` |
| Reset GAID (Google ad ID) | `resetGAID` | `client.instance.reset_gaid(...)` |
| Simulate incoming SMS | `simulateSendSms` | `client.instance.simulate_send_sms(...)` |
| Import call logs | `addPhoneRecord` | `client.instance.add_phone_record(...)` |
| Contacts | `updateContacts` | `client.request("POST", "/vcpcloud/api/padApi/updateContacts", json_body={...})` |
| Device display name | `updatePadName` | `client.phone.update_pad_name(...)` |
| Root | `switchRoot` | `client.instance.switch_root(...)` — ⚠️ real device: global root **not recommended** (detection risk) |

> 💡 **Smart IP** (`smartIp`) is the fastest way to sync a "regional identity": it auto-changes the exit IP, SIM info, GPS coordinates and timezone to the proxy's country (device restarts, effective within ~1 minute).

---

## 🧪 Experiment — which fields are actually changeable via the API? (real device)

> Tested directly on a **real device** (Pixel 7 Pro, Android 13) on 2026-07-24 with [`examples/09_probe_changeable_properties.py`](../../examples/09_probe_changeable_properties.py): wrote a test value to **each** field via `updatePadProperties` (both the dynamic and persistent layers), then verified against two oracles — a `pad_properties` read-back **and** ADB `getprop` (the live runtime). Originals were restored afterward.

**Result: 0/23 fields changed.** Every request returned **HTTP 200 (accepted)** but **none** altered the live runtime — confirmed by `getprop ro.product.model` still returning `Pixel 7 Pro` after the write.

| Group | Fields tried | Result |
|---|---|---|
| modem | IMEI, IMSI, ICCID, MCCMNC, OpName, PhoneNum | ✅ accepted (200) · ❌ no effect |
| system | ro.product.model/brand/manufacturer, ro.build.fingerprint, ro.build.version.release, wifiMac, bluetoothaddr, gpuRenderer | ✅ accepted (200) · ❌ no effect |
| setting | language, timezone, systemvolume, bt/mac, ssaid/&lt;pkg&gt; | ✅ accepted (200) · ❌ no effect |
| oaid | OAID, VAID, AAID, UDID | ✅ accepted (200) · ❌ no effect |

**➡️ Conclusion:** on a **real device**, per-key `updatePadProperties` **cannot change the identity** — the API swallows the request (returns 200) but the fingerprint is locked to the **ADI template**. To change it, use `client.phone.replace_real_adi_template(...)` or `replace_pad(...)` / `pad_replace_new(...)`. SIM/GPS/timezone/proxy are handled by the dedicated endpoints in section 3 (their write behavior was not mutated in this experiment).

### Deeper verification — which mechanism ACTUALLY changes identity? (real device, 2026-07-24)

Three more direct mutation experiments (device restored to Pixel 7 Pro / US / Verizon afterward):

| Mechanism | Endpoint / SDK | Result (verified via live `getprop`) |
|---|---|---|
| Per-key **dynamic** | `updatePadProperties` (systemPropertiesList) | ❌ **Ignored** — 200 but getprop unchanged |
| Per-key **persistent + reboot** | `updatePadProperties` (systemPersistPropertiesList) → `restart` | ❌ **Ignored** — after reboot getprop still `Pixel 7 Pro` |
| **ADI template** | `replace_real_adi_template(wipe_data=false, real_phone_template_id=44)` | ✅ **CHANGES IT** — `ro.product.model/brand/manufacturer` + `ro.build.fingerprint` flipped to Samsung `SM-A225F` (`samsung/a22nstur/...`) in ~40s (task 2→3). Re-applying id=36 → back to `Pixel 7 Pro`. |
| **SIM by country** | `update_sim(country_code="VN")` | ✅ **CHANGES IT** — getprop `gsm.operator.iso-country=vn`, `gsm.sim.operator.alpha=Vinaphone`, `MCCMNC=452,02`, `sim.state=LOADED` (needs ~2 min for the restart to settle). |
| **GPS inject** | `gps_inject_info(lat, lng)` | ⚪ **Accepted** (dispatch=true) but `dumpsys location` shows `last location=null` — needs an app actively requesting location to observe; inconclusive. |

**➡️ Overall conclusion:** on a real device you **cannot** change the fingerprint via per-key writes (dynamic or persistent-after-reboot). To change **model/fingerprint** → **ADI template** (verified). To change **SIM/operator/country** → `update_sim` by country code (verified). Each ADI/SIM change also **regenerates IMEI/IMSI**.

> 💡 Available Android-13 templates from `template_list()`: id 36=Google Pixel 7 Pro, 38=Samsung Galaxy A03s, 40=Vivo Y33S, 44=Samsung Galaxy A53, 48=OPPO Reno6, 50=Samsung A32, 52=Realme 9i, 54=Samsung A71, 56=Redmi 10, 60=Samsung Note 20, 62=Samsung A22… (`goodFingerprintId` + `goodFingerprintName` + `goodAndroidVersion`; must match the instance's Android version).

## Honest note on documentation limits

- The VMOS docs do **not** publish a separate "keys editable only on real devices" list. The key catalog in section 2 is **shared** across instances.
- The **only** place the docs explicitly branch virtual vs real behavior is the **One-Key New Device** note: real devices derive their fingerprint from an **ADI template**, not from per-key writes like a virtual machine.
- Therefore, on a real device, **prefer ADI templates** for the model/fingerprint; use the dedicated endpoints in section 3 for SIM/GPS/timezone/language/proxy/WiFi/OAID/GAID.
- Whether per-key `updatePadProperties`/`updatePadAndroidProp` writes are honored on a real device is **not stated explicitly** — **test on your own real-device pad** before relying on it in production.

## Quick example

```python
from vmos import VMOSClient

with VMOSClient() as c:
    # 1) Real device: swap the whole fingerprint via an ADI template
    templates = c.instance.template_list(page=1, size=20)           # find a realPhoneTemplateId
    c.phone.replace_real_adi_template(
        pad_codes=["ACP..."], wipe_data=False, real_phone_template_id=186,
    )

    # 2) Sync regional identity (IP + SIM + GPS + timezone) to the proxy
    c.instance.smart_ip(pad_codes=["ACP..."])   # proxy params: see docs/en/instance.md

    # 3) Per-key edits (if honored on real device) — SIM + locale, immediate
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
