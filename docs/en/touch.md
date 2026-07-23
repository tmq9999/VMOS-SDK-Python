# `client.touch` — Touch Simulation

> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.

Humanized click/swipe/long-press trajectories and raw multi-point touch.

## Methods

| Python | HTTP | Endpoint |
|---|---|---|
| [`simulate_touch`](#simulate-touch--simulate-touch) | POST | `/vcpcloud/api/padApi/simulateTouch` |
| [`simulate_click`](#simulate-click--simulate-click) | POST | `/vcpcloud/api/padApi/simulateClick` |
| [`simulate_swipe`](#simulate-swipe--simulate-swipe) | POST | `/vcpcloud/api/padApi/simulateSwipe` |
| [`simulate_long_press`](#simulate-long-press--simulate-long-press) | POST | `/vcpcloud/api/padApi/simulateLongPress` |

[Back to index](README.md)

---

### `simulate_touch` — Simulate Touch

- **Endpoint**: `POST /vcpcloud/api/padApi/simulateTouch`

**Signature**

```python
client.touch.simulate_touch(*, pad_codes=None, width=None, height=None, point_count=None, positions=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | String[] | no | Instances to trigger touch |
| `width` | `width` | Integer | no | Container width |
| `height` | `height` | Integer | no | Container height |
| `point_count` | `pointCount` | Integer | no | Multi-touch (1-10 fingers; default 1) |
| `positions` | `positions` | Object[] | no | Touch coordinate groups |

**Nested fields of `positions`:**

| API name | Type | Description |
|---|---|---|
| `actionType` | Integer | Action type (0: down; 1: up; 2: move) |
| `x` | float | X coordinate |
| `y` | float | Y coordinate |
| `nextPositionWaitTime` | Integer | Wait time (ms) before next group |
| `swipe` | float | Swipe distance (-1: down; 1: up) |
| `touchType` | String | gestureSwipe-swipe, gesture-touch, keystroke-key (default down+up) |
| `keyCode` | Integer | Key code |
| `pressure` | float | Touch pressure |
| `size` | float | Touch area ratio |

**Example** (JSON payload)

```json
{
  "padCodes": [
    "实例编号"
  ],
  "width": 1080,
  "height": 1920,
  "pointCount":1,
  "positions": [
    {
      "actionType": 0,
      "x": 100,
      "y": 100,
      "nextPositionWaitTime": 20,
      "swipe":-1,
      "touchType":"gestureSwipe",
      "keyCode":1,
        "pressure":0.5,
        "size":0.5
    },
    {
      "actionType": 2,
      "x": 110,
      "y": 110,
      "nextPositionWaitTime": 22
    },
    {
      "actionType": 2,
      "x": 120,
      "y": 120,
      "nextPositionWaitTime": 23
    },
    {
      "actionType": 1,
      "x": 120,
      "y": 120
    }
  ]
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `simulate_click` — Simulate Click

Generate a humanized click trajectory at the given coordinates. The click has four phases: press, hold, micro-move, release.

- **Endpoint**: `POST /vcpcloud/api/padApi/simulateClick`

**Signature**

```python
client.touch.simulate_click(pad_codes, x, y, *, width=None, height=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | Array[String] | yes | Instance code list; devices to execute the action |
| `x` | `x` | Number | yes | Click target X (screen physical pixels) |
| `y` | `y` | Number | yes | Click target Y (screen physical pixels) |
| `width` | `width` | Integer | no | Screen width (for coordinate normalization) |
| `height` | `height` | Integer | no | Screen height (for coordinate normalization) |

**Example** (JSON payload)

```json
{
  "padCodes": ["PAD_001", "PAD_002"],
  "x": 360,
  "y": 640,
  "width": 720,
  "height": 1280
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `simulate_swipe` — Simulate Swipe

Generate a humanized swipe trajectory. Supports fixed-direction mode (auto start/end) or custom start/end. Trajectory: press, swipe (ease-in-out), dwell, release.

- **Endpoint**: `POST /vcpcloud/api/padApi/simulateSwipe`

**Signature**

```python
client.touch.simulate_swipe(pad_codes, direction, *, width=None, height=None, start_x=None, start_y=None, end_x=None, end_y=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | Array[String] | yes | Instance code list |
| `direction` | `direction` | String | yes | Swipe direction enum |
| `width` | `width` | Integer | no | Screen width |
| `height` | `height` | Integer | no | Screen height |
| `start_x` | `startX` | Number | no | Start X (custom mode) |
| `start_y` | `startY` | Number | no | Start Y (custom mode) |
| `end_x` | `endX` | Number | no | End X (custom mode) |
| `end_y` | `endY` | Number | no | End Y (custom mode) |

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---

### `simulate_long_press` — Simulate Long Press

Generate a humanized long-press trajectory at the given coordinates. Hold duration is caller-configurable.

- **Endpoint**: `POST /vcpcloud/api/padApi/simulateLongPress`

**Signature**

```python
client.touch.simulate_long_press(pad_codes, x, y, *, hold_ms=None, width=None, height=None, **extra)
```

**Parameters**

| Python argument | API name | Type | Required | Description |
|---|---|---|---|---|
| `pad_codes` | `padCodes` | Array[String] | yes | Instance code list |
| `x` | `x` | Number | yes | Long-press target X |
| `y` | `y` | Number | yes | Long-press target Y |
| `hold_ms` | `holdMs` | Integer | no | Hold duration (ms); must be > 0 |
| `width` | `width` | Integer | no | Screen width |
| `height` | `height` | Integer | no | Screen height |

**Example** (JSON payload)

```json
{
  "padCodes": ["PAD_001"],
  "x": 360,
  "y": 640,
  "holdMs": 800,
  "width": 720,
  "height": 1280
}
```

**Returns**: the response `data` field (raises `VMOSAPIError` when `code != 200`).

---
