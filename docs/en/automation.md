# `client.automation` — Flow Automation (RPA)

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

RPA flow scripts, task dispatch & scheduling, account matrix, webview, unmanned live.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`scripts_list`](#scripts-list--flow-script-list) | POST | `/vcpcloud/api/padApi/automation/scripts/list` |
| [`scripts_get`](#scripts-get--flow-script-details) | POST | `/vcpcloud/api/padApi/automation/scripts/get` |
| [`tasks_batch_dispatch`](#tasks-batch-dispatch--batch-dispatch-flow-task) | POST | `/vcpcloud/api/padApi/automation/tasks/batch-dispatch` |
| [`tasks_list`](#tasks-list--flow-task-list) | POST | `/vcpcloud/api/padApi/automation/tasks/list` |
| [`tasks_get`](#tasks-get--flow-task-details) | POST | `/vcpcloud/api/padApi/automation/tasks/get` |
| [`tasks_logs`](#tasks-logs--flow-task-logs) | POST | `/vcpcloud/api/padApi/automation/tasks/logs` |
| [`tasks_cancel`](#tasks-cancel--cancel-flow-task) | POST | `/vcpcloud/api/padApi/automation/tasks/cancel` |
| [`accounts_list`](#accounts-list--account-list) | POST | `/vcpcloud/api/padApi/automation/accounts/list` |
| [`accounts_get`](#accounts-get--account-details) | POST | `/vcpcloud/api/padApi/automation/accounts/get` |
| [`accounts_snapshots`](#accounts-snapshots--account-data-snapshots) | POST | `/vcpcloud/api/padApi/automation/accounts/snapshots` |
| [`accounts_works`](#accounts-works--account-works-list) | POST | `/vcpcloud/api/padApi/automation/accounts/works` |
| [`accounts_work_snapshots`](#accounts-work-snapshots--account-work-data-snapshots) | POST | `/vcpcloud/api/padApi/automation/accounts/work-snapshots` |
| [`accounts_groups_list`](#accounts-groups-list--account-group-list) | POST | `/vcpcloud/api/padApi/automation/accounts/groups/list` |
| [`accounts_operations_batch`](#accounts-operations-batch--batch-trigger-account-operation) | POST | `/vcpcloud/api/padApi/automation/accounts/operations/batch` |
| [`accounts_scheduled_tasks_batch`](#accounts-scheduled-tasks-batch--account-batch-scheduled-tasks) | POST | `/vcpcloud/api/padApi/automation/accounts/scheduled-tasks/batch` |
| [`accounts_create`](#accounts-create--create-account) | POST | `/vcpcloud/api/padApi/automation/accounts/create` |
| [`accounts_bind`](#accounts-bind--bind-instance) | POST | `/vcpcloud/api/padApi/automation/accounts/bind` |
| [`accounts_unbind`](#accounts-unbind--unbind-instance) | POST | `/vcpcloud/api/padApi/automation/accounts/unbind` |
| [`accounts_delete`](#accounts-delete--delete-account) | POST | `/vcpcloud/api/padApi/automation/accounts/delete` |
| [`accounts_group`](#accounts-group--move-account-group) | POST | `/vcpcloud/api/padApi/automation/accounts/group` |
| [`scheduled_tasks_list`](#scheduled-tasks-list--scheduled-task-list) | POST | `/vcpcloud/api/padApi/automation/scheduled-tasks/list` |
| [`scheduled_tasks_create`](#scheduled-tasks-create--create-scheduled-task) | POST | `/vcpcloud/api/padApi/automation/scheduled-tasks/create` |
| [`scheduled_tasks_update`](#scheduled-tasks-update--update-scheduled-task) | POST | `/vcpcloud/api/padApi/automation/scheduled-tasks/update` |
| [`scheduled_tasks_toggle`](#scheduled-tasks-toggle--toggle-scheduled-task) | POST | `/vcpcloud/api/padApi/automation/scheduled-tasks/toggle` |
| [`scheduled_tasks_delete`](#scheduled-tasks-delete--delete-scheduled-task) | POST | `/vcpcloud/api/padApi/automation/scheduled-tasks/delete` |

[Back to index](README.md)

---

### `scripts_list` — Flow Script List

Paginate the flow scripts visible to the current account (official + your private scripts).

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scripts/list`

**Signature**

```python
client.automation.scripts_list(*, page=None, size=None, category=None, platform=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Page number, defaults to 1, min 1 |
| `size` | `size` | Integer | no | Page size, defaults to 20, range 1~100 |
| `category` | `category` | String | no | Filter by ownership type: `official` (platform-provided template) or `user` (your private script) |
| `platform` | `platform` | String | no | Filter by business platform, e.g. `instagram` / `tiktok` / `youtube` (set on `official` templates; may be null on user scripts) |

**Example** (JSON payload)

```json
{
  "page": 1,
  "size": 20,
  "category": "official",
  "platform": "tiktok"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `scripts_get` — Flow Script Details

Fetch a single flow script by `scriptId`.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scripts/get`

**Signature**

```python
client.automation.scripts_get(script_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `script_id` | `scriptId` | Long | yes | Script ID |

**Example** (JSON payload)

```json
{
  "scriptId": 1024
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `tasks_batch_dispatch` — Batch Dispatch Flow Task

Dispatch one script to multiple cloud instances in one call. Single-call limit is **200 devices**. Two mutually-exclusive modes: * **Mode A (shared params)**: `padCodes` lists the targets, all sharing the same `params` * **Mode B (per-device params)**: `items` is an array of `{padCode, params}` pairs Exactly one of `padCodes` / `items` must be non-empty; supplying both or neither fails parameter validation.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/tasks/batch-dispatch`

**Signature**

```python
client.automation.tasks_batch_dispatch(script_id, *, pad_codes=None, params=None, items=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `script_id` | `scriptId` | Long | yes | Script ID to execute |
| `pad_codes` | `padCodes` | String[] | no | **Mode A**: target devices, max 200, non-blank |
| `params` | `params` | String | no | **Mode A** shared params (JSON string); ignored in Mode B |
| `items` | `items` | Object[] | no | **Mode B**: per-device params, max 200 |

**Nested fields of `items`:**

| API name | Type | Description |
|---|---|---|
| `padCode` | String | Target device ID |
| `params` | String | Per-device params (JSON string) |

**Example** (JSON payload)

```json
{
  "scriptId": 1024,
  "padCodes": ["AC2025030770R92X", "AC2025030770R93Y"],
  "params": "{\"keyword\":\"summer sale\"}"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `tasks_list` — Flow Task List

Paginate the current account's flow tasks, ordered by `createdAt` desc. Supports time-range filtering.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/tasks/list`

**Signature**

```python
client.automation.tasks_list(*, page=None, size=None, start_time=None, end_time=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Page number, defaults to 1 |
| `size` | `size` | Integer | no | Page size, defaults to 20, range 1~100 |
| `start_time` | `startTime` | String | no | Start time (ISO-8601 UTC string); malformed values ignored |
| `end_time` | `endTime` | String | no | End time (ISO-8601 UTC string); malformed values ignored |

**Example** (JSON payload)

```json
{
  "page": 1,
  "size": 20,
  "startTime": "2026-05-25T00:00:00Z",
  "endTime": "2026-05-26T00:00:00Z"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `tasks_get` — Flow Task Details

Fetch a single flow task by `taskId`.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/tasks/get`

**Signature**

```python
client.automation.tasks_get(task_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Long | yes | Real task primary key (the `id` returned by dispatch — **not**`displayId`) |

**Example** (JSON payload)

```json
{
  "taskId": 30215
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `tasks_logs` — Flow Task Logs

Fetch step-level execution logs for a task (ascending by timestamp).

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/tasks/logs`

**Signature**

```python
client.automation.tasks_logs(task_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Long | yes | Task primary key |

**Example** (JSON payload)

```json
{
  "taskId": 30215
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `tasks_cancel` — Cancel Flow Task

Cancel a task. Semantics (**best-effort**): * `pending`: set to `cancelled` immediately, no device contact * `dispatched` / `running` / `cancel_requested`: set to `cancel_requested` and the device is notified to abort; the device transitions the task to a terminal state once it acknowledges * Already terminal (`success` / `failed` / `cancelled`): no-op, returns success idempotently

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/tasks/cancel`

**Signature**

```python
client.automation.tasks_cancel(task_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Long | yes | Task primary key |

**Example** (JSON payload)

```json
{
  "taskId": 30215
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_list` — Account List

Paginate the current user's accounts; supports platform / group / status / keyword / bind-status filtering and sorting.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/list`

**Signature**

```python
client.automation.accounts_list(*, page=None, size=None, platform=None, group_id=None, status=None, keyword=None, device_bound=None, sort_by=None, sort_dir=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Page number, default 1, min 1 |
| `size` | `size` | Integer | no | Page size, default 20, range 1–100 |
| `platform` | `platform` | String | no | Platform filter, e.g. `instagram` / `tiktok` / `youtube` |
| `group_id` | `groupId` | Long | no | Account group ID filter |
| `status` | `status` | String | no | Account status filter (login health): `inactive` (new, not logged in) / `active` (login OK) / `login_failed`; use deviceBound to filter by binding |
| `keyword` | `keyword` | String | no | Keyword, matches handle / display name |
| `device_bound` | `deviceBound` | Boolean | no | Bind status: `true` = bound only, `false` = unbound only, omit = no filter |
| `sort_by` | `sortBy` | String | no | Sort field: `createdAt` / `lastActiveAt` / `cachedFollowers`, etc. |
| `sort_dir` | `sortDir` | String | no | Sort direction: `asc` / `desc` |

**Example** (JSON payload)

```json
{
  "page": 1,
  "size": 20,
  "platform": "instagram",
  "status": "active",
  "deviceBound": true,
  "sortBy": "createdAt",
  "sortDir": "desc"
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_get` — Account Details

Fetch a single account by `accountId`. Returns the same fields as a `list` element of [Account List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#account-list).

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/get`

**Signature**

```python
client.automation.accounts_get(account_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |

**Example** (JSON payload)

```json
{
  "accountId": 22
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_snapshots` — Account Data Snapshots

Query account-level historical snapshots by `accountId` (followers / following / works count / likes time series), returned in descending order of collection time.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/snapshots`

**Signature**

```python
client.automation.accounts_snapshots(account_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |

**Example** (JSON payload)

```json
{
  "accountId": 22
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_works` — Account Works List

Paginate the account's collected works (deduplicated by `platformWorkId`). Each work carries the most recently collected metric snapshot.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/works`

**Signature**

```python
client.automation.accounts_works(account_id, *, page=None, size=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |
| `page` | `page` | Integer | no | Page number, default 1, min 1 |
| `size` | `size` | Integer | no | Page size, default 20, range 1–100 |

**Example** (JSON payload)

```json
{
  "accountId": 22,
  "page": 1,
  "size": 20
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_work_snapshots` — Account Work Data Snapshots

Query a single work's metric time series (one record per collection) by `accountId` + `workId`, returned in descending order of collection time. `accountId` is used for ownership validation.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/work-snapshots`

**Signature**

```python
client.automation.accounts_work_snapshots(account_id, work_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID (ownership validation) |
| `work_id` | `workId` | Long | yes | Work record ID |

**Example** (JSON payload)

```json
{
  "accountId": 22,
  "workId": 9001
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_groups_list` — Account Group List

List all account groups of the current user, returned in ascending order of `sortOrder`.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/groups/list`

**Signature**

```python
client.automation.accounts_groups_list(**extra)
```

This endpoint takes no parameters (besides optional `**extra`).

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_operations_batch` — Batch Trigger Account Operation

Batch-trigger a template to run **immediately** on multiple accounts. Each account's target instance is derived from its currently bound instance (no `padCode`); credentials are decrypted and injected server-side via `fromCredential` (never sent to or readable by the client). One request creates and concurrently dispatches multiple tasks; the task record structure matches [Batch Dispatch Flow Task](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#batch-dispatch-flow-task).

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/operations/batch`

**Signature**

```python
client.automation.accounts_operations_batch(script_id, account_ids, *, task_name=None, shared_options=None, per_account_options=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `script_id` | `scriptId` | Long | yes | Template ID to run |
| `account_ids` | `accountIds` | Long[] | yes | Target account IDs |
| `task_name` | `taskName` | String | no | Plan name (shown in the task list) |
| `shared_options` | `sharedOptions` | Object[] | no | Shared params: same set for all accounts |
| `per_account_options` | `perAccountOptions` | Object | no | Per-account params: accountId → option list |

**Example** (JSON payload)

```json
{
  "scriptId": 1024,
  "accountIds": [22, 17],
  "taskName": "Instagram batch",
  "sharedOptions": [
    { "key": "keyword", "value": "travel" },
    { "key": "account", "fromCredential": "username" },
    { "key": "password", "fromCredential": "password" }
  ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_scheduled_tasks_batch` — Account Batch Scheduled Tasks

Batch-create **scheduled** tasks for multiple accounts: one scheduled task per account, fired on a Cron schedule. At fire time the server resolves each account's current bound instance and decrypts/injects credentials (the stored params contain no plaintext, only the `fromCredential` mapping).

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/scheduled-tasks/batch`

**Signature**

```python
client.automation.accounts_scheduled_tasks_batch(script_id, account_ids, cron_expr, *, one_shot=None, enabled=None, task_name=None, shared_options=None, per_account_options=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `script_id` | `scriptId` | Long | yes | Template ID |
| `account_ids` | `accountIds` | Long[] | yes | Target account IDs |
| `cron_expr` | `cronExpr` | String | yes | Cron expression (6 fields, includes seconds); a one-shot task also uses it for its single trigger moment |
| `one_shot` | `oneShot` | Boolean | no | One-shot task (auto-disabled after firing), default false |
| `enabled` | `enabled` | Boolean | no | Enable immediately after creation, default true |
| `task_name` | `taskName` | String | no | Plan name |
| `shared_options` | `sharedOptions` | Object[] | no | Shared params; option item matches [Batch Trigger Account Operation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#batch-trigger-account-operation) |
| `per_account_options` | `perAccountOptions` | Object | no | Per-account params: accountId → option list |

**Example** (JSON payload)

```json
{
  "scriptId": 1024,
  "accountIds": [22, 17],
  "cronExpr": "0 0 9 * * *",
  "oneShot": false,
  "taskName": "Daily collect",
  "sharedOptions": [
    { "key": "account", "fromCredential": "username" },
    { "key": "password", "fromCredential": "password" }
  ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_create` — Create Account

Create an account in the matrix (credentials are AES-GCM encrypted at rest). `handle` is unique per platform.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/create`

**Signature**

```python
client.automation.accounts_create(platform, username, password, *, handle=None, twofa_secret=None, email=None, email_password=None, group_id=None, country=None, note=None, tags=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `platform` | `platform` | String | yes | Platform |
| `username` | `username` | String | yes | Login username (credential, stored encrypted) |
| `password` | `password` | String | yes | Login password (credential, stored encrypted) |
| `handle` | `handle` | String | no | Account @handle (unique per platform, may be empty) |
| `twofa_secret` | `twofaSecret` | String | no | 2FA secret (credential) |
| `email` | `email` | String | no | Email (credential) |
| `email_password` | `emailPassword` | String | no | Email password (credential) |
| `group_id` | `groupId` | Long | no | Group ID |
| `country` | `country` | String | no | Country/region |
| `note` | `note` | String | no | Note |
| `tags` | `tags` | String | no | Tags (comma-separated) |

**Example** (JSON payload)

```json
{
  "platform": "instagram",
  "username": "alice_ig",
  "password": "secret",
  "handle": "alice_ig",
  "groupId": 12
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_bind` — Bind Instance

Bind an account to a cloud instance. **Only one active account per instance+platform**; on conflict `force=false` returns 409, `force=true` rebinds (the old account is auto-unbound). padCode ownership is pre-checked at the gateway.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/bind`

**Signature**

```python
client.automation.accounts_bind(account_id, pad_code, *, force=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |
| `pad_code` | `padCode` | String | yes | Target instance code |
| `force` | `force` | Boolean | no | Force rebind on conflict, default false |

**Example** (JSON payload)

```json
{ "accountId": 22, "padCode": "AC2025030770R92X", "force": false }
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_unbind` — Unbind Instance

Unbind an account from its currently bound instance.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/unbind`

**Signature**

```python
client.automation.accounts_unbind(account_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_delete` — Delete Account

Soft-delete an account; credentials are cleared (recoverable by admin, but credentials must be re-entered).

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/delete`

**Signature**

```python
client.automation.accounts_delete(account_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `accounts_group` — Move Account Group

Move an account to a group; pass `null``groupId` to ungroup.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/accounts/group`

**Signature**

```python
client.automation.accounts_group(account_id, *, group_id=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | `accountId` | Long | yes | Account ID |
| `group_id` | `groupId` | Long | no | Target group ID; null = ungroup |

**Example** (JSON payload)

```json
{ "accountId": 22, "groupId": 12 }
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `scheduled_tasks_list` — Scheduled Task List

Paginate the current user's scheduled tasks.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scheduled-tasks/list`

**Signature**

```python
client.automation.scheduled_tasks_list(*, page=None, size=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `page` | `page` | Integer | no | Page number, default 1, min 1 |
| `size` | `size` | Integer | no | Page size, default 20, range 1–100 |

**Example** (JSON payload)

```json
{
  "page": 1,
  "size": 20
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `scheduled_tasks_create` — Create Scheduled Task

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scheduled-tasks/create`

**Signature**

```python
client.automation.scheduled_tasks_create(task_name, script_id, pad_codes, *, cron_expr=None, one_shot=None, params=None, enabled=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_name` | `taskName` | String | yes | Schedule name |
| `script_id` | `scriptId` | Long | yes | Template ID to run |
| `pad_codes` | `padCodes` | String[] | yes | Target instance codes; one scheduled task is created per instance |
| `cron_expr` | `cronExpr` | String | no | Cron expression (6 fields); required for recurring tasks, optional for one-shot |
| `one_shot` | `oneShot` | Boolean | no | Whether it is a one-shot task, default false |
| `params` | `params` | String | no | Template runtime params, a **JSON string**; invalid JSON is rejected |
| `enabled` | `enabled` | Boolean | no | Whether to enable immediately after creation, default true |

**Example** (JSON payload)

```json
{
  "taskName": "InstagramAutoCollect20260531",
  "scriptId": 1024,
  "padCodes": ["AC2025030770R92X"],
  "cronExpr": "0 0 9 * * *",
  "oneShot": false,
  "params": "{\"keyword\":\"travel\"}",
  "enabled": true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `scheduled_tasks_update` — Update Scheduled Task

Update a single scheduled task. **One scheduled task maps to a single instance**, so the singular `padCode` is used; to change to multiple devices, delete and recreate.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scheduled-tasks/update`

**Signature**

```python
client.automation.scheduled_tasks_update(task_id, task_name, script_id, pad_code, *, cron_expr=None, one_shot=None, params=None, enabled=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Long | yes | Scheduled task ID |
| `task_name` | `taskName` | String | yes | Schedule name |
| `script_id` | `scriptId` | Long | yes | Template ID |
| `pad_code` | `padCode` | String | yes | Target instance code (single) |
| `cron_expr` | `cronExpr` | String | no | Cron expression (6 fields) |
| `one_shot` | `oneShot` | Boolean | no | Whether it is a one-shot task |
| `params` | `params` | String | no | Template runtime params, a **JSON string** |
| `enabled` | `enabled` | Boolean | no | Whether enabled |

**Example** (JSON payload)

```json
{
  "taskId": 501,
  "taskName": "InstagramAutoCollect(edited)",
  "scriptId": 1024,
  "padCode": "AC2025030770R92X",
  "cronExpr": "0 30 9 * * *",
  "oneShot": false,
  "params": "{\"keyword\":\"food\"}",
  "enabled": true
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `scheduled_tasks_toggle` — Toggle Scheduled Task

Enable / disable a scheduled task. When disabled the scheduler no longer triggers it; enabling restores triggering.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scheduled-tasks/toggle`

**Signature**

```python
client.automation.scheduled_tasks_toggle(task_id, enabled, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Long | yes | Scheduled task ID |
| `enabled` | `enabled` | Boolean | yes | true = enable / false = disable |

**Example** (JSON payload)

```json
{
  "taskId": 501,
  "enabled": false
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `scheduled_tasks_delete` — Delete Scheduled Task

Delete a scheduled task.

- **Endpoint**: `POST /vcpcloud/api/padApi/automation/scheduled-tasks/delete`

**Signature**

```python
client.automation.scheduled_tasks_delete(task_id, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `task_id` | `taskId` | Long | yes | Scheduled task ID |

**Example** (JSON payload)

```json
{
  "taskId": 501
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
