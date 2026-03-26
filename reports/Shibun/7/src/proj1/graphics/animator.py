class Animator:
    def __init__(self, app):
        self.app = app
        self.paused = False

    def start(self):
        self.update()

    def update(self):
        if not self.paused:
            for obj in self.app.objects:
                obj.move()

        self.app.root.after(30, self.update)
