"""Take a screenshot and run an ADB command."""
from vmos import VMOSClient

PAD = "AC32010180421"

with VMOSClient() as client:
    # Screenshot (async - result arrives via screenshotInfo / callback)
    shot = client.instance.screenshot(pad_codes=[PAD])
    print("screenshot task:", shot)
    result = client.instance.screenshot_info(task_ids=[t["taskId"] for t in shot])
    print("screenshot result:", result)

    # Async ADB shell command (result via executeScriptInfo / callback)
    cmd = client.instance.async_cmd(pad_codes=[PAD], script_content="getprop ro.product.model")
    print("adb task:", cmd)
