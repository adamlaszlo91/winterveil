import tkinter as tk
import cv2
from PIL import Image, ImageTk, ImageOps


class ScaleFrame:
    def __init__(self):
        self.frame = tk.Frame(relief=tk.GROOVE, borderwidth=5)


class GUI:
    # TODO: Get from core
    cv_image = cv2.imread('examples/makise.jpg')

    def __init__(self):
        window = tk.Tk()
        window.title('Winterveil v0.0.2')
        window.geometry('600x400')

        main_frame = tk.Frame(bg='yellow')
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = self.create_left_frame(master=main_frame)
        left_frame.pack(fill=tk.BOTH, expand=True)

        window.mainloop()

    def create_left_frame(self, master: tk.Widget) -> tk.Frame:
        frame = tk.Frame(master=master)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        image_frame = self.create_image_frame(master=frame)
        image_frame.grid(row=0, column=0, sticky='NEWS')

        image_control_frame = self.create_image_control_frame(master=frame)
        image_control_frame.grid(row=1, column=0, sticky='EW')

        return frame

    def create_image_frame(self, master: tk.Widget) -> tk.Frame:
        frame = tk.Frame(master=master, padx=8, pady=8)
        image_label = tk.Label(master=frame)
        image_label.pack(fill=tk.BOTH, expand=True)
        image_label.bind("<Configure>", self.on_image_frame_resize)
        return frame

    def on_image_frame_resize(self, event):
        self.update_image(self.cv_image, event.widget)

    def update_image(self, image: cv2.Mat, widget: tk.Widget) -> None:
        width = widget.winfo_width()
        height = widget.winfo_height()
        pil_image = Image.fromarray(image)
        pil_image = ImageOps.contain(image=pil_image, size=(width, height))
        tk_image = ImageTk.PhotoImage(image=pil_image)
        # Use both setter to prevent gc
        widget.configure(image=tk_image)
        widget.image = tk_image

    def create_image_control_frame(self, master: tk.Widget) -> tk.Frame:
        frame = tk.Frame(master=master, padx=8, pady=8)
        frame.grid_columnconfigure(1, weight=1)

        open_button = tk.Button(master=frame, text='Open...')
        open_button.grid(row=0, column=0,)

        # TODO: 1 with sticky

        save_button = tk.Button(master=frame, text='Save')
        save_button.grid(row=0, column=2)

        return frame
