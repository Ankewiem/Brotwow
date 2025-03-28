import tkinter as tk #Thư viện tạo giao diện đồ họa
from tkinter import font as tkfont #Quản lý font chữ trong tkinter
from PIL import Image, ImageTk, ImageDraw #XXử lý ảnh
import os
import sys #Hệ thống


class ImageViewerApp:
    # Tạo cửa sổ chính với tiêu đề "Wow Images" với mã màu
    def __init__(self, root):
        self.root = root
        self.root.title("Wow Images")
        self.root.configure(bg="#536186")
       
        # Lưu ảnh hiện đang hiển thị
        self.current_photo = None
       
        # Cài icon vào giao diện
        self.set_window_icon(r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\BW logo.png")
       
        # Các hình ảnh và text được hiển thị(nội dung chính)
        self.images = [
            {"title": "FLOWER", "desc": " This area consists of several smaller bulbs around the main cardioid, forming petal-like structures. These symmetric patterns resemble a flower and showcase the fractal's repetitive, cyclical nature.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\FLOWER.png"},
            {"title": "JULIA ISLAND", "desc": "Refers to regions where the fractal resembles isolated clusters, similar to islands. These areas are connected to Julia sets and exhibit intricate and disconnected patterns when zoomed in.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\JULIA ISLAND.png"},
            {"title": "SEAHORSE VALLEY", "desc": "Known for its detailed, spiral-like structures resembling seahorses. It's located near the main cardioid and displays intricate, branching patterns that become more complex with zooming.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\SEAHORSE VALLEY.png"},
            {"title": "STARFISH", "desc": "A region where radial symmetry emerges, with arms extending outward from a central core. These arms appear similar to the limbs of a starfish and show how fractals exhibit radiating patterns.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\STARFISH.png"},
            {"title": "SUN", "desc": "Characterized by patterns that resemble sun rays, this area displays radial structures with bursts or rays emanating from a center, reflecting the fractal's infinite complexity.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\SUN.png"},
            {"title": "TENDRILS", "desc": "Long, winding, thread-like branches that appear as you zoom into the Mandelbrot Set. These delicate, fine structures are an example of the set's recursive, fractal nature.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\TENDRILS.png"},
            {"title": "TREE", "desc": "This region shows branching structures that resemble the trunk and branches of a tree. As you zoom in, these branches subdivide further, demonstrating the fractal's self-similarity.", "path": r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\TREE.png"}
        ]
       
        self.current_index = 0
        self.root.minsize(800, 950)
       
        # Hiệu ứng Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.desc_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
       
        # Khung chính mở rộng theo cả hai chiều, cách lề ngang 20px, lề dọc 30px (trang trí)
        self.main_frame = tk.Frame(root, bg="#536186")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=30)
       
        # Khung chứa text
        self.header_frame = tk.Frame(self.main_frame, bg="#B0C4DE")
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
       
        # Title label
        self.title_label = tk.Label(self.header_frame,
                                  text="",
                                  font=self.title_font,
                                  fg="#363636",
                                  bg="#B0C4DE",
                                  pady=5)
        self.title_label.pack()
       
        # Description label
        self.desc_label = tk.Label(self.header_frame,
                                 text="",
                                 font=self.desc_font,
                                 fg="#536186",
                                 bg="#B0C4DE",
                                 wraplength=750,
                                 justify=tk.CENTER,
                                 padx=20)
        self.desc_label.pack(fill=tk.X, expand=True, pady=(0, 10))
       
        # Navigation buttons frame - thay đổi ở đây
        self.nav_frame = tk.Frame(self.main_frame, bg="#B0C4DE")
        self.nav_frame.pack(fill=tk.X, pady=(0, 20))
       
        # Create navigation buttons - điều chỉnh lại khoảng cách
        self.create_navigation_buttons()
       
        # Image frame
        self.image_frame = tk.Frame(self.main_frame, bg="#B0C4DE")
        self.image_frame.pack(expand=True, fill=tk.BOTH)
       
        # Canvas for image display
        self.canvas_size = 600
        self.canvas = tk.Canvas(self.image_frame,
                               width=self.canvas_size,
                               height=self.canvas_size,
                               bg="#B0C4DE",
                               highlightthickness=0,
                               bd=0)
        self.canvas.pack(expand=True)
       
        # Show first image
        self.show_image()
   
    def set_window_icon(self, icon_path):
        """Set small window icon"""
        try:
            if os.path.exists(icon_path):
                if not icon_path.lower().endswith('.ico'):
                    img = Image.open(icon_path)
                    img.save("temp_icon.ico", format='ICO')
                    self.root.iconbitmap("temp_icon.ico")
                    os.remove("temp_icon.ico")
                else:
                    self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting window icon: {e}", file=sys.stderr)
   
    def create_navigation_buttons(self):
        """Create navigation buttons - điều chỉnh để nút PREV sát lề hơn"""
        # Bỏ spacer bên trái để nút PREV sát lề hơn
        # Previous button - đặt trực tiếp vào frame không qua spacer
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
        self.prev_btn.pack(side=tk.LEFT, anchor='w', padx=(0, 10))  # Thêm padding phải nhỏ
       
        # Center spacer
        tk.Frame(self.nav_frame, bg="#9099C4").pack(side=tk.LEFT, expand=True)
       
        # Next button
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
       
        # Hover effects
        self.prev_btn.bind("<Enter>", lambda e: self.prev_btn.config(bg="#D3D3D3"))
        self.prev_btn.bind("<Leave>", lambda e: self.prev_btn.config(bg="#9099C4"))
        self.next_btn.bind("<Enter>", lambda e: self.next_btn.config(bg="#D3D3D3"))
        self.next_btn.bind("<Leave>", lambda e: self.next_btn.config(bg="#9099C4"))
   
    # Các phương thức còn lại giữ nguyên...
    def show_image(self):
        current_img = self.images[self.current_index]
        self.title_label.config(text=current_img["title"])
        self.desc_label.config(text=current_img["desc"])
        self.canvas.delete("all")
       
        try:
            img = Image.open(current_img["path"])
            width, height = img.size
            ratio = min((self.canvas_size)/width, (self.canvas_size)/height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
           
            # Lưu trữ reference đến ảnh
            self.current_photo = ImageTk.PhotoImage(img)
           
            x_pos = (self.canvas_size - new_size[0]) // 2
            y_pos = (self.canvas_size - new_size[1]) // 2
            self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.current_photo)
        except Exception as e:
            self.canvas.create_text(self.canvas_size//2, self.canvas_size//2,
                                  text=f"Error loading image\n{str(e)}",
                                  font=tkfont.Font(size=14),
                                  fill="red")
       
        self.update_button_states()
   
    def update_button_states(self):
        """Update button states"""
        if self.current_index == 0:
            self.prev_btn.config(state=tk.DISABLED, bg="#9099C4", fg="#E0E0E0")
        else:
            self.prev_btn.config(state=tk.NORMAL, bg="#4b69b9", fg="white")
       
        if self.current_index == len(self.images)-1:
            self.next_btn.config(state=tk.DISABLED, bg="#9099C4", fg="#E0E0E0")
        else:
            self.next_btn.config(state=tk.NORMAL, bg="#4b69b9", fg="white")
   
    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
   
    def next_image(self):
        if self.current_index < len(self.images)-1:
            self.current_index += 1
            self.show_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.geometry("900x1000")
    root.mainloop()
