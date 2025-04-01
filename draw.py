import tkinter as tk
from tkinter import Canvas, simpledialog
from tkinter import filedialog
from tkinter import colorchooser
from collections import deque
from PIL import Image, ImageTk, ImageDraw
import os
from PIL import ImageGrab


# Dictionary to store the original line width of each canvas item
original_widths = {}
# Track the cumulative scale factor for the entire canvas
cumulative_scale = 1.0
# List to store drawn objects
drawn_objects = deque(maxlen=100)

def draw(root, background_image=None):
    # Global declarations for variables used across functions
    global start_x, start_y, last_x, last_y, shape_start_x, shape_start_y, current_shape
    global circle_start_x, circle_start_y, current_circle, drawn_objects, current_color, current_width
    global drawing_mode
    # Tạo cửa sổ chính
    # root = tk.Tk()
    root.title("Paint App")
    root.geometry("1100x600")
    root.minsize(800, 500)




    # Thanh công cụ (màu xanh dương) - luôn ở trên
    toolbar = tk.Frame(root, bg="#809BC4", height=50)
    toolbar.pack(fill="x")




    # Biến lưu kích thước mặc định của Canvas
    DEFAULT_CANVAS_WIDTH = 830
    DEFAULT_CANVAS_HEIGHT = 480




    # Hàm đổi con trỏ chuột khi nhấn vào nút trên thanh công cụ
    def change_cursor(cursor_type):
        root.config(cursor=cursor_type)




    # Canvas chính (khu vực vẽ) - màu trắng, viền ngoài cùng màu xanh dương
    canvas_frame = tk.Frame(root, bg="#809BC4")
    canvas_frame.place(relx=0.5, rely=0.55, anchor="center")  # Luôn nằm giữa








    canvas = Canvas(canvas_frame, bg="white", width=DEFAULT_CANVAS_WIDTH, height=DEFAULT_CANVAS_HEIGHT,
                    bd=0, highlightthickness=5, highlightbackground="#809BC4")
    canvas.pack(fill="both", expand=True)  # Cho phép mở rộng theo frame




    if background_image:
        try:
            # Resize the image to fit the canvas (optional)
            canvas_width = canvas.winfo_reqwidth()
            canvas_height = canvas.winfo_reqheight()
            background_image = background_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            # Convert the image to a PhotoImage for Tkinter
            photo = ImageTk.PhotoImage(background_image)
            # Add the image to the canvas at the center
            image_id = canvas.create_image(canvas_width // 2, canvas_height // 2, image=photo, anchor="center")
            # Keep a reference to the PhotoImage to prevent garbage collection
            canvas.image = photo  # Store the reference in the canvas object
            # Add the image to drawn_objects
            drawn_objects.append({
                'type': 'image',
                'id': image_id,
                'photo': photo
            })
        except Exception as e:
            print(f"Error displaying background image: {e}")
            # Optionally, show an error message to the user
            tk.messagebox.showerror("Error", f"Could not display image: {e}")







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








    btn_line = tk.Button(toolbar, text="➖", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=lambda: set_mode("line"))  # Gán chế độ "line"
    btn_line.grid(row=0, column=7, padx=10, pady=5)








    # Sự kiện vẽ đường thẳng
    canvas.bind("<ButtonPress-1>", start_line)
    canvas.bind("<ButtonRelease-1>", draw_line)




    #Hàm nhập văn bản
    def insert_text(event):
        """Chèn văn bản tại vị trí click chuột"""
        # Hiển thị hộp thoại nhập văn bản
        text = simpledialog.askstring("Nhập văn bản", "Nhập nội dung:")
        if text:  # Nếu người dùng nhập văn bản
            # Tạo văn bản trên canvas
            text_id = canvas.create_text(event.x, event.y,
                                    text=text,
                                    font=("Arial", 16),
                                    fill=current_color,
                                    anchor="nw")  # anchor="nw" để căn theo góc trái trên
       
            # Lưu thông tin văn bản vào danh sách để có thể undo
            drawn_objects.append({
                'type': 'text',
                'id': text_id,
                'coords': [event.x, event.y],
                'text': text,
                'font': ("Arial", 16),
                'color': current_color
            })








    btn_text = tk.Button(toolbar, text="🅰", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=lambda: set_mode("text"))
    btn_text.grid(row=0, column=8, padx=10, pady=5)








    # Biến lưu vị trí trước đó của chuột
    last_x, last_y = None, None








    # Hàm tạo pencil
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




    # Cập nhật nút bấm
    btn_pencil = tk.Button(toolbar, text="✏️", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=lambda: set_mode("pencil"))
    btn_pencil.grid(row=0, column=1, padx=10, pady=5)








       
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








    btn_rectangle = tk.Button(toolbar, text="🔲", font=("Arial", 14), bg="#DCEAF9", bd=0,
                            command=lambda: set_mode("rectangle"))
    btn_rectangle.grid(row=0, column=2, padx=10, pady=5)
















    # Hàm chức năng tẩy
    def start_erase(event):
        """Bắt đầu xóa khi nhấn chuột"""
        global last_x, last_y
        last_x, last_y = event.x, event.y
    # Hàm erase cập nhật
    def erase(event):
        if drawing_mode == "eraser":
            x, y = event.x, event.y
            erase_size = current_width * 2  # Kích thước tẩy

            # Xóa bằng cách vẽ màu nền (giả lập tẩy)
            canvas.create_line(x-erase_size, y-erase_size, x+erase_size, y+erase_size,
                            fill="white", width=current_width*2, capstyle=tk.ROUND)
    def reset_position(event):
        """Đặt lại vị trí sau khi nhả chuột"""
        global last_x, last_y
        last_x, last_y = None, None












    # Thêm nút chọn tẩy
    btn_eraser = tk.Button(toolbar, text="🧽", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=lambda: set_mode("eraser"))
    btn_eraser.grid(row=0, column=6, padx=10, pady=5)








    # Hàm chức năng hoàn tác
    def undo():
        if drawn_objects:
            last_item = drawn_objects.pop()  # Lấy phần tử cuối cùng
       
            if isinstance(last_item, dict):  # Nếu là dictionary chứa thông tin đối tượng
                if last_item['type'] == 'text':
                    # Xóa văn bản
                    canvas.delete(last_item['id'])
                elif 'id' in last_item:  # Cho các loại đối tượng khác
                    canvas.delete(last_item['id'])
            elif isinstance(last_item, int):  # Nếu là ID đơn giản
                canvas.delete(last_item)




    btn_undo = tk.Button(toolbar, text="↩", font=("Arial", 14), bg="#DCEAF9", bd=0, command=undo)
    btn_undo.grid(row=0, column=4, padx=10, pady=5)








    # Hàm chọn màu
    def choose_color():
        global current_color
        color = colorchooser.askcolor(title="Chọn màu")[1]  # Mở hộp thoại chọn màu
        if color:
            current_color = color  # Lưu màu được chọn
    btn_color = tk.Button(toolbar, text="🎨", font=("Arial", 14), bg="#DCEAF9", bd=0, command=choose_color)
    btn_color.grid(row=0, column=9, padx=10, pady=5)  # Thêm vào vị trí thích hợp trên toolbar












    # Biến lưu vị trí bắt đầu và đối tượng hình tròn
    circle_start_x, circle_start_y = None, None
    current_circle = None




    #Hàm vẽ hình tròn
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








    btn_circle = tk.Button(toolbar, text="◯", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=lambda: set_mode("circle"))
    btn_circle.grid(row=0, column=3, padx=10, pady=5)  # Đặt vị trí thích hợp








    def flood_fill(event):
        if drawing_mode != "flood_fill":
            return


        x, y = event.x, event.y


        # Kiểm tra tọa độ hợp lệ
        if not (0 <= x < canvas.winfo_width() and 0 <= y < canvas.winfo_height()):
            return


        # Tạo ảnh tạm thời từ canvas hiện tại
        img = Image.new("RGB", (canvas.winfo_width(), canvas.winfo_height()), (255, 255, 255))
        draw = ImageDraw.Draw(img)


        # Hàm chuyển đổi màu an toàn
        def safe_color_convert(color_str, default=(0, 0, 0)):
            if not color_str or color_str == "":
                return default
            try:
                if color_str.startswith("#"):
                    return tuple(int(color_str.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                elif color_str.lower() in color_names:  # Xử lý tên màu bằng tiếng Anh
                    return color_names[color_str.lower()]
                else:
                    return default
            except:
                return default


        # Từ điển các màu cơ bản
        color_names = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255)
        }


        # Vẽ tất cả đối tượng (trừ các vùng flood fill cũ)
        for item_id in canvas.find_all():
            item_tags = canvas.gettags(item_id)
            if "flood_fill" not in item_tags:
                item_type = canvas.type(item_id)
                coords = canvas.coords(item_id)
           
                # Xử lý từng loại đối tượng
                if item_type == "rectangle":
                    fill = canvas.itemcget(item_id, "fill")
                    outline = canvas.itemcget(item_id, "outline") or "black"
                    width = int(float(canvas.itemcget(item_id, "width") or 1))
               
                    fill_rgb = safe_color_convert(fill, None)
                    outline_rgb = safe_color_convert(outline)
               
                    if fill_rgb:
                        draw.rectangle(coords, fill=fill_rgb, outline=outline_rgb, width=width)
                    else:
                        draw.rectangle(coords, outline=outline_rgb, width=width)
           
                elif item_type == "oval":
                    fill = canvas.itemcget(item_id, "fill")
                    outline = canvas.itemcget(item_id, "outline") or "black"
                    width = int(float(canvas.itemcget(item_id, "width") or 1))
               
                    fill_rgb = safe_color_convert(fill, None)
                    outline_rgb = safe_color_convert(outline)
               
                    if fill_rgb:
                        draw.ellipse(coords, fill=fill_rgb, outline=outline_rgb, width=width)
                    else:
                        draw.ellipse(coords, outline=outline_rgb, width=width)
           
                elif item_type == "line":
                    color = canvas.itemcget(item_id, "fill") or "black"
                    width = int(float(canvas.itemcget(item_id, "width") or 1))
                    color_rgb = safe_color_convert(color)
                    draw.line(coords, fill=color_rgb, width=width)


        # Thực hiện đổ màu
        try:
            # Chuyển màu hiện tại sang RGB
            fill_color = safe_color_convert(current_color, (255, 0, 0))
       
            # Đổ màu vào ảnh tạm
            ImageDraw.floodfill(img, (x, y), fill_color, thresh=40)
       
            # Tạo ảnh mới chỉ chứa vùng đổ màu (với nền trong suốt)
            filled_area = Image.new("RGBA", img.size, (0, 0, 0, 0))
            filled_pixels = filled_area.load()
            original_pixels = img.load()
       
            # Đánh dấu các pixel đã được đổ màu
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    if original_pixels[i, j] != (255, 255, 255):  # Khác màu trắng
                        filled_pixels[i, j] = (*fill_color, 255)  # Thêm kênh alpha
       
            # Chuyển sang ảnh Tkinter
            photo = ImageTk.PhotoImage(filled_area)
       
            # Thêm vào canvas với tag "flood_fill"
            fill_id = canvas.create_image(0, 0, image=photo, anchor="nw", tags=("flood_fill",))
            canvas.lower(fill_id)  # Đặt dưới các đối tượng khác
       
            # Lưu tham chiếu ảnh
            canvas.image = photo
       
            # Lưu vào danh sách để undo
            drawn_objects.append({
                'type': 'flood_fill',
                'id': fill_id,
                'color': current_color,
                'coords': [x, y],
                'image': photo
            })
       
        except Exception as e:
            print(f"Lỗi khi đổ màu: {e}")




    # Thay đổi command của nút spraycan (🌊)
    btn_flood_fill = tk.Button(toolbar, text="🌊", font=("Arial", 14), bg="#DCEAF9", bd=0,
                            command=lambda: set_mode("flood_fill"))
    btn_flood_fill.grid(row=0, column=5, padx=10, pady=5)












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
        elif mode == "text":
            canvas.bind("<Button-1>", insert_text)
            root.config(cursor="xterm")








    drawn_objects = deque(maxlen=100)  # Chỉ lưu 100 thao tác gần nhất
    current_color = "black"












    def save_canvas():
        """Lưu nội dung Canvas dưới dạng file hình ảnh, bao gồm toàn bộ nội dung (kể cả phần không hiển thị)."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"),
                                                            ("All Files", "*.*")])
        if not file_path:
            return  # User canceled the save dialog

        try:
            # Ensure the canvas is fully updated before capturing
            root.update()

            # Method 2: Capture the entire canvas content using PostScript
            # Get the bounding box of all items on the canvas (including scrolled/zoomed areas)
            bbox = canvas.bbox("all")
            if not bbox:
                print("Canvas trống, không có gì để lưu.")
                return

            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1

            # Export the canvas as a PostScript file
            ps_file = "temp_canvas.ps"
            canvas.postscript(file=ps_file, colormode="color", x=x1, y=y1, width=width, height=height)

            # Convert the PostScript file to an image using Pillow
            img = Image.open(ps_file)
            img.save(file_path, "PNG")

            # Clean up the temporary PostScript file
            os.remove(ps_file)

            print("Đã lưu hình ảnh tại:", file_path)

        except Exception as e:
            print(f"Lỗi khi lưu hình ảnh: {e}")




    btn_open = tk.Button(toolbar, text="📁", font=("Arial", 14), bg="#DCEAF9", bd=0, command=save_canvas)
    btn_open.grid(row=0, column=0, padx=10, pady=5)

















    def scale_canvas(scale_factor, center_x=None, center_y=None):
        """
        Scale the entire canvas content (all objects) relative to a center point.
        Args:
            scale_factor (float): Factor to scale by (e.g., 1.2 for zoom-in, 0.8 for zoom-out).
            center_x (float, optional): X-coordinate of the scaling center. Defaults to canvas center.
            center_y (float, optional): Y-coordinate of the scaling center. Defaults to canvas center.
        """
        global cumulative_scale

        # Update the cumulative scale factor
        cumulative_scale *= scale_factor

        # Get canvas dimensions to determine the default center
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # Use the canvas center as the default scaling point if not specified
        if center_x is None:
            center_x = canvas_width / 2
        if center_y is None:
            center_y = canvas_height / 2

        try:
            # Scale all objects on the canvas relative to the center point
            canvas.scale("all", center_x, center_y, scale_factor, scale_factor)

            # Update line widths for all objects based on their original widths
            for item in canvas.find_all():
                try:
                    # Store the original width the first time we see the item
                    if item not in original_widths:
                        current_width = canvas.itemcget(item, "width")
                        if current_width:  # Ensure the item has a width property
                            original_widths[item] = float(current_width)
                        else:
                            continue  # Skip items without a width (e.g., text)

                    # Calculate the new width based on the original width and cumulative scale
                    original_width = original_widths[item]
                    new_width = max(1, int(original_width * cumulative_scale))
                    canvas.itemconfig(item, width=new_width)

                except tk.TclError:
                    continue  # Skip items that don’t support width or have been deleted

            # Update the scroll region to ensure all objects remain visible
            bbox = canvas.bbox("all")
            if bbox:
                canvas.configure(scrollregion=bbox)

        except tk.TclError as e:
            print(f"Error scaling canvas: {e}")

    # Zoom-in button
    btn_zoom_in = tk.Button(toolbar, text="🔍+", font=("Arial", 14), bg="#DCEAF9", bd=0,
                            command=lambda: scale_canvas(1.2))
    btn_zoom_in.grid(row=0, column=10, padx=10, pady=5)

    # Zoom-out button
    btn_zoom_out = tk.Button(toolbar, text="🔍-", font=("Arial", 14), bg="#DCEAF9", bd=0,
                            command=lambda: scale_canvas(0.8))
    btn_zoom_out.grid(row=0, column=11, padx=10, pady=5)




    def clear_canvas():
        """Xóa toàn bộ nội dung trên Canvas và reset về trạng thái ban đầu."""
        global cumulative_scale, drawn_objects, original_widths

        # Delete all objects on the canvas
        canvas.delete("all")

        # Clear the drawn_objects list
        drawn_objects.clear()

        # Reset the zoom scale and original widths
        cumulative_scale = 1.0
        original_widths.clear()

        # Reset the scroll region to the default (optional: set to canvas size)
        canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), canvas.winfo_height()))

        # Optionally, reset the canvas background to white (in case it was changed)
        canvas.configure(bg="white")

        print("Đã xóa toàn bộ nội dung trên Canvas.")

    # New "Clear Canvas" button
    btn_clear = tk.Button(toolbar, text="🗑️ Clear", font=("Arial", 14), bg="#DCEAF9", bd=0,
                        command=clear_canvas)
    btn_clear.grid(row=0, column=13, padx=10, pady=5)







    # Thêm ở phần khai báo biến toàn cục
    current_width = 3  # Giá trị mặc định








    # Thêm thanh trượt điều chỉnh độ rộng
    width_slider = tk.Scale(toolbar, from_=1, to=20, orient="horizontal",
                        label="Độ rộng", command=lambda w: set_width(w))
    width_slider.set(current_width)
    width_slider.grid(row=0, column=12, padx=5)








    def set_width(w):
        global current_width
        current_width = int(w)








    root.mainloop()

