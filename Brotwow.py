import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.colorchooser import askcolor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk


class BrotWowapp:
    def __init__(self, root):
        """Lớp chính tạo giao diện ứng dụng BrotWow"""
        self.root = root
        self.root.title("BrotWow")  # Đặt tiêu đề cửa sổ
        self.root.geometry("800x600")  # Kích thước cửa sổ
       
        # Tải hình ảnh logo để làm biểu tượng cửa sổ
        self.logo = Image.open(r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/BW logo.png")
        self.logo = self.logo.resize((32, 32))  # Thay đổi kích thước logo
        self.logo = ImageTk.PhotoImage(self.logo)  # Chuyển đổi sang định dạng Tkinter


        # Đặt biểu tượng cửa sổ
        self.root.iconphoto(False, self.logo)
        self.root.config(bg="#C7D6F7")  # Màu nền chính


        # Nhãn hiển thị "Welcome to BrotWow" với font chữ đậm
        self.label = tk.Label(root, text="Welcome to BrotWow!", font=("Adobe Clean", 40, "bold"), fg="#536186", bg="#C7D6F7")
        self.label.pack(pady=40)  # Thêm padding dọc


        # Tạo các nút tùy chỉnh
        # Nút xem tương tác Mandelbrot
        self.new_button = ctk.CTkButton(root, text="INTERACTIVE VIEW", width=200, height=50, command=self.open_mandelbrot_view,
                                      corner_radius=20, fg_color="#536186", hover_color="#809BC4", font=("Roboto", 17),
                                      border_width=2, border_color="gray")
        self.new_button.pack(pady=10)  # Thêm padding dọc


        # Nút xem hình ảnh Wow
        self.open_button = ctk.CTkButton(root, text="WOW IMAGES", width=200, height=50, command=self.open_wow_images,
                                       corner_radius=20, fg_color="#536186", hover_color="#809BC4", font=("Roboto", 17),
                                       border_width=2, border_color="gray")
        self.open_button.pack(pady=10)


        # Nút thoát ứng dụng
        self.exit_button = ctk.CTkButton(root, text="EXIT", width=200, height=50, command=self.exit_app,
                                       corner_radius=20, fg_color="#536186", hover_color="#809BC4", font=("Roboto", 17),
                                       border_width=2, border_color="gray")
        self.exit_button.pack(pady=10)
   
    def open_mandelbrot_view(self):
        """Mở cửa sổ xem Mandelbrot tương tác"""
        self.root.withdraw()  # Ẩn cửa sổ chính
        mandelbrot_window = tk.Toplevel()  # Tạo cửa sổ mới
        # Xử lý khi đóng cửa sổ
        mandelbrot_window.protocol("WM_DELETE_WINDOW", lambda: self.close_mandelbrot_view(mandelbrot_window))
        # Tạo ứng dụng MandelbrotViewer trong cửa sổ mới
        mandelbrot_app = MandelbrotViewer(mandelbrot_window, self)


    def close_mandelbrot_view(self, window):
        """Đóng cửa sổ xem Mandelbrot và hiển thị lại cửa sổ chính"""
        window.destroy()  # Hủy cửa sổ
        self.root.deiconify()  # Hiển thị lại cửa sổ chính


    def open_wow_images(self):
        """Mở cửa sổ xem hình ảnh Wow"""
        self.root.withdraw()  # Ẩn cửa sổ chính
        wow_images_window = tk.Toplevel()  # Tạo cửa sổ mới
        # Xử lý khi đóng cửa sổ
        wow_images_window.protocol("WM_DELETE_WINDOW", lambda: self.close_wow_images(wow_images_window))
        # Tạo ứng dụng WowImagesApp trong cửa sổ mới
        wow_images_app = WowImagesApp(wow_images_window, self)


    def close_wow_images(self, window):
        """Đóng cửa sổ hình ảnh Wow và hiển thị lại cửa sổ chính"""
        window.destroy()  # Hủy cửa sổ
        self.root.deiconify()  # Hiển thị lại cửa sổ chính


    def exit_app(self):
        """Thoát ứng dụng sau khi xác nhận"""
        response = messagebox.askyesno("Exit", "Do you want to exit?")  # Hộp thoại xác nhận
        if response:  # Nếu người dùng chọn Yes
            self.root.quit()  # Thoát ứng dụng


    def mainloop(self):
        """Vòng lặp chính của ứng dụng"""
        self.root.mainloop()


class WowImagesApp:
    def __init__(self, root, main_app):
        """Lớp quản lý giao diện xem hình ảnh Wow"""
        self.root = root
        self.main_app = main_app  # Tham chiếu đến ứng dụng chính
        self.root.title("Wow Images")  # Tiêu đề cửa sổ
        self.root.configure(bg="#536186")  # Màu nền
       
        self.current_photo = None  # Ảnh hiện tại đang hiển thị
       
        # Đặt biểu tượng cửa sổ
        self.set_window_icon(r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/BW logo.png")
       
        # Danh sách các hình ảnh với thông tin mô tả
        self.images = [
            {"title": "FLOWER", "desc": " This area consists of several smaller bulbs around the main cardioid, forming petal-like structures. These symmetric patterns resemble a flower and showcase the fractal's repetitive, cyclical nature.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/FLOWER.png"},
            {"title": "JULIA ISLAND", "desc": "Refers to regions where the fractal resembles isolated clusters, similar to islands. These areas are connected to Julia sets and exhibit intricate and disconnected patterns when zoomed in.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/JULIA ISLAND.png"},
            {"title": "SEAHORSE VALLEY", "desc": "Known for its detailed, spiral-like structures resembling seahorses. It's located near the main cardioid and displays intricate, branching patterns that become more complex with zooming.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/SEAHORSE VALLEY.png"},
            {"title": "STARFISH", "desc": "A region where radial symmetry emerges, with arms extending outward from a central core. These arms appear similar to the limbs of a starfish and show how fractals exhibit radiating patterns.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/STARFISH.png"},
            {"title": "SUN", "desc": "Characterized by patterns that resemble sun rays, this area displays radial structures with bursts or rays emanating from a center, reflecting the fractal's infinite complexity.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/SUN.png"},
            {"title": "TENDRILS", "desc": "Long, winding, thread-like branches that appear as you zoom into the Mandelbrot Set. These delicate, fine structures are an example of the set's recursive, fractal nature.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/TENDRILS.png"},
            {"title": "TREE", "desc": "This region shows branching structures that resemble the trunk and branches of a tree. As you zoom in, these branches subdivide further, demonstrating the fractal's self-similarity.", "path": r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/TREE.png"}
        ]
       
        self.current_index = 0  # Chỉ số hình ảnh hiện tại
        self.root.minsize(800, 950)  # Kích thước tối thiểu của cửa sổ
       
        # Các font chữ sử dụng
        self.title_font = tk.font.Font(family="Helvetica", size=22, weight="bold")
        self.desc_font = tk.font.Font(family="Helvetica", size=12)
        self.button_font = tk.font.Font(family="Helvetica", size=14, weight="bold")
       
        # Khung chính
        self.main_frame = tk.Frame(root, bg="#536186")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=30)
       
        # Khung header chứa nút back
        self.header_frame = tk.Frame(self.main_frame, bg="#B0C4DE")
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
       
        # Nút quay lại
        self.back_button = tk.Button(
            self.header_frame,
            text="← BACK",
            command=self.go_back,
            bg="#9099C4",
            fg="white",
            relief=tk.FLAT,
            font=self.button_font,
            padx=15,
            pady=5,
            borderwidth=0,
            highlightthickness=0
        )
        self.back_button.pack(side=tk.LEFT, anchor='w', padx=10)
       
        # Nhãn tiêu đề hình ảnh
        self.title_label = tk.Label(self.header_frame,
                                  text="",
                                  font=self.title_font,
                                  fg="#363636",
                                  bg="#B0C4DE",
                                  pady=5)
        self.title_label.pack(side=tk.LEFT, expand=True)
       
        # Nhãn mô tả hình ảnh
        self.desc_label = tk.Label(self.header_frame,
                                 text="",
                                 font=self.desc_font,
                                 fg="#536186",
                                 bg="#B0C4DE",
                                 wraplength=750,
                                 justify=tk.CENTER,
                                 padx=20)
        self.desc_label.pack(fill=tk.X, expand=True, pady=(0, 10))
       
        # Khung chứa nút điều hướng
        self.nav_frame = tk.Frame(self.main_frame, bg="#B0C4DE")
        self.nav_frame.pack(fill=tk.X, pady=(0, 20))
       
        # Tạo các nút điều hướng
        self.create_navigation_buttons()
       
        # Khung hiển thị hình ảnh
        self.image_frame = tk.Frame(self.main_frame, bg="#B0C4DE")
        self.image_frame.pack(expand=True, fill=tk.BOTH)
       
        # Canvas để hiển thị hình ảnh
        self.canvas_size = 600
        self.canvas = tk.Canvas(self.image_frame,
                               width=self.canvas_size,
                               height=self.canvas_size,
                               bg="#B0C4DE",
                               highlightthickness=0,
                               bd=0)
        self.canvas.pack(expand=True)
       
        # Hiển thị hình ảnh đầu tiên
        self.show_image()
   
    def go_back(self):
        """Quay lại giao diện chính"""
        self.root.destroy()  # Đóng cửa sổ hiện tại
        self.main_app.root.deiconify()  # Hiển thị lại cửa sổ chính
   
    def set_window_icon(self, icon_path):
        """Đặt biểu tượng cho cửa sổ"""
        try:
            if icon_path.lower().endswith('.ico'):
                self.root.iconbitmap(icon_path)  # Sử dụng trực tiếp nếu là file .ico
            else:
                # Chuyển đổi sang định dạng .ico tạm thời nếu không phải
                img = Image.open(icon_path)
                img.save("temp_icon.ico", format='ICO')
                self.root.iconbitmap("temp_icon.ico")
                import os
                os.remove("temp_icon.ico")  # Xóa file tạm sau khi sử dụng
        except Exception as e:
            print(f"Error setting window icon: {e}")  # In lỗi nếu có
   
    def create_navigation_buttons(self):
        """Tạo các nút điều hướng hình ảnh"""
        # Nút xem hình trước
        self.prev_btn = tk.Button(
            self.nav_frame,
            text="⏪ PREV",
            command=self.prev_image,
            bg="#9099C4",
            fg="white",
            relief=tk.FLAT,
            font=self.button_font,
            padx=15,
            pady=5,
            borderwidth=0,
            highlightthickness=0
        )
        self.prev_btn.pack(side=tk.LEFT, anchor='w', padx=(0, 10))
       
        # Khung trống để căn giữa
        tk.Frame(self.nav_frame, bg="#9099C4").pack(side=tk.LEFT, expand=True)
       
        # Nút xem hình tiếp theo
        self.next_btn = tk.Button(
            self.nav_frame,
            text="NEXT ⏩",
            command=self.next_image,
            bg="#9099C4",
            fg="white",
            relief=tk.FLAT,
            font=self.button_font,
            padx=15,
            pady=5,
            borderwidth=0,
            highlightthickness=0
        )
        self.next_btn.pack(side=tk.RIGHT, anchor='e')
       
        # Hiệu ứng khi di chuột qua nút
        self.prev_btn.bind("<Enter>", lambda e: self.prev_btn.config(bg="#D3D3D3"))
        self.prev_btn.bind("<Leave>", lambda e: self.prev_btn.config(bg="#9099C4"))
        self.next_btn.bind("<Enter>", lambda e: self.next_btn.config(bg="#D3D3D3"))
        self.next_btn.bind("<Leave>", lambda e: self.next_btn.config(bg="#9099C4"))
   
    def show_image(self):
        """Hiển thị hình ảnh hiện tại"""
        current_img = self.images[self.current_index]
        self.title_label.config(text=current_img["title"])  # Cập nhật tiêu đề
        self.desc_label.config(text=current_img["desc"])  # Cập nhật mô tả
        self.canvas.delete("all")  # Xóa hình ảnh cũ
       
        try:
            # Mở và xử lý hình ảnh
            img = Image.open(current_img["path"])
            width, height = img.size
            # Tính tỷ lệ để phù hợp với kích thước canvas
            ratio = min((self.canvas_size)/width, (self.canvas_size)/height)
            new_size = (int(width * ratio), int(height * ratio))
            # Thay đổi kích thước hình ảnh
            img = img.resize(new_size, Image.Resampling.LANCZOS)
           
            # Chuyển đổi sang định dạng PhotoImage của Tkinter
            self.current_photo = ImageTk.PhotoImage(img)
           
            # Tính vị trí để căn giữa hình ảnh
            x_pos = (self.canvas_size - new_size[0]) // 2
            y_pos = (self.canvas_size - new_size[1]) // 2
            # Hiển thị hình ảnh trên canvas
            self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.current_photo)
        except Exception as e:
            # Hiển thị thông báo lỗi nếu không tải được hình ảnh
            self.canvas.create_text(self.canvas_size//2, self.canvas_size//2,
                                  text=f"Error loading image\n{str(e)}",
                                  font=tk.font.Font(size=14),
                                  fill="red")
       
        # Cập nhật trạng thái các nút điều hướng
        self.update_button_states()
   
    def update_button_states(self):
        """Cập nhật trạng thái của các nút điều hướng"""
        # Vô hiệu hóa nút PREV nếu đang ở hình đầu tiên
        if self.current_index == 0:
            self.prev_btn.config(state=tk.DISABLED, bg="#9099C4", fg="#E0E0E0")
        else:
            self.prev_btn.config(state=tk.NORMAL, bg="#4b69b9", fg="white")
       
        # Vô hiệu hóa nút NEXT nếu đang ở hình cuối cùng
        if self.current_index == len(self.images)-1:
            self.next_btn.config(state=tk.DISABLED, bg="#9099C4", fg="#E0E0E0")
        else:
            self.next_btn.config(state=tk.NORMAL, bg="#4b69b9", fg="white")
   
    def prev_image(self):
        """Xem hình ảnh trước đó"""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
   
    def next_image(self):
        """Xem hình ảnh tiếp theo"""
        if self.current_index < len(self.images)-1:
            self.current_index += 1
            self.show_image()


class MandelbrotViewer:
    def __init__(self, root, main_app):
        """Lớp xem Mandelbrot và Julia tương tác"""
        self.root = root
        self.main_app = main_app  # Tham chiếu đến ứng dụng chính
        self.root.title("BrotWow - Mandelbrot & Julia Explorer")  # Tiêu đề cửa sổ
        self.setup_constants()  # Thiết lập các hằng số
        self.setup_ui()  # Thiết lập giao diện người dùng
        self.draw_mandel()  # Vẽ tập Mandelbrot
        self.draw_julia(self.current_c, self.ax_julia)  # Vẽ tập Julia
       
        # Thêm nút quay lại vào bảng điều khiển
        self.add_back_button()


    def add_back_button(self):
        """Thêm nút quay lại giao diện chính"""
        back_button = tk.Button(
            self.right_frame,
            text="← BACK TO MAIN",
            command=self.go_back,
            bg="#9099C4",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=5,
            borderwidth=0,
            highlightthickness=0
        )
        back_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
       
        # Hiệu ứng khi di chuột qua nút
        back_button.bind("<Enter>", lambda e: back_button.config(bg="#D3D3D3"))
        back_button.bind("<Leave>", lambda e: back_button.config(bg="#9099C4"))


    def go_back(self):
        """Quay lại giao diện chính"""
        self.root.destroy()  # Đóng cửa sổ hiện tại
        self.main_app.root.deiconify()  # Hiển thị lại cửa sổ chính


    def setup_constants(self):
        """Khởi tạo các hằng số và biến"""
        self.WIDTH, self.HEIGHT = 1400, 1150  # Kích thước cửa sổ
        self.INITIAL_ITER = 23  # Số lần lặp ban đầu
        self.ZOOM_OUT_FACTOR = 1.5  # Hệ số phóng to
        self.ZOOM_IN_FACTOR = 1 / self.ZOOM_OUT_FACTOR  # Hệ số thu nhỏ
        self.colormap = "inferno"  # Bảng màu mặc định
       
        # Màu sắc giao diện
        self.BG_COLOR = "#B0C4DE"
        self.PANEL_COLOR = "#536186"
        self.TEXT_COLOR = "#536186"
        self.BUTTON_COLOR = "#D3D3D3"
        self.HOVER_COLOR = "#bacbe1"
        self.BUTTON_ACTIVE = "#a8b8d1"
        self.BUTTON_FG = "#536186"
        self.BORDER_COLOR = "#a0a0a0"
       
        # Font chữ
        self.FONT_LARGE = ("Segoe UI", 14, "bold")
        self.FONT_NORMAL = ("Segoe UI", 10)
        self.FONT_SMALL = ("Segoe UI", 9)
       
        # Biến toàn cục
        self.xmin, self.xmax = -2.5, 2.5  # Giới hạn trục x
        self.ymin, self.ymax = -2.0, 2.0  # Giới hạn trục y
        self.history = []  # Lịch sử các trạng thái xem
        self.current_state = {"xmin": self.xmin, "xmax": self.xmax, "ymin": self.ymin, "ymax": self.ymax}
        self.pan_start = None  # Vị trí bắt đầu khi pan
        self.current_c = complex(-0.7, 0.27)  # Giá trị phức mặc định cho Julia
       
        # Đặt kích thước cửa sổ
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.configure(bg=self.BG_COLOR)  # Màu nền
       
        try:
            # Thử đặt biểu tượng cửa sổ
            icon_img = tk.PhotoImage(file="BW logo.png")
            self.root.iconphoto(True, icon_img)
        except Exception as e:
            print("⚠️ Could not load window icon:", e)  # Thông báo nếu không tải được icon


    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.configure_styles()  # Cấu hình kiểu dáng
       
        # Khung chính
        self.main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.main_frame.pack(fill="both", expand=True)
       
        # Khung bên trái (hiển thị đồ họa)
        self.left_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.left_frame.pack(side="left", fill="both", expand=True)
       
        # Khung bên phải (bảng điều khiển)
        self.right_frame = tk.Frame(self.main_frame, bg=self.PANEL_COLOR, width=380)
        self.right_frame.pack(side="right", fill="y")
       
        # Thiết lập bảng điều khiển
        self.setup_control_panel()
       
        # Thiết lập các hình vẽ matplotlib
        self.setup_matplotlib_figures()
       
        # Thiết lập các sự kiện
        self.setup_event_bindings()


    def configure_styles(self):
        """Cấu hình kiểu dáng cho các widget"""
        style = ttk.Style()
        style.theme_use('clam')  # Sử dụng theme clam
       
        # Kiểu dáng cho khung
        style.configure('TFrame', background=self.PANEL_COLOR)
       
        # Kiểu dáng cho ô nhập liệu
        style.configure('TEntry',
                      fieldbackground='white',
                      foreground=self.BUTTON_FG,
                      bordercolor=self.BORDER_COLOR,
                      lightcolor=self.BORDER_COLOR,
                      darkcolor=self.BORDER_COLOR,
                      padding=5)
       
        # Kiểu dáng cho thanh trượt
        style.configure('Horizontal.TScale',
                      background=self.PANEL_COLOR,
                      troughcolor=self.BUTTON_COLOR,
                      bordercolor=self.BORDER_COLOR,
                      darkcolor=self.BORDER_COLOR,
                      lightcolor=self.BORDER_COLOR)


    def setup_control_panel(self):
        """Thiết lập bảng điều khiển bên phải"""
        # Nhãn tiêu đề
        title_label = tk.Label(self.right_frame, text="BROTWOW CONTROL PANEL",
                             font=("Segoe UI", 16, "bold"), fg="black", bg=self.PANEL_COLOR)
        title_label.pack(pady=15)
       
        # Khung điều khiển chính
        self.control_frame = tk.Frame(self.right_frame, bg=self.PANEL_COLOR)
        self.control_frame.pack(padx=10, pady=5, fill="both", expand=True)
       
        # Điều khiển số lần lặp
        self.setup_iteration_controls()
       
        # Tùy chọn màu sắc
        self.setup_color_options()
       
        # Xem trước Julia
        self.setup_julia_preview()
       
        # Điều khiển di chuyển
        self.setup_navigation_controls()


    def setup_iteration_controls(self):
        """Thiết lập điều khiển số lần lặp"""
        iter_frame = tk.Frame(self.control_frame, bg=self.PANEL_COLOR)
        iter_frame.pack(anchor="w", pady=5, fill="x")
       
        # Nhãn
        iter_label = tk.Label(iter_frame, text="MAX ITERATIONS:", fg="white",
                            bg=self.PANEL_COLOR, font=self.FONT_NORMAL)
        iter_label.pack(side="left")
       
        # Ô nhập số lần lặp
        self.iter_var = tk.StringVar()
        self.iter_var.set(str(self.INITIAL_ITER))
        self.iter_entry = ttk.Entry(iter_frame, textvariable=self.iter_var,
                                   width=8, font=self.FONT_NORMAL)
        # Xử lý sự kiện nhấn Enter
        self.iter_entry.bind('<Return>', self.validate_iteration_input)
        self.iter_entry.pack(side="left", padx=5)
       
        # Thanh trượt điều chỉnh số lần lặp
        self.iter_slider = ttk.Scale(self.control_frame, from_=1, to=150,
                                   orient="horizontal", command=self.on_iter_slider_change)
        self.iter_slider.set(self.INITIAL_ITER)
        self.iter_slider.pack(fill="x", pady=5)


    def setup_color_options(self):
        """Thiết lập tùy chọn màu sắc"""
        color_frame = tk.Frame(self.control_frame, bg=self.PANEL_COLOR)
        color_frame.pack(pady=5, fill="x")
       
        # Nút chọn màu
        color_button = self.create_beautiful_button(color_frame, "Color", self.choose_color, width=8)
        color_button.pack(side="left", padx=2)
       
        # Checkbox hiển thị trục tọa độ
        self.show_axes_var = tk.BooleanVar(value=True)
        axes_checkbox = tk.Checkbutton(
            color_frame, text="SHOW AXES", variable=self.show_axes_var,
            fg="white", bg=self.PANEL_COLOR, selectcolor=self.PANEL_COLOR,
            font=self.FONT_NORMAL, activebackground=self.PANEL_COLOR,
            activeforeground="white",
            command=lambda: [self.draw_mandel(), self.draw_julia(self.current_c, self.ax_julia)]
        )
        axes_checkbox.pack(side="left", padx=10)


    def setup_julia_preview(self):
        """Thiết lập xem trước tập Julia"""
        julia_frame = tk.Frame(self.control_frame, bg=self.PANEL_COLOR)
        julia_frame.pack(pady=5, fill="x")
       
        # Nhãn
        julia_label = tk.Label(julia_frame, text="JULIA PREVIEW", fg="white",
                              bg=self.PANEL_COLOR, font=self.FONT_NORMAL)
        julia_label.pack(anchor="w", pady=2)
       
        # Canvas để hiển thị tập Julia
        self.julia_canvas = tk.Canvas(julia_frame, width=350, height=350, bg="black",
                                    highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        self.julia_canvas.pack(pady=2)


    def setup_navigation_controls(self):
        """Thiết lập điều khiển di chuyển"""
        nav_frame = tk.Frame(self.control_frame, bg=self.PANEL_COLOR)
        nav_frame.pack(pady=15, fill="x")
       
        # Hàng trên cùng với các nút điều khiển chính
        top_row = tk.Frame(nav_frame, bg=self.PANEL_COLOR)
        top_row.pack(fill="x")
       
        # Nút phóng to
        zoom_in_btn = self.create_beautiful_button(top_row, "Zoom Out", self.zoom_in, width=8)
        zoom_in_btn.pack(side="left", padx=2)
       
        # Nút thu nhỏ
        zoom_out_btn = self.create_beautiful_button(top_row, "Zoom In", self.zoom_out, width=8)
        zoom_out_btn.pack(side="left", padx=2)
       
        # Nút về view mặc định
        home_button = self.create_beautiful_button(top_row, "Home", self.home_view, width=6)
        home_button.pack(side="left", padx=2)
       
        # Nút quay lại view trước đó
        undo_button = self.create_beautiful_button(top_row, "Undo", self.undo_view, width=6)
        undo_button.pack(side="left", padx=2)
       
        # Nút lưu hình ảnh
        save_button = self.create_beautiful_button(top_row, "Save", self.save_image, width=6)
        save_button.pack(side="left", padx=2)
       
        # Hàng dưới cùng với các nút di chuyển
        bottom_row = tk.Frame(nav_frame, bg=self.PANEL_COLOR)
        bottom_row.pack(fill="x", pady=5)
       
        # Nhãn
        tk.Label(bottom_row, text="PAN:", fg="white", bg=self.PANEL_COLOR,
                font=self.FONT_NORMAL).pack(side="left", padx=2)
       
        # Nút di chuyển lên
        up_btn = self.create_arrow_button(bottom_row, "↑", lambda: self.pan('up'))
        up_btn.pack(side="left", padx=2)
       
        # Khung chứa nút trái/phải
        middle_frame = tk.Frame(bottom_row, bg=self.PANEL_COLOR)
        middle_frame.pack(side="left")
       
        # Nút di chuyển trái
        left_btn = self.create_arrow_button(middle_frame, "←", lambda: self.pan('left'))
        left_btn.pack(side="left", padx=2)
       
        # Nút di chuyển phải
        right_btn = self.create_arrow_button(middle_frame, "→", lambda: self.pan('right'))
        right_btn.pack(side="left", padx=2)
       
        # Nút di chuyển xuống
        down_btn = self.create_arrow_button(bottom_row, "↓", lambda: self.pan('down'))
        down_btn.pack(side="left", padx=2)


    def setup_matplotlib_figures(self):
        """Thiết lập các hình vẽ matplotlib"""
        # Hình vẽ Mandelbrot
        self.fig_mandel = Figure(figsize=(10, 7), dpi=100)
        self.fig_mandel.patch.set_facecolor("#A1B0B9")  # Màu nền
        self.ax_mandel = self.fig_mandel.add_subplot(111)  # Tạo subplot
        self.ax_mandel.set_facecolor("black")  # Màu nền
        # Nhúng vào Tkinter
        self.canvas_mandel = FigureCanvasTkAgg(self.fig_mandel, master=self.left_frame)
        self.canvas_mandel.get_tk_widget().pack(fill="both", expand=True)
       
        # Hình vẽ Julia
        self.fig_julia = Figure(figsize=(3.5, 3.5), dpi=100)
        self.fig_julia.patch.set_facecolor("#536186")
        self.ax_julia = self.fig_julia.add_subplot(111)
        self.ax_julia.set_facecolor("black")
        # Nhúng vào Tkinter
        self.canvas_julia = FigureCanvasTkAgg(self.fig_julia, master=self.julia_canvas)
        self.canvas_julia.get_tk_widget().pack(fill="both", expand=True)


    def setup_event_bindings(self):
        """Thiết lập các sự kiện cho canvas"""
        # Các sự kiện chuột
        self.canvas_mandel.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas_mandel.mpl_connect('button_press_event', self.on_click)
        self.canvas_mandel.mpl_connect('button_press_event', self.on_press)
        self.canvas_mandel.mpl_connect('button_release_event', self.on_release)
        self.canvas_mandel.mpl_connect('scroll_event', self.on_scroll)


    def create_beautiful_button(self, parent, text, command, width=None):
        """Tạo nút có hiệu ứng đẹp khi di chuột qua"""
        btn = tk.Button(parent,
                      text=text,
                      command=command,
                      bg=self.BUTTON_COLOR,
                      fg=self.BUTTON_FG,
                      activebackground=self.HOVER_COLOR,
                      activeforeground=self.BUTTON_FG,
                      font=self.FONT_NORMAL,
                      bd=0,
                      highlightthickness=1,
                      highlightbackground=self.BORDER_COLOR,
                      highlightcolor=self.BORDER_COLOR,
                      relief="raised",
                      padx=8,
                      pady=2,
                      width=width)
       
        # Hiệu ứng khi di chuột qua
        btn.config(overrelief="groove")
        btn.bind("<Enter>", lambda e: btn.config(bg=self.HOVER_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.BUTTON_COLOR))
        return btn


    def create_arrow_button(self, parent, text, command):
        """Tạo nút mũi tên"""
        btn = tk.Button(parent,
                      text=text,
                      command=command,
                      bg=self.BUTTON_COLOR,
                      fg=self.BUTTON_FG,
                      activebackground=self.HOVER_COLOR,
                      activeforeground=self.BUTTON_FG,
                      font=self.FONT_NORMAL,
                      bd=0,
                      highlightthickness=1,
                      highlightbackground=self.BORDER_COLOR,
                      highlightcolor=self.BORDER_COLOR,
                      relief="raised",
                      padx=0,
                      pady=0,
                      width=3)
       
        # Hiệu ứng khi di chuột qua
        btn.config(overrelief="groove")
        btn.bind("<Enter>", lambda e: btn.config(bg=self.HOVER_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.BUTTON_COLOR))
        return btn


    def mandelbrot(self, xmin, xmax, ymin, ymax, width, height, max_iter):
        """Tính toán tập Mandelbrot"""
        # Tạo lưới điểm phức
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        div_time = np.zeros(Z.shape, dtype=int)


        # Tính toán số lần lặp cho mỗi điểm
        for i in range(max_iter):
            mask = np.abs(Z) < 2  # Chỉ tính toán các điểm chưa phân kỳ
            Z[mask] = Z[mask]**2 + C[mask]
            div_time[mask] += 1
        return div_time


    def julia(self, c, xmin, xmax, ymin, ymax, width, height, max_iter):
        """Tính toán tập Julia"""
        # Tạo lưới điểm phức
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        div_time = np.zeros(Z.shape, dtype=int)


        # Tính toán số lần lặp cho mỗi điểm
        for i in range(max_iter):
            mask = np.abs(Z) < 2  # Chỉ tính toán các điểm chưa phân kỳ
            Z[mask] = Z[mask]**2 + c
            div_time[mask] += 1
        return div_time


    def draw_mandel(self):
        """Vẽ tập Mandelbrot"""
        self.ax_mandel.clear()  # Xóa hình cũ
        current_iter = int(self.iter_slider.get())  # Lấy số lần lặp hiện tại
        # Tính toán dữ liệu Mandelbrot
        data = self.mandelbrot(self.xmin, self.xmax, self.ymin, self.ymax,
                              self.WIDTH, self.HEIGHT, current_iter)
        # Hiển thị hình ảnh
        self.ax_mandel.imshow(data, extent=[self.xmin, self.xmax, self.ymin, self.ymax],
                            cmap=self.colormap, origin='lower')


        # Hiển thị hoặc ẩn trục tọa độ
        if self.show_axes_var.get():
            self.ax_mandel.set_xlabel("Real")
            self.ax_mandel.set_ylabel("Imaginary")
        else:
            self.ax_mandel.set_xticks([])
            self.ax_mandel.set_yticks([])


        # Đặt tiêu đề
        self.ax_mandel.set_title("MANDELBROT SET", color="Black")
        self.canvas_mandel.draw()  # Vẽ lại canvas
        self.update_iter_display()  # Cập nhật hiển thị số lần lặp


    def draw_julia(self, c, ax):
        """Vẽ tập Julia"""
        ax.clear()  # Xóa hình cũ
        current_iter = int(self.iter_slider.get())  # Lấy số lần lặp hiện tại
        # Tính toán dữ liệu Julia
        data = self.julia(c, -2, 2, -2, 2, 350, 350, current_iter)
        # Hiển thị hình ảnh
        ax.imshow(data, extent=[-2, 2, -2, 2], cmap=self.colormap, origin='lower')
       
        # Hiển thị hoặc ẩn trục tọa độ
        if self.show_axes_var.get():
            ax.set_xlabel("Real")
            ax.set_ylabel("Imaginary")
        else:
            ax.set_xticks([])
            ax.set_yticks([])
       
        # Đặt tiêu đề với giá trị phức hiện tại
        ax.set_title(f"JULIA SET at ({c.real:.3f}, {c.imag:.3f})",
                    color="Black",
                    fontsize=10)
        self.canvas_julia.draw()  # Vẽ lại canvas


    def update_julia_preview(self, c):
        """Cập nhật xem trước tập Julia"""
        self.current_c = c  # Cập nhật giá trị phức hiện tại
        self.draw_julia(c, self.ax_julia)  # Vẽ lại tập Julia


    def on_motion(self, event):
        """Xử lý sự kiện di chuyển chuột trên tập Mandelbrot"""
        if event.inaxes == self.ax_mandel:  # Nếu chuột trong vùng vẽ
            c = complex(event.xdata, event.ydata)  # Lấy tọa độ phức
            self.update_julia_preview(c)  # Cập nhật xem trước Julia


    def on_click(self, event):
        """Xử lý sự kiện nhấn chuột trên tập Mandelbrot"""
        if event.inaxes == self.ax_mandel:  # Nếu chuột trong vùng vẽ
            c = complex(event.xdata, event.ydata)  # Lấy tọa độ phức
            self.update_julia_preview(c)  # Cập nhật xem trước Julia


    def on_press(self, event):
        """Xử lý sự kiện nhấn chuột để bắt đầu pan"""
        if event.inaxes == self.ax_mandel and event.button == 1:  # Nút trái chuột
            self.pan_start = (event.xdata, event.ydata)  # Lưu vị trí bắt đầu


    def on_release(self, event):
        """Xử lý sự kiện thả chuột sau khi pan"""
        if self.pan_start and event.button == 1:  # Nếu đang trong chế độ pan
            self.save_state()  # Lưu trạng thái hiện tại
            x_center, y_center = self.pan_start  # Vị trí bắt đầu
            x_end, y_end = event.xdata, event.ydata  # Vị trí kết thúc
            dx = x_end - x_center  # Tính độ dịch chuyển theo x
            dy = y_end - y_center  # Tính độ dịch chuyển theo y
            # Cập nhật giới hạn tọa độ
            self.xmin -= dx
            self.xmax -= dx
            self.ymin -= dy
            self.ymax -= dy
            self.draw_mandel()  # Vẽ lại
            self.pan_start = None  # Kết thúc pan


    def on_scroll(self, event):
        """Xử lý sự kiện cuộn chuột để zoom"""
        if event.inaxes == self.ax_mandel:  # Nếu chuột trong vùng vẽ
            self.save_state()  # Lưu trạng thái hiện tại
            x_center = event.xdata  # Tọa độ x tâm zoom
            y_center = event.ydata  # Tọa độ y tâm zoom
            if event.button == 'up':  # Cuộn lên - zoom out
                width = (self.xmax - self.xmin) * self.ZOOM_OUT_FACTOR
                height = (self.ymax - self.ymin) * self.ZOOM_OUT_FACTOR
            else:  # Cuộn xuống - zoom in
                width = (self.xmax - self.xmin) * self.ZOOM_IN_FACTOR
                height = (self.ymax - self.ymin) * self.ZOOM_IN_FACTOR
               
            # Cập nhật giới hạn tọa độ
            self.xmin = x_center - width / 2
            self.xmax = x_center + width / 2
            self.ymin = y_center - height / 2
            self.ymax = y_center + height / 2
            self.draw_mandel()  # Vẽ lại


    def zoom_out(self):
        """Phóng to để xem nhiều hơn"""
        self.save_state()  # Lưu trạng thái hiện tại
        # Tính tâm hiện tại
        x_center = (self.xmin + self.xmax) / 2
        y_center = (self.ymin + self.ymax) / 2
        # Tính kích thước mới
        width = (self.xmax - self.xmin) * self.ZOOM_OUT_FACTOR
        height = (self.ymax - self.ymin) * self.ZOOM_OUT_FACTOR
        # Cập nhật giới hạn tọa độ
        self.xmin = x_center - width / 2
        self.xmax = x_center + width / 2
        self.ymin = y_center - height / 2
        self.ymax = y_center + height / 2
        self.draw_mandel()  # Vẽ lại


    def zoom_in(self):
        """Thu nhỏ để xem chi tiết"""
        self.save_state()  # Lưu trạng thái hiện tại
        # Tính tâm hiện tại
        x_center = (self.xmin + self.xmax) / 2
        y_center = (self.ymin + self.ymax) / 2
        # Tính kích thước mới
        width = (self.xmax - self.xmin) * self.ZOOM_IN_FACTOR
        height = (self.ymax - self.ymin) * self.ZOOM_IN_FACTOR
        # Cập nhật giới hạn tọa độ
        self.xmin = x_center - width / 2
        self.xmax = x_center + width / 2
        self.ymin = y_center - height / 2
        self.ymax = y_center + height / 2
        self.draw_mandel()  # Vẽ lại


    def pan(self, direction):
        """Di chuyển view theo hướng chỉ định"""
        self.save_state()  # Lưu trạng thái hiện tại
        # Tính độ dịch chuyển
        dx = (self.xmax - self.xmin) * 0.2
        dy = (self.ymax - self.ymin) * 0.2
       
        # Cập nhật giới hạn tọa độ theo hướng
        if direction == 'left':
            self.xmin -= dx
            self.xmax -= dx
        elif direction == 'right':
            self.xmin += dx
            self.xmax += dx
        elif direction == 'up':
            self.ymin += dy
            self.ymax += dy
        elif direction == 'down':
            self.ymin -= dy
            self.ymax -= dy
       
        self.draw_mandel()  # Vẽ lại


    def home_view(self):
        """Reset về view mặc định"""
        self.save_state()  # Lưu trạng thái hiện tại
        # Đặt lại giới hạn tọa độ mặc định
        self.xmin, self.xmax, self.ymin, self.ymax = -2.5, 2.5, -2.0, 2.0
        self.draw_mandel()  # Vẽ lại


    def undo_view(self):
        """Quay lại view trước đó"""
        if self.history:  # Nếu có lịch sử
            state = self.history.pop()  # Lấy trạng thái gần nhất
            # Khôi phục giới hạn tọa độ
            self.xmin, self.xmax, self.ymin, self.ymax = state["xmin"], state["xmax"], state["ymin"], state["ymax"]
            self.draw_mandel()  # Vẽ lại


    def save_state(self):
        """Lưu trạng thái view hiện tại"""
        state = {"xmin": self.xmin, "xmax": self.xmax, "ymin": self.ymin, "ymax": self.ymax}
        self.history.append(state)  # Thêm vào lịch sử


    def choose_color(self):
        """Mở hộp thoại chọn màu"""
        color = askcolor()[1]  # Hiển thị hộp thoại chọn màu
        if color:
            # Tạo bảng màu tùy chỉnh từ màu đã chọn đến đen
            self.colormap = LinearSegmentedColormap.from_list("custom_colormap", [color, "black"])
            self.draw_mandel()  # Vẽ lại Mandelbrot
            self.draw_julia(self.current_c, self.ax_julia)  # Vẽ lại Julia


    def save_image(self):
        """Lưu hình ảnh fractal hiện tại"""
        # Hiển thị hộp thoại chọn nơi lưu
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Fractal Image"
        )
        if filepath:  # Nếu người dùng chọn file
            dpi = 300  # Độ phân giải
            width_inches = 10  # Chiều rộng (inch)
            height_inches = 7  # Chiều cao (inch)
           
            # Tạo figure mới để lưu
            fig_save = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)
            ax_save = fig_save.add_subplot(111)
           
            # Tính toán dữ liệu Mandelbrot
            current_iter = int(self.iter_slider.get())
            data = self.mandelbrot(self.xmin, self.xmax, self.ymin, self.ymax,
                                 width_inches*dpi, height_inches*dpi, current_iter)
            # Hiển thị hình ảnh
            ax_save.imshow(data, extent=[self.xmin, self.xmax, self.ymin, self.ymax],
                         cmap=self.colormap, origin='lower')
           
            # Hiển thị hoặc ẩn trục tọa độ
            if self.show_axes_var.get():
                ax_save.set_xlabel("Real")
                ax_save.set_ylabel("Imaginary")
            else:
                ax_save.set_xticks([])
                ax_save.set_yticks([])
           
            # Đặt tiêu đề và lưu hình ảnh
            ax_save.set_title("MANDELBROT SET", color="Black")
            fig_save.savefig(filepath, dpi=dpi, bbox_inches='tight')
            plt.close(fig_save)  # Đóng figure


    def update_iter_display(self):
        """Cập nhật hiển thị số lần lặp"""
        current_iter = int(self.iter_slider.get())  # Lấy giá trị từ thanh trượt
        self.iter_entry.delete(0, tk.END)  # Xóa nội dung cũ
        self.iter_entry.insert(0, str(current_iter))  # Chèn giá trị mới


    def validate_iteration_input(self, event=None):
        """Kiểm tra tính hợp lệ của đầu vào số lần lặp"""
        try:
            new_iter = int(self.iter_var.get())  # Lấy giá trị nhập vào
            if 1 <= new_iter <= 150:  # Kiểm tra trong khoảng hợp lệ
                self.iter_slider.set(new_iter)  # Cập nhật thanh trượt
                self.draw_mandel()  # Vẽ lại Mandelbrot
                self.draw_julia(self.current_c, self.ax_julia)  # Vẽ lại Julia
                return True
            else:
                # Hiển thị cảnh báo nếu ngoài khoảng
                messagebox.showwarning("Invalid Value", "Please enter a value between 1 and 150")
                self.update_iter_display()  # Khôi phục giá trị hợp lệ
                return False
        except ValueError:
            # Hiển thị cảnh báo nếu không phải số
            messagebox.showwarning("Invalid Input", "Please enter a valid number")
            self.update_iter_display()  # Khôi phục giá trị hợp lệ
            return False


    def on_iter_slider_change(self, event):
        """Xử lý thay đổi trên thanh trượt số lần lặp"""
        self.update_iter_display()  # Cập nhật hiển thị
        self.draw_mandel()  # Vẽ lại Mandelbrot
        self.draw_julia(self.current_c, self.ax_julia)  # Vẽ lại Julia


if __name__ == "__main__":
    root = tk.Tk()  # Tạo cửa sổ chính
    app = BrotWowapp(root)  # Tạo ứng dụng
    app.mainloop()  # Chạy vòng lặp chính


