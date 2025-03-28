import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from tkinter.colorchooser import askcolor
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure


# ========== APP CONFIGURATION ==========
WIDTH, HEIGHT = 1400, 1150
INITIAL_ITER = 23
ZOOM_OUT_FACTOR = 1.5
ZOOM_IN_FACTOR = 1 / ZOOM_OUT_FACTOR
colormap = "inferno"


# Color scheme
BG_COLOR = "#B0C4DE"
PANEL_COLOR = "#536186"
TEXT_COLOR = "#536186"  
BUTTON_COLOR = "#D3D3D3"
HOVER_COLOR = "#bacbe1"  
BUTTON_ACTIVE = "#a8b8d1"  
BUTTON_FG = "#536186"  
BORDER_COLOR = "#a0a0a0"


# Fonts
FONT_LARGE = ("Segoe UI", 14, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)


# ========== GLOBAL VARIABLES ==========
xmin, xmax = -2.5, 2.5
ymin, ymax = -2.0, 2.0
history = []
current_state = {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}
pan_start = None
current_c = complex(-0.7, 0.27)


# ========== BUTTON STYLING FUNCTIONS ==========
def configure_styles():
    """Configure custom styles for all widgets"""
    style = ttk.Style()
    style.theme_use('clam')
   
    # Frame style
    style.configure('TFrame', background=PANEL_COLOR)
   
    # Entry style
    style.configure('TEntry',
                  fieldbackground='white',
                  foreground=BUTTON_FG,
                  bordercolor=BORDER_COLOR,
                  lightcolor=BORDER_COLOR,
                  darkcolor=BORDER_COLOR,
                  padding=5)
   
    # Scale style
    style.configure('Horizontal.TScale',
                  background=PANEL_COLOR,
                  troughcolor=BUTTON_COLOR,
                  bordercolor=BORDER_COLOR,
                  darkcolor=BORDER_COLOR,
                  lightcolor=BORDER_COLOR)


def create_beautiful_button(parent, text, command, width=None):
    """Create a styled button with hover effects"""
    btn = tk.Button(parent,
                   text=text,
                   command=command,
                   bg=BUTTON_COLOR,
                   fg=BUTTON_FG,
                   activebackground=HOVER_COLOR,
                   activeforeground=BUTTON_FG,
                   font=FONT_NORMAL,
                   bd=0,
                   highlightthickness=1,
                   highlightbackground=BORDER_COLOR,
                   highlightcolor=BORDER_COLOR,
                   relief="raised",
                   padx=8,
                   pady=2,
                   width=width)
   
    # Add rounded effect and hover animations
    btn.config(overrelief="groove")
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_COLOR))
    btn.bind("<Leave>", lambda e: btn.config(bg=BUTTON_COLOR))
    return btn


def create_arrow_button(parent, text, command):
    """Create styled arrow buttons"""
    btn = tk.Button(parent,
                   text=text,
                   command=command,
                   bg=BUTTON_COLOR,
                   fg=BUTTON_FG,
                   activebackground=HOVER_COLOR,
                   activeforeground=BUTTON_FG,
                   font=FONT_NORMAL,
                   bd=0,
                   highlightthickness=1,
                   highlightbackground=BORDER_COLOR,
                   highlightcolor=BORDER_COLOR,
                   relief="raised",
                   padx=0,
                   pady=0,
                   width=3)
   
    btn.config(overrelief="groove")
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_COLOR))
    btn.bind("<Leave>", lambda e: btn.config(bg=BUTTON_COLOR))
    return btn


# ========== FRACTAL CALCULATIONS ==========
def mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    """Calculate Mandelbrot set"""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    div_time = np.zeros(Z.shape, dtype=int)


    for i in range(max_iter):
        mask = np.abs(Z) < 2
        Z[mask] = Z[mask]**2 + C[mask]
        div_time[mask] += 1
    return div_time


def julia(c, xmin, xmax, ymin, ymax, width, height, max_iter):
    """Calculate Julia set"""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    div_time = np.zeros(Z.shape, dtype=int)


    for i in range(max_iter):
        mask = np.abs(Z) < 2
        Z[mask] = Z[mask]**2 + c
        div_time[mask] += 1
    return div_time


# ========== DRAWING FUNCTIONS ==========
def draw_mandel():
    """Draw the Mandelbrot set"""
    ax_mandel.clear()
    current_iter = int(iter_slider.get())
    data = mandelbrot(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, current_iter)
    ax_mandel.imshow(data, extent=[xmin, xmax, ymin, ymax], cmap=colormap, origin='lower')


    if show_axes_var.get():
        ax_mandel.set_xlabel("Real")
        ax_mandel.set_ylabel("Imaginary")
    else:
        ax_mandel.set_xticks([])
        ax_mandel.set_yticks([])


    ax_mandel.set_title("MANDELBROT SET", color="Black")
    canvas_mandel.draw()
    update_iter_display()


def draw_julia(c, ax):
    """Draw the Julia set"""
    ax.clear()
    current_iter = int(iter_slider.get())
    data = julia(c, -2, 2, -2, 2, 350, 350, current_iter)
    ax.imshow(data, extent=[-2, 2, -2, 2], cmap=colormap, origin='lower')
   
    if show_axes_var.get():
        ax.set_xlabel("Real")
        ax.set_ylabel("Imaginary")
    else:
        ax.set_xticks([])
        ax.set_yticks([])
   
    # Update Julia set title with smaller white text for coordinates
    ax.set_title(f"JULIA SET at ({c.real:.3f}, {c.imag:.3f})",
                color="Black",
                fontsize=10)
    # Make the coordinates part white and smaller
    for text in ax.texts:
        if "(" in text.get_text():
            text.set_color("white")
            text.set_fontsize(8)
    canvas_julia.draw()


def update_julia_preview(c):
    """Update Julia set preview"""
    global current_c
    current_c = c
    draw_julia(c, ax_julia)


# ========== EVENT HANDLERS ==========
def on_motion(event):
    """Handle mouse motion over Mandelbrot set"""
    if event.inaxes == ax_mandel:
        c = complex(event.xdata, event.ydata)
        update_julia_preview(c)


def on_click(event):
    """Handle mouse clicks on Mandelbrot set"""
    if event.inaxes == ax_mandel:
        c = complex(event.xdata, event.ydata)
        update_julia_preview(c)


def on_press(event):
    """Handle mouse press for panning"""
    global pan_start
    if event.inaxes == ax_mandel and event.button == 1:
        pan_start = (event.xdata, event.ydata)


def on_release(event):
    """Handle mouse release after panning"""
    global pan_start, xmin, xmax, ymin, ymax
    if pan_start and event.button == 1:
        save_state()
        x_center, y_center = pan_start
        x_end, y_end = event.xdata, event.ydata
        dx = x_end - x_center
        dy = y_end - y_center
        xmin -= dx
        xmax -= dx
        ymin -= dy
        ymax -= dy
        draw_mandel()
        pan_start = None


def on_scroll(event):
    """Handle mouse scroll for zooming"""
    global xmin, xmax, ymin, ymax
    if event.inaxes == ax_mandel:
        save_state()
        x_center = event.xdata
        y_center = event.ydata
        if event.button == 'up':
            width = (xmax - xmin) * ZOOM_OUT_FACTOR
            height = (ymax - ymin) * ZOOM_OUT_FACTOR
        else:
            width = (xmax - xmin) * ZOOM_IN_FACTOR
            height = (ymax - ymin) * ZOOM_IN_FACTOR
           
        xmin = x_center - width / 2
        xmax = x_center + width / 2
        ymin = y_center - height / 2
        ymax = y_center + height / 2
        draw_mandel()


# ========== ZOOM & PAN FUNCTIONS ==========
def zoom_out():
    """Zoom out to see more area"""
    global xmin, xmax, ymin, ymax
    save_state()
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    width = (xmax - xmin) * ZOOM_OUT_FACTOR
    height = (ymax - ymin) * ZOOM_OUT_FACTOR
    xmin = x_center - width / 2
    xmax = x_center + width / 2
    ymin = y_center - height / 2
    ymax = y_center + height / 2
    draw_mandel()


def zoom_in():
    """Zoom in to see details"""
    global xmin, xmax, ymin, ymax
    save_state()
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    width = (xmax - xmin) * ZOOM_IN_FACTOR
    height = (ymax - ymin) * ZOOM_IN_FACTOR
    xmin = x_center - width / 2
    xmax = x_center + width / 2
    ymin = y_center - height / 2
    ymax = y_center + height / 2
    draw_mandel()


def pan(direction):
    """Pan the view in specified direction"""
    global xmin, xmax, ymin, ymax
    save_state()
    dx = (xmax - xmin) * 0.2
    dy = (ymax - ymin) * 0.2
   
    if direction == 'left':
        xmin -= dx
        xmax -= dx
    elif direction == 'right':
        xmin += dx
        xmax += dx
    elif direction == 'up':
        ymin += dy
        ymax += dy
    elif direction == 'down':
        ymin -= dy
        ymax -= dy
   
    draw_mandel()


# ========== VIEW MANAGEMENT ==========
def home_view():
    """Reset to default view"""
    global xmin, xmax, ymin, ymax
    save_state()
    xmin, xmax, ymin, ymax = -2.5, 2.5, -2.0, 2.0
    draw_mandel()


def undo_view():
    """Undo last view change"""
    global xmin, xmax, ymin, ymax
    if history:
        state = history.pop()
        xmin, xmax, ymin, ymax = state["xmin"], state["xmax"], state["ymin"], state["ymax"]
        draw_mandel()


def save_state():
    """Save current view state"""
    state = {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}
    history.append(state)


# ========== COLOR CHOOSER ==========
def choose_color():
    """Open color chooser dialog"""
    global colormap
    color = askcolor()[1]
    if color:
        colormap = LinearSegmentedColormap.from_list("custom_colormap", [color, "black"])
        draw_mandel()
        draw_julia(current_c, ax_julia)


# ========== SAVE IMAGE FUNCTION ==========
def save_image():
    """Save current fractal image"""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save Fractal Image"
    )
    if filepath:
        dpi = 300
        width_inches = 10
        height_inches = 7
       
        fig_save = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)
        ax_save = fig_save.add_subplot(111)
       
        current_iter = int(iter_slider.get())
        data = mandelbrot(xmin, xmax, ymin, ymax, width_inches*dpi, height_inches*dpi, current_iter)
        ax_save.imshow(data, extent=[xmin, xmax, ymin, ymax], cmap=colormap, origin='lower')
       
        if show_axes_var.get():
            ax_save.set_xlabel("Real")
            ax_save.set_ylabel("Imaginary")
        else:
            ax_save.set_xticks([])
            ax_save.set_yticks([])
       
        ax_save.set_title("MANDELBROT SET", color="Black")
        fig_save.savefig(filepath, dpi=dpi, bbox_inches='tight')
        plt.close(fig_save)


# ========== ITERATION CONTROL ==========
def update_iter_display():
    """Update iteration display"""
    current_iter = int(iter_slider.get())
    iter_entry.delete(0, tk.END)
    iter_entry.insert(0, str(current_iter))


def validate_iteration_input(event=None):
    """Validate iteration input"""
    try:
        new_iter = int(iter_var.get())
        if 1 <= new_iter <= 150:
            iter_slider.set(new_iter)
            draw_mandel()
            draw_julia(current_c, ax_julia)
            return True
        else:
            messagebox.showwarning("Invalid Value", "Please enter a value between 1 and 150")
            update_iter_display()
            return False
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number")
        update_iter_display()
        return False


def on_iter_slider_change(event):
    """Handle iteration slider change"""
    update_iter_display()
    draw_mandel()
    draw_julia(current_c, ax_julia)


# ========== MAIN WINDOW ==========
root = tk.Tk()
root.title("BrotWow - Mandelbrot & Julia Explorer")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg=BG_COLOR)


# Configure custom styles
configure_styles()


try:
    icon_img = PhotoImage(file=r"C:\Users\TRAM ANH\Downloads\ẢNH BT LỚN-20250328T025055Z-001\ẢNH BT LỚN\BW logo.png")
    root.iconphoto(True, icon_img)
except Exception as e:
    print("⚠️ Không thể tải icon nhỏ ở tiêu đề:", e)


# ========== FRAMES LAYOUT ==========
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)


left_frame = tk.Frame(main_frame, bg=BG_COLOR)
left_frame.pack(side="left", fill="both", expand=True)


right_frame = tk.Frame(main_frame, bg=PANEL_COLOR, width=380)
right_frame.pack(side="right", fill="y")


# ========== CONTROL PANEL ==========
# Make the title more prominent with black color and larger font
title_label = tk.Label(right_frame, text="BROTWOW CONTROL PANEL",
                     font=("Segoe UI", 16, "bold"), fg="black", bg=PANEL_COLOR)
title_label.pack(pady=15)


# Main control frame
control_frame = tk.Frame(right_frame, bg=PANEL_COLOR)
control_frame.pack(padx=10, pady=5, fill="both", expand=True)


# Iteration Control
iter_frame = tk.Frame(control_frame, bg=PANEL_COLOR)
iter_frame.pack(anchor="w", pady=5, fill="x")


iter_label = tk.Label(iter_frame, text="MAX ITERATIONS:", fg="white", bg=PANEL_COLOR, font=FONT_NORMAL)
iter_label.pack(side="left")


iter_var = tk.StringVar()
iter_var.set(str(INITIAL_ITER))
iter_entry = ttk.Entry(iter_frame, textvariable=iter_var, width=8, font=FONT_NORMAL)
iter_entry.bind('<Return>', validate_iteration_input)
iter_entry.pack(side="left", padx=5)


iter_slider = ttk.Scale(control_frame, from_=1, to=150, orient="horizontal", command=on_iter_slider_change)
iter_slider.set(INITIAL_ITER)
iter_slider.pack(fill="x", pady=5)


# Color and Options
color_frame = tk.Frame(control_frame, bg=PANEL_COLOR)
color_frame.pack(pady=5, fill="x")


color_button = create_beautiful_button(color_frame, "Color", choose_color, width=8)
color_button.pack(side="left", padx=2)


show_axes_var = tk.BooleanVar(value=True)
axes_checkbox = tk.Checkbutton(
    color_frame, text="SHOW AXES", variable=show_axes_var,
    fg="white", bg=PANEL_COLOR, selectcolor=PANEL_COLOR, font=FONT_NORMAL,
    activebackground=PANEL_COLOR, activeforeground="white",
    command=lambda: [draw_mandel(), draw_julia(current_c, ax_julia)]
)
axes_checkbox.pack(side="left", padx=10)


# Julia Preview
julia_frame = tk.Frame(control_frame, bg=PANEL_COLOR)
julia_frame.pack(pady=5, fill="x")


julia_label = tk.Label(julia_frame, text="JULIA PREVIEW", fg="white", bg=PANEL_COLOR, font=FONT_NORMAL)
julia_label.pack(anchor="w", pady=2)


julia_canvas = tk.Canvas(julia_frame, width=350, height=350, bg="black", highlightthickness=1, highlightbackground=BORDER_COLOR)
julia_canvas.pack(pady=2)


# Navigation Controls
nav_frame = tk.Frame(control_frame, bg=PANEL_COLOR)
nav_frame.pack(pady=15, fill="x")


# Top row with main controls
top_row = tk.Frame(nav_frame, bg=PANEL_COLOR)
top_row.pack(fill="x")


zoom_in_btn = create_beautiful_button(top_row, "Zoom Out", zoom_in, width=8)
zoom_in_btn.pack(side="left", padx=2)


zoom_out_btn = create_beautiful_button(top_row, "Zoom In", zoom_out, width=8)
zoom_out_btn.pack(side="left", padx=2)


home_button = create_beautiful_button(top_row, "Home", home_view, width=6)
home_button.pack(side="left", padx=2)


undo_button = create_beautiful_button(top_row, "Undo", undo_view, width=6)
undo_button.pack(side="left", padx=2)


save_button = create_beautiful_button(top_row, "Save", save_image, width=6)
save_button.pack(side="left", padx=2)


# Bottom row with pan controls
bottom_row = tk.Frame(nav_frame, bg=PANEL_COLOR)
bottom_row.pack(fill="x", pady=5)


tk.Label(bottom_row, text="PAN:", fg="white", bg=PANEL_COLOR, font=FONT_NORMAL).pack(side="left", padx=2)


up_btn = create_arrow_button(bottom_row, "↑", lambda: pan('up'))
up_btn.pack(side="left", padx=2)


middle_frame = tk.Frame(bottom_row, bg=PANEL_COLOR)
middle_frame.pack(side="left")


left_btn = create_arrow_button(middle_frame, "←", lambda: pan('left'))
left_btn.pack(side="left", padx=2)


right_btn = create_arrow_button(middle_frame, "→", lambda: pan('right'))
right_btn.pack(side="left", padx=2)


down_btn = create_arrow_button(bottom_row, "↓", lambda: pan('down'))
down_btn.pack(side="left", padx=2)


# ========== MATPLOTLIB FIGURES ==========
fig_mandel = Figure(figsize=(10, 7), dpi=100)
fig_mandel.patch.set_facecolor("#A1B0B9")
ax_mandel = fig_mandel.add_subplot(111)
ax_mandel.set_facecolor("black")
canvas_mandel = FigureCanvasTkAgg(fig_mandel, master=left_frame)
canvas_mandel.get_tk_widget().pack(fill="both", expand=True)


fig_julia = Figure(figsize=(3.5, 3.5), dpi=100)
fig_julia.patch.set_facecolor("#536186")
ax_julia = fig_julia.add_subplot(111)
ax_julia.set_facecolor("black")
canvas_julia = FigureCanvasTkAgg(fig_julia, master=julia_canvas)
canvas_julia.get_tk_widget().pack(fill="both", expand=True)


# ========== EVENT BINDINGS ==========
canvas_mandel.mpl_connect('motion_notify_event', on_motion)
canvas_mandel.mpl_connect('button_press_event', on_click)
canvas_mandel.mpl_connect('button_press_event', on_press)
canvas_mandel.mpl_connect('button_release_event', on_release)
canvas_mandel.mpl_connect('scroll_event', on_scroll)


# ========== INITIAL DRAW ==========
draw_mandel()
draw_julia(current_c, ax_julia)


root.mainloop()
