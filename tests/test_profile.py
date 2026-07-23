"""Unit tests for the Device Profile Framework core (no network/device)."""

import random

from vmos.profile import (
    COUNTRIES,
    Profile,
    gen_iccid,
    gen_imei,
    gen_imsi,
    generate_profile,
    luhn_check_digit,
    luhn_valid,
    validate,
)


def test_luhn_known_vector():
    assert luhn_valid("490154203237518")          # canonical valid IMEI
    assert not luhn_valid("490154203237519")
    assert luhn_check_digit("49015420323751") == "8"


def test_gen_imei_is_luhn_valid_15_digits():
    rng = random.Random(1)
    for _ in range(200):
        imei = gen_imei(rng)
        assert len(imei) == 15 and imei.isdigit() and luhn_valid(imei)


def test_gen_imei_respects_tac():
    imei = gen_imei(random.Random(1), tac="35012345")
    assert imei.startswith("35012345") and luhn_valid(imei)


def test_gen_imsi_prefix_and_length():
    imsi = gen_imsi(random.Random(2), "452", "04")
    assert imsi.startswith("45204") and len(imsi) == 15 and imsi.isdigit()


def test_gen_iccid_shape():
    iccid = gen_iccid(random.Random(3), "84", "04")
    assert iccid.startswith("89") and 19 <= len(iccid) <= 20 and luhn_valid(iccid)


def test_generate_profile_is_consistent():
    p = generate_profile("pixel10pro", "VN", "Viettel", seed=42)
    assert p.build.model == "Pixel 10 Pro"
    assert p.build.device in p.build.fingerprint          # codename consistency
    assert p.telephony.operator == "Viettel"
    assert p.telephony.mcc_mnc == "45204"
    assert p.telephony.imsi.startswith("45204")
    assert p.locale.country == "VN" and p.locale.timezone == "Asia/Ho_Chi_Minh"
    # only the (honest) generic-TAC warning, no errors
    issues = validate(p)
    assert not [i for i in issues if i["level"] == "error"]


def test_generate_profile_deterministic():
    a = generate_profile("pixel10", "US", "AT&T", seed=7)
    b = generate_profile("pixel10", "US", "AT&T", seed=7)
    assert a.to_json() == b.to_json()


def test_json_roundtrip():
    p = generate_profile("pixel10proxl", "GB", "EE", seed=9, dual_sim=True)
    p2 = Profile.from_json(p.to_json())
    assert p2.telephony.imei == p.telephony.imei
    assert len(p2.telephony.imei) == 2
    assert p2.build.fingerprint == p.build.fingerprint


def test_bridges_to_layers():
    p = generate_profile("pixel10pro", "VN", "Mobifone", seed=1,
                         target_apps=["com.liuzh.deviceinfo"])
    dp = p.to_device_profile()
    assert dp.model == "Pixel 10 Pro"
    assert dp.extra_props["ro.serialno"] == p.build.serial
    props = p.identity_props()
    assert props["persist.vmos.spoof.imei"] == p.telephony.imei[0]
    assert props["persist.vmos.spoof.gaid"] == p.identity.gaid
    assert p.runtime.target_apps == ["com.liuzh.deviceinfo"]


def test_validate_catches_errors():
    p = generate_profile("pixel10pro", "VN", "Viettel", seed=42)
    p.telephony.imei = ["123"]                            # bad IMEI
    p.telephony.imsi = "310150000000000"                  # wrong MCC for VN Viettel
    issues = validate(p)
    fields = {i["field"] for i in issues if i["level"] == "error"}
    assert "telephony.imei[0]" in fields
    assert "telephony.imsi" in fields


def test_validate_flags_fingerprint_mismatch():
    p = generate_profile("pixel10pro", "VN", "Viettel", seed=42)
    p.build.device = "tokay"                              # not in the blazer fingerprint
    warns = {i["field"] for i in validate(p) if i["level"] == "warn"}
    assert "build.fingerprint" in warns
