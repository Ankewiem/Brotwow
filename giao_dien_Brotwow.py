import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk  # Import customtkinter
from PIL import Image, ImageTk  # Cần cài thư viện Pillow nếu bạn chưa cài (pip install pillow)
import subprocess
class BrotWowapp:
    def __init__(self, root):
        self.root = root
        self.root.title("BrotWow")
        self.root.geometry("800x600")  # Set window size
   
        # Load logo image for window icon
        self.logo = Image.open(r"ẢNH BT LỚN-20250328T025055Z-001/ẢNH BT LỚN/BW logo.png")   # Đường dẫn đến tệp logo đã tải lên
        self.logo = self.logo.resize((32, 32))  # Resize logo cho phù hợp với icon
        self.logo = ImageTk.PhotoImage(self.logo)

        # Set window icon
        self.root.iconphoto(False, self.logo)
        # Set background color to #C7D6F7
        self.root.config(bg="#C7D6F7")

        # Label displaying "Welcome to BrotWow" with bold font
        self.label = tk.Label(root, text="Welcome to BrotWow!", font=("Adobe Clean", 40, "bold"), fg="#536186", bg="#C7D6F7")
        self.label.pack(pady=40)  # Adjust padding to make the label occupy a large portion of the screen

        # Create custom buttons with rounded corners and hover effects using customtkinter
        self.new_button = ctk.CTkButton(root, text="INTERACTIVE VIEW", width=200, height=50, command=self.new_file,
                                        corner_radius=20, fg_color="#536186", hover_color="#809BC4", font=("Roboto", 17),
                                        border_width=2, border_color="gray")
        self.new_button.pack(pady=10)

        self.open_button = ctk.CTkButton(root, text="WOW IMAGES", width=200, height=50, command=self.open_file,
                                         corner_radius=20, fg_color="#536186", hover_color="#809BC4", font=("Roboto", 17),
                                         border_width=2, border_color="gray")
        self.open_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(root, text="EXIT", width=200, height=50, command=self.exit_app,
                                         corner_radius=20, fg_color="#536186", hover_color="#809BC4", font=("Roboto", 17),
                                         border_width=2, border_color="gray")
        self.exit_button.pack(pady=10)
   
    

    def new_file(self):
        """Function to launch the BrotWow interactive view"""
        try:
            subprocess.Popen(["python3", "Brotwow.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open BrotWow Interactive View:\n{e}")


    def open_file(self):
        """Run Brotwow_anh.py when WOW IMAGES is clicked"""
        subprocess.Popen(["python3", "Brotwow_anh.py"])  # Runs Brotwow_anh.py in a separate process

    def exit_app(self):
        """Function for 'Exit' button/menu item"""
        response = messagebox.askyesno("Exit", "Do you want to exit?")
        if response:
            self.root.quit()

    def mainloop(self):
        self.root.mainloop()

root = tk.Tk()
app = BrotWowapp(root)
app.mainloop()
