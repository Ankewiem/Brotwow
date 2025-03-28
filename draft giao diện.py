import tkinter as tk
from tkinter import Canvas, simpledialog
from tkinter import filedialog
from tkinter import colorchooser
from collections import deque
from PIL import Image, ImageTk, ImageDraw
import os


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Paint App")
root.geometry("1100x600")
root.minsize(800, 500)
root.configure(bg="#EDEBFA")  # Nền hồng nhạt




# Biến lưu kích thước mặc định của Canvas
DEFAULT_CANVAS_WIDTH = 830
DEFAULT_CANVAS_HEIGHT = 480




# Hàm đổi con trỏ chuột khi nhấn vào nút trên thanh công cụ
def change_cursor(cursor_type):
    root.config(cursor=cursor_type)


# Hàm vẽ đường thẳng
def start_line(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y




def draw_line(event):
    global start_x, start_y
    if drawing_mode == "line":
        line_id = canvas.create_line(start_x, start_y, event.x, event.y,
                                   fill=current_color,
                                   width=current_width)
        drawn_objects.append({
            'type': 'line',
            'id': line_id,
            'coords': [start_x, start_y, event.x, event.y],
            'width': current_width,
            'color': current_color
        })


# Hàm nhập văn bản
def insert_text(event):
    text = simpledialog.askstring("Nhập văn bản", "Nhập nội dung:")
    if text:
        canvas.create_text(event.x, event.y, text=text, font=("Arial", 16), fill="black")








# Thanh công cụ (màu xanh dương) - luôn ở trên
toolbar = tk.Frame(root, bg="#809BC4", height=50)
toolbar.pack(fill="x")












# Canvas chính (khu vực vẽ) - màu trắng, viền ngoài cùng màu xanh dương
canvas_frame = tk.Frame(root, bg="#809BC4")
canvas_frame.place(relx=0.5, rely=0.55, anchor="center")  # Luôn nằm giữa












canvas = Canvas(canvas_frame, bg="white", width=DEFAULT_CANVAS_WIDTH, height=DEFAULT_CANVAS_HEIGHT,
                bd=0, highlightthickness=5, highlightbackground="#809BC4")
canvas.pack(fill="both", expand=True)  # Cho phép mở rộng theo frame
















# Danh sách biểu tượng và kiểu con trỏ tương ứng
icons = [
    ("📁", "arrow"),    # Mở file
    ("✏️", "pencil"),   # Bút
    ("🔲", "cross"),    # hình vuông
    ("◯", "circle"),    # Hình tròn
    ("↩", "exchange"),  # Hoàn tác
    ("🌊", "spraycan"),   # fill màu
    ("🧽", "dotbox"),   # Tẩy
    ("➖", "tcross"),    # Vẽ đường thẳng
    ("🅰", "xterm"),     # Nhập chữ
    ("🎨", "circle")    # Colour Wheel
]




# Thêm nút vào thanh công cụ
for i, (icon, cursor_type) in enumerate(icons):
    btn = tk.Button(toolbar, text=icon, font=("Arial", 14), bg="#DCEAF9", bd=0,
                    command=lambda c=cursor_type: change_cursor(c))
    btn.grid(row=0, column=i, padx=10, pady=5)








# Sự kiện vẽ đường thẳng
canvas.bind("<ButtonPress-1>", start_line)
canvas.bind("<ButtonRelease-1>", draw_line)








# Sự kiện nhập văn bản khi nhấn vào canvas
canvas.bind("<Double-Button-1>", insert_text)




# Hàm tự động thay đổi kích thước Canvas khi cửa sổ thay đổi
def resize_canvas(event):
    new_width = root.winfo_width() - 100  # Trừ khoảng trống hai bên
    new_height = root.winfo_height() - 150  # Trừ khoảng trống từ thanh công cụ








    # Đảm bảo Canvas không bị thu nhỏ quá mức
    new_width = max(new_width, 500)
    new_height = max(new_height, 300)








    canvas.config(width=new_width, height=new_height)








    # Cập nhật vị trí khung chứa Canvas
    canvas_frame.place(relx=0.5, rely=0.55, anchor="center")








# Kết nối sự kiện thay đổi kích thước
root.bind("<Configure>", resize_canvas)




# Mặc định không vẽ gì
drawing_mode = "none"








# Thêm nút chọn bút chì để vẽ tự do
btn_pencil = tk.Button(toolbar, text="✏️", font=("Arial", 14), bg="#DCEAF9", bd=0,
                       command=lambda: set_mode("pencil"))
btn_pencil.grid(row=0, column=1, padx=10, pady=5)








# Biến lưu vị trí trước đó của chuột
last_x, last_y = None, None








def start_draw(event):
    """Khi nhấn chuột, chỉ bắt đầu vẽ nếu đang chọn pencil"""
    global last_x, last_y
    if drawing_mode == "pencil":
        last_x, last_y = event.x, event.y
    else:
        last_x, last_y = None, None  # Không lưu vị trí nếu không ở chế độ pencil








drawn_objects = []




def draw_pencil(event):
    global last_x, last_y
    if drawing_mode == "pencil" and last_x is not None and last_y is not None:
        line_id = canvas.create_line(last_x, last_y, event.x, event.y,
                                   fill=current_color,
                                   width=current_width,
                                   capstyle="round",
                                   smooth=True)
        # Lưu dưới dạng dictionary
        drawn_objects.append({
            'type': 'pencil',
            'id': line_id,
            'coords': [last_x, last_y, event.x, event.y],
            'width': current_width,
            'color': current_color
        })
        last_x, last_y = event.x, event.y








       
def scale_objects(scale_factor):
    """Phóng to hoặc thu nhỏ tất cả đối tượng trên Canvas"""
    for i, item in enumerate(drawn_objects):
        if isinstance(item, dict):  # Chỉ xử lý các đối tượng dictionary
            if 'id' in item and 'coords' in item and 'width' in item:
                # Scale tọa độ
                scaled_coords = [coord * scale_factor for coord in item['coords']]
                canvas.coords(item['id'], *scaled_coords)
               
                # Scale độ rộng nét vẽ
                new_width = max(1, int(item['width'] * scale_factor))
                canvas.itemconfig(item['id'], width=new_width)
               
                # Cập nhật lại thông tin
                item['coords'] = scaled_coords
                item['width'] = new_width
        elif isinstance(item, int):  # Xử lý các đối tượng là ID đơn giản
            # Lấy tọa độ hiện tại
            coords = canvas.coords(item)
            if coords:  # Nếu có tọa độ
                # Scale tọa độ
                scaled_coords = [coord * scale_factor for coord in coords]
                canvas.coords(item, *scaled_coords)


def reset_position(event):
    """Đặt lại vị trí khi nhả chuột"""
    global last_x, last_y
    last_x, last_y = None, None








canvas.bind("<ButtonPress-1>", start_draw)   # Khi nhấn chuột, bắt đầu vẽ
canvas.bind("<B1-Motion>", draw_pencil)      # Khi kéo chuột, vẽ tự do
canvas.bind("<ButtonRelease-1>", reset_position)  # Khi thả chuột, dừng vẽ








# Thêm chế độ vẽ hình vuông
btn_rectangle = tk.Button(toolbar, text="🔲", font=("Arial", 14), bg="#DCEAF9", bd=0,
                          command=lambda: set_mode("rectangle"))
btn_rectangle.grid(row=0, column=2, padx=10, pady=5)








# Biến lưu tọa độ vẽ hình
shape_start_x, shape_start_y = None, None
current_shape = None








def start_shape(event):
    """Bắt đầu vẽ hình vuông nếu chế độ rectangle được chọn"""
    global shape_start_x, shape_start_y, current_shape
    if drawing_mode == "rectangle":
        shape_start_x, shape_start_y = event.x, event.y
        current_shape = canvas.create_rectangle(shape_start_x, shape_start_y, shape_start_x, shape_start_y, outline="black", width=2)








def draw_shape(event):
    """Cập nhật hình vuông khi kéo chuột"""
    global current_shape
    if drawing_mode == "rectangle" and current_shape:
        canvas.coords(current_shape, shape_start_x, shape_start_y, event.x, event.y)




def finish_shape(event):
    global current_shape
    if drawing_mode == "rectangle" and current_shape:
        drawn_objects.append({
            'type': 'rectangle',
            'id': current_shape,
            'coords': canvas.coords(current_shape),
            'width': current_width,
            'color': current_color
        })
        current_shape = None




# Gán sự kiện vẽ hình vuông
canvas.bind("<ButtonPress-1>", start_shape)  
canvas.bind("<B1-Motion>", draw_shape)      
canvas.bind("<ButtonRelease-1>", finish_shape)  




# Cập nhật nút bấm
btn_pencil = tk.Button(toolbar, text="✏️", font=("Arial", 14), bg="#DCEAF9", bd=0,
                       command=lambda: set_mode("pencil"))
btn_pencil.grid(row=0, column=1, padx=10, pady=5)








btn_rectangle = tk.Button(toolbar, text="🔲", font=("Arial", 14), bg="#DCEAF9", bd=0,
                          command=lambda: set_mode("rectangle"))
btn_rectangle.grid(row=0, column=2, padx=10, pady=5)








# Thêm nút chọn tẩy
btn_eraser = tk.Button(toolbar, text="🧽", font=("Arial", 14), bg="#DCEAF9", bd=0,
                       command=lambda: set_mode("eraser"))
btn_eraser.grid(row=0, column=6, padx=10, pady=5)
















def set_mode(mode):
    global drawing_mode
    drawing_mode = mode
   
    # Xóa tất cả sự kiện cũ
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
   
    # Gán sự kiện cho từng chế độ
    if mode == "pencil":
        canvas.bind("<ButtonPress-1>", start_draw)
        canvas.bind("<B1-Motion>", draw_pencil)
        canvas.bind("<ButtonRelease-1>", reset_position)
    elif mode == "rectangle":
        canvas.bind("<ButtonPress-1>", start_shape)
        canvas.bind("<B1-Motion>", draw_shape)
        canvas.bind("<ButtonRelease-1>", finish_shape)
    elif mode == "line":
        canvas.bind("<ButtonPress-1>", start_line)
        canvas.bind("<ButtonRelease-1>", draw_line)
    elif mode == "eraser":
        canvas.bind("<ButtonPress-1>", start_erase)
        canvas.bind("<B1-Motion>", erase)
        canvas.bind("<ButtonRelease-1>", reset_position)
    elif mode == "circle":
        canvas.bind("<ButtonPress-1>", start_circle)
        canvas.bind("<B1-Motion>", draw_circle)
        canvas.bind("<ButtonRelease-1>", finish_circle)
    elif mode == "flood_fill":
        canvas.bind("<Button-1>", flood_fill)
        root.config(cursor="spraycan")


def start_erase(event):
    """Bắt đầu xóa khi nhấn chuột"""
    global last_x, last_y
    last_x, last_y = event.x, event.y
# Hàm erase cập nhật
def erase(event):
    """Xóa tại điểm click chuột với kích thước bằng độ rộng hiện tại"""
    if drawing_mode == "eraser":
        # Tạo một hình tròn nhỏ tại vị trí click để xóa
        x, y = event.x, event.y
        erase_size = current_width * 2  # Kích thước tẩy
       
        # Tạo hình oval trắng để "xóa" (thực chất là vẽ đè màu trắng)
        canvas.create_oval(x-erase_size, y-erase_size,
                          x+erase_size, y+erase_size,
                          fill="white", outline="white")
       
        # Cập nhật lại danh sách đối tượng (nếu cần)
        # Bạn có thể bỏ qua phần này nếu không cần undo cho thao tác xóa
        erase_id = canvas.create_oval(x-erase_size, y-erase_size,
                                    x+erase_size, y+erase_size,
                                    fill="white", outline="white")
        drawn_objects.append({
            'type': 'erase',
            'id': erase_id,
            'coords': [x-erase_size, y-erase_size, x+erase_size, y+erase_size],
            'color': 'white'
        })
def reset_position(event):
    """Đặt lại vị trí sau khi nhả chuột"""
    global last_x, last_y
    last_x, last_y = None, None




# Lưu ID của các hình đã vẽ
drawn_objects = []




def draw_shape(event):
    global current_shape
    if drawing_mode == "rectangle" and current_shape:
        canvas.coords(current_shape, shape_start_x, shape_start_y, event.x, event.y)




def finish_shape(event):
    global current_shape
    if drawing_mode == "rectangle" and current_shape:
        drawn_objects.append({
            'type': 'rectangle',
            'id': current_shape,
            'coords': canvas.coords(current_shape),
            'width': current_width,
            'color': current_color
        })
        current_shape = None
def insert_text(event):
    text = simpledialog.askstring("Nhập văn bản", "Nhập nội dung:")
    if text:
        text_id = canvas.create_text(event.x, event.y, text=text, font=("Arial", 16), fill="black")
        drawn_objects.append(text_id)  # Lưu ID của văn bản
def undo():
    if drawn_objects:
        last_item = drawn_objects.pop()  # Lấy phần tử cuối cùng
       
        if isinstance(last_item, dict):  # Nếu là dictionary
            canvas.delete(last_item['id'])
        elif isinstance(last_item, int):  # Nếu là ID đơn giản
            canvas.delete(last_item)
btn_undo = tk.Button(toolbar, text="↩", font=("Arial", 14), bg="#DCEAF9", bd=0, command=undo)
btn_undo.grid(row=0, column=4, padx=10, pady=5)




drawn_objects = deque(maxlen=100)  # Chỉ lưu 100 thao tác gần nhất
current_color = "black"








def choose_color():
    global current_color
    color = colorchooser.askcolor(title="Chọn màu")[1]  # Mở hộp thoại chọn màu
    if color:
        current_color = color  # Lưu màu được chọn
btn_color = tk.Button(toolbar, text="🎨", font=("Arial", 14), bg="#DCEAF9", bd=0, command=choose_color)
btn_color.grid(row=0, column=9, padx=10, pady=5)  # Thêm vào vị trí thích hợp trên toolbar








def start_shape(event):
    global shape_start_x, shape_start_y, current_shape
    if drawing_mode == "rectangle":
        shape_start_x, shape_start_y = event.x, event.y
        current_shape = canvas.create_rectangle(shape_start_x, shape_start_y, shape_start_x, shape_start_y, outline=current_color, width=2)








btn_line = tk.Button(toolbar, text="➖", font=("Arial", 14), bg="#DCEAF9", bd=0,
                     command=lambda: set_mode("line"))  # Gán chế độ "line"
btn_line.grid(row=0, column=7, padx=10, pady=5)




btn_circle = tk.Button(toolbar, text="◯", font=("Arial", 14), bg="#DCEAF9", bd=0,
                       command=lambda: set_mode("circle"))
btn_circle.grid(row=0, column=3, padx=10, pady=5)  # Đặt vị trí thích hợp




# Biến lưu vị trí bắt đầu và đối tượng hình tròn
circle_start_x, circle_start_y = None, None
current_circle = None






def start_circle(event):
    """Bắt đầu vẽ hình tròn"""
    global circle_start_x, circle_start_y, current_circle
    if drawing_mode == "circle":
        circle_start_x, circle_start_y = event.x, event.y
        current_circle = canvas.create_oval(circle_start_x, circle_start_y, circle_start_x, circle_start_y,
                                            outline=current_color, width=2)








def draw_circle(event):
    """Cập nhật hình tròn khi kéo chuột"""
    global current_circle
    if drawing_mode == "circle" and current_circle:
        canvas.coords(current_circle, circle_start_x, circle_start_y, event.x, event.y)




def finish_circle(event):
    """Hoàn tất vẽ hình tròn"""
    global current_circle
    if drawing_mode == "circle":
        drawn_objects.append(current_circle)  # Lưu vào danh sách để có thể hoàn tác
        current_circle = None  # Dừng cập nhật


def save_canvas():
    """Lưu nội dung Canvas dưới dạng file hình ảnh."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("All Files", "*.*")])
    if file_path:
        # Lấy kích thước của Canvas
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        width = canvas.winfo_width()
        height = canvas.winfo_height()


        # Chụp ảnh màn hình khu vực canvas
        image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        image.save(file_path)
        print("Đã lưu hình ảnh tại:", file_path)
btn_open = tk.Button(toolbar, text="📁", font=("Arial", 14), bg="#DCEAF9", bd=0, command=save_canvas)
btn_open.grid(row=0, column=0, padx=10, pady=5)




btn_zoom_in = tk.Button(toolbar, text="🔍+", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=lambda: scale_objects(1.2))  # Phóng to 20%
btn_zoom_in.grid(row=0, column=10, padx=10, pady=5)




btn_zoom_out = tk.Button(toolbar, text="🔍-", font=("Arial", 14), bg="#DCEAF9", bd=0,
                         command=lambda: scale_objects(0.8))  # Thu nhỏ 20%
btn_zoom_out.grid(row=0, column=11, padx=10, pady=5)




# Thêm ở phần khai báo biến toàn cục
current_width = 2  # Giá trị mặc định




# Thêm thanh trượt điều chỉnh độ rộng
width_slider = tk.Scale(toolbar, from_=1, to=20, orient="horizontal",
                       label="Độ rộng", command=lambda w: set_width(w))
width_slider.set(current_width)
width_slider.grid(row=0, column=12, padx=5)




def set_width(w):
    global current_width
    current_width = int(w)




def flood_fill(event):
    if drawing_mode != "flood_fill":
        return
   
    # Lấy tọa độ click
    x, y = event.x, event.y
   
    # Lấy màu tại điểm click
    item = canvas.find_closest(x, y)
    if not item:
        return
       
    # Tạo hình chữ nhật nhỏ để kiểm tra màu
    color = canvas.itemcget(item, "fill")
    if not color or color == "":  # Nếu không có màu fill
        color = canvas.itemcget(item, "outline")
   
    # Nếu trùng màu thì không làm gì
    if color == current_color:
        return
       
    # Tô màu đối tượng
    canvas.itemconfig(item, fill=current_color)
   
    # Lưu vào danh sách để undo
    drawn_objects.append({
        'type': 'fill',
        'id': item,
        'old_color': color,
        'new_color': current_color
    })


# Thay đổi command của nút spraycan (🌊)
btn_flood_fill = tk.Button(toolbar, text="🌊", font=("Arial", 14), bg="#DCEAF9", bd=0,
                          command=lambda: set_mode("flood_fill"))
btn_flood_fill.grid(row=0, column=5, padx=10, pady=5)


root.mainloop()


