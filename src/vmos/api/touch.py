"""Humanized touch simulation: click / swipe / long-press with human-like trajectories, plus raw multi-point touch.

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["TouchAPI", "AsyncTouchAPI"]


class TouchAPI(SyncAPIResource):
    """Humanized touch simulation: click / swipe / long-press with human-like trajectories, plus raw multi-point touch."""

    def simulate_touch(
        self,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        point_count: Optional[int] = None,
        positions: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Touch.

        ``POST /vcpcloud/api/padApi/simulateTouch``

        Args:
            pad_codes: Instances to trigger touch (API: ``padCodes``)
            width: Container width (API: ``width``)
            height: Container height (API: ``height``)
            point_count: Multi-touch (1-10 fingers; default 1) (API: ``pointCount``)
            positions: Touch coordinate groups (API: ``positions``) Nested fields: ``actionType``, ``x``, ``y``, ``nextPositionWaitTime``, ``swipe``, ``touchType``, ``keyCode``, ``pressure``, ``size``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "width": width, "height": height, "pointCount": point_count, "positions": positions}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/simulateTouch", json_body=payload)

    def simulate_click(
        self,
        pad_codes: Sequence[str],
        x: float,
        y: float,
        *,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Click.

        Generate a humanized click trajectory at the given coordinates. The click has four phases: press, hold, micro-move, release.

        ``POST /vcpcloud/api/padApi/simulateClick``

        Args:
            pad_codes: Instance code list; devices to execute the action (API: ``padCodes``, required)
            x: Click target X (screen physical pixels) (API: ``x``, required)
            y: Click target Y (screen physical pixels) (API: ``y``, required)
            width: Screen width (for coordinate normalization) (API: ``width``)
            height: Screen height (for coordinate normalization) (API: ``height``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "x": x, "y": y, "width": width, "height": height}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/simulateClick", json_body=payload)

    def simulate_swipe(
        self,
        pad_codes: Sequence[str],
        direction: str,
        *,
        width: Optional[int] = None,
        height: Optional[int] = None,
        start_x: Optional[float] = None,
        start_y: Optional[float] = None,
        end_x: Optional[float] = None,
        end_y: Optional[float] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Swipe.

        Generate a humanized swipe trajectory. Supports fixed-direction mode (auto start/end) or custom start/end. Trajectory: press, swipe (ease-in-out), dwell, release.

        ``POST /vcpcloud/api/padApi/simulateSwipe``

        Args:
            pad_codes: Instance code list (API: ``padCodes``, required)
            direction: Swipe direction enum (API: ``direction``, required)
            width: Screen width (API: ``width``)
            height: Screen height (API: ``height``)
            start_x: Start X (custom mode) (API: ``startX``)
            start_y: Start Y (custom mode) (API: ``startY``)
            end_x: End X (custom mode) (API: ``endX``)
            end_y: End Y (custom mode) (API: ``endY``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "direction": direction, "width": width, "height": height, "startX": start_x, "startY": start_y, "endX": end_x, "endY": end_y}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/simulateSwipe", json_body=payload)

    def simulate_long_press(
        self,
        pad_codes: Sequence[str],
        x: float,
        y: float,
        *,
        hold_ms: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Long Press.

        Generate a humanized long-press trajectory at the given coordinates. Hold duration is caller-configurable.

        ``POST /vcpcloud/api/padApi/simulateLongPress``

        Args:
            pad_codes: Instance code list (API: ``padCodes``, required)
            x: Long-press target X (API: ``x``, required)
            y: Long-press target Y (API: ``y``, required)
            hold_ms: Hold duration (ms); must be > 0 (API: ``holdMs``)
            width: Screen width (API: ``width``)
            height: Screen height (API: ``height``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "x": x, "y": y, "holdMs": hold_ms, "width": width, "height": height}, extra)
        return self._client.request("POST", "/vcpcloud/api/padApi/simulateLongPress", json_body=payload)


class AsyncTouchAPI(AsyncAPIResource):
    """Async variant of :class:`TouchAPI`."""

    async def simulate_touch(
        self,
        *,
        pad_codes: Optional[Sequence[str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        point_count: Optional[int] = None,
        positions: Optional[Sequence[Mapping[str, Any]]] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Touch.

        ``POST /vcpcloud/api/padApi/simulateTouch``

        Args:
            pad_codes: Instances to trigger touch (API: ``padCodes``)
            width: Container width (API: ``width``)
            height: Container height (API: ``height``)
            point_count: Multi-touch (1-10 fingers; default 1) (API: ``pointCount``)
            positions: Touch coordinate groups (API: ``positions``) Nested fields: ``actionType``, ``x``, ``y``, ``nextPositionWaitTime``, ``swipe``, ``touchType``, ``keyCode``, ``pressure``, ``size``.
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "width": width, "height": height, "pointCount": point_count, "positions": positions}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/simulateTouch", json_body=payload)

    async def simulate_click(
        self,
        pad_codes: Sequence[str],
        x: float,
        y: float,
        *,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Click.

        Generate a humanized click trajectory at the given coordinates. The click has four phases: press, hold, micro-move, release.

        ``POST /vcpcloud/api/padApi/simulateClick``

        Args:
            pad_codes: Instance code list; devices to execute the action (API: ``padCodes``, required)
            x: Click target X (screen physical pixels) (API: ``x``, required)
            y: Click target Y (screen physical pixels) (API: ``y``, required)
            width: Screen width (for coordinate normalization) (API: ``width``)
            height: Screen height (for coordinate normalization) (API: ``height``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "x": x, "y": y, "width": width, "height": height}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/simulateClick", json_body=payload)

    async def simulate_swipe(
        self,
        pad_codes: Sequence[str],
        direction: str,
        *,
        width: Optional[int] = None,
        height: Optional[int] = None,
        start_x: Optional[float] = None,
        start_y: Optional[float] = None,
        end_x: Optional[float] = None,
        end_y: Optional[float] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Swipe.

        Generate a humanized swipe trajectory. Supports fixed-direction mode (auto start/end) or custom start/end. Trajectory: press, swipe (ease-in-out), dwell, release.

        ``POST /vcpcloud/api/padApi/simulateSwipe``

        Args:
            pad_codes: Instance code list (API: ``padCodes``, required)
            direction: Swipe direction enum (API: ``direction``, required)
            width: Screen width (API: ``width``)
            height: Screen height (API: ``height``)
            start_x: Start X (custom mode) (API: ``startX``)
            start_y: Start Y (custom mode) (API: ``startY``)
            end_x: End X (custom mode) (API: ``endX``)
            end_y: End Y (custom mode) (API: ``endY``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "direction": direction, "width": width, "height": height, "startX": start_x, "startY": start_y, "endX": end_x, "endY": end_y}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/simulateSwipe", json_body=payload)

    async def simulate_long_press(
        self,
        pad_codes: Sequence[str],
        x: float,
        y: float,
        *,
        hold_ms: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **extra: Any,
    ) -> Any:
        """Simulate Long Press.

        Generate a humanized long-press trajectory at the given coordinates. Hold duration is caller-configurable.

        ``POST /vcpcloud/api/padApi/simulateLongPress``

        Args:
            pad_codes: Instance code list (API: ``padCodes``, required)
            x: Long-press target X (API: ``x``, required)
            y: Long-press target Y (API: ``y``, required)
            hold_ms: Hold duration (ms); must be > 0 (API: ``holdMs``)
            width: Screen width (API: ``width``)
            height: Screen height (API: ``height``)
            **extra: Extra parameters sent verbatim (forward compatibility).

        Returns:
            The response ``data`` field.
        """
        payload = build_payload({"padCodes": pad_codes, "x": x, "y": y, "holdMs": hold_ms, "width": width, "height": height}, extra)
        return await self._client.request("POST", "/vcpcloud/api/padApi/simulateLongPress", json_body=payload)
