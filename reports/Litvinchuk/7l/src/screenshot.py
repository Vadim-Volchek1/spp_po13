"""Screenshot utilities for Tkinter widgets."""

import time
from pathlib import Path

from PIL import ImageGrab


def save_widget_screenshot(widget):
    """Save a screenshot of the given widget to the current directory."""
    widget.update()

    x_coord = widget.winfo_rootx()
    y_coord = widget.winfo_rooty()
    width = widget.winfo_width()
    height = widget.winfo_height()

    image = ImageGrab.grab(
        bbox=(
            x_coord,
            y_coord,
            x_coord + width,
            y_coord + height,
        )
    )
    filename = Path.cwd() / f"screenshot_{int(time.time())}.png"
    image.save(filename)
    return filename
