import tkinter as tk


class ControlsPanel:
    def __init__(self, root, app):
        self.app = app

        frame = tk.Frame(root, bg="#222")
        frame.pack(fill="x")

        # Pause button
        self.pause_btn = tk.Button(frame, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(side="left", padx=5, pady=5)

        # Speed slider
        self.speed = tk.DoubleVar(value=1.0)
        tk.Label(frame, text="Speed:", fg="white", bg="#222").pack(side="left")
        tk.Scale(
            frame, from_=0.1, to=5.0, resolution=0.1,
            orient="horizontal", variable=self.speed,
            command=self.update_speed
        ).pack(side="left")

        # Reload strings
        tk.Button(frame, text="Reload strings", command=self.app.load_strings).pack(side="left", padx=5)

        # Screenshot
        tk.Button(frame, text="Screenshot", command=self.app.take_screenshot).pack(side="left", padx=5)

    def toggle_pause(self):
        self.app.animator.paused = not self.app.animator.paused
        self.pause_btn.config(text="Resume" if self.app.animator.paused else "Pause")

    def update_speed(self, _):
        for obj in self.app.objects:
            obj.speed = self.speed.get()
