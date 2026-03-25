import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def side(self, p: Point):
        return self.A * p.x + self.B * p.y + self.C


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Point–Line Visualization")

        self.points = []
        self.line = Line(1, -1, 0)
        self.paused = False
        self.after_id = None  # ID таймера

        # UI
        self.build_ui()

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Запуск цикла обновления
        self.update_plot()

    def build_ui(self):
        control = ttk.Frame(self.root)
        control.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(control, text="Количество точек:").pack()
        self.n_entry = ttk.Entry(control)
        self.n_entry.insert(0, "20")
        self.n_entry.pack(pady=5)

        ttk.Button(control, text="Сгенерировать точки", command=self.generate_points).pack(pady=5)

        ttk.Label(control, text="Прямая Ax + By + C = 0").pack(pady=10)

        self.A_entry = ttk.Entry(control)
        self.B_entry = ttk.Entry(control)
        self.C_entry = ttk.Entry(control)

        for label, entry, val in [
            ("A:", self.A_entry, "1"),
            ("B:", self.B_entry, "-1"),
            ("C:", self.C_entry, "0")
        ]:
            ttk.Label(control, text=label).pack()
            entry.insert(0, val)
            entry.pack(pady=2)

        ttk.Button(control, text="Обновить прямую", command=self.update_line).pack(pady=10)

        ttk.Button(control, text="Пауза / Продолжить", command=self.toggle_pause).pack(pady=10)
        ttk.Button(control, text="Скриншот", command=self.save_screenshot).pack(pady=10)

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side="right", fill="both", expand=True)

    # ДЕЙСТВИЯ

    def generate_points(self):
        try:
            n = int(self.n_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число точек")
            return

        self.points = [
            Point(random.uniform(-10, 10), random.uniform(-10, 10))
            for _ in range(n)
        ]

    def update_line(self):
        try:
            A = float(self.A_entry.get())
            B = float(self.B_entry.get())
            C = float(self.C_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные коэффициенты")
            return

        self.line = Line(A, B, C)

    def toggle_pause(self):
        self.paused = not self.paused

    def save_screenshot(self):
        self.fig.savefig("screenshot.png")
        messagebox.showinfo("Готово", "Скриншот сохранён как screenshot.png")

    # ВИЗУАЛИЗАЦИЯ

    def update_plot(self):
        # Если окно закрыто — не продолжаем
        if not self.root.winfo_exists():
            return

        if not self.paused:
            self.ax.clear()
            self.ax.grid(True)
            self.ax.set_title("Point–Line Side Detection")

            # Рисуем прямую
            A, B, C = self.line.A, self.line.B, self.line.C
            x_vals = [-10, 10]

            if B != 0:
                y_vals = [(-A * x - C) / B for x in x_vals]
            else:
                x_vals = [-C / A] * 2
                y_vals = [-10, 10]

            self.ax.plot(x_vals, y_vals, 'k-', label="Line")

            # Разделяем точки
            left, right, on_line = [], [], []

            for p in self.points:
                s = self.line.side(p)
                if s > 0:
                    right.append(p)
                elif s < 0:
                    left.append(p)
                else:
                    on_line.append(p)

            self.ax.scatter([p.x for p in left], [p.y for p in left], color='red', label='Left')
            self.ax.scatter([p.x for p in right], [p.y for p in right], color='blue', label='Right')
            self.ax.scatter([p.x for p in on_line], [p.y for p in on_line], color='green', label='On line')

            self.ax.legend()
            self.canvas.draw()

        # Планируем следующее обновление
        self.after_id = self.root.after(200, self.update_plot)

    #ЗАКРЫТИЕ ОКНА

    def on_close(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


#ЗАПУСК

r = tk.Tk()
app = App(r)
r.mainloop()
