"""Reseller device-profile toolkit CLI — spoof a real device to any target model.

Turns one VMOS real-device instance into a custom device profile (even models
VMOS does not offer, e.g. Pixel 10 Pro / Android 17 / SDK 37), persisting across
reboots via a Magisk module. Prerequisite: Kitsune Magisk enabled on the pad.

Examples
--------
Apply the built-in Pixel 10 Pro / Android 17 profile and verify:

    VMOS_ACCESS_KEY=... VMOS_SECRET_KEY=... \
        python examples/12_device_spoof_toolkit.py --pad ACP... --preset pixel10pro --verify

Apply a fully custom profile:

    python examples/12_device_spoof_toolkit.py --pad ACP... \
        --model "Galaxy Z Fold7" --brand samsung --manufacturer samsung \
        --release 16 --sdk 36 --android-id 0123456789abcdef --verify

Enable Magisk first (headless Toolbox automation) if it is not on yet:

    python examples/12_device_spoof_toolkit.py --pad ACP... --enable-magisk --preset pixel10pro

Remove the persistent spoof:

    python examples/12_device_spoof_toolkit.py --pad ACP... --remove
"""
import argparse
import json
import sys

from vmos import VMOSClient
from vmos.spoof import (
    PIXEL_10_PRO_A17,
    PIXEL_10_A17,
    PIXEL_10_PRO_XL_A17,
    DeviceProfile,
    apply_profile,
    enable_magisk_ui,
    magisk_ready,
    remove_spoof,
    verify_profile,
    PadRootShell,
)

PRESETS = {"pixel10pro": PIXEL_10_PRO_A17, "pixel10": PIXEL_10_A17, "pixel10proxl": PIXEL_10_PRO_XL_A17}


def main() -> int:
    ap = argparse.ArgumentParser(description="VMOS real-device profile spoof toolkit")
    ap.add_argument("--pad", required=True, help="pad code (real-device instance)")
    ap.add_argument("--preset", choices=sorted(PRESETS), help="built-in target profile")
    ap.add_argument("--model")
    ap.add_argument("--brand", default="google")
    ap.add_argument("--manufacturer")
    ap.add_argument("--device")
    ap.add_argument("--fingerprint")
    ap.add_argument("--release", help="ro.build.version.release, e.g. 17")
    ap.add_argument("--sdk", type=int, help="ro.build.version.sdk, e.g. 37")
    ap.add_argument("--android-id", dest="android_id")
    ap.add_argument("--enable-magisk", action="store_true", help="auto-enable Kitsune Magisk via Toolbox UI")
    ap.add_argument("--no-persist", action="store_true", help="apply for this session only (no boot module)")
    ap.add_argument("--remove", action="store_true", help="remove persistent spoof payload and exit")
    ap.add_argument("--verify", action="store_true", help="read back props via getprop after applying")
    args = ap.parse_args()

    with VMOSClient() as client:
        if args.remove:
            remove_spoof(client, args.pad)
            print("Removed persistent spoof payload. Reboot to fully restore runtime props.")
            return 0

        if args.enable_magisk:
            print("Enabling Kitsune Magisk via Toolbox UI ...")
            ok = enable_magisk_ui(client, args.pad)
            print("Magisk ready:", ok)
            if not ok:
                print("Could not confirm Magisk; drive the toggle manually and retry.")
                return 2

        if args.preset:
            profile = PRESETS[args.preset]
        elif args.model:
            profile = DeviceProfile(
                model=args.model, brand=args.brand, manufacturer=args.manufacturer,
                device=args.device, fingerprint=args.fingerprint,
                release=args.release, sdk=args.sdk, android_id=args.android_id,
            )
        else:
            ap.error("provide --preset or --model")

        if not magisk_ready(PadRootShell(client, args.pad)):
            print("Kitsune Magisk is not enabled on this pad. Run with --enable-magisk first.")
            return 2

        summary = apply_profile(client, args.pad, profile, persist=not args.no_persist)
        print("Applied:", json.dumps(summary))

        if args.verify:
            result = verify_profile(client, args.pad, profile)
            print("Verify OK:", result["ok"])
            for key, c in result["checks"].items():
                mark = "OK " if c["match"] else "XX "
                print(f"  {mark}{key}: {c['got']!r} (want {c['want']!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
