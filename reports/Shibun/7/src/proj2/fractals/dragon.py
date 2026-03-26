def generate_dragon_points(iterations, length):
    # начальный отрезок
    points = [(0.0, 0.0), (float(length), 0.0)]

    for _ in range(iterations):
        new_points = [points[0]]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2

            dx = x2 - x1
            dy = y2 - y1

            # поворот на 90° вокруг середины
            rx = mx - dy / 2
            ry = my + dx / 2

            new_points.append((rx, ry))
            new_points.append((x2, y2))

        points = new_points

    return points


def draw_dragon(canvas, iterations=10, length=10, color="cyan"):
    canvas.update_idletasks()
    w = canvas.winfo_width() or 800
    h = canvas.winfo_height() or 600

    points = generate_dragon_points(iterations, length)

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # центрируем фрактал
    offset_x = (w - (max_x - min_x)) / 2 - min_x
    offset_y = (h - (max_y - min_y)) / 2 - min_y

    shifted = [(x + offset_x, y + offset_y) for x, y in points]

    for i in range(len(shifted) - 1):
        x1, y1 = shifted[i]
        x2, y2 = shifted[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill=color)
