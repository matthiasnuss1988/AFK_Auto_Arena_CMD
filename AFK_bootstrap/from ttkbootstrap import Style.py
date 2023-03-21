import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk
from PIL import ImageTk, Image

root = tb.Window(themename='yeti')
# Load the background image
bg_image = Image.open("C:/Users/matth/Desktop/AFK_bootstrap/images/background.png")

# Create a larger PIL image with the same dimensions as the root window
root_width = root.winfo_width()
root_height = root.winfo_height()
bg_width, bg_height = bg_image.size
x_offset = (root_width - bg_width) // 2
y_offset = (root_height - bg_height) // 2
bg_large = Image.new("RGBA", (root_width, root_height), (255, 255, 255, 255))

# Paste the original image onto the larger image at the center
bg_large.paste(bg_image, (x_offset, y_offset))

# Crop the larger image to fit the root window size
bg_cropped = bg_large.crop((0, 0, root_width, root_height))

# Convert the cropped image to a PhotoImage object and set it as the background image
bg_photo = ImageTk.PhotoImage(bg_cropped)
bg_label = tb.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a canvas
canvas = tb.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# Create the widgets
label1 = ttk.Label(canvas, text="This is a label with colspan 7 and font size 32", font=("TkDefaultFont", 32), anchor="center")
checkbox1 = ttk.Checkbutton(canvas, text="Checkbox 1")
checkbox2 = ttk.Checkbutton(canvas, text="Checkbox 2")
checkbox3 = ttk.Checkbutton(canvas, text="Checkbox 3")
checkbox4 = ttk.Checkbutton(canvas, text="Checkbox 4")
checkbox5 = ttk.Checkbutton(canvas, text="Checkbox 5")
entry_box = ttk.Entry(canvas)
label2 = ttk.Label(canvas, text="This is a label with columnspan 5 and font size 12", font=("TkDefaultFont", 12), anchor="center")
option_menu1 = ttk.OptionMenu(canvas, tk.StringVar(), "Option 1", "Option 1", "Option 2", "Option 3", "Option 4", "Option 5")
option_menu2 = ttk.OptionMenu(canvas, tk.StringVar(), "Option 1", "Option 1", "Option 2", "Option 3", "Option 4", "Option 5")
button = ttk.Button(canvas, text="Start")
button_stop = ttk.Button(canvas, text="Stop")
button_exit = ttk.Button(canvas, text="Exit")

# Set the position of the widgets on the canvas
canvas.create_window(0, 0, anchor="nw", window=label1, width=700, height=60)
canvas.create_window(0, 60, anchor="nw", window=checkbox1)
canvas.create_window(120, 60, anchor="nw", window=checkbox2)
canvas.create_window(240, 60, anchor="nw", window=checkbox3)
canvas.create_window(360, 60, anchor="nw", window=checkbox4)
canvas.create_window(480, 60, anchor="nw", window=checkbox5)
canvas.create_window(0, 90, anchor="nw", window=entry_box, width=500)
canvas.create_window(100, 130, anchor="nw", window=label2, width=500, height=30)
canvas.create_window(0, 160, anchor="nw", window=option_menu1, width=500)
canvas.create_window(0, 190, anchor="nw", window=option_menu2, width=500)
canvas.create_window(0, 220, anchor="nw", window=button, width=100)
canvas.create_window(100, 220, anchor="nw", window=button_stop, width=100)
canvas.create_window(200, 220, anchor="nw", window=button_exit, width=100)

root.mainloop()