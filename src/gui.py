import tkinter as tk
from tkinter import filedialog as fd
import cv2
from PIL import Image, ImageTk, ImageOps
from core import Core


class GUI:

    def __init__(self, core: Core):
        self.core = core

        self.window = tk.Tk()
        self.window.title('Winterveil v0.0.2')
        self.window.geometry('600x400')

        main_frame = tk.Frame()
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = self.create_left_frame(master=main_frame)
        left_frame.pack(fill=tk.BOTH, expand=True)

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
        self.image_label = tk.Label(master=frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.image_label.bind("<Configure>", self.on_image_frame_resize)
        return frame

    def on_image_frame_resize(self, _):
        self.update_image()

    def update_image(self) -> None:
        if self.core.cv_image is not None:
            width = self.image_label.winfo_width()
            height = self.image_label.winfo_height()
            pil_image = Image.fromarray(self.core.cv_image)
            pil_image = ImageOps.contain(image=pil_image, size=(width, height))
            tk_image = ImageTk.PhotoImage(image=pil_image)
            # Use both setter to prevent gc
            self.image_label.configure(image=tk_image)
            self.image_labelimage = tk_image

    def create_image_control_frame(self, master: tk.Widget) -> tk.Frame:
        frame = tk.Frame(master=master, padx=8, pady=8)
        frame.grid_columnconfigure(1, weight=1)

        open_button = tk.Button(
            master=frame, text='Open...', command=self.open_file)
        open_button.grid(row=0, column=0,)

        # TODO: 1 with sticky

        save_button = tk.Button(master=frame, text='Save')
        save_button.grid(row=0, column=2)

        return frame

    def open_file(self) -> None:
        filetypes = [
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp *.ico')
        ]
        file_path = fd.askopenfilename(filetypes=filetypes)
        self.core.load_image(path=file_path)
        self.update_image()

    def mainloop(self) -> None:
        self.window.mainloop()
