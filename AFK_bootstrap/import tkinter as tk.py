import tkinter as tk
from tkinter import *
import time
import ttkbootstrap as tb
from PIL import Image, ImageTk
import threading
import time
from loop_process import my_loop


def start_loop():
    global loop_thread, stop_flag
    stop_flag = True
    loop_thread = threading.Thread(target=my_loop, args=(stop_flag,))
    loop_thread.start()

def stop_loop():
    global loop_thread, stop_flag
    if loop_thread is not None:
        stop_flag = False
        loop_thread.join()
        loop_thread = None


#Create the main application
root = tb.Window(themename='flatly')
off_x=10
off_y=10
app_width=595
app_height=900
screen_width = root.winfo_screenwidth()
screen_height= root.winfo_screenheight()
app_x_pos=screen_width -app_width-10
app_y_pos=0
#Set the window size, title and location
root.title("AFK Auto Arena")
root.iconbitmap("C:/Users/matth/Desktop/AFK_bootstrap/images/icon.ico")
root.geometry(f'{app_width}x{app_height}+{app_x_pos}+{app_y_pos}')
root.resizable(False, False)

# Open the background image and convert it to a tkinter-compatible format
bg= PhotoImage(file="C:/Users/matth/Desktop/AFK_bootstrap/images/background.png")
my_label = Label(root, image=bg)
my_label.place(x=0,y=0,relwidth=1, relheight=1)
# my_text=Label(root,text="Welcome!", font=("Helvetica",50),fg="white")
# my_text.pack(pady=50)
my_canvas = Canvas(root,width=600, height=900,highlightthickness=0)
my_canvas.pack(fill="both", expand=True)


#Set image in canvas
my_canvas.create_image(300,465,image=bg,ancho="center")
my_canvas.create_text(300,50, text="AFK Auto Arena", font=("Helvetica",32),fill='white')

def rounded_rect(canvas, x, y, w, h, c):
    canvas.create_arc(x,   y,   x+2*c,   y+2*c,   start= 90, extent=90, style="arc",outline="white",width=4)
    canvas.create_arc(x+w-2*c, y+h-2*c, x+w, y+h, start=270, extent=90, style="arc",outline="white",width=4)
    canvas.create_arc(x+w-2*c, y,   x+w, y+2*c,   start=  0, extent=90, style="arc",outline="white",width=4)
    canvas.create_arc(x,   y+h-2*c, x+2*c,   y+h, start=180, extent=90, style="arc",outline="white",width=4)
    canvas.create_line(x+c, y,   x+w-c, y    , fill="white",width=4)
    canvas.create_line(x+c, y+h, x+w-c, y+h  , fill="white",width=4)
    canvas.create_line(x,   y+c, x,     y+h-c, fill="white",width=4)
    canvas.create_line(x+w, y+c, x+w,   y+h-c, fill="white",width=4)

my_rectangle = rounded_rect(my_canvas, off_x, off_y, app_width-2*off_x, app_height-2*off_y, 25)

#Buttons
#Style
button_font_size=20
button_width=7
button_pixel_width=button_font_size*button_width-off_x
button_y=app_height-off_y**2
line_width=4*button_pixel_width
my_style=tb.Style()
my_style.configure('success.Outline.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white')
my_style.configure('danger.Outline.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white')
my_style.configure('warning.Outline.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white')
my_style.configure('dark.Outline.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white')

start_button = tb.Button(root, text="Start",bootstyle="success-Outline",style='success.Outline.TButton',width=button_width,command=start_loop)
stop_button = tb.Button(root, text="Stop",bootstyle="danger-Outline",style='danger.Outline.TButton',width=button_width,command=stop_loop)
clear_button = tb.Button(root, text="Clear",bootstyle="warning-Outline",style='warning.Outline.TButton',width=button_width)
exit_button = tb.Button(root, text="Exit",bootstyle="dark-Outline",style='dark.Outline.TButton',width=button_width)

start_window=my_canvas.create_window(4*off_x,button_y, anchor="nw",window=start_button)
stop_window=my_canvas.create_window(4*off_x+button_pixel_width,button_y,anchor="nw",window=stop_button)
clear_window=my_canvas.create_window(4*off_x+2*button_pixel_width,button_y, anchor="nw",window=clear_button)
exit_window=my_canvas.create_window(4*off_x+3*button_pixel_width,button_y,anchor="nw",window=exit_button)

#Entry Boxes
#Style
# Define a 20% transparent white color using the RGB method
# Create a new 50x50 image with a white background
# Create a semi-transparent white image
# create a transparent image
# create a transparent image
width = 40
font_size = 18
semitrans_image = Image.new("RGBA", (width * font_size, font_size), (0, 200, 255, 50))
semitrans_photo = ImageTk.PhotoImage(semitrans_image)

# Function to update the labelFrame text of the meters
def update_meter_labelFrame_text(event=None):
    new_text = entry_teamtime.get().strip()
    if new_text:
        lf.config(text=new_text)




entry_teamtime = tb.Entry(root, style="primary.TEntry", width=40, font=('Helvetica', 18))
entry_teamtime.insert(0, "Kampfzeit pro Team, z.B. 3, 5 oder 10 min")
def on_entry_teamtime_click(event):
    entry_teamtime.delete(0, tk.END)
    entry_teamtime.configure(foreground='gray')
    entry_teamtime.insert(0, "Kampfzeit pro Team, z.B. 3, 5 oder 10 min")

def on_entry_teamtime_type(event):
    if entry_teamtime.get() == "Kampfzeit pro Team, z.B. 3, 5 oder 10 min":
        entry_teamtime.delete(0, tk.END)
        entry_teamtime.configure(foreground='black')
    else:
        entry_teamtime.configure(foreground='black')

# Bind the '<FocusIn>' event to the on_entry_click function
entry_teamtime.bind('<FocusIn>', on_entry_teamtime_click)

# Bind the '<Key>' event to the on_entry_type function
entry_teamtime.bind('<Key>', on_entry_teamtime_type)
 # bind the Enter key to the entry widget

entry_teamtime.bind('<Return>', update_meter_labelFrame_text)
entry_scriptime=Entry(root,font=('Helvetica',24),width=14, bg='#336d92',bd=0)
entry_teamtime_window=my_canvas.create_window(34,290,anchor='nw',window=entry_teamtime)

##Meters
# Configure the 'TMeter' style to have a transparent background
my_style.configure('primary.TLabelframe', borderwidth=2,labelmargins=0,labeloutside=False,padding=0, relief='solid')
my_style.configure('primary.TLabelframe.Label',font=('Helvetica',12,'bold'))
lf =tb.LabelFrame(my_canvas,text='Kampfmodus: ', style='primary.TLabelframe')
#meter_window=my_canvas.create_window(0,100, anchor="nw",window=meter_labelframe)
meterdim=165
# Create 3 meters
meterstyle_list=['danger','primry','success']
for i in range(3):
    meter = tb.Meter(lf, metersize=meterdim,
    padding=4,
    bootstyle=meterstyle_list[i],
    showtext=True,
    stripethickness=0,
    amountused=0,
    textfont="-size 32 -weight bold",
    textright="%",
    amounttotal=100,
    metertype="full",
    subtext="",
    subtextfont="-size 12 -weight bold",
    interactive=False,)
    meter.pack(side=tk.LEFT, padx=0, pady=off_y)
#meter_labelframe.place(x=2*off_x, y=500, width=app_width-12*off_x, height=200)
#meter_restart.place(x=3*off_x, y=500+off_x)
meter_height=button_y-off_y*5-1-meterdim
meter_window=my_canvas.create_window(4*off_x,meter_height,width=line_width-1, anchor="nw",window=lf)
#meter_restart.configure(background="")
#start_meter_window=my_canvas.create_window(4*off_x,app_height-6*off_y-meterdim, anchor="nw",window=meter_restart)






root.mainloop()