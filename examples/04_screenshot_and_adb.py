"""Take a screenshot and run an ADB command - production-verified flow."""
import time

from vmos import VMOSClient

PAD = "AC32010180421"

with VMOSClient() as client:
    # Screenshot: production returns a signed, expiring accessUrl per pad -
    # download it immediately (no task polling needed).
    shots = client.instance.screenshot(pad_codes=[PAD], rotation=0, definition=90)
    for shot in shots:
        print(shot["padCode"], "->", shot["accessUrl"])

    # Async ADB shell command -> track the task to completion.
    tasks = client.instance.async_cmd(pad_codes=[PAD], script_content="getprop ro.product.model")
    task_id = tasks[0]["taskId"]
    while True:
        info = client.tasks.pad_task_detail(task_ids=[task_id])[0]
        if info["taskStatus"] in (3, -1, 4, 5):  # 3 = success
            print("adb output:", info.get("taskResult"))
            break
        time.sleep(2)
