"""Push an APK to instances by URL and manage the app lifecycle."""
from vmos import VMOSClient

PAD = "AC32010180421"
APK_URL = "https://example.com/your-app.apk"

with VMOSClient() as client:
    # Push + auto-install an APK from a public URL (async task)
    task = client.apps.upload_file_v3(
        pad_codes=[PAD], url=APK_URL, auto_install=1, file_name="your-app.apk"
    )
    print("upload task:", task)

    # Installed apps on the instance
    apps = client.apps.list_installed_app(pad_codes=[PAD])
    print("installed:", apps)

    # Start / stop by package name
    client.apps.start_app(pad_codes=[PAD], pkg_name="com.android.chrome")
    client.apps.stop_app(pad_codes=[PAD], pkg_name="com.android.chrome")
