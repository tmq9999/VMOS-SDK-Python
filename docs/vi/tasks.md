# `client.tasks` — Quản lý tác vụ

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Truy vấn trạng thái & chi tiết các tác vụ bất đồng bộ (thao tác instance, đẩy file).

## Danh sách phương thức

| Python | HTTP | Endpoint |
|---|---|---|
| [`get_task_status`](#get-task-status--device-task-execution-result-query) | POST | `/vcpcloud/api/padApi/getTaskStatus` |
| [`pad_task_detail`](#pad-task-detail--instance-operation-task-details) | POST | `/vcpcloud/api/padApi/padTaskDetail` |
| [`pad_execute_task_info`](#pad-execute-task-info--instance-restart-reset-execution-result) | POST | `/vcpcloud/api/padApi/padExecuteTaskInfo` |
| [`file_task_detail`](#file-task-detail--file-task-details) | POST | `/vcpcloud/api/padApi/fileTaskDetail` |

[Về trang chính](README.md)

---

### `get_task_status` — Device Task Execution Result Query

Query task execution result using task number (for smart IP).

- **Endpoint**: `POST /vcpcloud/api/padApi/getTaskStatus`

**Chữ ký hàm**

```python
client.tasks.get_task_status(task_id, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `task_id` | `taskId` | String | có | Task ID |

**Ví dụ** (JSON payload)

```json
{
    "taskId": "TASK-278784482960609280"
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `pad_task_detail` — Instance Operation Task Details

Query detailed execution results for specified instance operation task.

- **Endpoint**: `POST /vcpcloud/api/padApi/padTaskDetail`

**Chữ ký hàm**

```python
client.tasks.pad_task_detail(task_ids, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | có |  |

**Các trường con của `taskIds`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `taskId` | Integer | Task ID |

**Ví dụ** (JSON payload)

```json
{
 "taskIds":[1,2]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `pad_execute_task_info` — Instance Restart/Reset Execution Result

Get instance restart/reset execution result via task ID.

- **Endpoint**: `POST /vcpcloud/api/padApi/padExecuteTaskInfo`

**Chữ ký hàm**

```python
client.tasks.pad_execute_task_info(task_ids, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | có |  |

**Các trường con của `taskIds`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `` | Integer | Task ID |

**Ví dụ** (JSON payload)

```json
{
    "taskIds": [1]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---

### `file_task_detail` — File Task Details

Query the detailed execution result of a specified file task.

- **Endpoint**: `POST /vcpcloud/api/padApi/fileTaskDetail`

**Chữ ký hàm**

```python
client.tasks.file_task_detail(task_ids, **extra)
```

**Tham số**

| Tham số Python | Tên trong API | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `task_ids` | `taskIds` | Integer[] | có | List of task IDs |

**Các trường con của `taskIds`:**

| Tên trong API | Kiểu | Mô tả |
|---|---|---|
| `taskId` | Integer | Task ID |

**Ví dụ** (JSON payload)

```json
{
	"taskIds":[
		1,2
	]
}
```

**Trả về**: trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).

---
