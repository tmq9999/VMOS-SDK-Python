"""Generate + validate a consistent Device Profile (vmos_profile.json).

Part of the Device Profile Framework (docs/en/device-profile-framework.md). This
is pure SDK work — no device needed. The JSON it emits is the single source of
truth both the Layer-1 system applier and the Layer-2 XPose plugin read.

Examples
--------
    python examples/14_generate_profile.py --model pixel10pro --country VN \
        --operator Viettel --target-app com.liuzh.deviceinfo --out vmos_profile.json

    python examples/14_generate_profile.py --model pixel10 --country US --seed 7
"""
import argparse
import sys

from vmos.profile import COUNTRIES, MODEL_CATALOG, generate_profile, validate


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a consistent VMOS device profile")
    ap.add_argument("--model", default="pixel10pro", choices=sorted(MODEL_CATALOG))
    ap.add_argument("--country", default="VN", choices=sorted(COUNTRIES))
    ap.add_argument("--operator", help="operator name (default: random for the country)")
    ap.add_argument("--name", help="profile display name")
    ap.add_argument("--base-adi", dest="base_adi", help="base ADI model (e.g. Pixel 7 Pro)")
    ap.add_argument("--target-app", dest="target_apps", action="append", default=[],
                    help="app package to scope the Layer-2 hook to (repeatable)")
    ap.add_argument("--dual-sim", action="store_true")
    ap.add_argument("--seed", type=int, help="reproducible output")
    ap.add_argument("--out", help="write vmos_profile.json to this path")
    args = ap.parse_args()

    profile = generate_profile(
        args.model, args.country, args.operator, name=args.name,
        base_adi=args.base_adi, target_apps=args.target_apps,
        dual_sim=args.dual_sim, seed=args.seed,
    )
    print(profile.to_json())

    issues = validate(profile)
    if issues:
        print("\n--- validation ---", file=sys.stderr)
        for it in issues:
            print(f"  [{it['level']}] {it['field']}: {it['message']}", file=sys.stderr)
    errors = [i for i in issues if i["level"] == "error"]
    print(f"\n{len(errors)} error(s), {len(issues) - len(errors)} warning(s)", file=sys.stderr)

    if args.out:
        profile.save(args.out)
        print(f"saved {args.out}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
