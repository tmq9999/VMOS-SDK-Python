"""Probe which instance properties are actually changeable via the API.

Writes a TEST value to each candidate property (using the DYNAMIC / non-persistent
group — effective immediately per docs, discarded on restart), then verifies the
change against TWO oracles:

  * pad_properties read-back, and
  * ADB `getprop` (the live Android runtime — the real ground truth).

Finally it restores the original values. No restart/reset is issued, so the probe
is reversible even if a restore step fails (the non-persistent layer resets on
reboot anyway).

Result on a **cloud real device** (empirically, 2026-07): every write is accepted
(HTTP 200) but NONE take effect — the device fingerprint is locked to the ADI
template. Use `client.phone.replace_real_adi_template(...)` to change a real
device's identity. On a **virtual** instance the per-key writes are expected to
take effect (run this probe to confirm for your instance type).

Usage:
    VMOS_ACCESS_KEY=... VMOS_SECRET_KEY=... VMOS_TEST_PAD_CODE=... \
        python examples/09_probe_changeable_properties.py
"""
import os
import sys
import time

from vmos import VMOSClient, VMOSAPIError, VMOSError

PAD = os.environ["VMOS_TEST_PAD_CODE"].strip()

# group -> [(write_key, test_value)]; test values are format-valid.
PROBES = {
    "modemPropertiesList": [
        ("IMEI", "358240051111110"), ("IMSI", "460110000000000"),
        ("MCCMNC", "460,00"), ("OpName", "PROBE-Op"), ("PhoneNum", "8613800000000"),
    ],
    "systemPropertiesList": [
        ("ro.product.model", "PROBE-Model"), ("ro.product.brand", "probe-brand"),
        ("ro.build.fingerprint", "probe/fp:13/PROBE/1:user/release-keys"),
        ("ro.build.version.release", "14"), ("wifiMac", "02:00:00:AA:BB:CC"),
        ("bluetoothaddr", "02:00:00:DD:EE:FF"), ("gpuRenderer", "PROBE-GPU"),
    ],
    "settingPropertiesList": [
        ("language", "vi-VN"), ("timezone", "Asia/Ho_Chi_Minh"), ("systemvolume", "7"),
        ("bt/mac", "02:00:00:11:22:33"), ("ssaid/com.android.chrome", "1122334455667788"),
    ],
    "oaidPropertiesList": [
        ("OAID", "probe-oaid-0001"), ("VAID", "probe-vaid-0001"),
        ("AAID", "probe-aaid-0001"), ("UDID", "probe-udid-0001"),
    ],
}

# ro.* keys can be verified via ADB getprop (the live oracle).
GETPROP_KEYS = {
    "ro.product.model", "ro.product.brand", "ro.build.fingerprint",
    "ro.build.version.release",
}

READ_ALIASES = {"imei": "IMEI", "phonenum": "PhoneNum", "simoperatorname": "OpName",
                "iccid": "ICCID", "imsi": "IMSI", "mccmnc": "MCCMNC"}


def flat_read(c):
    data = c.instance.pad_properties(pad_code=PAD)
    out = {}
    if isinstance(data, dict):
        for items in data.values():
            if isinstance(items, list):
                for it in items:
                    if isinstance(it, dict) and it.get("propertiesName") is not None:
                        out[str(it["propertiesName"]).lower()] = it.get("propertiesValue")
    return out


def readback(flat, key):
    if key.lower() in flat:
        return flat[key.lower()]
    for rk, wk in READ_ALIASES.items():
        if wk == key and rk in flat:
            return flat[rk]
    return None


def getprop(c, key):
    resp = c.instance.async_cmd(pad_codes=[PAD], script_content=f"getprop {key}")
    tid = resp[0]["taskId"]
    for _ in range(30):
        info = c.tasks.pad_task_detail(task_ids=[tid])[0]
        if info.get("taskStatus") in (3, -1, 4, 5):
            return (info.get("taskResult") or "").strip()
        time.sleep(2)
    return "(timeout)"


def main():
    results = []
    with VMOSClient() as c:
        base = flat_read(c)
        print(f"baseline: {len(base)} keys\n")
        for group, probes in PROBES.items():
            for key, test in probes:
                original = readback(base, key)
                try:
                    c.instance.update_pad_properties(
                        pad_codes=[PAD], **{group: [{"propertiesName": key, "propertiesValue": test}]})
                    write = "accepted"
                except VMOSAPIError as e:
                    write = f"rejected({e.code})"
                except VMOSError as e:
                    write = f"error({type(e).__name__})"

                effective = None
                if write == "accepted":
                    time.sleep(1)
                    effective = str(readback(flat_read(c), key)) == str(test)
                    if key in GETPROP_KEYS:  # cross-check against live runtime
                        effective = effective or getprop(c, key) == test
                    if original is not None:
                        try:
                            c.instance.update_pad_properties(
                                pad_codes=[PAD], **{group: [{"propertiesName": key, "propertiesValue": original}]})
                        except VMOSError:
                            pass
                verdict = ("CHANGEABLE" if effective else "accepted-but-ignored") if write == "accepted" else write
                results.append((group, key, verdict))
                print(f"  [{group.replace('PropertiesList',''):8s}] {key:28s} -> {verdict}  (was={original!r})")
                time.sleep(0.4)

    chg = [r for r in results if r[2] == "CHANGEABLE"]
    print(f"\nChangeable & verified: {len(chg)}/{len(results)}")
    print("Changeable:", ", ".join(r[1] for r in chg) or "(none — likely a real device: use ADI template)")


if __name__ == "__main__":
    main()
