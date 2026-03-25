# pylint: disable=too-many-positional-arguments
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

# ФРАКТАЛ
def minkowski_curve(x1, y1, x2, y2, depth, points):
    if depth == 0:
        points.append((x1, y1))
        return

    dx = (x2 - x1) / 4
    dy = (y2 - y1) / 4

    x = x1
    y = y1

    pts = [
        (x, y),
        (x + dx, y + dy),
        (x + dx - dy, y + dy + dx),
        (x + 2*dx - dy, y + 2*dy + dx),
        (x + 2*dx, y + 2*dy),
        (x + 3*dx, y + 3*dy),
        (x + 3*dx + dy, y + 3*dy - dx),
        (x + 4*dx + dy, y + 4*dy - dx),
        (x2, y2),
    ]

    for i in range(len(pts) - 1):
        minkowski_curve(pts[i][0], pts[i][1],
                        pts[i+1][0], pts[i+1][1],
                        depth - 1, points)


def minkowski_island(depth):
    points = []
    minkowski_curve(0, 0, 1, 0, depth, points)
    minkowski_curve(1, 0, 1, 1, depth, points)
    minkowski_curve(1, 1, 0, 1, depth, points)
    minkowski_curve(0, 1, 0, 0, depth, points)
    points.append((0, 0))
    return points


# ПРИЛОЖЕНИЕ

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Фрактал: Остров Минковского")

        self.depth = 1

        self.build_ui()

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.draw_fractal()

    def build_ui(self):
        control = ttk.Frame(self.root)
        control.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(control, text="Глубина рекурсии:").pack()
        self.depth_entry = ttk.Entry(control)
        self.depth_entry.insert(0, "1")
        self.depth_entry.pack(pady=5)

        ttk.Button(control, text="Построить", command=self.update_depth).pack(pady=10)

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side="right", fill="both", expand=True)

    def update_depth(self):
        try:
            self.depth = int(self.depth_entry.get())
        except ValueError:
            self.depth = 1

        self.draw_fractal()

    def draw_fractal(self):
        self.ax.clear()
        pts = minkowski_island(self.depth)

        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]

        self.ax.plot(xs, ys, color="blue", linewidth=1)
        self.ax.set_aspect("equal")
        self.ax.set_title(f"Остров Минковского (глубина {self.depth})")
        self.ax.axis("off")

        self.canvas.draw()
    def on_close(self):
        plt.close(self.fig)
        self.root.destroy()

r = tk.Tk()
app = App(r)
r.mainloop()
