
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from shared_functions import  disable_combat_modes, master_meter_timer,calc_scale_meters
from shared_functions import *
from loop import makro
import time
import sys
import os
import win32con
import ctypes
#import queue
#from multiprocessing import Process, Pipe
import threading
initial_communication_data= {
        'autokampf': None,
        'script_time': 0,
        'stage_time': 0,
        'formation_time': 0,
        'stage_mode': 1,
        'restart_time': 120 * 60,
        'formations': [1, 2, 3, 4, 5],
        'formation_stripe':0,
        'formation_progress': 0.0,
        'formation_message': '',
        'formation_remaining': None,
        'formation_counter': 0,
        'formation_active': 1,
        'stage_stripe':0,
        'stage_progress': 0.0,
        'stage_message': '',
        'stage_remaining': None,
        'stage_level': 0,
        'stage_counter': 0,
        'script_stripe':0,
        'script_progress': 0.0,
        'script_message': '',
        'script_runtime': None,
        'script_counter': 0
    }
communication_data=initial_communication_data.copy()

stop_event = threading.Event()
formation_start_event= threading.Event()
stage_start_event= threading.Event()
script_start_event= threading.Event()
restart_event= threading.Event()
my_lock = threading.Lock()

def is_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            print("Script is admin")
            return True
    except:
        pass
    print("Set script to admin")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(sys.argv[0])}"', None,  win32con.SW_SHOWMINIMIZED)
    return False

def callback_handler(local_dict):
        formation_meter.configure(amountused=local_dict['formation_progress'], subtext=local_dict['formation_message'])
        stage_meter.configure( amountused=local_dict['stage_progress'], subtext=local_dict['stage_message'])
        script_meter.configure(amountused=local_dict['script_progress'], subtext=local_dict['script_message'])

def stop_threads():
    if stage_start_event.is_set():
        stage_start_event.clear() 
    if formation_start_event.is_set():
        formation_start_event.clear() 
    if restart_event.is_set():
        restart_event.clear()
    if script_start_event.is_set():
        script_start_event.clear() 
    stop_event.set()
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    clear_button.config(state="normal")


def start_threads():
  # Clear the stop event before starting the threads
    threading.Thread(target=master_meter_timer, args=(communication_data, callback_handler, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event,my_lock), daemon=True).start()
    threading.Thread(target=makro, args=(communication_data, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event,my_lock), daemon=True).start()      

def start_script():
    global communication_data
    if stop_event.is_set():
        stop_event.clear()

    communication_data=initial_communication_data.copy()

    # Create a mapping of time options to seconds
    time_mappings = {"1 h": 3600, "3 h": 180*60, "6 h": 360*60, "infinite loop": 9999*60}
    script_time = time_mappings.get(selected_script_time.get(), 60)
    
    # Set up combat_modes_dict and get the selected combat mode
    combat_modes_dict = {"Campaign": 1,"King's Tower": 2,"Celestial Sanctum": 3,"Tower of Light": 4, "The Brutal Citadel": 5,"Infernal Fortress": 6,"The Forsaken Necropolis": 7,"The World Tree": 8}
    combat_mode = selected_combat_mode.get()
    stage_mode = combat_modes_dict.get(combat_mode, 1) # map empty or not found case to Campaign (1)

    # Calculate and update communication data
    communication_data['script_time'] = script_time
    communication_data['stage_mode'] = stage_mode
    communication_data['formation_time'] = int(float(entry_formation_time.get()))*60
    communication_data['formations'] = calculate_checked_indices()
    communication_data['stage_time'] = (communication_data['formation_time']+5)*len(communication_data['formations'])

    # Update meters
    calc_scale_meters(communication_data)
    meter_labelFrame.configure(text=f"Combat mode:  {combat_mode}")
    formation_meter.configure(stripethickness=communication_data['formation_stripe'], subtext=communication_data['formation_message'])
    stage_meter.configure(stripethickness=communication_data['stage_stripe'],  subtext=communication_data['stage_message'])
    script_meter.configure(stripethickness=communication_data['script_stripe'], subtext=communication_data['script_message'])

    # Start threads and configure button states
    start_threads()
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    clear_button.config(state="disabled")

def clear_entry():
    communication_data=initial_communication_data.copy()
    start_button.config(state="normal")
    stop_button.config(state="normal")
    entry_formation_time.configure(foreground='gray')
    selected_script_time.set(value="Select script time")
    selected_combat_mode.set(value="Select combat mode")
    my_style.configure("combat_mode.TMenubutton",arrowcolor='white',font=('Helvetica',18),background='#191919',foreground='gray',bordercolor='white',border=2,padding=6)
    my_style.configure("script_time.TMenubutton",arrowcolor='white',font=('Helvetica',18),background='#191919',foreground='gray',bordercolor='white',border=2,padding=6)
    entry_formation_time.delete(0, tb.END)
    entry_formation_time.insert(0, "Combat time per formation")
    formation_meter.configure(amountused=0.0, subtext='')
    stage_meter.configure(amountused=0.0, subtext='')
    script_meter.configure(amountused=0.0,subtext='')

def exit_app():
    root.destroy()

def on_entry_formation_time_click(event):
    if entry_formation_time.get() == "Combat time per formation":
        entry_formation_time.delete(0, tb.END)
        entry_formation_time.configure(foreground='gray')

def on_entry_formation_time_type(event):
    if entry_formation_time.get() == "Combat time per formation":
        entry_formation_time.delete(0, tb.END)
        entry_formation_time.configure(foreground='white')
    else:
        entry_formation_time.configure(foreground='white')

def on_entry_keypress(event):
    if event.char.isdigit() or event.keysym == "BackSpace" or event.keysym == "Delete":
        entry_formation_time.after_idle(on_entry_formation_time_type, event)
        return None
    else:
        return "break"






#Create the main application
root = tb.Window(themename='cyborg')
off_x=10
off_y=10
app_width=595
app_height=900
screen_width = root.winfo_screenwidth()
screen_height= root.winfo_screenheight()
app_x_pos=screen_width -app_width-10
app_y_pos=0

##Set the window size, title and location
root.title("AFK Auto Arena")
root.iconbitmap(get_image_path("icon.ico"))
root.geometry(f'{app_width}x{app_height}+{app_x_pos}+{app_y_pos}')
root.resizable(False, False)

##Open the background image and convert it to a tkinter-compatible format
bg= PhotoImage(file=get_image_path("background.png"))
my_label = Label(root, image=bg)
my_label.place(x=0,y=0,relwidth=1, relheight=1)

##Create canvas
my_canvas = Canvas(root,width=600, height=900,highlightthickness=0)
my_canvas.pack(fill="both", expand=True)


##Set image in canvas
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

#Style
my_style=tb.Style()

##Buttons
     
button_font_size=20
button_width=7
button_pixel_width=button_font_size*button_width-off_x
button_y=app_height-off_y**2
line_width=4*button_pixel_width

my_style.configure('success.TButton', font=('Helvetica',button_font_size,'bold'),bordercolor='white')
my_style.configure('danger.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white')
my_style.configure('warning.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white')
my_style.configure('dark.TButton', font=('Helvetica',button_font_size,'bold'), bordercolor='white',foreground='white')

start_button = tb.Button(root, text="Start",bootstyle="success",style='success.TButton',width=button_width,command=start_script)
stop_button = tb.Button(root, text="Stop",bootstyle="danger",style='danger.TButton',width=button_width,command=stop_threads)
stop_button.config(state="disabled")
clear_button = tb.Button(root, text="Clear",bootstyle="warning",style='warning.TButton',width=button_width,command=clear_entry)
exit_button = tb.Button(root, text="Exit",bootstyle="dark",style='dark.TButton',width=button_width,command=exit_app)

start_window=my_canvas.create_window(4*off_x,button_y, anchor="nw",window=start_button)
stop_window=my_canvas.create_window(4*off_x+button_pixel_width,button_y,anchor="nw",window=stop_button)
clear_window=my_canvas.create_window(4*off_x+2*button_pixel_width,button_y, anchor="nw",window=clear_button)
exit_window=my_canvas.create_window(4*off_x+3*button_pixel_width,button_y,anchor="nw",window=exit_button)

##Entry box
my_style.configure('dark.TEntry',borderwith=2,bordercolor='white')
entry_formation_time = tb.Entry(root, style="dark.TEntry", font=('Helvetica', 18),foreground='gray')
entry_formation_time.insert(0, "Combat time per formation")
    
#Bind the Enter key to the entry widget

entry_formation_time.bind('<FocusIn>', on_entry_formation_time_click)
entry_formation_time.bind('<Key>', on_entry_keypress)

entry_formation_time_window=my_canvas.create_window(4*off_x,290,width=line_width-1,anchor='nw',window=entry_formation_time)

##OptionMenus
# create a new style based on dark.TMenubutton with a red foreground color
my_style.configure("combat_mode.TMenubutton",**my_style.configure('dark.TMenubutton'))
my_style.configure('script_time.TMenubutton', **my_style.configure('dark.TMenubutton'))
my_style.configure("combat_mode.TMenubutton",arrowcolor='white',font=('Helvetica',18),background='#191919',foreground='gray',bordercolor='white',border=2,padding=6)
my_style.configure('script_time.TMenubutton', arrowcolor='white',font=('Helvetica',18),background='#191919',foreground='gray',bordercolor='white',border=2,padding=6)
my_style.map('combat_mode.TMenubutton',background=[('active','#191919')],bordercolor=[('active','withe')])
my_style.map('script_time.TMenubutton',background=[('active','#191919')],bordercolor=[('active','withe')])

#combat mode
def combat_mode_selected(e):
    my_style.configure("combat_mode.TMenubutton",foreground='white')

selected_combat_mode = tb.StringVar(value="Select combat mode")
combat_modes = ["","Campaign", "King's Tower", "Celestial Sanctum", "Tower of Light", "The Brutal Citadel", "Infernal Fortress", "The Forsaken Necropolis", "The World Tree"]
combat_mode_menu = tb.OptionMenu(root,  selected_combat_mode,bootstyle='dark',style='combat_mode.TMenubutton', *combat_modes, command=combat_mode_selected)
combat_mode_menu['menu'].configure(font=('Helvetica',18), background='white')
#print(combat_mode_menu["menu"].keys())
combat_modes.pop(0)
combat_mode_menu_window=my_canvas.create_window(4*off_x,190,width=line_width-1,anchor='nw',window=combat_mode_menu)

#Script time
def script_time_selected(f):
    my_style.configure("script_time.TMenubutton",foreground='white')

selected_script_time = tb.StringVar(value="Select script time")
script_times = ["","1 h", "3 h", "6 h", "infinite loop"]
script_time_menu = tb.OptionMenu(root,  selected_script_time,bootstyle='dark',style='script_time.TMenubutton', *script_times, command=script_time_selected)
script_time_menu['menu'].configure(font=('Helvetica',18),background='white', border=4,foreground='black')
#print(script_mode_menu["menu"].keys())
script_times.pop(0)
script_time_menu_window=my_canvas.create_window(4*off_x,190-off_y-2*18,width=line_width-1,anchor='nw',window=script_time_menu)

#LabelFrame Style
my_style.configure('primary.TLabelframe', bordercolor='white',border=4,borderwidth=2,labelmargins=4,labeloutside=False,padding=0, relief='solid')
my_style.configure('primary.TLabelframe.Label',font=('Helvetica',12,'bold'),foreground='white')

##Meters
meterdim=165
meter_height=button_y-off_y*5-10-meterdim

# Create 3 meters
meter_labelFrame=tb.LabelFrame(my_canvas,text='Combat mode: ', style='primary.TLabelframe')
meterstyle_list=['danger','primry','success']
meters=[]
meter_list=['script_meter','stage_meter','formation_meter']
for i in range(3):
    meter = tb.Meter(meter_labelFrame, metersize=meterdim,
    padding=4,
    bootstyle=meterstyle_list[i],
    showtext=True,
    stripethickness=0,
    amountused=0,
    textfont="-size 28 -weight bold",
    textright="%",
    amounttotal=100,
    metertype="full",
    subtext="",
    subtextfont="-size 11 -weight bold",
    interactive=False,)
    #meter.configure(amountused = 0)
    locals()[meter_list[i]] = meter
    meter.pack(side=tb.LEFT, padx=0, pady=off_y)
meter_window=my_canvas.create_window(4*off_x,meter_height,width=line_width-1, anchor="nw",window=meter_labelFrame)

#FormationLabelFrame
formation_labelFrame=tb.LabelFrame(my_canvas,text='Formation: [1,2,3,4,5]', style='primary.TLabelframe')
#Checkbuttons
def calculate_checked_indices():
    checked_indices = []
    for i, var in enumerate([var_f1, var_f2, var_f3, var_f4, var_f5]):
        if var.get():
            checked_indices.append(i+1)  # append index starting from 1 instead of 0
        formation_labelFrame.configure(text=f"Formation:{str(checked_indices)}")
    return checked_indices

my_style.configure('success.TCheckbutton',font=('Helvetica',18))
formation_label_text=['F-1','F-2','F-3','F-4','F-5']
check_names=['var_f1','var_f2','var_f3','var_f4','var_f5']
formationlabel_names=['formation_label_1','formation_label__2','formation_label__3','formation_label__4','formation_label__5']
formation_names=['formation_1','formation_2','formation_3','formation_4','formation_5']


for i in range(5):
    check= tb.BooleanVar(value=True)
    formation_label=tb.Label(formation_labelFrame,
    text=formation_label_text[i],
    font=('Helvetica,12')
    )
    formation = tb.Checkbutton(formation_labelFrame,
    text='',
    variable=check,
    compound='top',
    onvalue=1,
    offvalue=0,
    style='success.TCheckbutton',
    bootstyle=SUCCESS,
    command=calculate_checked_indices
    )
    locals()[formationlabel_names[i]] = formation_label
    locals()[formation_names[i]] = formation
    locals()[check_names[i]] = check
    formation_label.grid(column=i,row=1, padx=3, pady=1)
    formation.grid(column=i,row=2, padx=3, pady=1)
 
formation_window=my_canvas.create_window(4*off_x+line_width-1-meterdim-4-4,meter_height-off_y*7+2,width=int((line_width-1)/3), anchor="nw",window=formation_labelFrame)

#Tooltips
tooltip1=ToolTip(entry_formation_time,text='Here you specify the combat time per formation, e.g., 3 min for easy, 5 min for medium and 10 min for hard combats',bootstyle=(SECONDARY,INVERSE))
tooltip2=ToolTip(script_time_menu,text='Here you specify the total running time of the battle mode, e.g., 1 h, 3 h, 6 h or in infinite loop.',bootstyle=(SECONDARY,INVERSE))
tooltip3=ToolTip(combat_mode_menu,text='Here you specify the battle mode that you want your teams to combat in.',bootstyle=(SECONDARY,INVERSE))


disable_combat_modes(root,combat_mode_menu,combat_modes)


# def update_widget():
#     if parent_conn.poll():
#         communication_data = parent_conn.recv()
#         # Update the widget using the updated communication_data
#         formation_meter.configure(stripethickness=calc_stripethickness(communication_data['formation_time']), amountused=communication_data['format_progress'], subtext=communication_data['format_message'])
#         stage_meter.configure(stripethickness=calc_stripethickness(communication_data['stage_time'] ), amountused=communication_data['stage_progress'], subtext=communication_data['stage_message'])
#         script_meter.configure(stripethickness=calc_stripethickness(communication_data['script_time']),amountused=communication_data['script_progress'],subtext=communication_data['script_message'])
#     # Schedule the function to run again after a delay
#     root.after(1000, update_widget)
if not is_admin():
    sys.exit() 
root.mainloop()

