import tkinter as tk


def quarterWindowGeometry(window: tk):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/1.5))
    return f"{width}x{height}+{x}+{y}"
