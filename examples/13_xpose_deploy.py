"""Deploy + verify the private XPose spoof plugin on a VMOS real device.

Pipeline: set persist.vmos.spoof.* identity props (Magisk resetprop) -> load the
plugin into the target app via `apmt` -> restart the target app -> print the
loaded-plugin list and tail the plugin's logcat so you can confirm the hooks
installed. See docs/en/xpose-custom-hook.md and xpose_plugin/BUILD.md.

Prereqs on the pad: Kitsune Magisk enabled; the plugin APK reachable either by
public URL (--apk-url, downloaded on the pad by apmt) or already pushed to the
pad (--apk-path). Build the APK with xpose_plugin/ (see BUILD.md).

Examples
--------
Host the APK and deploy, spoofing IMEI + GAID + Android ID into an app:

    VMOS_ACCESS_KEY=... VMOS_SECRET_KEY=... \
        python examples/13_xpose_deploy.py --pad ACP... \
        --target-pkg com.example.targetapp \
        --apk-url https://your-host/vmos-xpose-spoof.apk \
        --imei 356789012345678 --gaid 38400000-8cf0-11bd-b23e-10b96e40000d \
        --android-id a1b2c3d4e5f60718

Push a local APK onto the pad first, then load by file path:

    python examples/13_xpose_deploy.py --pad ACP... --target-pkg com.example.app \
        --apk-path /sdcard/vmos-xpose-spoof.apk --imei 356789012345678

List / remove loaded plugins:

    python examples/13_xpose_deploy.py --pad ACP... --list
    python examples/13_xpose_deploy.py --pad ACP... --remove --name vmosid
"""
import argparse
import sys

from vmos import VMOSClient
from vmos.spoof import (
    PadRootShell,
    list_xpose_plugins,
    load_xpose_plugin,
    remove_xpose_plugin,
    set_identity_props,
)

# CLI flag -> set_identity_props keyword
_IDENTITY_FLAGS = {
    "imei": "imei", "meid": "meid", "imsi": "imsi", "iccid": "iccid",
    "line1": "line1", "android_id": "android_id", "gaid": "gaid", "oaid": "oaid",
    "wifi_mac": "wifi_mac", "bssid": "bssid", "serial": "serial", "drm_id": "drm_id",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Deploy/verify the private XPose spoof plugin")
    ap.add_argument("--pad", required=True, help="pad code (real-device instance)")
    ap.add_argument("--target-pkg", help="package to hook (e.g. com.example.app)")
    ap.add_argument("--name", default="vmosid", help="apmt patch name (default: vmosid)")
    ap.add_argument("--apk-url", help="public URL to the plugin APK (apmt downloads on the pad)")
    ap.add_argument("--apk-path", help="path to the plugin APK already on the pad")
    # identity values
    ap.add_argument("--imei")
    ap.add_argument("--meid")
    ap.add_argument("--imsi")
    ap.add_argument("--iccid")
    ap.add_argument("--line1")
    ap.add_argument("--android-id", dest="android_id")
    ap.add_argument("--gaid", help="Google Advertising ID")
    ap.add_argument("--oaid")
    ap.add_argument("--wifi-mac", dest="wifi_mac")
    ap.add_argument("--bssid")
    ap.add_argument("--serial")
    ap.add_argument("--drm-id", dest="drm_id", help="MediaDrm/Widevine device id (hex)")
    # actions
    ap.add_argument("--no-restart", action="store_true", help="do not force-stop/relaunch the target app")
    ap.add_argument("--list", action="store_true", help="just print loaded plugins and exit")
    ap.add_argument("--remove", action="store_true", help="remove the named plugin and exit")
    args = ap.parse_args()

    with VMOSClient() as client:
        if args.list:
            print(list_xpose_plugins(client, args.pad))
            return 0
        if args.remove:
            print(remove_xpose_plugin(client, args.pad, args.name))
            return 0

        if not args.target_pkg:
            ap.error("--target-pkg is required to deploy (or use --list/--remove)")
        if bool(args.apk_url) == bool(args.apk_path):
            ap.error("provide exactly one of --apk-url or --apk-path")

        # 1) push identity values (resetprop now + persist in the Magisk module)
        identity = {kw: getattr(args, flag) for flag, kw in _IDENTITY_FLAGS.items()
                    if getattr(args, flag)}
        if identity:
            written = set_identity_props(client, args.pad, **identity)
            print(f"set {len(written)} identity prop(s): {', '.join(sorted(written))}")
        else:
            print("no identity flags given — plugin will leave all fields real")

        # 2) load the plugin into the target app
        out = load_xpose_plugin(client, args.pad, name=args.name,
                                target_pkg=args.target_pkg,
                                apk_url=args.apk_url, apk_path=args.apk_path)
        print(f"apmt: {out.strip()}")

        shell = PadRootShell(client, args.pad)
        # 3) restart the target so the hook attaches to a fresh process
        if not args.no_restart:
            shell.sh(f"am force-stop {args.target_pkg}; "
                     f"monkey -p {args.target_pkg} -c android.intent.category.LAUNCHER 1 "
                     f">/dev/null 2>&1 || true")
            print(f"restarted {args.target_pkg}")

        # 4) confirm: loaded-plugin list + plugin logcat ("hooked ..." lines)
        print("\n--- apmt patch list ---")
        print(list_xpose_plugins(client, args.pad).strip())
        print("\n--- logcat VMOSSpoof (hook install confirmation) ---")
        print(shell.sh("logcat -d -s VMOSSpoof:D 2>/dev/null | tail -n 40").strip()
              or "(no VMOSSpoof logs yet — open/use the app, then re-run with --list)")

        print("\nVerify from a SCOPED app that calls the Java getter (e.g. a device-info "
              "app showing IMEI/GAID). Do NOT use `service call iphonesubinfo` or `getprop` "
              "— those bypass the app-process Java hook.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
