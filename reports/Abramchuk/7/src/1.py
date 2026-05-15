import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import ImageGrab

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def is_inside(self, point):
        # Метод барицентрических координат
        def area(a, b, c):
            return abs((a.x*(b.y - c.y) + b.x*(c.y - a.y) + c.x*(a.y - b.y)) / 2.0)

        A = area(self.p1, self.p2, self.p3)
        A1 = area(point, self.p2, self.p3)
        A2 = area(self.p1, point, self.p3)
        A3 = area(self.p1, self.p2, point)

        # Если сумма маленьких площадей равна большой — точка внутри
        return abs(A - (A1 + A2 + A3)) < 1e-5

class App:
    def __init__(self, master):
        self.master = master
        master.title("App")

        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        # Кнопки
        self.btn_add_points = tk.Button(master, text="Добавить точки", command=self.add_points)
        self.btn_add_points.pack(side="left")

        self.btn_screenshot = tk.Button(master, text="Скриншот", command=self.take_screenshot)
        self.btn_screenshot.pack(side="left")

        # Треугольник по умолчанию
        self.triangle = Triangle(Point(100, 100), Point(500, 100), Point(300, 400))
        self.points = []
        self.speed = 500
        self.draw_triangle()

    def draw_triangle(self):
        self.canvas.delete("triangle")
        self.canvas.create_polygon(
            self.triangle.p1.x, self.triangle.p1.y,
            self.triangle.p2.x, self.triangle.p2.y,
            self.triangle.p3.x, self.triangle.p3.y,
            outline="black", fill="", width=2, tags="triangle"
        )

    def add_points(self):
        n = simpledialog.askinteger("Количество точек", "Введите количество точек:", minvalue=1, maxvalue=50)
        self.points.clear()

        for _ in range(n):
            x = simpledialog.askinteger("X координата", "Введите X:")
            y = simpledialog.askinteger("Y координата", "Введите Y:")
            self.points.append(Point(x, y))

        self.visualize_points()

    def visualize_points(self):
        self.canvas.delete("points")

        for p in self.points:
            color = "green" if self.triangle.is_inside(p) else "red"

            self.canvas.create_oval(
                p.x-5, p.y-5, p.x+5, p.y+5,
                fill=color, tags="points"
            )

            self.master.update()
            self.master.after(self.speed)

    def take_screenshot(self):
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()

        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")],
                                                initialfile="screenshot.png")
        if filename:
            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
            tk.messagebox.showinfo("Скриншот", f"Сохранено как {filename}")

root = tk.Tk()
app = App(root)
root.mainloop()
