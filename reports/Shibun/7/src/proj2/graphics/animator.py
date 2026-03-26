class Animator:
    def __init__(self, canvas):
        self.canvas = canvas
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
