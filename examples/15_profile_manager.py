"""Provision a whole device from ONE profile via the Profile Manager.

This is the profile-driven entry point: instead of calling ``apply_profile`` for
Layer 1 and ``set_identity_props`` + ``load_xpose_plugin`` for Layer 2 by hand,
you build one :class:`~vmos.Profile` and hand it to a
:class:`~vmos.ProfileManager`. The manager fans it out to every backend
(``system_applier`` = Layer 1 build props, ``java_hook`` = Layer 2 framework
getters) and can read it all back with ``verify``.

See docs/en/device-profile-framework.md.

Examples
--------
Generate a profile and provision it (Layer 1 + Layer 2 props), scoping the
plugin into two device-info apps (APK hosted at a URL, downloaded on the pad):

    VMOS_ACCESS_KEY=... VMOS_SECRET_KEY=... \
        python examples/15_profile_manager.py --pad ACP... \
        --model pixel10pro --country VN --operator Viettel --seed 20260724 \
        --target-app com.liuzh.deviceinfo --target-app com.ytheekshana.deviceinfo \
        --apk-url https://your-host/vmos-xpose-spoof.apk --verify

Re-apply from a saved profile without reloading the plugin (props only):

    python examples/15_profile_manager.py --pad ACP... \
        --profile-json vmos_profile.json --verify

Just print the profile the manager would apply (no device, no client):

    python examples/15_profile_manager.py --model pixel10 --country US --dry-run
"""
import argparse
import json
import sys

from vmos import (
    Profile,
    ProfileManager,
    ProfileValidationError,
    generate_profile,
    standard_manager,
    validate_profile,
)
from vmos.profile import COUNTRIES, MODEL_CATALOG


def _load_or_generate(args) -> Profile:
    if args.profile_json:
        return Profile.load(args.profile_json)
    return generate_profile(
        args.model, args.country, args.operator, name=args.name,
        base_adi=args.base_adi, target_apps=args.target_apps,
        dual_sim=args.dual_sim, seed=args.seed,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Provision a device from one profile (Profile Manager)")
    ap.add_argument("--pad", help="pad code (real-device instance); omit only with --dry-run")
    # profile source
    ap.add_argument("--profile-json", dest="profile_json", help="load an existing vmos_profile.json")
    ap.add_argument("--model", default="pixel10pro", choices=sorted(MODEL_CATALOG))
    ap.add_argument("--country", default="VN", choices=sorted(COUNTRIES))
    ap.add_argument("--operator", help="operator name (default: random for the country)")
    ap.add_argument("--name", help="profile display name")
    ap.add_argument("--base-adi", dest="base_adi", help="base ADI model (e.g. Pixel 7 Pro)")
    ap.add_argument("--target-app", dest="target_apps", action="append", default=[],
                    help="app package to scope the Layer-2 hook to (repeatable)")
    ap.add_argument("--dual-sim", action="store_true")
    ap.add_argument("--seed", type=int, help="reproducible output")
    # plugin source (only needed to (re)load the XPose plugin)
    ap.add_argument("--apk-url", dest="apk_url", help="public URL to the plugin APK")
    ap.add_argument("--apk-path", dest="apk_path", help="plugin APK path already on the pad")
    # behaviour
    ap.add_argument("--no-persist", action="store_true", help="do not install boot persistence")
    ap.add_argument("--verify", action="store_true", help="read back + diff after applying")
    ap.add_argument("--dry-run", action="store_true", help="print the profile only; no device calls")
    args = ap.parse_args()

    if args.apk_url and args.apk_path:
        ap.error("provide at most one of --apk-url or --apk-path")

    profile = _load_or_generate(args)

    # Validate up front so the report is honest either way.
    issues = validate_profile(profile)
    errors = [i for i in issues if i["level"] == "error"]
    for it in issues:
        print(f"  [{it['level']}] {it['field']}: {it['message']}", file=sys.stderr)
    print(f"validation: {len(errors)} error(s), {len(issues) - len(errors)} warning(s)", file=sys.stderr)

    if args.dry_run:
        print(profile.to_json())
        return 1 if errors else 0

    if not args.pad:
        ap.error("--pad is required (or use --dry-run)")

    from vmos import VMOSClient

    with VMOSClient() as client:
        mgr: ProfileManager = standard_manager(
            client, args.pad,
            apk_url=args.apk_url, apk_path=args.apk_path,
            persist=not args.no_persist,
        )
        try:
            result = mgr.apply(profile)
        except ProfileValidationError as exc:
            print(f"\nrefusing to apply an invalid profile: {exc}", file=sys.stderr)
            return 1
        print("\n--- apply ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if args.verify:
            print("\n--- verify ---")
            print(json.dumps(mgr.verify(profile), indent=2, ensure_ascii=False))
            print("\nNOTE: Layer-2 verify confirms the persist.vmos.spoof.* props are set. "
                  "To prove the app-observed values changed, read a SCOPED device-info app "
                  "(screenshot) — never `service call` / `getprop` of the real getters.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
