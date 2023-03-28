import cv2
import numpy as np
import win32gui
import tkinter as tk
from Vision import capture_window,capture_window_normalized

bluestacks = "BlueStacks App Player"
window_handle = win32gui.FindWindow(None, bluestacks)
img_np = cv2.cvtColor(capture_window_normalized(window_handle), cv2.COLOR_BGR2RGB)

# Define the initial crop coordinates as relative values
x_rel = 0.2
y_rel = 0.2
w_rel = 0.6
h_rel = 0.6

def update_cords():
    global x_rel, y_rel, w_rel, h_rel
    x_rel = x_slider.get() / 100
    y_rel = y_slider.get() / 100
    w_rel = w_slider.get() / 100
    h_rel = h_slider.get() / 100
    update_preview()

def update_preview():
    global img_np, x_rel, y_rel, w_rel, h_rel
    height, width, _ = img_np.shape
    x_abs = int(x_rel * width)
    y_abs = int(y_rel * height)
    w_abs = int(w_rel * width)
    h_abs = int(h_rel * height)
    if 0 <= x_abs < width and 0 <= y_abs < height and x_abs + w_abs <= width and y_abs + h_abs <= height:
        img_crop = img_np[y_abs:y_abs + h_abs, x_abs:x_abs + w_abs]
    else:
        img_crop = img_np
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(img_crop))
    preview_label.config(image=img_tk)
    preview_label.image = img_tk

# Create the GUI
root = tk.Tk()
root.title("Crop Coordinates")

# Create the sliders
x_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="X", command=update_cords)
y_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Y", command=update_cords)
w_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Width", command=update_cords)
h_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Height", command=update_cords)

# Set the initial slider values
x_slider.set(x_rel * 100)
y_slider.set(y_rel * 100)
w_slider.set(w_rel * 100)
h_slider.set(h_rel * 100)

# Create the preview image label
preview_label = tk.Label(root)
preview_label.pack()

# Pack the sliders
x_slider.pack(fill=tk.X, padx=10, pady=10)
y_slider.pack(fill=tk.X, padx=10, pady=10)
w_slider.pack(fill=tk.X, padx=10, pady=10)
h_slider.pack(fill=tk.X, padx=10, pady=10)

# Update the preview image
update_preview()

# Run the GUI
root.mainloop()