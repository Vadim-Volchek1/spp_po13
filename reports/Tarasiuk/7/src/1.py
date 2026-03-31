import tkinter as tk
from tkinter import ttk
import math
import time
import colorsys

from PIL import ImageGrab


class RotatingSegment:
    def __init__(self, x, y, length=100, angle=0):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.hue = 0  # для изменения цвета

    def update(self, speed):
        self.angle += speed
        self.hue += 0.01
        if self.hue > 1:
            self.hue = 0

    def get_coords(self):
        x2 = self.x + self.length * math.cos(self.angle)
        y2 = self.y + self.length * math.sin(self.angle)
        return self.x, self.y, x2, y2

    def get_color(self):
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


class App:
    def __init__(self, master):
        self.root = master
        self.root.title("Rotating Segment")

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack()

        control_frame = ttk.Frame(self.root)
        control_frame.pack()

        ttk.Label(control_frame, text="Скорость:").grid(row=0, column=0)
        self.speed_var = tk.DoubleVar(value=0.05)
        ttk.Entry(control_frame, textvariable=self.speed_var, width=10).grid(row=0, column=1)

        ttk.Label(control_frame, text="Длина:").grid(row=0, column=2)
        self.length_var = tk.DoubleVar(value=100)
        ttk.Entry(control_frame, textvariable=self.length_var, width=10).grid(row=0, column=3)

        self.pause = False

        ttk.Button(control_frame, text="Пауза", command=self.toggle_pause).grid(row=1, column=0)
        ttk.Button(control_frame, text="Скриншот", command=self.screenshot).grid(row=1, column=1)

        self.segment = RotatingSegment(300, 200)

        self.animate()

    def toggle_pause(self):
        self.pause = not self.pause

    def screenshot(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        x1 = x + self.root.winfo_width()
        y1 = y + self.root.winfo_height()

        img = ImageGrab.grab().crop((x, y, x1, y1))
        filename = f"screenshot_{int(time.time())}.png"
        img.save(filename)
        print("Сохранено:", filename)

    def animate(self):
        self.canvas.delete("all")

        if not self.pause:
            self.segment.length = self.length_var.get()
            self.segment.update(self.speed_var.get())

        x1, y1, x2, y2 = self.segment.get_coords()
        color = self.segment.get_color()

        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3)

        self.root.after(16, self.animate)  # ~60 FPS


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
