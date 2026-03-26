import tkinter as tk
from ui.controls import ControlsPanel
from graphics.animator import Animator
from graphics.moving_text import MovingText
from graphics.screenshot import make_screenshot


class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Moving Text Animation")
        self.root.geometry("800x600")

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Controls
        self.controls = ControlsPanel(self.root, self)

        # Animation objects
        self.objects = []
        self.animator = Animator(self)

        # Load initial strings
        self.load_strings()

    def load_strings(self):
    # удалить старые надписи
        for obj in self.objects:
            self.canvas.delete(obj.id)

        self.objects.clear()

        try:
            with open("data/strings.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            lines = ["Hello", "Python", "Moving text"]

        for text in lines:
            obj = MovingText(self.canvas, text, self.controls.speed.get())
            self.objects.append(obj)


    def take_screenshot(self):
        make_screenshot(self.root)

    def run(self):
        self.animator.start()
        self.root.mainloop()
