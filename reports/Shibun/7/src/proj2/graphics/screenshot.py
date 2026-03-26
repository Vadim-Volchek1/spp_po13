from PIL import ImageGrab


def make_screenshot(root, filename="dragon_screenshot.png"):
    root.update()
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()

    img = ImageGrab.grab((x, y, x + w, y + h))
    img.save(filename)
