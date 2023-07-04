import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from PIL import ImageTk, Image

import font_module
import img_module
from font_module import SystemFont


class ParamView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.file_path = tk.StringVar()
        self.text = tk.StringVar()
        self.font_size = tk.IntVar(value=18)
        self.sf = font_module.SystemFont()
        self.font_name = tk.StringVar(value="Arial")
        self.rotate = tk.IntVar(value=45)
        self.opacity = tk.IntVar(value=255)

        self.original_img: Image = None
        self.watermark_img: Image = None
        self.preview_target: PhotoView = None

        # 文件选择组
        ttk.Label(self, text="文件").grid(row=0, column=0, sticky="W")
        ttk.Button(self, text="选择", command=self.open_file).grid(row=0, column=1, sticky="W")

        # 水印文本组
        ttk.Label(self, text="水印文本").grid(row=1, column=0, sticky="W")
        tk.Entry(self, textvariable=self.text).grid(row=1, column=1, sticky="W")

        # 字体选择组
        sf = SystemFont()
        ttk.Label(self, text="字体").grid(row=2, column=0, sticky="W")
        font_name = ttk.Combobox(self, values=sf.get_names(), textvariable=self.font_name)
        font_name.grid(row=2, column=1, sticky="W")
        self.font_type = ttk.Combobox(self)
        self.font_type.grid(row=2, column=2, sticky="W")

        font_name.bind("<<ComboboxSelected>>", self.update_font_type)
        self.update_font_type()

        # 字体大小选择组
        ttk.Label(self, text="字体大小").grid(row=3, column=0, sticky="W")
        font_size = ttk.Spinbox(self, from_=1, to=100, textvariable=self.font_size)
        font_size.grid(row=3, column=1, sticky="W")

        # 旋转组
        ttk.Label(self, text="旋转").grid(row=4, column=0, sticky="W")
        rotate = ttk.Spinbox(self, from_=-180, to=180, textvariable=self.rotate)
        rotate.grid(row=4, column=1, sticky="W")

        # 不透明度组
        ttk.Label(self, text="不透明度").grid(row=5, column=0, sticky="W")
        rotate = ttk.Spinbox(self, from_=0, to=255, textvariable=self.opacity)
        rotate.grid(row=5, column=1, sticky="W")

        # 预览与生成按钮组
        yl_btn = ttk.Button(self, text="预览", command=self.view).grid(row=7, column=0, sticky="W")
        sc_btn = ttk.Button(self, text="保存", command=self.save).grid(row=7, column=1, sticky="W")

    def on_input(self):
        """
        输入参数变化时更新预览图片小窗口
        :return:
        """
        if self.original_img:
            # find font_path
            font_path = self.sf.get_path((self.font_name.get(), self.font_type.get()))
            # update the photo_view
            self.watermark_img = img_module.add_watermark(self.original_img, text=self.text.get(),
                                           font_color=(30, 136, 229),
                                           font_size=self.font_size.get(),
                                           font_path=font_path,
                                           space=(32, 64),
                                           angle=self.rotate.get(),
                                           alpha=self.opacity.get()
                                           )
            self.preview_target.set_img(self.watermark_img)

    def update_font_type(self, event=None):
        """
        字体选择框绑定事件，更新字体样式框的可选项
        :param event:
        :return:
        """
        options = self.sf.get_styles(self.font_name.get())
        self.font_type.config(values=options)
        self.font_type.current(0)

    def view(self):
        """
        点击预览按钮触发，打开水印图片
        :return:
        """
        if self.watermark_img:
            self.watermark_img.show()

    def save(self):
        if self.watermark_img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=(("Image files", "*.png"), ("All files", "*.*")))
            if file_path:
                self.watermark_img.save(file_path)

    # 文件选择
    def open_file(self):
        filetypes = [
            ("Image Files", ("*.png", "*.jpg", "*.jpeg", "*.gif"))
        ]

        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            # 用户选择了文件
            self.file_path = file_path
            self.original_img = Image.open(file_path)
            self.preview_target.set_img(self.original_img)


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
        self.title("ID-photo-watermark-adder")
        # self.geometry()
        # self.resizable(width=False, height=False)

        # Define the UI
        self.photo_view = PhotoView(self)
        self.photo_view.grid(row=0, column=1)
        self.param_view = ParamView(self)
        self.param_view.grid(row=0, column=0)
        self.param_view.preview_target = self.photo_view
        self.columnconfigure(0, weight=1)


# 为app添加所有输入事件
def listen_input(app: tk.Tk):
    # 防抖等待时间（秒）
    debounce_wait_time = 0.2
    # 计时器
    last_timer: threading.Timer = None

    def debounce_handler(*args, **kwargs):
        nonlocal last_timer
        if last_timer is not None:
            last_timer.cancel()
        last_timer = threading.Timer(debounce_wait_time, handle_input, args=args, kwargs=kwargs)
        last_timer.start()

    def handle_input(event):
        param_view: ParamView = app.param_view
        param_view.on_input()

    app.bind_all("<Key>", debounce_handler)  # 绑定所有键盘事件
    app.bind_all("<Button>", debounce_handler)  # 绑定所有鼠标按钮事件
    app.bind_all("<MouseWheel>", debounce_handler)  # 绑定滚轮事件


if __name__ == '__main__':
    app = MyApplication()
    listen_input(app)
    app.mainloop()
