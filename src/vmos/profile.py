"""Device Profile Framework — canonical, profile-driven device identity.

A **Profile** is the single source of truth for one device's identity. It is a
language-neutral document (``vmos_profile.json``) that every applier reads:

* **Layer 1 (system)** — :meth:`Profile.to_device_profile` yields a
  :class:`vmos.spoof.DeviceProfile` that ``apply_profile`` writes with
  ``resetprop`` + a Magisk module (build identity, serial, density).
* **Layer 2 (app hook)** — :meth:`Profile.identity_props` yields the
  ``persist.vmos.spoof.*`` map the XPose plugin reads for the framework-held
  getters (IMEI/IMSI/ICCID/GAID/Android-ID/serial/MAC/MediaDrm). The same data
  is also emitted as ``vmos_profile.json`` for the plugin to consume directly.

:func:`generate_profile` builds a **believable, internally consistent** profile
(the real product value); :func:`validate` checks consistency before you apply.

Data provenance / honesty
--------------------------
* **MCC/MNC, country ISO, dialing codes** below are accurate public values for
  the listed operators.
* **Fingerprints** come from the vetted Pixel-Props presets in :mod:`vmos.spoof`.
* **TAC (IMEI type-allocation code) and display specs** are **unverified
  samples**, clearly flagged — supply real per-model values (``tac=``,
  ``display=``) for production believability. :func:`validate` warns when a TAC
  looks generic/unregistered.
"""
from __future__ import annotations

import json
import random
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from .spoof import (
    DeviceProfile,
    PIXEL_10_A17,
    PIXEL_10_PRO_A17,
    PIXEL_10_PRO_XL_A17,
)

__all__ = [
    "SCHEMA_VERSION",
    "Profile",
    "BuildSection",
    "TelephonySection",
    "IdentitySection",
    "NetworkSection",
    "DisplaySection",
    "LocaleSection",
    "RuntimeSection",
    "COUNTRIES",
    "MODEL_CATALOG",
    "generate_profile",
    "validate",
    "luhn_valid",
    "luhn_check_digit",
]

SCHEMA_VERSION = "1.0"

# ---------------------------------------------------------------------------
# Reference data (accurate public values)
# ---------------------------------------------------------------------------
#: country -> locale + dialing + {operator: (mcc, mnc)}
COUNTRIES: Dict[str, Dict[str, Any]] = {
    "VN": {
        "language": "vi", "country": "VN", "timezone": "Asia/Ho_Chi_Minh",
        "iso": "vn", "dialing": "84",
        "operators": {"Viettel": ("452", "04"), "Vinaphone": ("452", "02"),
                      "Mobifone": ("452", "01"), "Vietnamobile": ("452", "05")},
    },
    "US": {
        "language": "en", "country": "US", "timezone": "America/New_York",
        "iso": "us", "dialing": "1",
        "operators": {"AT&T": ("310", "410"), "T-Mobile": ("310", "260"),
                      "Verizon": ("311", "480")},
    },
    "GB": {
        "language": "en", "country": "GB", "timezone": "Europe/London",
        "iso": "gb", "dialing": "44",
        "operators": {"EE": ("234", "30"), "Vodafone": ("234", "15"),
                      "O2": ("234", "10")},
    },
}


@dataclass
class ModelInfo:
    """Catalog entry: a vetted build preset + (sample) display + (sample) TAC."""
    profile: DeviceProfile
    width_px: int
    height_px: int
    density_dpi: int
    refresh_rate: int
    tac: Optional[str] = None          # 8-digit TAC; None -> generic (flagged)
    display_verified: bool = False     # set True only with real specs
    tac_verified: bool = False


#: model_key -> ModelInfo. Fingerprints are vetted (Pixel-Props); display & TAC
#: are UNVERIFIED samples — override with real values for production.
MODEL_CATALOG: Dict[str, ModelInfo] = {
    "pixel10pro": ModelInfo(PIXEL_10_PRO_A17, 1344, 2992, 480, 120),
    "pixel10": ModelInfo(PIXEL_10_A17, 1080, 2424, 420, 120),
    "pixel10proxl": ModelInfo(PIXEL_10_PRO_XL_A17, 1344, 2992, 480, 120),
}


# ---------------------------------------------------------------------------
# Luhn + identity generators
# ---------------------------------------------------------------------------
def _luhn_sum(number: str) -> int:
    total, alt = 0, False
    for ch in reversed(number):
        d = int(ch)
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total


def luhn_valid(number: str) -> bool:
    """True if ``number`` (digits only) passes the Luhn checksum."""
    return number.isdigit() and _luhn_sum(number) % 10 == 0


def luhn_check_digit(payload: str) -> str:
    """Check digit to append to ``payload`` so the result is Luhn-valid."""
    return str((10 - _luhn_sum(payload + "0") % 10) % 10)


def _digits(rng: random.Random, n: int) -> str:
    return "".join(str(rng.randint(0, 9)) for _ in range(n))


def gen_imei(rng: random.Random, tac: Optional[str] = None) -> str:
    """15-digit Luhn-valid IMEI. ``tac`` = 8-digit type-allocation code; if
    omitted a generic RBI-35 TAC is used (flag it as unverified)."""
    if tac and (len(tac) != 8 or not tac.isdigit()):
        raise ValueError("tac must be 8 digits")
    tac = tac or ("35" + _digits(rng, 6))
    payload = tac + _digits(rng, 6)          # TAC(8) + serial(6) = 14
    return payload + luhn_check_digit(payload)


def gen_imsi(rng: random.Random, mcc: str, mnc: str) -> str:
    """15-digit IMSI = MCC + MNC + random MSIN."""
    body = mcc + mnc
    return body + _digits(rng, 15 - len(body))


def gen_iccid(rng: random.Random, dialing: str, mnc: str) -> str:
    """19-digit ICCID: 89 (telecom) + country dialing code + issuer + Luhn."""
    base = "89" + dialing + mnc
    base = (base + _digits(rng, 18))[:18]
    return base + luhn_check_digit(base)


def gen_android_id(rng: random.Random) -> str:
    return "".join(rng.choice("0123456789abcdef") for _ in range(16))


def gen_gaid(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def gen_gsf_id(rng: random.Random) -> str:
    return "".join(rng.choice("0123456789abcdef") for _ in range(16))


def gen_media_drm_id(rng: random.Random) -> str:
    return "".join(rng.choice("0123456789abcdef") for _ in range(32))


def gen_mac(rng: random.Random) -> str:
    """Locally-administered MAC (honest default; override with a vendor OUI)."""
    first = rng.choice((0x02, 0x06, 0x0A, 0x0E))
    octets = [first] + [rng.randint(0, 255) for _ in range(5)]
    return ":".join(f"{o:02x}" for o in octets)


# ---------------------------------------------------------------------------
# Profile schema
# ---------------------------------------------------------------------------
@dataclass
class BuildSection:
    brand: str = ""
    manufacturer: str = ""
    model: str = ""
    device: str = ""
    product: str = ""
    fingerprint: str = ""
    build_id: str = ""
    release: str = ""
    sdk: Optional[int] = None
    security_patch: str = ""
    serial: str = ""


@dataclass
class TelephonySection:
    imei: List[str] = field(default_factory=list)   # per SIM slot
    meid: str = ""
    imsi: str = ""
    iccid: str = ""
    line1: str = ""
    mcc_mnc: str = ""                # e.g. "45204"
    operator: str = ""
    sim_country_iso: str = ""


@dataclass
class IdentitySection:
    android_id: str = ""
    gaid: str = ""
    oaid: str = ""
    gsf_id: str = ""
    media_drm_id: str = ""


@dataclass
class NetworkSection:
    wifi_mac: str = ""
    bssid: str = ""
    ssid: str = ""


@dataclass
class DisplaySection:
    width_px: Optional[int] = None
    height_px: Optional[int] = None
    density_dpi: Optional[int] = None
    refresh_rate: Optional[int] = None


@dataclass
class LocaleSection:
    language: str = ""
    country: str = ""
    timezone: str = ""


@dataclass
class RuntimeSection:
    target_apps: List[str] = field(default_factory=list)     # Layer-2 hook scope
    enabled_sections: List[str] = field(default_factory=list)


@dataclass
class Profile:
    """Canonical device profile (the source of truth). Serialize to
    ``vmos_profile.json`` with :meth:`to_json`."""
    meta: Dict[str, Any] = field(default_factory=dict)
    build: BuildSection = field(default_factory=BuildSection)
    telephony: TelephonySection = field(default_factory=TelephonySection)
    identity: IdentitySection = field(default_factory=IdentitySection)
    network: NetworkSection = field(default_factory=NetworkSection)
    display: DisplaySection = field(default_factory=DisplaySection)
    locale: LocaleSection = field(default_factory=LocaleSection)
    features: Dict[str, bool] = field(default_factory=dict)
    runtime: RuntimeSection = field(default_factory=RuntimeSection)

    # -- serialization --------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["schema_version"] = SCHEMA_VERSION
        return d

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.to_json())

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Profile":
        return cls(
            meta=d.get("meta", {}),
            build=BuildSection(**d.get("build", {})),
            telephony=TelephonySection(**d.get("telephony", {})),
            identity=IdentitySection(**d.get("identity", {})),
            network=NetworkSection(**d.get("network", {})),
            display=DisplaySection(**d.get("display", {})),
            locale=LocaleSection(**d.get("locale", {})),
            features=d.get("features", {}),
            runtime=RuntimeSection(**d.get("runtime", {})),
        )

    @classmethod
    def from_json(cls, text: str) -> "Profile":
        return cls.from_dict(json.loads(text))

    @classmethod
    def load(cls, path: str) -> "Profile":
        with open(path, encoding="utf-8") as fh:
            return cls.from_json(fh.read())

    # -- bridges to the appliers ---------------------------------------
    def to_device_profile(self) -> DeviceProfile:
        """Layer 1: a :class:`vmos.spoof.DeviceProfile` (build identity + serial
        + density) to feed ``apply_profile`` (resetprop + Magisk module)."""
        b = self.build
        extra: Dict[str, str] = {}
        if b.build_id:
            extra["ro.build.id"] = b.build_id
        if b.serial:
            extra["ro.serialno"] = b.serial
            extra["ro.boot.serialno"] = b.serial
        if self.display.density_dpi:
            extra["ro.sf.lcd_density"] = str(self.display.density_dpi)
        return DeviceProfile(
            model=b.model, brand=b.brand or "google",
            manufacturer=b.manufacturer or None, device=b.device or None,
            product_name=b.product or None, fingerprint=b.fingerprint or None,
            release=b.release or None, sdk=b.sdk,
            security_patch=b.security_patch or None,
            android_id=self.identity.android_id or None,
            extra_props=extra,
        )

    def identity_props(self) -> Dict[str, str]:
        """Layer 2: the ``persist.vmos.spoof.*`` map the XPose plugin reads."""
        t, i, n, b = self.telephony, self.identity, self.network, self.build
        m = {
            "persist.vmos.spoof.imei": t.imei[0] if t.imei else "",
            "persist.vmos.spoof.meid": t.meid,
            "persist.vmos.spoof.imsi": t.imsi,
            "persist.vmos.spoof.iccid": t.iccid,
            "persist.vmos.spoof.line1": t.line1,
            "persist.vmos.spoof.androidid": i.android_id,
            "persist.vmos.spoof.gaid": i.gaid,
            "persist.vmos.spoof.oaid": i.oaid,
            "persist.vmos.spoof.wifimac": n.wifi_mac,
            "persist.vmos.spoof.bssid": n.bssid,
            "persist.vmos.spoof.serial": b.serial,
            "persist.vmos.spoof.drmid": i.media_drm_id,
        }
        return {k: v for k, v in m.items() if v}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------
def generate_profile(
    model_key: str = "pixel10pro",
    country: str = "VN",
    operator: Optional[str] = None,
    *,
    name: Optional[str] = None,
    base_adi: Optional[str] = None,
    target_apps: Optional[List[str]] = None,
    dual_sim: bool = False,
    seed: Optional[int] = None,
) -> Profile:
    """Build a believable, internally consistent :class:`Profile`.

    ``model_key`` indexes :data:`MODEL_CATALOG`; ``country``/``operator`` index
    :data:`COUNTRIES`. Pass ``seed`` for reproducible output. TAC/display come
    from the (sample) catalog entry — override afterwards with real values.
    """
    if model_key not in MODEL_CATALOG:
        raise ValueError(f"unknown model_key {model_key!r}; have {sorted(MODEL_CATALOG)}")
    if country not in COUNTRIES:
        raise ValueError(f"unknown country {country!r}; have {sorted(COUNTRIES)}")
    rng = random.Random(seed)
    mi = MODEL_CATALOG[model_key]
    dp = mi.profile
    c = COUNTRIES[country]
    op = operator or rng.choice(list(c["operators"]))
    if op not in c["operators"]:
        raise ValueError(f"operator {op!r} not in {country}; have {sorted(c['operators'])}")
    mcc, mnc = c["operators"][op]

    n_sim = 2 if dual_sim else 1
    imei = [gen_imei(rng, mi.tac) for _ in range(n_sim)]

    prof = Profile(
        meta={
            "name": name or f"{dp.model} / {op} / {country}",
            "version": 1,
            "base_adi": base_adi or "",
            "model_key": model_key,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tac_verified": mi.tac_verified,
            "display_verified": mi.display_verified,
        },
        build=BuildSection(
            brand=dp.brand, manufacturer=dp.manufacturer or dp.brand,
            model=dp.model, device=dp.device or "", product=dp.product_name or dp.device or "",
            fingerprint=dp.fingerprint or "",
            build_id=(dp.fingerprint or "//::/").split("/")[3].split(":")[0] if dp.fingerprint else "",
            release=str(dp.release or ""), sdk=dp.sdk,
            security_patch=dp.security_patch or "",
            serial=_serial(rng),
        ),
        telephony=TelephonySection(
            imei=imei, imsi=gen_imsi(rng, mcc, mnc),
            iccid=gen_iccid(rng, c["dialing"], mnc),
            mcc_mnc=mcc + mnc, operator=op, sim_country_iso=c["iso"],
        ),
        identity=IdentitySection(
            android_id=gen_android_id(rng), gaid=gen_gaid(rng),
            gsf_id=gen_gsf_id(rng), media_drm_id=gen_media_drm_id(rng),
        ),
        network=NetworkSection(wifi_mac=gen_mac(rng), bssid=gen_mac(rng)),
        display=DisplaySection(mi.width_px, mi.height_px, mi.density_dpi, mi.refresh_rate),
        locale=LocaleSection(c["language"], c["country"], c["timezone"]),
        runtime=RuntimeSection(
            target_apps=list(target_apps or []),
            enabled_sections=["build", "telephony", "identity", "network", "display", "locale"],
        ),
    )
    return prof


def _serial(rng: random.Random) -> str:
    return "".join(rng.choice("0123456789ABCDEF") for _ in range(16)).lower()


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------
def validate(profile: Profile) -> List[Dict[str, str]]:
    """Return a list of issues ``{level, field, message}``. ``level`` is
    ``"error"`` (inconsistent / invalid) or ``"warn"`` (believability risk).
    Empty list == a clean, internally consistent profile."""
    issues: List[Dict[str, str]] = []

    def err(fieldname: str, msg: str) -> None:
        issues.append({"level": "error", "field": fieldname, "message": msg})

    def warn(fieldname: str, msg: str) -> None:
        issues.append({"level": "warn", "field": fieldname, "message": msg})

    b, t, i, n, loc = (profile.build, profile.telephony, profile.identity,
                       profile.network, profile.locale)

    # build consistency
    if not b.model:
        err("build.model", "model is required")
    if b.fingerprint:
        if b.device and b.device not in b.fingerprint:
            warn("build.fingerprint", f"device codename {b.device!r} not present in fingerprint")
        if b.release and f":{b.release}/" not in b.fingerprint:
            warn("build.fingerprint", f"release {b.release!r} not present in fingerprint")
        if b.build_id and b.build_id not in b.fingerprint:
            warn("build.fingerprint", f"build_id {b.build_id!r} not present in fingerprint")

    # telephony
    for idx, imei in enumerate(t.imei):
        if len(imei) != 15 or not imei.isdigit():
            err(f"telephony.imei[{idx}]", "IMEI must be 15 digits")
        elif not luhn_valid(imei):
            err(f"telephony.imei[{idx}]", "IMEI fails Luhn checksum")
        elif imei[:2] == "35" and imei[2:8] and _looks_generic_tac(imei[:8]):
            warn(f"telephony.imei[{idx}]", "TAC looks generic/unregistered — use a real per-model TAC")
    if t.imsi:
        if len(t.imsi) != 15 or not t.imsi.isdigit():
            err("telephony.imsi", "IMSI must be 15 digits")
        elif t.mcc_mnc and not t.imsi.startswith(t.mcc_mnc):
            err("telephony.imsi", f"IMSI does not start with MCC+MNC {t.mcc_mnc}")
    if t.iccid:
        if not t.iccid.startswith("89"):
            err("telephony.iccid", "ICCID must start with 89")
        if not (18 <= len(t.iccid) <= 20):
            err("telephony.iccid", "ICCID length must be 19-20")
        elif not luhn_valid(t.iccid):
            warn("telephony.iccid", "ICCID fails Luhn checksum")
    # operator/country consistency
    if loc.country and loc.country in COUNTRIES and t.operator:
        ops = COUNTRIES[loc.country]["operators"]
        if t.operator in ops and t.mcc_mnc and "".join(ops[t.operator]) != t.mcc_mnc:
            err("telephony.mcc_mnc", f"MCC+MNC {t.mcc_mnc} != {t.operator} in {loc.country}")

    # identity formats
    if i.android_id and (len(i.android_id) != 16 or not _is_hex(i.android_id)):
        err("identity.android_id", "android_id must be 16 hex chars")
    if i.gaid and not _is_uuid(i.gaid):
        err("identity.gaid", "GAID must be a UUID")
    if i.media_drm_id and (len(i.media_drm_id) != 32 or not _is_hex(i.media_drm_id)):
        warn("identity.media_drm_id", "MediaDrm id is usually 32 hex chars")

    # network
    for macname, mac in (("wifi_mac", n.wifi_mac), ("bssid", n.bssid)):
        if mac and not _is_mac(mac):
            err(f"network.{macname}", "MAC must be 6 colon-separated hex octets")

    # locale
    if loc.country and loc.country not in COUNTRIES:
        warn("locale.country", f"country {loc.country!r} not in reference table")

    return issues


def _is_hex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def _is_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False


def _is_mac(s: str) -> bool:
    parts = s.split(":")
    return len(parts) == 6 and all(len(p) == 2 and _is_hex(p) for p in parts)


def _looks_generic_tac(tac: str) -> bool:
    """Heuristic: a TAC generated as RBI-35 + random (our fallback) is not a
    registered model TAC. We can't positively verify TACs without a TAC DB, so
    this only flags the obvious fallback pattern for believability review."""
    return not any(mi.tac == tac for mi in MODEL_CATALOG.values())
