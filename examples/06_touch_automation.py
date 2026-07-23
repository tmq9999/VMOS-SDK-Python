"""Humanized touch: click, swipe and long-press with human-like trajectories."""
from vmos import VMOSClient

PADS = ["AC32010180421"]

with VMOSClient() as client:
    # Humanized click at (360, 640) on a 720x1280 screen
    client.touch.simulate_click(PADS, 360, 640, width=720, height=1280)

    # Humanized swipe up
    client.touch.simulate_swipe(
        PADS, start_x=360, start_y=1000, end_x=360, end_y=300, width=720, height=1280
    )

    # Long press for 1.2 s (hold_ms)
    client.touch.simulate_long_press(PADS, 360, 640, hold_ms=1200)
