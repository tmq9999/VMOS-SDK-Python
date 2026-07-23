"""Task management: query the status and details of asynchronous instance/file tasks.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["TasksAPI", "AsyncTasksAPI"]


class TasksAPI(SyncAPIResource):
    """Task management: query the status and details of asynchronous instance/file tasks."""

    def get_task_status(
        self,
        task_id: str,
        **extra: Any,
    ) -> Any:
        """Device Task Execution Result Query.

        Query task execution result using task number (for smart IP).

        ``POST /vcpcloud/api/padApi/getTaskStatus``

        Args:
            task_id: Task ID (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/getTaskStatus", json_body=payload)

    def pad_task_detail(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Instance Operation Task Details.

        Query detailed execution results for specified instance operation task.

        ``POST /vcpcloud/api/padApi/padTaskDetail``

        Args:
            task_ids: (API: ``taskIds``, required) Nested fields: ``taskId``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/padTaskDetail", json_body=payload)

    def pad_execute_task_info(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Instance Restart/Reset Execution Result.

        Get instance restart/reset execution result via task ID.

        ``POST /vcpcloud/api/padApi/padExecuteTaskInfo``

        Args:
            task_ids: (API: ``taskIds``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/padExecuteTaskInfo", json_body=payload)

    def file_task_detail(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """File Task Details.

        Query the detailed execution result of a specified file task.

        ``POST /vcpcloud/api/padApi/fileTaskDetail``

        Args:
            task_ids: List of task IDs (API: ``taskIds``, required) Nested fields: ``taskId``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/fileTaskDetail", json_body=payload)


class AsyncTasksAPI(AsyncAPIResource):
    """Async variant of :class:`TasksAPI`."""

    async def get_task_status(
        self,
        task_id: str,
        **extra: Any,
    ) -> Any:
        """Device Task Execution Result Query.

        Query task execution result using task number (for smart IP).

        ``POST /vcpcloud/api/padApi/getTaskStatus``

        Args:
            task_id: Task ID (API: ``taskId``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskId": task_id}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/getTaskStatus", json_body=payload)

    async def pad_task_detail(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Instance Operation Task Details.

        Query detailed execution results for specified instance operation task.

        ``POST /vcpcloud/api/padApi/padTaskDetail``

        Args:
            task_ids: (API: ``taskIds``, required) Nested fields: ``taskId``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/padTaskDetail", json_body=payload)

    async def pad_execute_task_info(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """Instance Restart/Reset Execution Result.

        Get instance restart/reset execution result via task ID.

        ``POST /vcpcloud/api/padApi/padExecuteTaskInfo``

        Args:
            task_ids: (API: ``taskIds``, required)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/padExecuteTaskInfo", json_body=payload)

    async def file_task_detail(
        self,
        task_ids: Sequence[Any],
        **extra: Any,
    ) -> Any:
        """File Task Details.

        Query the detailed execution result of a specified file task.

        ``POST /vcpcloud/api/padApi/fileTaskDetail``

        Args:
            task_ids: List of task IDs (API: ``taskIds``, required) Nested fields: ``taskId``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"taskIds": task_ids}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/fileTaskDetail", json_body=payload)
