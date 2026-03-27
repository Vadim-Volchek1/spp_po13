import time
import tkinter as tk
import math
import colorsys
from tkinter import messagebox
from PIL import ImageGrab


# pylint: disable=too-many-instance-attributes
class RotatingLineApp:
    def __init__(self, root):
        self.canvas = None
        self.screenshot_btn = None
        self.y_entry = None
        self.y_var = None
        self.x_entry = None
        self.x_var = None
        self.length_entry = None
        self.length_var = None
        self.speed_entry = None
        self.speed_var = None
        self.play_pause_btn = None

        self.root = root
        self.root.title("Вращающийся отрезок")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)

        self.length = 150.0
        self.fixed_x = 400.0
        self.fixed_y = 300.0
        self.angle = 0.0
        self.angular_speed = 0.05
        self.running = False
        self.after_id = None

        self.create_widgets()
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        self.redraw()

    def create_widgets(self):
        control_frame = tk.Frame(self.root, bg='lightgray', relief=tk.RAISED, bd=2)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        btn_frame = tk.Frame(control_frame, bg='lightgray')
        btn_frame.pack(side=tk.LEFT, padx=10, pady=5)

        speed_frame = tk.Frame(control_frame, bg='lightgray')
        speed_frame.pack(side=tk.LEFT, padx=10, pady=5)

        length_frame = tk.Frame(control_frame, bg='lightgray')
        length_frame.pack(side=tk.LEFT, padx=10, pady=5)

        pos_frame = tk.Frame(control_frame, bg='lightgray')
        pos_frame.pack(side=tk.LEFT, padx=10, pady=5)

        screenshot_frame = tk.Frame(control_frame, bg='lightgray')
        screenshot_frame.pack(side=tk.RIGHT, padx=10, pady=5)

        self.play_pause_btn = tk.Button(btn_frame, text="▶ Старт",
                                        command=self.toggle_animation,
                                        width=10, height=1, font=('Arial', 10, 'bold'))
        self.play_pause_btn.pack()

        # Скорость вращения (градусы/сек)
        tk.Label(speed_frame, text="Скорость вращения:", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.StringVar(
            value=str(int(self.angular_speed * (1000 / 50) * 180 / math.pi)))
        self.speed_entry = tk.Entry(speed_frame, textvariable=self.speed_var,
                                    width=8, font=('Arial', 9))
        self.speed_entry.pack(side=tk.LEFT, padx=5)
        self.speed_var.trace('w', lambda *args: self.update_speed())
        tk.Label(speed_frame, text="град/сек", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=2)

        # Длина отрезка
        tk.Label(length_frame, text="Длина отрезка:", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.length_var = tk.StringVar(value=str(self.length))
        self.length_entry = tk.Entry(length_frame, textvariable=self.length_var,
                                     width=8, font=('Arial', 9))
        self.length_entry.pack(side=tk.LEFT, padx=5)
        self.length_var.trace('w', lambda *args: self.update_length())
        tk.Label(length_frame, text="пикс", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=2)

        tk.Label(pos_frame, text="Точка вращения:", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=5)

        tk.Label(pos_frame, text="X:", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        self.x_var = tk.StringVar(value=str(self.fixed_x))
        self.x_entry = tk.Entry(pos_frame, textvariable=self.x_var,
                                width=6, font=('Arial', 9))
        self.x_entry.pack(side=tk.LEFT, padx=2)
        self.x_var.trace('w', lambda *args: self.update_fixed_point())

        tk.Label(pos_frame, text="Y:", bg='lightgray',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        self.y_var = tk.StringVar(value=str(self.fixed_y))
        self.y_entry = tk.Entry(pos_frame, textvariable=self.y_var,
                                width=6, font=('Arial', 9))
        self.y_entry.pack(side=tk.LEFT, padx=2)
        self.y_var.trace('w', lambda *args: self.update_fixed_point())

        self.screenshot_btn = tk.Button(screenshot_frame, text="Скриншот",
                                        command=self.take_screenshot,
                                        width=12, height=1, font=('Arial', 9))
        self.screenshot_btn.pack()
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def on_canvas_resize(self, _):
        self.redraw()

    def toggle_animation(self):
        if self.running:
            self.running = False
            self.play_pause_btn.config(text="Старт", bg='SystemButtonFace')
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
        else:
            self.running = True
            self.play_pause_btn.config(text="Пауза", bg='lightgreen')
            self.animate()

    def animate(self):
        if not self.running:
            return
        self.angle += self.angular_speed
        self.redraw()
        self.after_id = self.root.after(50, self.animate)

    def redraw(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        if (self.fixed_x < 0 or self.fixed_x > canvas_width or
                self.fixed_y < 0 or self.fixed_y > canvas_height):
            self.canvas.create_text(canvas_width // 2, canvas_height // 2,
                                    text="Точка вращения вне области видимости!",
                                    fill="red", font=('Arial', 14, 'bold'))
            return

        end_x = self.fixed_x + self.length * math.cos(self.angle)
        end_y = self.fixed_y - self.length * math.sin(self.angle)
        color = self.angle_to_color(self.angle)
        self.canvas.create_line(self.fixed_x, self.fixed_y, end_x, end_y,
                                fill=color, width=3)
        self.canvas.create_oval(self.fixed_x - 6, self.fixed_y - 6,
                                self.fixed_x + 6, self.fixed_y + 6,
                                fill="red", outline="darkred", width=2)

        angle_deg = int(self.angle * 180 / math.pi) % 360
        self.canvas.create_text(10, 10, text=f"Угол: {angle_deg}°",
                                anchor=tk.NW, fill="gray", font=('Arial', 9))

    @staticmethod
    def angle_to_color(angle):
        hue = angle % (2 * math.pi)
        hue /= (2 * math.pi)
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

    def update_speed(self):
        try:
            value = self.speed_var.get().strip()
            if value:
                deg_per_sec = float(value)
                self.angular_speed = (deg_per_sec * math.pi / 180) * 0.05
        except ValueError:
            current_deg = self.angular_speed * (1000 / 50) * 180 / math.pi
            self.speed_var.set(str(int(current_deg)))
            messagebox.showerror("Ошибка",
                                 "Введите корректное число для скорости.")

    def update_length(self):
        try:
            value = self.length_var.get().strip()
            if value:
                new_len = float(value)
                if new_len > 0:
                    self.length = new_len
                    self.redraw()
                else:
                    raise ValueError
        except ValueError:
            self.length_var.set(str(self.length))
            messagebox.showerror("Ошибка",
                                 "Длина должна быть положительным числом.")

    def update_fixed_point(self):
        try:
            x_value = self.x_var.get().strip()
            y_value = self.y_var.get().strip()

            if x_value and y_value:
                x = float(x_value)
                y = float(y_value)

                if x >= 0 and y >= 0:
                    self.fixed_x = x
                    self.fixed_y = y
                    self.redraw()
                else:
                    raise ValueError
        except ValueError:
            self.x_var.set(str(self.fixed_x))
            self.y_var.set(str(self.fixed_y))
            messagebox.showerror("Ошибка",
                                 "Введите корректные положительные координаты.")

    def take_screenshot(self):
        try:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()

            if w <= 1 or h <= 1:
                messagebox.showwarning("Предупреждение",
                                       "Canvas еще не инициализирован.")
                return

            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            img.save(filename)
            messagebox.showinfo("Скриншот",
                                f"Сохранён как {filename}")
        except (OSError, IOError, AttributeError) as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось создать скриншот: {str(e)}")


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = RotatingLineApp(tk_root)
    tk_root.mainloop()
