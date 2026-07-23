"""Flow Automation (RPA): flow script templates, task dispatch/scheduling, account matrix operations, webview and unmanned live streaming.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["AutomationAPI", "AsyncAutomationAPI"]


class AutomationAPI(SyncAPIResource):
    """Flow Automation (RPA): flow script templates, task dispatch/scheduling, account matrix operations, webview and unmanned live streaming."""

    def scripts_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        category: Optional[str] = None,
        platform: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Flow Script List.

        Paginate the flow scripts visible to the current account (official + your private scripts).

        ``POST /vcpcloud/api/padApi/automation/scripts/list``

        Args:
            page: Page number, defaults to 1, min 1 (API: ``page``)
            size: Page size, defaults to 20, range 1~100 (API: ``size``)
            category: Filter by ownership type: `official` (platform-provided template) or `user` (your private script) (API: ``category``)
            platform: Filter by business platform, e.g. `instagram` / `tiktok` / `youtube` (set on `official` templates; may be null on user scripts) (API: ``platform``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "category": category, "platform": platform}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scripts/list", json_body=payload)

    def scripts_get(
        self,
        script_id: int,
        **extra: Any,
    ) -> Any:
        """Flow Script Details.

        Fetch a single flow script by `scriptId`.

        ``POST /vcpcloud/api/padApi/automation/scripts/get``

        Args:
            script_id: Script ID (API: ``scriptId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scripts/get", json_body=payload)

    def tasks_batch_dispatch(
        self,
        script_id: int,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        params: Optional[str] = None,
        items: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Batch Dispatch Flow Task.

        Dispatch one script to multiple cloud instances in one call. Single-call limit is **200 devices**. Two mutually-exclusive modes: * **Mode A (shared params)**: `padCodes` lists the targets, all sharing the same `params` * **Mode B (per-device params)**: `items` is an array of `{padCode, params}` pairs Exactly one of `padCodes` / `items` must be non-empty; supplying both or neither fails parameter validation.

        ``POST /vcpcloud/api/padApi/automation/tasks/batch-dispatch``

        Args:
            script_id: Script ID to execute (API: ``scriptId``, required)
            pad_codes: **Mode A**: target devices, max 200, non-blank (API: ``padCodes``)
            params: **Mode A** shared params (JSON string); ignored in Mode B (API: ``params``)
            items: **Mode B**: per-device params, max 200 (API: ``items``) Nested fields: ``padCode``, ``params``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id, "padCodes": pad_codes, "params": params, "items": items}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/batch-dispatch", json_body=payload)

    def tasks_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Flow Task List.

        Paginate the current account's flow tasks, ordered by `createdAt` desc. Supports time-range filtering.

        ``POST /vcpcloud/api/padApi/automation/tasks/list``

        Args:
            page: Page number, defaults to 1 (API: ``page``)
            size: Page size, defaults to 20, range 1~100 (API: ``size``)
            start_time: Start time (ISO-8601 UTC string); malformed values ignored (API: ``startTime``)
            end_time: End time (ISO-8601 UTC string); malformed values ignored (API: ``endTime``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "startTime": start_time, "endTime": end_time}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/list", json_body=payload)

    def tasks_get(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Flow Task Details.

        Fetch a single flow task by `taskId`.

        ``POST /vcpcloud/api/padApi/automation/tasks/get``

        Args:
            task_id: Real task primary key (the `id` returned by dispatch — **not**`displayId`) (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/get", json_body=payload)

    def tasks_logs(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Flow Task Logs.

        Fetch step-level execution logs for a task (ascending by timestamp).

        ``POST /vcpcloud/api/padApi/automation/tasks/logs``

        Args:
            task_id: Task primary key (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/logs", json_body=payload)

    def tasks_cancel(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Cancel Flow Task.

        Cancel a task. Semantics (**best-effort**): * `pending`: set to `cancelled` immediately, no device contact * `dispatched` / `running` / `cancel_requested`: set to `cancel_requested` and the device is notified to abort; the device transitions the task to a terminal state once it acknowledges * Already terminal (`success` / `failed` / `cancelled`): no-op, returns success idempotently

        ``POST /vcpcloud/api/padApi/automation/tasks/cancel``

        Args:
            task_id: Task primary key (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/cancel", json_body=payload)

    def accounts_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        platform: Optional[str] = None,
        group_id: Optional[int] = None,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        device_bound: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Account List.

        Paginate the current user's accounts; supports platform / group / status / keyword / bind-status filtering and sorting.

        ``POST /vcpcloud/api/padApi/automation/accounts/list``

        Args:
            page: Page number, default 1, min 1 (API: ``page``)
            size: Page size, default 20, range 1–100 (API: ``size``)
            platform: Platform filter, e.g. `instagram` / `tiktok` / `youtube` (API: ``platform``)
            group_id: Account group ID filter (API: ``groupId``)
            status: Account status filter (login health): `inactive` (new, not logged in) / `active` (login OK) / `login_failed`; use deviceBound to filter by binding (API: ``status``)
            keyword: Keyword, matches handle / display name (API: ``keyword``)
            device_bound: Bind status: `true` = bound only, `false` = unbound only, omit = no filter (API: ``deviceBound``)
            sort_by: Sort field: `createdAt` / `lastActiveAt` / `cachedFollowers`, etc. (API: ``sortBy``)
            sort_dir: Sort direction: `asc` / `desc` (API: ``sortDir``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "platform": platform, "groupId": group_id, "status": status, "keyword": keyword, "deviceBound": device_bound, "sortBy": sort_by, "sortDir": sort_dir}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/list", json_body=payload)

    def accounts_get(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Account Details.

        Fetch a single account by `accountId`. Returns the same fields as a `list` element of [Account List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#account-list).

        ``POST /vcpcloud/api/padApi/automation/accounts/get``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/get", json_body=payload)

    def accounts_snapshots(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Account Data Snapshots.

        Query account-level historical snapshots by `accountId` (followers / following / works count / likes time series), returned in descending order of collection time.

        ``POST /vcpcloud/api/padApi/automation/accounts/snapshots``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/snapshots", json_body=payload)

    def accounts_works(
        self,
        account_id: int,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Account Works List.

        Paginate the account's collected works (deduplicated by `platformWorkId`). Each work carries the most recently collected metric snapshot.

        ``POST /vcpcloud/api/padApi/automation/accounts/works``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            page: Page number, default 1, min 1 (API: ``page``)
            size: Page size, default 20, range 1–100 (API: ``size``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "page": page, "size": size}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/works", json_body=payload)

    def accounts_work_snapshots(
        self,
        account_id: int,
        work_id: int,
        **extra: Any,
    ) -> Any:
        """Account Work Data Snapshots.

        Query a single work's metric time series (one record per collection) by `accountId` + `workId`, returned in descending order of collection time. `accountId` is used for ownership validation.

        ``POST /vcpcloud/api/padApi/automation/accounts/work-snapshots``

        Args:
            account_id: Account ID (ownership validation) (API: ``accountId``, required)
            work_id: Work record ID (API: ``workId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "workId": work_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/work-snapshots", json_body=payload)

    def accounts_groups_list(
        self,
        **extra: Any,
    ) -> Any:
        """Account Group List.

        List all account groups of the current user, returned in ascending order of `sortOrder`.

        ``POST /vcpcloud/api/padApi/automation/accounts/groups/list``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/groups/list", json_body=payload)

    def accounts_operations_batch(
        self,
        script_id: int,
        account_ids: Sequence[Any],
        *,
        task_name: Optional[str] = None,
        shared_options: Optional[Sequence[Mapping[str, Any]]] = None,
        per_account_options: Optional[Mapping[str, Any]] = None,
        **extra: Any,
    ) -> Any:
        """Batch Trigger Account Operation.

        Batch-trigger a template to run **immediately** on multiple accounts. Each account's target instance is derived from its currently bound instance (no `padCode`); credentials are decrypted and injected server-side via `fromCredential` (never sent to or readable by the client). One request creates and concurrently dispatches multiple tasks; the task record structure matches [Batch Dispatch Flow Task](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#batch-dispatch-flow-task).

        ``POST /vcpcloud/api/padApi/automation/accounts/operations/batch``

        Args:
            script_id: Template ID to run (API: ``scriptId``, required)
            account_ids: Target account IDs (API: ``accountIds``, required)
            task_name: Plan name (shown in the task list) (API: ``taskName``)
            shared_options: Shared params: same set for all accounts (API: ``sharedOptions``)
            per_account_options: Per-account params: accountId → option list (API: ``perAccountOptions``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id, "accountIds": account_ids, "taskName": task_name, "sharedOptions": shared_options, "perAccountOptions": per_account_options}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/operations/batch", json_body=payload)

    def accounts_scheduled_tasks_batch(
        self,
        script_id: int,
        account_ids: Sequence[Any],
        cron_expr: str,
        *,
        one_shot: Optional[bool] = None,
        enabled: Optional[bool] = None,
        task_name: Optional[str] = None,
        shared_options: Optional[Sequence[Mapping[str, Any]]] = None,
        per_account_options: Optional[Mapping[str, Any]] = None,
        **extra: Any,
    ) -> Any:
        """Account Batch Scheduled Tasks.

        Batch-create **scheduled** tasks for multiple accounts: one scheduled task per account, fired on a Cron schedule. At fire time the server resolves each account's current bound instance and decrypts/injects credentials (the stored params contain no plaintext, only the `fromCredential` mapping).

        ``POST /vcpcloud/api/padApi/automation/accounts/scheduled-tasks/batch``

        Args:
            script_id: Template ID (API: ``scriptId``, required)
            account_ids: Target account IDs (API: ``accountIds``, required)
            cron_expr: Cron expression (6 fields, includes seconds); a one-shot task also uses it for its single trigger moment (API: ``cronExpr``, required)
            one_shot: One-shot task (auto-disabled after firing), default false (API: ``oneShot``)
            enabled: Enable immediately after creation, default true (API: ``enabled``)
            task_name: Plan name (API: ``taskName``)
            shared_options: Shared params; option item matches [Batch Trigger Account Operation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#batch-trigger-account-operation) (API: ``sharedOptions``)
            per_account_options: Per-account params: accountId → option list (API: ``perAccountOptions``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id, "accountIds": account_ids, "cronExpr": cron_expr, "oneShot": one_shot, "enabled": enabled, "taskName": task_name, "sharedOptions": shared_options, "perAccountOptions": per_account_options}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/scheduled-tasks/batch", json_body=payload)

    def accounts_create(
        self,
        platform: str,
        username: str,
        password: str,
        *,
        handle: Optional[str] = None,
        twofa_secret: Optional[str] = None,
        email: Optional[str] = None,
        email_password: Optional[str] = None,
        group_id: Optional[int] = None,
        country: Optional[str] = None,
        note: Optional[str] = None,
        tags: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Create Account.

        Create an account in the matrix (credentials are AES-GCM encrypted at rest). `handle` is unique per platform.

        ``POST /vcpcloud/api/padApi/automation/accounts/create``

        Args:
            platform: Platform (API: ``platform``, required)
            username: Login username (credential, stored encrypted) (API: ``username``, required)
            password: Login password (credential, stored encrypted) (API: ``password``, required)
            handle: Account @handle (unique per platform, may be empty) (API: ``handle``)
            twofa_secret: 2FA secret (credential) (API: ``twofaSecret``)
            email: Email (credential) (API: ``email``)
            email_password: Email password (credential) (API: ``emailPassword``)
            group_id: Group ID (API: ``groupId``)
            country: Country/region (API: ``country``)
            note: Note (API: ``note``)
            tags: Tags (comma-separated) (API: ``tags``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"platform": platform, "username": username, "password": password, "handle": handle, "twofaSecret": twofa_secret, "email": email, "emailPassword": email_password, "groupId": group_id, "country": country, "note": note, "tags": tags}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/create", json_body=payload)

    def accounts_bind(
        self,
        account_id: int,
        pad_code: str,
        *,
        force: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Bind Instance.

        Bind an account to a cloud instance. **Only one active account per instance+platform**; on conflict `force=false` returns 409, `force=true` rebinds (the old account is auto-unbound). padCode ownership is pre-checked at the gateway.

        ``POST /vcpcloud/api/padApi/automation/accounts/bind``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            pad_code: Target instance code (API: ``padCode``, required)
            force: Force rebind on conflict, default false (API: ``force``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "padCode": pad_code, "force": force}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/bind", json_body=payload)

    def accounts_unbind(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Unbind Instance.

        Unbind an account from its currently bound instance.

        ``POST /vcpcloud/api/padApi/automation/accounts/unbind``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/unbind", json_body=payload)

    def accounts_delete(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Delete Account.

        Soft-delete an account; credentials are cleared (recoverable by admin, but credentials must be re-entered).

        ``POST /vcpcloud/api/padApi/automation/accounts/delete``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/delete", json_body=payload)

    def accounts_group(
        self,
        account_id: int,
        *,
        group_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Move Account Group.

        Move an account to a group; pass `null``groupId` to ungroup.

        ``POST /vcpcloud/api/padApi/automation/accounts/group``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            group_id: Target group ID; null = ungroup (API: ``groupId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "groupId": group_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/group", json_body=payload)

    def scheduled_tasks_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Scheduled Task List.

        Paginate the current user's scheduled tasks.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/list``

        Args:
            page: Page number, default 1, min 1 (API: ``page``)
            size: Page size, default 20, range 1–100 (API: ``size``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/list", json_body=payload)

    def scheduled_tasks_create(
        self,
        task_name: str,
        script_id: int,
        pad_codes: Sequence[str],
        *,
        cron_expr: Optional[str] = None,
        one_shot: Optional[bool] = None,
        params: Optional[str] = None,
        enabled: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Create Scheduled Task.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/create``

        Args:
            task_name: Schedule name (API: ``taskName``, required)
            script_id: Template ID to run (API: ``scriptId``, required)
            pad_codes: Target instance codes; one scheduled task is created per instance (API: ``padCodes``, required)
            cron_expr: Cron expression (6 fields); required for recurring tasks, optional for one-shot (API: ``cronExpr``)
            one_shot: Whether it is a one-shot task, default false (API: ``oneShot``)
            params: Template runtime params, a **JSON string**; invalid JSON is rejected (API: ``params``)
            enabled: Whether to enable immediately after creation, default true (API: ``enabled``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskName": task_name, "scriptId": script_id, "padCodes": pad_codes, "cronExpr": cron_expr, "oneShot": one_shot, "params": params, "enabled": enabled}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/create", json_body=payload)

    def scheduled_tasks_update(
        self,
        task_id: int,
        task_name: str,
        script_id: int,
        pad_code: str,
        *,
        cron_expr: Optional[str] = None,
        one_shot: Optional[bool] = None,
        params: Optional[str] = None,
        enabled: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Update Scheduled Task.

        Update a single scheduled task. **One scheduled task maps to a single instance**, so the singular `padCode` is used; to change to multiple devices, delete and recreate.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/update``

        Args:
            task_id: Scheduled task ID (API: ``taskId``, required)
            task_name: Schedule name (API: ``taskName``, required)
            script_id: Template ID (API: ``scriptId``, required)
            pad_code: Target instance code (single) (API: ``padCode``, required)
            cron_expr: Cron expression (6 fields) (API: ``cronExpr``)
            one_shot: Whether it is a one-shot task (API: ``oneShot``)
            params: Template runtime params, a **JSON string** (API: ``params``)
            enabled: Whether enabled (API: ``enabled``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id, "taskName": task_name, "scriptId": script_id, "padCode": pad_code, "cronExpr": cron_expr, "oneShot": one_shot, "params": params, "enabled": enabled}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/update", json_body=payload)

    def scheduled_tasks_toggle(
        self,
        task_id: int,
        enabled: bool,
        **extra: Any,
    ) -> Any:
        """Toggle Scheduled Task.

        Enable / disable a scheduled task. When disabled the scheduler no longer triggers it; enabling restores triggering.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/toggle``

        Args:
            task_id: Scheduled task ID (API: ``taskId``, required)
            enabled: true = enable / false = disable (API: ``enabled``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id, "enabled": enabled}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/toggle", json_body=payload)

    def scheduled_tasks_delete(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Delete Scheduled Task.

        Delete a scheduled task.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/delete``

        Args:
            task_id: Scheduled task ID (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/delete", json_body=payload)


class AsyncAutomationAPI(AsyncAPIResource):
    """Async variant of :class:`AutomationAPI`."""

    async def scripts_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        category: Optional[str] = None,
        platform: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Flow Script List.

        Paginate the flow scripts visible to the current account (official + your private scripts).

        ``POST /vcpcloud/api/padApi/automation/scripts/list``

        Args:
            page: Page number, defaults to 1, min 1 (API: ``page``)
            size: Page size, defaults to 20, range 1~100 (API: ``size``)
            category: Filter by ownership type: `official` (platform-provided template) or `user` (your private script) (API: ``category``)
            platform: Filter by business platform, e.g. `instagram` / `tiktok` / `youtube` (set on `official` templates; may be null on user scripts) (API: ``platform``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "category": category, "platform": platform}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scripts/list", json_body=payload)

    async def scripts_get(
        self,
        script_id: int,
        **extra: Any,
    ) -> Any:
        """Flow Script Details.

        Fetch a single flow script by `scriptId`.

        ``POST /vcpcloud/api/padApi/automation/scripts/get``

        Args:
            script_id: Script ID (API: ``scriptId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scripts/get", json_body=payload)

    async def tasks_batch_dispatch(
        self,
        script_id: int,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        params: Optional[str] = None,
        items: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Batch Dispatch Flow Task.

        Dispatch one script to multiple cloud instances in one call. Single-call limit is **200 devices**. Two mutually-exclusive modes: * **Mode A (shared params)**: `padCodes` lists the targets, all sharing the same `params` * **Mode B (per-device params)**: `items` is an array of `{padCode, params}` pairs Exactly one of `padCodes` / `items` must be non-empty; supplying both or neither fails parameter validation.

        ``POST /vcpcloud/api/padApi/automation/tasks/batch-dispatch``

        Args:
            script_id: Script ID to execute (API: ``scriptId``, required)
            pad_codes: **Mode A**: target devices, max 200, non-blank (API: ``padCodes``)
            params: **Mode A** shared params (JSON string); ignored in Mode B (API: ``params``)
            items: **Mode B**: per-device params, max 200 (API: ``items``) Nested fields: ``padCode``, ``params``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id, "padCodes": pad_codes, "params": params, "items": items}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/batch-dispatch", json_body=payload)

    async def tasks_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Flow Task List.

        Paginate the current account's flow tasks, ordered by `createdAt` desc. Supports time-range filtering.

        ``POST /vcpcloud/api/padApi/automation/tasks/list``

        Args:
            page: Page number, defaults to 1 (API: ``page``)
            size: Page size, defaults to 20, range 1~100 (API: ``size``)
            start_time: Start time (ISO-8601 UTC string); malformed values ignored (API: ``startTime``)
            end_time: End time (ISO-8601 UTC string); malformed values ignored (API: ``endTime``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "startTime": start_time, "endTime": end_time}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/list", json_body=payload)

    async def tasks_get(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Flow Task Details.

        Fetch a single flow task by `taskId`.

        ``POST /vcpcloud/api/padApi/automation/tasks/get``

        Args:
            task_id: Real task primary key (the `id` returned by dispatch — **not**`displayId`) (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/get", json_body=payload)

    async def tasks_logs(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Flow Task Logs.

        Fetch step-level execution logs for a task (ascending by timestamp).

        ``POST /vcpcloud/api/padApi/automation/tasks/logs``

        Args:
            task_id: Task primary key (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/logs", json_body=payload)

    async def tasks_cancel(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Cancel Flow Task.

        Cancel a task. Semantics (**best-effort**): * `pending`: set to `cancelled` immediately, no device contact * `dispatched` / `running` / `cancel_requested`: set to `cancel_requested` and the device is notified to abort; the device transitions the task to a terminal state once it acknowledges * Already terminal (`success` / `failed` / `cancelled`): no-op, returns success idempotently

        ``POST /vcpcloud/api/padApi/automation/tasks/cancel``

        Args:
            task_id: Task primary key (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/tasks/cancel", json_body=payload)

    async def accounts_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        platform: Optional[str] = None,
        group_id: Optional[int] = None,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        device_bound: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Account List.

        Paginate the current user's accounts; supports platform / group / status / keyword / bind-status filtering and sorting.

        ``POST /vcpcloud/api/padApi/automation/accounts/list``

        Args:
            page: Page number, default 1, min 1 (API: ``page``)
            size: Page size, default 20, range 1–100 (API: ``size``)
            platform: Platform filter, e.g. `instagram` / `tiktok` / `youtube` (API: ``platform``)
            group_id: Account group ID filter (API: ``groupId``)
            status: Account status filter (login health): `inactive` (new, not logged in) / `active` (login OK) / `login_failed`; use deviceBound to filter by binding (API: ``status``)
            keyword: Keyword, matches handle / display name (API: ``keyword``)
            device_bound: Bind status: `true` = bound only, `false` = unbound only, omit = no filter (API: ``deviceBound``)
            sort_by: Sort field: `createdAt` / `lastActiveAt` / `cachedFollowers`, etc. (API: ``sortBy``)
            sort_dir: Sort direction: `asc` / `desc` (API: ``sortDir``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size, "platform": platform, "groupId": group_id, "status": status, "keyword": keyword, "deviceBound": device_bound, "sortBy": sort_by, "sortDir": sort_dir}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/list", json_body=payload)

    async def accounts_get(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Account Details.

        Fetch a single account by `accountId`. Returns the same fields as a `list` element of [Account List](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#account-list).

        ``POST /vcpcloud/api/padApi/automation/accounts/get``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/get", json_body=payload)

    async def accounts_snapshots(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Account Data Snapshots.

        Query account-level historical snapshots by `accountId` (followers / following / works count / likes time series), returned in descending order of collection time.

        ``POST /vcpcloud/api/padApi/automation/accounts/snapshots``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/snapshots", json_body=payload)

    async def accounts_works(
        self,
        account_id: int,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Account Works List.

        Paginate the account's collected works (deduplicated by `platformWorkId`). Each work carries the most recently collected metric snapshot.

        ``POST /vcpcloud/api/padApi/automation/accounts/works``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            page: Page number, default 1, min 1 (API: ``page``)
            size: Page size, default 20, range 1–100 (API: ``size``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "page": page, "size": size}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/works", json_body=payload)

    async def accounts_work_snapshots(
        self,
        account_id: int,
        work_id: int,
        **extra: Any,
    ) -> Any:
        """Account Work Data Snapshots.

        Query a single work's metric time series (one record per collection) by `accountId` + `workId`, returned in descending order of collection time. `accountId` is used for ownership validation.

        ``POST /vcpcloud/api/padApi/automation/accounts/work-snapshots``

        Args:
            account_id: Account ID (ownership validation) (API: ``accountId``, required)
            work_id: Work record ID (API: ``workId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "workId": work_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/work-snapshots", json_body=payload)

    async def accounts_groups_list(
        self,
        **extra: Any,
    ) -> Any:
        """Account Group List.

        List all account groups of the current user, returned in ascending order of `sortOrder`.

        ``POST /vcpcloud/api/padApi/automation/accounts/groups/list``

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/groups/list", json_body=payload)

    async def accounts_operations_batch(
        self,
        script_id: int,
        account_ids: Sequence[Any],
        *,
        task_name: Optional[str] = None,
        shared_options: Optional[Sequence[Mapping[str, Any]]] = None,
        per_account_options: Optional[Mapping[str, Any]] = None,
        **extra: Any,
    ) -> Any:
        """Batch Trigger Account Operation.

        Batch-trigger a template to run **immediately** on multiple accounts. Each account's target instance is derived from its currently bound instance (no `padCode`); credentials are decrypted and injected server-side via `fromCredential` (never sent to or readable by the client). One request creates and concurrently dispatches multiple tasks; the task record structure matches [Batch Dispatch Flow Task](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#batch-dispatch-flow-task).

        ``POST /vcpcloud/api/padApi/automation/accounts/operations/batch``

        Args:
            script_id: Template ID to run (API: ``scriptId``, required)
            account_ids: Target account IDs (API: ``accountIds``, required)
            task_name: Plan name (shown in the task list) (API: ``taskName``)
            shared_options: Shared params: same set for all accounts (API: ``sharedOptions``)
            per_account_options: Per-account params: accountId → option list (API: ``perAccountOptions``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id, "accountIds": account_ids, "taskName": task_name, "sharedOptions": shared_options, "perAccountOptions": per_account_options}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/operations/batch", json_body=payload)

    async def accounts_scheduled_tasks_batch(
        self,
        script_id: int,
        account_ids: Sequence[Any],
        cron_expr: str,
        *,
        one_shot: Optional[bool] = None,
        enabled: Optional[bool] = None,
        task_name: Optional[str] = None,
        shared_options: Optional[Sequence[Mapping[str, Any]]] = None,
        per_account_options: Optional[Mapping[str, Any]] = None,
        **extra: Any,
    ) -> Any:
        """Account Batch Scheduled Tasks.

        Batch-create **scheduled** tasks for multiple accounts: one scheduled task per account, fired on a Cron schedule. At fire time the server resolves each account's current bound instance and decrypts/injects credentials (the stored params contain no plaintext, only the `fromCredential` mapping).

        ``POST /vcpcloud/api/padApi/automation/accounts/scheduled-tasks/batch``

        Args:
            script_id: Template ID (API: ``scriptId``, required)
            account_ids: Target account IDs (API: ``accountIds``, required)
            cron_expr: Cron expression (6 fields, includes seconds); a one-shot task also uses it for its single trigger moment (API: ``cronExpr``, required)
            one_shot: One-shot task (auto-disabled after firing), default false (API: ``oneShot``)
            enabled: Enable immediately after creation, default true (API: ``enabled``)
            task_name: Plan name (API: ``taskName``)
            shared_options: Shared params; option item matches [Batch Trigger Account Operation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html#batch-trigger-account-operation) (API: ``sharedOptions``)
            per_account_options: Per-account params: accountId → option list (API: ``perAccountOptions``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"scriptId": script_id, "accountIds": account_ids, "cronExpr": cron_expr, "oneShot": one_shot, "enabled": enabled, "taskName": task_name, "sharedOptions": shared_options, "perAccountOptions": per_account_options}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/scheduled-tasks/batch", json_body=payload)

    async def accounts_create(
        self,
        platform: str,
        username: str,
        password: str,
        *,
        handle: Optional[str] = None,
        twofa_secret: Optional[str] = None,
        email: Optional[str] = None,
        email_password: Optional[str] = None,
        group_id: Optional[int] = None,
        country: Optional[str] = None,
        note: Optional[str] = None,
        tags: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """Create Account.

        Create an account in the matrix (credentials are AES-GCM encrypted at rest). `handle` is unique per platform.

        ``POST /vcpcloud/api/padApi/automation/accounts/create``

        Args:
            platform: Platform (API: ``platform``, required)
            username: Login username (credential, stored encrypted) (API: ``username``, required)
            password: Login password (credential, stored encrypted) (API: ``password``, required)
            handle: Account @handle (unique per platform, may be empty) (API: ``handle``)
            twofa_secret: 2FA secret (credential) (API: ``twofaSecret``)
            email: Email (credential) (API: ``email``)
            email_password: Email password (credential) (API: ``emailPassword``)
            group_id: Group ID (API: ``groupId``)
            country: Country/region (API: ``country``)
            note: Note (API: ``note``)
            tags: Tags (comma-separated) (API: ``tags``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"platform": platform, "username": username, "password": password, "handle": handle, "twofaSecret": twofa_secret, "email": email, "emailPassword": email_password, "groupId": group_id, "country": country, "note": note, "tags": tags}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/create", json_body=payload)

    async def accounts_bind(
        self,
        account_id: int,
        pad_code: str,
        *,
        force: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Bind Instance.

        Bind an account to a cloud instance. **Only one active account per instance+platform**; on conflict `force=false` returns 409, `force=true` rebinds (the old account is auto-unbound). padCode ownership is pre-checked at the gateway.

        ``POST /vcpcloud/api/padApi/automation/accounts/bind``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            pad_code: Target instance code (API: ``padCode``, required)
            force: Force rebind on conflict, default false (API: ``force``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "padCode": pad_code, "force": force}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/bind", json_body=payload)

    async def accounts_unbind(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Unbind Instance.

        Unbind an account from its currently bound instance.

        ``POST /vcpcloud/api/padApi/automation/accounts/unbind``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/unbind", json_body=payload)

    async def accounts_delete(
        self,
        account_id: int,
        **extra: Any,
    ) -> Any:
        """Delete Account.

        Soft-delete an account; credentials are cleared (recoverable by admin, but credentials must be re-entered).

        ``POST /vcpcloud/api/padApi/automation/accounts/delete``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/delete", json_body=payload)

    async def accounts_group(
        self,
        account_id: int,
        *,
        group_id: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Move Account Group.

        Move an account to a group; pass `null``groupId` to ungroup.

        ``POST /vcpcloud/api/padApi/automation/accounts/group``

        Args:
            account_id: Account ID (API: ``accountId``, required)
            group_id: Target group ID; null = ungroup (API: ``groupId``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"accountId": account_id, "groupId": group_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/accounts/group", json_body=payload)

    async def scheduled_tasks_list(
        self,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Scheduled Task List.

        Paginate the current user's scheduled tasks.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/list``

        Args:
            page: Page number, default 1, min 1 (API: ``page``)
            size: Page size, default 20, range 1–100 (API: ``size``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"page": page, "size": size}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/list", json_body=payload)

    async def scheduled_tasks_create(
        self,
        task_name: str,
        script_id: int,
        pad_codes: Sequence[str],
        *,
        cron_expr: Optional[str] = None,
        one_shot: Optional[bool] = None,
        params: Optional[str] = None,
        enabled: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Create Scheduled Task.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/create``

        Args:
            task_name: Schedule name (API: ``taskName``, required)
            script_id: Template ID to run (API: ``scriptId``, required)
            pad_codes: Target instance codes; one scheduled task is created per instance (API: ``padCodes``, required)
            cron_expr: Cron expression (6 fields); required for recurring tasks, optional for one-shot (API: ``cronExpr``)
            one_shot: Whether it is a one-shot task, default false (API: ``oneShot``)
            params: Template runtime params, a **JSON string**; invalid JSON is rejected (API: ``params``)
            enabled: Whether to enable immediately after creation, default true (API: ``enabled``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskName": task_name, "scriptId": script_id, "padCodes": pad_codes, "cronExpr": cron_expr, "oneShot": one_shot, "params": params, "enabled": enabled}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/create", json_body=payload)

    async def scheduled_tasks_update(
        self,
        task_id: int,
        task_name: str,
        script_id: int,
        pad_code: str,
        *,
        cron_expr: Optional[str] = None,
        one_shot: Optional[bool] = None,
        params: Optional[str] = None,
        enabled: Optional[bool] = None,
        **extra: Any,
    ) -> Any:
        """Update Scheduled Task.

        Update a single scheduled task. **One scheduled task maps to a single instance**, so the singular `padCode` is used; to change to multiple devices, delete and recreate.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/update``

        Args:
            task_id: Scheduled task ID (API: ``taskId``, required)
            task_name: Schedule name (API: ``taskName``, required)
            script_id: Template ID (API: ``scriptId``, required)
            pad_code: Target instance code (single) (API: ``padCode``, required)
            cron_expr: Cron expression (6 fields) (API: ``cronExpr``)
            one_shot: Whether it is a one-shot task (API: ``oneShot``)
            params: Template runtime params, a **JSON string** (API: ``params``)
            enabled: Whether enabled (API: ``enabled``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id, "taskName": task_name, "scriptId": script_id, "padCode": pad_code, "cronExpr": cron_expr, "oneShot": one_shot, "params": params, "enabled": enabled}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/update", json_body=payload)

    async def scheduled_tasks_toggle(
        self,
        task_id: int,
        enabled: bool,
        **extra: Any,
    ) -> Any:
        """Toggle Scheduled Task.

        Enable / disable a scheduled task. When disabled the scheduler no longer triggers it; enabling restores triggering.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/toggle``

        Args:
            task_id: Scheduled task ID (API: ``taskId``, required)
            enabled: true = enable / false = disable (API: ``enabled``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id, "enabled": enabled}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/toggle", json_body=payload)

    async def scheduled_tasks_delete(
        self,
        task_id: int,
        **extra: Any,
    ) -> Any:
        """Delete Scheduled Task.

        Delete a scheduled task.

        ``POST /vcpcloud/api/padApi/automation/scheduled-tasks/delete``

        Args:
            task_id: Scheduled task ID (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/automation/scheduled-tasks/delete", json_body=payload)
