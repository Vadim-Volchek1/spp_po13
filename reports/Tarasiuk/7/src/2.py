import turtle
import math

def draw_square(t, size):
    for _ in range(4):
        t.forward(size)
        t.left(90)

def pythagoras_tree(t, size, depth, angle, scale):
    if depth == 0:
        return

    draw_square(t, size)

    pos = t.position()
    heading = t.heading()

    t.forward(size)

    t.left(angle)
    pythagoras_tree(t, size * scale, depth - 1, angle, scale)

    t.setposition(pos)
    t.setheading(heading)
    t.forward(size)

    t.right(90 - angle)
    pythagoras_tree(t, size * scale, depth - 1, angle, scale)

    t.setposition(pos)
    t.setheading(heading)

depth = int(input("Глубина рекурсии: "))
size = int(input("Размер квадрата: "))
angle = int(input("Угол (градусы): "))
scale = float(input("Коэффициент масштаба (0.5–0.8): "))

t = turtle.Turtle()
t.speed(0)
t.left(90)

pythagoras_tree(t, size, depth, angle, scale)

turtle.done()
