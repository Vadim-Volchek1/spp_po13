import random


class MovingText:
    def __init__(self, canvas, text, speed):
        self.canvas = canvas
        self.text = text
        self.speed = speed

        w = canvas.winfo_width() or 800
        h = canvas.winfo_height() or 600

        self.x = random.randint(0, w)
        self.y = random.randint(0, h)

        self.dx = random.choice([-1, 1]) * random.uniform(1, 3)
        self.dy = random.choice([-1, 1]) * random.uniform(1, 3)

        self.id = canvas.create_text(self.x, self.y, text=text, fill="white", font=("Arial", 20))

    def move(self):
        self.canvas.move(self.id, self.dx * self.speed, self.dy * self.speed)
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Wrap around screen
        if self.x < 0:
            self.x = w
            self.canvas.coords(self.id, self.x, self.y)
        if self.x > w:
            self.x = 0
            self.canvas.coords(self.id, self.x, self.y)
        if self.y < 0:
            self.y = h
            self.canvas.coords(self.id, self.x, self.y)
        if self.y > h:
            self.y = 0
            self.canvas.coords(self.id, self.x, self.y)
