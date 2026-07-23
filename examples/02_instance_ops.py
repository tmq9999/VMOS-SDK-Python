"""Restart an instance and follow the async task to completion."""
import sys
import time

from vmos import VMOSClient

PAD_CODE = sys.argv[1] if len(sys.argv) > 1 else "AC32010180421"

with VMOSClient() as client:
    tasks = client.instance.restart(pad_codes=[PAD_CODE])
    task_id = tasks[0]["taskId"]
    print(f"restart dispatched, taskId={task_id}")

    # Poll the async task until it finishes (status 3 = success)
    while True:
        detail = client.tasks.pad_task_detail(task_ids=[task_id])
        status = detail[0]["taskStatus"]
        print("  taskStatus =", status)
        if status in (3, -1, 4, 5):  # terminal states
            break
        time.sleep(3)
