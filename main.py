import tkinter as tk
from tkinter import filedialog, font as tkfont
from tkinter import ttk

from PIL import ImageTk, Image


class ParamView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.file_path = tk.StringVar()
        self.text = tk.StringVar()
        self.font_size = 18
        self.font_path = "Arial"
        self.rotate = 0
        self.opacity = 255

        self.preview_target: PhotoView = None

        # 文件上传组
        ttk.Label(self, text="文件").grid(row=0, column=0, sticky="W")
        ttk.Button(self, text="上传", command=self.upload_file).grid(row=0, column=1, sticky="W")

        # 水印文本组
        ttk.Label(self, text="水印文本").grid(row=1, column=0, sticky="W")
        tk.Text(self, width=30).grid(row=1, column=1)

        # 字体选择组
        options = tkfont.families()
        ttk.Label(self, text="字体").grid(row=2, column=0, sticky="W")
        font_path = ttk.Combobox(self, values=options)
        font_path.set(self.font_path)
        font_path.grid(row=2, column=1, sticky="W")

        # 字体大小选择组
        ttk.Label(self, text="字体大小").grid(row=3, column=0, sticky="W")
        font_size = ttk.Spinbox(self, from_=1, to=100)
        font_size.set(self.font_size)
        font_size.grid(row=3, column=1, sticky="W")

        # 旋转组
        ttk.Label(self, text="旋转").grid(row=4, column=0, sticky="W")
        rotate = ttk.Spinbox(self, from_=-180, to=180)
        rotate.set(self.rotate)
        rotate.grid(row=4, column=1, sticky="W")

        # 不透明度组
        ttk.Label(self, text="不透明度").grid(row=5, column=0, sticky="W")
        rotate = ttk.Spinbox(self, from_=0, to=255)
        rotate.set(self.opacity)
        rotate.grid(row=5, column=1, sticky="W")

        # 预览与生成按钮组
        yl_btn = ttk.Button(self, text="预览", command=self.preview).grid(row=7, column=0, sticky="W")
        sc_btn = ttk.Button(self, text="生成", command=self.generate).grid(row=7, column=1, sticky="W")

    def preview(self):
        pass  # todo

    def generate(self):
        pass  # todo

    # 文件上传
    def upload_file(self):
        filetypes = [
            ("Image Files", ("*.png", "*.jpg", "*.jpeg", "*.gif"))
        ]

        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            # 用户选择了文件
            self.file_path = file_path
            self.preview_target.set_img(file_path)


class PhotoView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # 视图宽高
        self.width = 300
        self.height = 300
        self.label = tk.Label(self, bg="gray", width=self.width, height=self.height)
        empty_image = Image.new("RGB", (300, 300), "white")
        self.set_img(empty_image)
        self.label.pack()

    def set_img(self, image):
        if type(image) == str:
            image = Image.open(image)
        # 限制图片宽高
        max_width = self.width
        max_height = self.height
        w, h = image.size
        if w > max_width:
            scale = max_width / w
            w, h = max_width, int(h * scale)
            image = image.resize((w, h))
        if h > max_height:
            scale = max_height / h
            w, h = int(w * scale), max_height
            image = image.resize((w, h))
        photo = ImageTk.PhotoImage(image)
        self.label.image = photo  # important! 保持对图片对象的引用，否则会触发垃圾回收不显示图片
        self.label.config(image=photo)


class MyApplication(tk.Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("Hello Tkinter")
        # self.geometry()
        # self.resizable(width=False, height=False)

        # Define the UI

        photo_view = PhotoView(self)
        photo_view.grid(row=0, column=1)
        param_view = ParamView(self)
        param_view.grid(row=0, column=0)
        param_view.preview_target = photo_view
        self.columnconfigure(0, weight=1)


if __name__ == '__main__':
    app = MyApplication()
    app.mainloop()
