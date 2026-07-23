# `client.tasks` — Task Management

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Query status & details of asynchronous tasks (instance ops, file pushes).

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`get_task_status`](#get-task-status--device-task-execution-result-query) | POST | `/vcpcloud/api/padApi/getTaskStatus` |
| [`pad_task_detail`](#pad-task-detail--instance-operation-task-details) | POST | `/vcpcloud/api/padApi/padTaskDetail` |
| [`pad_execute_task_info`](#pad-execute-task-info--instance-restart-reset-execution-result) | POST | `/vcpcloud/api/padApi/padExecuteTaskInfo` |
| [`file_task_detail`](#file-task-detail--file-task-details) | POST | `/vcpcloud/api/padApi/fileTaskDetail` |

[Back to index](README.md)

---

### `get_task_status` — Device Task Execution Result Query

Query task execution result using task number (for smart IP).

- **Endpoint**: `POST /vcpcloud/api/padApi/getTaskStatus`

**Signature**

```python
client.tasks.get_task_status(task_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | String | yes | Task ID |

**Example** (JSON payload)

```json
{
    "taskId": "TASK-278784482960609280"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `pad_task_detail` — Instance Operation Task Details

Query detailed execution results for specified instance operation task.

- **Endpoint**: `POST /vcpcloud/api/padApi/padTaskDetail`

**Signature**

```python
client.tasks.pad_task_detail(task_ids, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | yes |  |

**Nested fields of `taskIds`:**

| API name | Type | Description |
|---|---|---|
| `taskId` | Integer | Task ID |

**Example** (JSON payload)

```json
{
 "taskIds":[1,2]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `pad_execute_task_info` — Instance Restart/Reset Execution Result

Get instance restart/reset execution result via task ID.

- **Endpoint**: `POST /vcpcloud/api/padApi/padExecuteTaskInfo`

**Signature**

```python
client.tasks.pad_execute_task_info(task_ids, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | yes |  |

**Nested fields of `taskIds`:**

| API name | Type | Description |
|---|---|---|
| `` | Integer | Task ID |

**Example** (JSON payload)

```json
{
    "taskIds": [1]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `file_task_detail` — File Task Details

Query the detailed execution result of a specified file task.

- **Endpoint**: `POST /vcpcloud/api/padApi/fileTaskDetail`

**Signature**

```python
client.tasks.file_task_detail(task_ids, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | yes | List of task IDs |

**Nested fields of `taskIds`:**

| API name | Type | Description |
|---|---|---|
| `taskId` | Integer | Task ID |

**Example** (JSON payload)

```json
{
	"taskIds":[
		1,2
	]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
