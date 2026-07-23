"""Change a REAL DEVICE's identity — the mechanisms proven to work on production.

Empirically verified on a Pixel 7 Pro (Android 13), 2026-07-24:
  * ADI template swap changes the whole fingerprint (model/brand/manufacturer/
    build.fingerprint) — verified live via `getprop`.
  * update_sim by country code changes SIM/operator/country/IMSI — verified via
    `getprop gsm.*` (sim.state LOADED).
  * Per-key updatePadProperties writes (dynamic AND persistent+reboot) are
    IGNORED on real devices — the identity is locked to the ADI template.

Run:
    VMOS_ACCESS_KEY=... VMOS_SECRET_KEY=... VMOS_TEST_PAD_CODE=... \
        python examples/10_real_device_identity.py
"""
import os
import sys
import time

from vmos import VMOSClient, VMOSError

PAD = os.environ["VMOS_TEST_PAD_CODE"].strip()


def getprop(client, key):
    """Read a live Android system property via ADB (ground truth)."""
    resp = client.instance.async_cmd(pad_codes=[PAD], script_content=f"getprop {key}")
    task_id = resp[0]["taskId"]
    for _ in range(30):
        info = client.tasks.pad_task_detail(task_ids=[task_id])[0]
        if info.get("taskStatus") in (3, -1, 4, 5):
            return (info.get("taskResult") or "").strip()
        time.sleep(2)
    return "(timeout)"


def apply_template(client, template_id):
    """Swap the ADI template and wait for the task to finish."""
    resp = client.phone.replace_real_adi_template(
        pad_codes=[PAD], wipe_data=False, real_phone_template_id=template_id)
    task_id = resp[0]["taskId"]
    while True:
        info = client.tasks.pad_task_detail(task_ids=[task_id])[0]
        if info.get("taskStatus") in (3, -1, 4, 5):
            return info.get("taskStatus") == 3
        time.sleep(3)


with VMOSClient() as c:
    # 1) Discover Android-version-compatible templates
    templates = c.instance.template_list(page=1, rows=20)
    items = templates.get("records") or templates.get("list") or []
    print("templates:", [(t["goodFingerprintId"], t["goodFingerprintName"]) for t in items[:6]])

    print("\nBEFORE:", getprop(c, "ro.product.model"), "/", getprop(c, "ro.build.fingerprint"))

    # 2) Swap the whole fingerprint via ADI template (id 44 = a Samsung template)
    print("\napplying ADI template 44 ...")
    apply_template(c, 44)
    time.sleep(10)
    print("AFTER swap:", getprop(c, "ro.product.model"), "/", getprop(c, "ro.build.fingerprint"))

    # 3) Change the SIM to a country (regenerates IMSI/operator; restarts, ~2 min)
    print("\nupdate_sim(country_code='VN') ...")
    c.apps.update_sim(pad_code=PAD, country_code="VN")
    time.sleep(120)
    print("SIM country:", getprop(c, "gsm.operator.iso-country"),
          "operator:", getprop(c, "gsm.sim.operator.alpha"))

    # 4) Restore original identity (id 36 = Google Pixel 7 Pro) + US SIM
    print("\nrestoring Pixel 7 Pro + US SIM ...")
    apply_template(c, 36)
    c.apps.update_sim(pad_code=PAD, country_code="US")
    print("done.")
