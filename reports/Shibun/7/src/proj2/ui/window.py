import tkinter as tk
from ui.controls import ControlsPanel
from fractals.dragon import draw_dragon
from graphics.screenshot import make_screenshot


class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dragon Curve Fractal")
        self.root.geometry("900x700")

        # Canvas для фрактала
        self.canvas = tk.Canvas(self.root, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Панель управления
        self.controls = ControlsPanel(self.root, self)

    def build_fractal(self):
        iterations = self.controls.iter_var.get()
        length = self.controls.len_var.get()
        color = self.controls.color_var.get()
        self.canvas.delete("all")
        draw_dragon(self.canvas, iterations=iterations, length=length, color=color)

    def clear_canvas(self):
        self.canvas.delete("all")

    def take_screenshot(self):
        make_screenshot(self.root)

    def run(self):
        self.root.mainloop()
