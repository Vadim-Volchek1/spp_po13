import tkinter as tk
from tkinter import colorchooser


class ControlsPanel:
    def __init__(self, root, app):
        self.app = app

        frame = tk.Frame(root, bg="#222")
        frame.pack(fill="x")

        # Итерации
        tk.Label(frame, text="Iterations:", fg="white", bg="#222").pack(side="left", padx=5)
        self.iter_var = tk.IntVar(value=12)
        tk.Entry(frame, textvariable=self.iter_var, width=5).pack(side="left")

        # Длина сегмента
        tk.Label(frame, text="Length:", fg="white", bg="#222").pack(side="left", padx=5)
        self.len_var = tk.IntVar(value=8)
        tk.Entry(frame, textvariable=self.len_var, width=5).pack(side="left")

        # Цвет
        tk.Label(frame, text="Color:", fg="white", bg="#222").pack(side="left", padx=5)
        self.color_var = tk.StringVar(value="cyan")
        self.color_btn = tk.Button(frame, text="Choose", command=self.choose_color)
        self.color_btn.pack(side="left")

        # Кнопка построения
        tk.Button(frame, text="Build Dragon", command=self.app.build_fractal).pack(side="left", padx=10)

        # Очистка
        tk.Button(frame, text="Clear", command=self.app.clear_canvas).pack(side="left", padx=5)

        # Скриншот
        tk.Button(frame, text="Screenshot", command=self.app.take_screenshot).pack(side="left", padx=5)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")[1]
        if color:
            self.color_var.set(color)
