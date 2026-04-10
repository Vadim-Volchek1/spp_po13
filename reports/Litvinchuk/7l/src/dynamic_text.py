"""Dynamic text animation utilities."""

from dataclasses import dataclass


@dataclass
class LetterTarget:
    """Store target coordinates for a flying letter."""

    x_coord: float
    y_coord: float


class FlyingLetter:  # pylint: disable=too-few-public-methods
    """Animated letter moving from a corner to a target position."""

    def __init__(self, canvas, char, start_position, target):
        """Initialize a flying letter."""
        self.canvas = canvas
        self.char = char
        self.x_coord, self.y_coord = start_position
        self.target = target
        self.item = self.canvas.create_text(
            self.x_coord,
            self.y_coord,
            text=char,
            font=("Arial", 20, "bold"),
        )

    def move_step(self, speed):
        """Move the letter one step toward the target."""
        delta_x = self.target.x_coord - self.x_coord
        delta_y = self.target.y_coord - self.y_coord

        if abs(delta_x) < 1 and abs(delta_y) < 1:
            self.canvas.coords(self.item, self.target.x_coord, self.target.y_coord)
            self.x_coord = self.target.x_coord
            self.y_coord = self.target.y_coord
            return True

        self.x_coord += delta_x / speed
        self.y_coord += delta_y / speed
        self.canvas.coords(self.item, self.x_coord, self.y_coord)
        return False
