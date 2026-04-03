import time
import tkinter as tk
import math
from tkinter import messagebox
from PIL import ImageGrab


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-statements
class PythagorasTreeApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Дерево Пифагора")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)

        self.start_x = 500.0
        self.start_y = 400.0
        self.base_length = 120.0
        self.angle_left = 45.0
        self.angle_right = 45.0
        self.shrink_factor = 0.7
        self.depth = 8

        self.animate = False
        self.current_depth = 1
        self.animation_speed = 100
        self.after_id = None
        self.max_depth = self.depth

        self.canvas = None
        self.x_scale = None
        self.y_scale = None
        self.length_scale = None
        self.left_angle_scale = None
        self.right_angle_scale = None
        self.shrink_scale = None
        self.shrink_label = None
        self.depth_scale = None
        self.depth_label = None
        self.animate_btn = None
        self.speed_scale = None
        self.screenshot_btn = None

        self.create_widgets()
        self.canvas.bind("<Configure>", lambda e: self.draw_tree())
        self.draw_tree()

    def create_widgets(self):
        control_frame = self._create_control_frame()
        self._create_row1(control_frame)
        self._create_row2(control_frame)
        self._create_row3(control_frame)
        self._create_row4(control_frame)
        self._create_canvas()

    def _create_control_frame(self):
        frame = tk.Frame(self.root, bg="lightgray", relief=tk.RAISED, bd=1)
        frame.pack(side=tk.TOP, fill=tk.X, padx=3, pady=3)
        return frame

    def _create_row1(self, parent):
        row = tk.Frame(parent, bg="lightgray")
        row.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(row, text="X:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=2)
        self.x_scale = tk.Scale(
            row, from_=0, to=800, resolution=5, orient=tk.HORIZONTAL,
            length=120, command=self.update_start_x, bg="lightgray",
            highlightthickness=0
        )
        self.x_scale.set(self.start_x)
        self.x_scale.pack(side=tk.LEFT, padx=2)

        tk.Label(row, text="Y:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=2)
        self.y_scale = tk.Scale(
            row, from_=0, to=600, resolution=5, orient=tk.HORIZONTAL,
            length=120, command=self.update_start_y, bg="lightgray",
            highlightthickness=0
        )
        self.y_scale.set(self.start_y)
        self.y_scale.pack(side=tk.LEFT, padx=2)

        tk.Label(row, text="Длина:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=5)
        self.length_scale = tk.Scale(
            row, from_=50, to=250, resolution=5, orient=tk.HORIZONTAL,
            length=120, command=self.update_base_length, bg="lightgray",
            highlightthickness=0
        )
        self.length_scale.set(self.base_length)
        self.length_scale.pack(side=tk.LEFT, padx=2)

    def _create_row2(self, parent):
        row = tk.Frame(parent, bg="lightgray")
        row.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(row, text="Левый угол:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=2)
        self.left_angle_scale = tk.Scale(
            row, from_=15, to=75, resolution=1, orient=tk.HORIZONTAL,
            length=120, command=self.update_left_angle, bg="lightgray",
            highlightthickness=0
        )
        self.left_angle_scale.set(self.angle_left)
        self.left_angle_scale.pack(side=tk.LEFT, padx=2)

        tk.Label(row, text="Правый угол:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=5)
        self.right_angle_scale = tk.Scale(
            row, from_=15, to=75, resolution=1, orient=tk.HORIZONTAL,
            length=120, command=self.update_right_angle, bg="lightgray",
            highlightthickness=0
        )
        self.right_angle_scale.set(self.angle_right)
        self.right_angle_scale.pack(side=tk.LEFT, padx=2)

    def _create_row3(self, parent):
        row = tk.Frame(parent, bg="lightgray")
        row.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(row, text="Уменьшение:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=2)
        self.shrink_scale = tk.Scale(
            row, from_=0.4, to=0.9, resolution=0.02, orient=tk.HORIZONTAL,
            length=120, command=self.update_shrink_factor, bg="lightgray",
            highlightthickness=0
        )
        self.shrink_scale.set(self.shrink_factor)
        self.shrink_scale.pack(side=tk.LEFT, padx=2)

        self.shrink_label = tk.Label(
            row, text=f"{self.shrink_factor:.2f}", bg="lightgray",
            width=4, font=("Arial", 8)
        )
        self.shrink_label.pack(side=tk.LEFT, padx=2)

        tk.Label(row, text="Глубина:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=5)
        self.depth_scale = tk.Scale(
            row, from_=2, to=12, resolution=1, orient=tk.HORIZONTAL,
            length=120, command=self.update_depth, bg="lightgray",
            highlightthickness=0
        )
        self.depth_scale.set(self.depth)
        self.depth_scale.pack(side=tk.LEFT, padx=2)

        self.depth_label = tk.Label(
            row, text=str(self.depth), bg="lightgray",
            width=2, font=("Arial", 8)
        )
        self.depth_label.pack(side=tk.LEFT, padx=2)

    def _create_row4(self, parent):
        row = tk.Frame(parent, bg="lightgray")
        row.pack(fill=tk.X, padx=5, pady=3)

        self.animate_btn = tk.Button(
            row, text="Анимация", command=self.toggle_animation,
            width=10, height=1, font=("Arial", 8, "bold")
        )
        self.animate_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(row, text="Скорость:", bg="lightgray", font=("Arial", 8)) \
            .pack(side=tk.LEFT, padx=5)
        self.speed_scale = tk.Scale(
            row, from_=500, to=30, orient=tk.HORIZONTAL,
            length=100, command=self.update_animation_speed,
            bg="lightgray", highlightthickness=0
        )
        self.speed_scale.set(self.animation_speed)
        self.speed_scale.pack(side=tk.LEFT, padx=2)

        tk.Label(row, text="быстрее→", bg="lightgray", font=("Arial", 7)) \
            .pack(side=tk.LEFT, padx=2)

        self.screenshot_btn = tk.Button(
            row, text="Скриншот", command=self.take_screenshot,
            width=10, height=1, font=("Arial", 8)
        )
        self.screenshot_btn.pack(side=tk.RIGHT, padx=5)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=3, pady=3)

    def draw_tree(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        self.max_depth = self.current_depth if self.animate else self.depth
        self.draw_branch((self.start_x, self.start_y), self.base_length, -90, 0)

    def _get_branch_style(self, depth):
        if depth == 0:
            return "#8b4513", 5

        ratio = min(1.0, depth / self.max_depth) if self.max_depth > 0 else 1.0
        r = int(139 + (34 - 139) * ratio)
        g = int(69 + (139 - 69) * ratio)
        b = int(19 + (34 - 19) * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        line_width = max(1, 5 - depth) if depth < 5 else 1
        return color, line_width

    def draw_branch(self, point, length, angle_deg, depth=0):
        if depth > self.max_depth or length < 1:
            return

        x, y = point
        angle_rad = math.radians(angle_deg)
        end_x = x + length * math.cos(angle_rad)
        end_y = y + length * math.sin(angle_rad)

        color, line_width = self._get_branch_style(depth)
        self.canvas.create_line(x, y, end_x, end_y, fill=color, width=line_width)

        new_length = length * self.shrink_factor
        self.draw_branch((end_x, end_y), new_length, angle_deg + self.angle_left, depth + 1)
        self.draw_branch((end_x, end_y), new_length, angle_deg - self.angle_right, depth + 1)

    def update_start_x(self, value):
        self.start_x = float(value)
        self.draw_tree()

    def update_start_y(self, value):
        self.start_y = float(value)
        self.draw_tree()

    def update_base_length(self, value):
        self.base_length = float(value)
        self.draw_tree()

    def update_left_angle(self, value):
        self.angle_left = float(value)
        self.draw_tree()

    def update_right_angle(self, value):
        self.angle_right = float(value)
        self.draw_tree()

    def update_shrink_factor(self, value):
        self.shrink_factor = float(value)
        self.shrink_label.config(text=f"{self.shrink_factor:.2f}")
        self.draw_tree()

    def update_depth(self, value):
        self.depth = int(value)
        self.depth_label.config(text=str(self.depth))
        self.current_depth = min(self.current_depth, self.depth)
        if not self.animate:
            self.draw_tree()

    def toggle_animation(self):
        if self.animate:
            self.animate = False
            self.animate_btn.config(text="Анимация", bg="SystemButtonFace")
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.draw_tree()
            return

        self.animate = True
        self.current_depth = 1
        self.animate_btn.config(text="Сброс", bg="lightgreen")
        self.animate_step()

    def animate_step(self):
        if not self.animate:
            return

        self.draw_tree()

        if self.current_depth < self.depth:
            self.current_depth += 1
            self.after_id = self.root.after(
                self.animation_speed, self.animate_step
            )
        else:
            self.animate = False
            self.animate_btn.config(text="Анимация", bg="SystemButtonFace")
            self.after_id = None

    def update_animation_speed(self, value):
        self.animation_speed = int(value)

    def take_screenshot(self):
        try:
            self.root.update()
            # коэффициент масштабирования (DPI fix)
            scale = self.root.winfo_fpixels('1i') / 72
            x = int(self.root.winfo_rootx() * scale)
            y = int(self.root.winfo_rooty() * scale)
            w = int(self.root.winfo_width() * scale)
            h = int(self.root.winfo_height() * scale)

            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"pythagoras_tree_{timestamp}.png"
            img.save(filename)
            messagebox.showinfo("Скриншот", f"Сохранён как {filename}")
        except (OSError, IOError, AttributeError) as e:
            messagebox.showerror(
                "Ошибка", f"Не удалось создать скриншот: {str(e)}"
            )


if __name__ == "__main__":
    tk_root_window = tk.Tk()
    app = PythagorasTreeApp(tk_root_window)
    tk_root_window.mainloop()
