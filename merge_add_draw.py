import tkinter as tk
from tkinter import Canvas, simpledialog, filedialog, colorchooser, messagebox
from collections import deque
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import os
import io
import customtkinter as ctk
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
class DrawzyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DrawZy")
        self.root.geometry("800x600")
        self.root.config(bg="#DCEAF9")

        # Load and set the logo icon
        self.icon_logo = Image.open(r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/DRAWZY.png")
        self.icon_logo = self.icon_logo.resize((32, 32))
        self.icon_logo = ImageTk.PhotoImage(self.icon_logo)
        self.root.iconphoto(False, self.icon_logo)

        # Welcome label
        self.label = tk.Label(root, text="Welcome to DrawZy!", font=("Adobe Clean", 40, "bold"),
                              fg="#536186", bg="#DCEAF9")
        self.label.pack(pady=40)

        # Buttons for the main menu
        self.new_button = ctk.CTkButton(root, text="New File", width=200, height=50, command=self.new_file,
                                        corner_radius=20, fg_color="#B9B0D6", hover_color="#debbd8",
                                        text_color="#536186", font=("Arial", 20),
                                        border_width=2, border_color="#8e79d1")
        self.new_button.pack(pady=10)

        self.open_button = ctk.CTkButton(root, text="Open File", width=200, height=50, command=self.open_file,
                                         corner_radius=20, fg_color="#B9B0D6", hover_color="#debbd8",
                                         text_color="#536186", font=("Arial", 20),
                                         border_width=2, border_color="#8e79d1")
        self.open_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(root, text="Exit", width=200, height=50, command=self.exit_app,
                                         corner_radius=20, fg_color="#B9B0D6", hover_color="#debbd8",
                                         text_color="#536186", font=("Arial", 20),
                                         border_width=2, border_color="#8e79d1")
        self.exit_button.pack(pady=10)

        # Initialize drawing-related variables
        self.original_widths = {}
        self.cumulative_scale = 1.0
        self.drawn_objects = deque(maxlen=100)
        self.current_color = "black"
        self.current_width = 3
        self.drawing_mode = "none"
        self.last_x = None
        self.last_y = None
        self.start_x = None
        self.start_y = None
        self.shape_start_x = None
        self.shape_start_y = None
        self.current_shape = None
        self.circle_start_x = None
        self.circle_start_y = None
        self.current_circle = None

    def setup_drawing_area(self, background_image=None):
        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Paint App")
        self.root.geometry("1100x600")
        self.root.minsize(800, 500)

        # Toolbar
        self.toolbar = tk.Frame(self.root, bg="#809BC4", height=50)
        self.toolbar.pack(fill="x")

        # Canvas frame and canvas
        self.DEFAULT_CANVAS_WIDTH = 830
        self.DEFAULT_CANVAS_HEIGHT = 480
        self.canvas_frame = tk.Frame(self.root, bg="#809BC4")
        self.canvas_frame.place(relx=0.5, rely=0.55, anchor="center")
        self.canvas = Canvas(self.canvas_frame, bg="white", width=self.DEFAULT_CANVAS_WIDTH,
                             height=self.DEFAULT_CANVAS_HEIGHT, bd=0, highlightthickness=5,
                             highlightbackground="#809BC4")
        self.canvas.pack(fill="both", expand=True)

        # Handle background image
        if background_image:
            try:
                canvas_width = self.canvas.winfo_reqwidth()
                canvas_height = self.canvas.winfo_reqheight()
                background_image = background_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(background_image)
                image_id = self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=photo, anchor="center")
                self.canvas.image = photo
                self.drawn_objects.append({'type': 'image', 'id': image_id, 'photo': photo})
            except Exception as e:
                print(f"Error displaying background image: {e}")
                messagebox.showerror("Error", f"Could not display image: {e}")

        # Bind resize event
        self.root.bind("<Configure>", self.resize_canvas)

        # Toolbar buttons
        icons = [
            ("📁", "arrow", self.save_canvas),  # Save file
            ("✏️", "pencil", lambda: self.set_mode("pencil")),
            ("🔲", "cross", lambda: self.set_mode("rectangle")),
            ("◯", "circle", lambda: self.set_mode("circle")),
            ("↩", "exchange", self.undo),
            ("🌊", "spraycan", lambda: self.set_mode("flood_fill")),
            ("🧽", "dotbox", lambda: self.set_mode("eraser")),
            ("➖", "tcross", lambda: self.set_mode("line")),
            ("🅰", "xterm", lambda: self.set_mode("text")),
            ("🎨", "circle", self.choose_color),
            ("🔍+", "plus", lambda: self.scale_canvas(1.2)),
            ("🔍-", "arrow", lambda: self.scale_canvas(0.8)),
            ("🖼️", "arrow", self.generate_image_from_text),
            ("🗑️ Clear", "arrow", self.clear_canvas)
        ]
        for i, (icon, cursor_type, command) in enumerate(icons):
            btn = tk.Button(self.toolbar, text=icon, font=("Arial", 14), bg="#DCEAF9", bd=0,
                            command=lambda c=cursor_type, cmd=command: [self.change_cursor(c), cmd()])
            btn.grid(row=0, column=i, padx=10, pady=5)

        # Width slider
        self.width_slider = tk.Scale(self.toolbar, from_=1, to=20, orient="horizontal",
                                     label="Độ rộng", command=self.set_width)
        self.width_slider.set(self.current_width)
        self.width_slider.grid(row=0, column=len(icons), padx=5)
    def generate_image_from_text(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Image from Text")
        dialog.geometry("400x300")

        tk.Label(dialog, text="Enter your text prompt:").pack(pady=5)
        prompt_entry = tk.Entry(dialog, width=40)
        prompt_entry.insert(0, "A colorful bird flying over a forest")
        prompt_entry.pack(pady=5)

        tk.Label(dialog, text="Select style:").pack(pady=5)
        style_var = tk.StringVar(value="default")  # Stable Diffusion doesn't use styles in this endpoint
        styles = ["default"]  # No style selection for this endpoint
        style_menu = tk.OptionMenu(dialog, style_var, *styles)
        style_menu.pack(pady=5)

        def generate_and_display():
            prompt = prompt_entry.get()
            if not prompt:
                tk.messagebox.showerror("Error", "Please enter a text prompt.")
                return

            try:
                # Set up retries
                session = requests.Session()
                retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
                session.mount("https://", HTTPAdapter(max_retries=retries))

                # Stable Diffusion API (ModelsLab)
                api_key = "xqiXmn1kiO2DukggaUPjrSpu6u2FQ4FSPuQZ7LzW0RCpP6ozIH3FcpEwLTCg"  # Replace with your ModelsLab API key
                url = "https://modelslab.com/api/v6/realtime/text2img"
                print(f"Requesting URL: {url} with prompt: {prompt}")
                response = session.post(url, json={
                    "key": api_key,
                    "prompt": prompt,
                    "negative_prompt": "bad quality",
                    "width": "512",
                    "height": "512",
                    "safety_checker": False,
                    "seed": None,
                    "samples": 1,
                    "base64": False,
                    "webhook": None,
                    "track_id": None
                }, headers={
                    "Content-Type": "application/json"
                }, timeout=30)
                response.raise_for_status()
                result = response.json()

                if "output" not in result or not result["output"]:
                    tk.messagebox.showerror("Error", "Failed to generate image. Try a different prompt.")
                    return

                image_url = result["output"][0]
                print(f"Generated image URL: {image_url}")
                image_response = requests.get(image_url, timeout=30)
                image_response.raise_for_status()

                image_data = image_response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.canvas.create_image(0, 0, anchor="nw", image=photo)
                self.canvas.image = photo

                self.drawn_objects.append({
                    "type": "image",
                    "id": None,
                    "image": photo,
                    "coords": [0, 0]
                })

                dialog.destroy()

            except requests.exceptions.RequestException as e:
                tk.messagebox.showerror("Error", f"Failed to generate image: {str(e)}")

        tk.Button(dialog, text="Generate Image", command=generate_and_display).pack(pady=20)

        dialog.transient(self.root)
        dialog.grab_set()
        dialog.wait_window()
    def change_cursor(self, cursor_type):
        self.root.config(cursor=cursor_type)

    def resize_canvas(self, event):
        new_width = self.root.winfo_width() - 100
        new_height = self.root.winfo_height() - 150
        new_width = max(new_width, 500)
        new_height = max(new_height, 300)
        self.canvas.config(width=new_width, height=new_height)
        self.canvas_frame.place(relx=0.5, rely=0.55, anchor="center")

    def start_draw(self, event):
        if self.drawing_mode == "pencil":
            self.last_x, self.last_y = event.x, event.y
        else:
            self.last_x, self.last_y = None, None

    def draw_pencil(self, event):
        if self.drawing_mode == "pencil" and self.last_x is not None and self.last_y is not None:
            line_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                              fill=self.current_color, width=self.current_width,
                                              capstyle="round", smooth=True)
            self.drawn_objects.append({
                'type': 'pencil', 'id': line_id, 'coords': [self.last_x, self.last_y, event.x, event.y],
                'width': self.current_width, 'color': self.current_color
            })
            self.last_x, self.last_y = event.x, event.y

    def reset_position(self, event):
        self.last_x, self.last_y = None, None

    def start_line(self, event):
        self.start_x, self.start_y = event.x, event.y

    def draw_line(self, event):
        if self.drawing_mode == "line":
            line_id = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                              fill=self.current_color, width=self.current_width)
            self.drawn_objects.append({
                'type': 'line', 'id': line_id, 'coords': [self.start_x, self.start_y, event.x, event.y],
                'width': self.current_width, 'color': self.current_color
            })

    def start_shape(self, event):
        if self.drawing_mode == "rectangle":
            self.shape_start_x, self.shape_start_y = event.x, event.y
            self.current_shape = self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y,
                                                              self.shape_start_x, self.shape_start_y,
                                                              outline=self.current_color, width=self.current_width)

    def draw_shape(self, event):
        if self.drawing_mode == "rectangle" and self.current_shape:
            self.canvas.coords(self.current_shape, self.shape_start_x, self.shape_start_y, event.x, event.y)

    def finish_shape(self, event):
        if self.drawing_mode == "rectangle" and self.current_shape:
            self.drawn_objects.append({
                'type': 'rectangle', 'id': self.current_shape, 'coords': self.canvas.coords(self.current_shape),
                'width': self.current_width, 'color': self.current_color
            })
            self.current_shape = None

    def start_circle(self, event):
        if self.drawing_mode == "circle":
            self.circle_start_x, self.circle_start_y = event.x, event.y
            self.current_circle = self.canvas.create_oval(self.circle_start_x, self.circle_start_y,
                                                          self.circle_start_x, self.circle_start_y,
                                                          outline=self.current_color, width=self.current_width)

    def draw_circle(self, event):
        if self.drawing_mode == "circle" and self.current_circle:
            self.canvas.coords(self.current_circle, self.circle_start_x, self.circle_start_y, event.x, event.y)

    def finish_circle(self, event):
        if self.drawing_mode == "circle" and self.current_circle:
            self.drawn_objects.append({
                'type': 'circle', 'id': self.current_circle, 'coords': self.canvas.coords(self.current_circle),
                'width': self.current_width, 'color': self.current_color
            })
            self.current_circle = None

    def insert_text(self, event):
        if self.drawing_mode == "text":
            text = simpledialog.askstring("Nhập văn bản", "Nhập nội dung:")
            if text:
                text_id = self.canvas.create_text(event.x, event.y, text=text, font=("Arial", 16),
                                                  fill=self.current_color, anchor="nw")
                self.drawn_objects.append({
                    'type': 'text', 'id': text_id, 'coords': [event.x, event.y], 'text': text,
                    'font': ("Arial", 16), 'color': self.current_color
                })

    def start_erase(self, event):
        self.last_x, self.last_y = event.x, event.y

    def erase(self, event):
        if self.drawing_mode == "eraser":
            x, y = event.x, event.y
            erase_size = self.current_width * 2
            self.canvas.create_line(x - erase_size, y - erase_size, x + erase_size, y + erase_size,
                                    fill="white", width=self.current_width * 2, capstyle=tk.ROUND)

    def flood_fill(self, event):
        if self.drawing_mode != "flood_fill":
            return
        x, y = event.x, event.y
        if not (0 <= x < self.canvas.winfo_width() and 0 <= y < self.canvas.winfo_height()):
            return
        img = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        def safe_color_convert(color_str, default=(0, 0, 0)):
            if not color_str or color_str == "":
                return default
            try:
                if color_str.startswith("#"):
                    return tuple(int(color_str.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                elif color_str.lower() in self.color_names:
                    return self.color_names[color_str.lower()]
                else:
                    return default
            except:
                return default

        self.color_names = {
            'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 128, 0),
            'blue': (0, 0, 255), 'yellow': (255, 255, 0), 'cyan': (0, 255, 255), 'magenta': (255, 0, 255)
        }

        for item_id in self.canvas.find_all():
            item_tags = self.canvas.gettags(item_id)
            if "flood_fill" not in item_tags:
                item_type = self.canvas.type(item_id)
                coords = self.canvas.coords(item_id)
                if item_type == "rectangle":
                    fill = self.canvas.itemcget(item_id, "fill")
                    outline = self.canvas.itemcget(item_id, "outline") or "black"
                    width = int(float(self.canvas.itemcget(item_id, "width") or 1))
                    fill_rgb = safe_color_convert(fill, None)
                    outline_rgb = safe_color_convert(outline)
                    if fill_rgb:
                        draw.rectangle(coords, fill=fill_rgb, outline=outline_rgb, width=width)
                    else:
                        draw.rectangle(coords, outline=outline_rgb, width=width)
                elif item_type == "oval":
                    fill = self.canvas.itemcget(item_id, "fill")
                    outline = self.canvas.itemcget(item_id, "outline") or "black"
                    width = int(float(self.canvas.itemcget(item_id, "width") or 1))
                    fill_rgb = safe_color_convert(fill, None)
                    outline_rgb = safe_color_convert(outline)
                    if fill_rgb:
                        draw.ellipse(coords, fill=fill_rgb, outline=outline_rgb, width=width)
                    else:
                        draw.ellipse(coords, outline=outline_rgb, width=width)
                elif item_type == "line":
                    color = self.canvas.itemcget(item_id, "fill") or "black"
                    width = int(float(self.canvas.itemcget(item_id, "width") or 1))
                    color_rgb = safe_color_convert(color)
                    draw.line(coords, fill=color_rgb, width=width)

        try:
            fill_color = safe_color_convert(self.current_color, (255, 0, 0))
            ImageDraw.floodfill(img, (x, y), fill_color, thresh=40)
            filled_area = Image.new("RGBA", img.size, (0, 0, 0, 0))
            filled_pixels = filled_area.load()
            original_pixels = img.load()
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    if original_pixels[i, j] != (255, 255, 255):
                        filled_pixels[i, j] = (*fill_color, 255)
            photo = ImageTk.PhotoImage(filled_area)
            fill_id = self.canvas.create_image(0, 0, image=photo, anchor="nw", tags=("flood_fill",))
            self.canvas.lower(fill_id)
            self.canvas.image = photo
            self.drawn_objects.append({
                'type': 'flood_fill', 'id': fill_id, 'color': self.current_color, 'coords': [x, y], 'image': photo
            })
        except Exception as e:
            print(f"Lỗi khi đổ màu: {e}")

    def undo(self):
        if self.drawn_objects:
            last_item = self.drawn_objects.pop()
            if isinstance(last_item, dict) and 'id' in last_item:
                self.canvas.delete(last_item['id'])

    def choose_color(self):
        color = colorchooser.askcolor(title="Chọn màu")[1]
        if color:
            self.current_color = color

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if not file_path:
            return
        try:
            self.root.update()
            bbox = self.canvas.bbox("all")
            if not bbox:
                print("Canvas trống, không có gì để lưu.")
                return
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
            ps_file = "temp_canvas.ps"
            self.canvas.postscript(file=ps_file, colormode="color", x=x1, y=y1, width=width, height=height)
            img = Image.open(ps_file)
            img.save(file_path, "PNG")
            os.remove(ps_file)
            print("Đã lưu hình ảnh tại:", file_path)
        except Exception as e:
            print(f"Lỗi khi lưu hình ảnh: {e}")

    def scale_canvas(self, scale_factor, center_x=None, center_y=None):
        self.cumulative_scale *= scale_factor
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if center_x is None:
            center_x = canvas_width / 2
        if center_y is None:
            center_y = canvas_height / 2
        try:
            self.canvas.scale("all", center_x, center_y, scale_factor, scale_factor)
            for item in self.canvas.find_all():
                try:
                    if item not in self.original_widths:
                        current_width = self.canvas.itemcget(item, "width")
                        if current_width:
                            self.original_widths[item] = float(current_width)
                        else:
                            continue
                    original_width = self.original_widths[item]
                    new_width = max(1, int(original_width * self.cumulative_scale))
                    self.canvas.itemconfig(item, width=new_width)
                except tk.TclError:
                    continue
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.configure(scrollregion=bbox)
        except tk.TclError as e:
            print(f"Error scaling canvas: {e}")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.drawn_objects.clear()
        self.cumulative_scale = 1.0
        self.original_widths.clear()
        self.canvas.configure(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))
        self.canvas.configure(bg="white")
        print("Đã xóa toàn bộ nội dung trên Canvas.")

    def set_width(self, w):
        self.current_width = int(w)

    def set_mode(self, mode):
        self.drawing_mode = mode
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if mode == "pencil":
            self.canvas.bind("<ButtonPress-1>", self.start_draw)
            self.canvas.bind("<B1-Motion>", self.draw_pencil)
            self.canvas.bind("<ButtonRelease-1>", self.reset_position)
        elif mode == "rectangle":
            self.canvas.bind("<ButtonPress-1>", self.start_shape)
            self.canvas.bind("<B1-Motion>", self.draw_shape)
            self.canvas.bind("<ButtonRelease-1>", self.finish_shape)
        elif mode == "line":
            self.canvas.bind("<ButtonPress-1>", self.start_line)
            self.canvas.bind("<ButtonRelease-1>", self.draw_line)
        elif mode == "eraser":
            self.canvas.bind("<ButtonPress-1>", self.start_erase)
            self.canvas.bind("<B1-Motion>", self.erase)
            self.canvas.bind("<ButtonRelease-1>", self.reset_position)
        elif mode == "circle":
            self.canvas.bind("<ButtonPress-1>", self.start_circle)
            self.canvas.bind("<B1-Motion>", self.draw_circle)
            self.canvas.bind("<ButtonRelease-1>", self.finish_circle)
        elif mode == "flood_fill":
            self.canvas.bind("<Button-1>", self.flood_fill)
            self.root.config(cursor="spraycan")
        elif mode == "text":
            self.canvas.bind("<Button-1>", self.insert_text)
            self.root.config(cursor="xterm")

    def new_file(self):
        self.setup_drawing_area()

    def open_file(self):
        file = filedialog.askopenfilename(
            defaultextension=".png",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file:
            try:
                image = Image.open(file)
                print(f"Image format: {image.format}, Size: {image.size}, Mode: {image.mode}")
                image.verify()
                image = Image.open(file)
                self.setup_drawing_area(background_image=image)
                print(f"Opened image: {file}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {e}")

    def exit_app(self):
        response = messagebox.askyesno("Exit", "Do you want to exit?")
        if response:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawzyApp(root)
    root.mainloop()