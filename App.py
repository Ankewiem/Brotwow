import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
from draw import draw


class DrawzyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DrawZy")
        self.root.geometry("800x600")  
   
        # Màu nền xanh lam
        self.root.config(bg="#DCEAF9")




        # Nhập ảnh logo vào window
        self.icon_logo = Image.open(r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/DRAWZY.png")
        self.icon_logo = self.icon_logo.resize((32, 32))  
        self.icon_logo = ImageTk.PhotoImage(self.icon_logo)
       
        # Tạo icon bằng logo
        self.root.iconphoto(False, self.icon_logo)




        # Chỉnh chữ Welcome to DrawZy
        self.label = tk.Label(root, text="Welcome to DrawZy!", font=("Adobe Clean", 40, "bold"),
                              fg="#536186", bg="#DCEAF9")
        self.label.pack(pady=40)  




        # Chỉnh hiệu ứng, hình thức các nút hiển thị
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




    def new_file(self):
# Clear all widgets from the current window
        for widget in self.root.winfo_children():
            widget.destroy()
        draw(self.root)




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
                for widget in self.root.winfo_children():
                    widget.destroy()
                draw(self.root, background_image=image)
                print(f"Opened image: {file}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {e}")




    def exit_app(self):
        response = messagebox.askyesno("Exit", "Do you want to exit?")
        if response:
            self.root.quit()




# if name == "main":
root = tk.Tk()
app = DrawzyApp(root)
root.mainloop()

