import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.master = master
        master.title("Фрактал Мандельброта")

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4)

        # Ползунки для параметров
        self.iter_scale = tk.Scale(master, from_=10, to=1000, label="Итерации", orient="horizontal")
        self.iter_scale.set(100)
        self.iter_scale.grid(row=1, column=0)
        self.iter_scale.bind("<ButtonRelease-1>", self.update_fractal)

        self.re_min_scale = tk.Scale(master, from_=-2.5, to=0.5, resolution=0.01, label="Re min", orient="horizontal")
        self.re_min_scale.set(-2.0)
        self.re_min_scale.grid(row=1, column=1)
        self.re_min_scale.bind("<ButtonRelease-1>", self.update_fractal)

        self.re_max_scale = tk.Scale(master, from_=0.5, to=2.5, resolution=0.01, label="Re max", orient="horizontal")
        self.re_max_scale.set(1.0)
        self.re_max_scale.grid(row=1, column=2)
        self.re_max_scale.bind("<ButtonRelease-1>", self.update_fractal)

        self.im_min_scale = tk.Scale(master, from_=-2.0, to=0.0, resolution=0.01, label="Im min", orient="horizontal")
        self.im_min_scale.set(-1.0)
        self.im_min_scale.grid(row=2, column=0)
        self.im_min_scale.bind("<ButtonRelease-1>", self.update_fractal)

        self.im_max_scale = tk.Scale(master, from_=0.0, to=2.0, resolution=0.01, label="Im max", orient="horizontal")
        self.im_max_scale.set(1.0)
        self.im_max_scale.grid(row=2, column=1)
        self.im_max_scale.bind("<ButtonRelease-1>", self.update_fractal)

        # Первичная отрисовка
        self.update_fractal()

    def update_fractal(self, event=None):   # pylint: disable=unused-argument
        width = self.canvas_width
        height = self.canvas_height
        max_iter = self.iter_scale.get()
        re_start = self.re_min_scale.get()
        re_end = self.re_max_scale.get()
        im_start = self.im_min_scale.get()
        im_end = self.im_max_scale.get()

        image = Image.new("RGB", (width, height))
        pixels = image.load()

        for x in range(width):
            for y in range(height):
                c = complex(re_start + (x / width) * (re_end - re_start),
                            im_start + (y / height) * (im_end - im_start))
                z = 0 + 0j
                iteration = 0
                while abs(z) <= 2 and iteration < max_iter:
                    z = z*z + c
                    iteration += 1
                color = 255 - int(iteration * 255 / max_iter)
                pixels[x, y] = (color, color, color)

        self.fractal_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.fractal_image)

root = tk.Tk()
app = App(root)
root.mainloop()
