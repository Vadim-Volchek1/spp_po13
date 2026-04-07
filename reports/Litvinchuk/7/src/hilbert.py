"""Hilbert curve utilities."""


# pylint: disable=too-many-statements
def hilbert_curve_points(order, step, x0, y0):
    """Return points for drawing a Hilbert curve."""
    points = []
    x_coord, y_coord = x0, y0
    direction = 0

    def move():
        """Move one step in the current direction."""
        nonlocal x_coord, y_coord
        if direction == 0:
            x_coord += step
        elif direction == 1:
            y_coord -= step
        elif direction == 2:
            x_coord -= step
        else:
            y_coord += step
        points.append((x_coord, y_coord))

    def turn_left():
        """Turn left."""
        nonlocal direction
        direction = (direction + 1) % 4

    def turn_right():
        """Turn right."""
        nonlocal direction
        direction = (direction - 1) % 4

    def hilbert(level, angle):
        """Recursively build Hilbert curve."""
        if level == 0:
            return

        if angle == 90:
            turn_left()
            hilbert(level - 1, -90)
            move()
            turn_right()
            hilbert(level - 1, 90)
            move()
            hilbert(level - 1, 90)
            turn_right()
            move()
            hilbert(level - 1, -90)
            turn_left()
        else:
            turn_right()
            hilbert(level - 1, 90)
            move()
            turn_left()
            hilbert(level - 1, -90)
            move()
            hilbert(level - 1, -90)
            turn_left()
            move()
            hilbert(level - 1, 90)
            turn_right()

    points.append((x_coord, y_coord))
    hilbert(order, 90)
    return points
