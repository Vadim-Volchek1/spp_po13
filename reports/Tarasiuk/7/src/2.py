import turtle


def draw_square(turtle_obj, side_length):
    for _ in range(4):
        turtle_obj.forward(side_length)
        turtle_obj.left(90)


def pythagoras_tree(turtle_obj, side_length, depth_val, angle_val, scale_val):
    if depth_val == 0:
        return

    draw_square(turtle_obj, side_length)

    pos = turtle_obj.position()
    heading = turtle_obj.heading()

    turtle_obj.forward(side_length)

    turtle_obj.left(angle_val)
    pythagoras_tree(
        turtle_obj,
        side_length * scale_val,
        depth_val - 1,
        angle_val,
        scale_val
    )

    turtle_obj.setposition(pos)
    turtle_obj.setheading(heading)
    turtle_obj.forward(side_length)

    turtle_obj.right(90 - angle_val)
    pythagoras_tree(
        turtle_obj,
        side_length * scale_val,
        depth_val - 1,
        angle_val,
        scale_val
    )

    turtle_obj.setposition(pos)
    turtle_obj.setheading(heading)


def main():
    depth_input = int(input("Глубина рекурсии: "))
    size_input = int(input("Размер квадрата: "))
    angle_input = int(input("Угол (градусы): "))
    scale_input = float(input("Коэффициент масштаба (0.5–0.8): "))

    turtle_obj = turtle.Turtle()
    turtle_obj.speed(0)
    turtle_obj.left(90)

    pythagoras_tree(
        turtle_obj,
        size_input,
        depth_input,
        angle_input,
        scale_input
    )

    turtle.done()


if __name__ == "__main__":
    main()
