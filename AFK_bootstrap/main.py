from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from PIL import ImageTk, Image
import sys
from  shared_functions import  disable_combat_modes, update_meters

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
root.iconbitmap("C:/Users/matth/Desktop/AFK_bootstrap/images/icon.ico")
root.geometry(f'{app_width}x{app_height}+{app_x_pos}+{app_y_pos}')
root.resizable(False, False)

##Open the background image and convert it to a tkinter-compatible format
bg= PhotoImage(file="C:/Users/matth/Desktop/AFK_bootstrap/images/background.png")
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

start_button = tb.Button(root, text="Start",bootstyle="success",style='success.TButton',width=button_width)
stop_button = tb.Button(root, text="Stop",bootstyle="danger",style='danger.TButton',width=button_width)
clear_button = tb.Button(root, text="Clear",bootstyle="warning",style='warning.TButton',width=button_width)
exit_button = tb.Button(root, text="Exit",bootstyle="dark",style='dark.TButton',width=button_width)

start_window=my_canvas.create_window(4*off_x,button_y, anchor="nw",window=start_button)
stop_window=my_canvas.create_window(4*off_x+button_pixel_width,button_y,anchor="nw",window=stop_button)
clear_window=my_canvas.create_window(4*off_x+2*button_pixel_width,button_y, anchor="nw",window=clear_button)
exit_window=my_canvas.create_window(4*off_x+3*button_pixel_width,button_y,anchor="nw",window=exit_button)

##Entry box
my_style.configure('dark.TEntry',borderwith=2,bordercolor='white')
entry_Formationtime = tb.Entry(root, style="dark.TEntry", font=('Helvetica', 18),foreground='gray')
entry_Formationtime.insert(0, "Combat time per formation")
def on_entry_Formationtime_click(event):
    entry_Formationtime.delete(0, tb.END)
    entry_Formationtime.configure(foreground='gray')
    entry_Formationtime.insert(0, "Combat time per formation")

def on_entry_Formationtime_type(event):
    if entry_Formationtime.get() == "Combat time per formation":
        entry_Formationtime.delete(0, tb.END)
        entry_Formationtime.configure(foreground='white')
    else:
        entry_Formationtime.configure(foreground='white')
#Bind the '<FocusIn>' event to the on_entry_click function
entry_Formationtime.bind('<FocusIn>', on_entry_Formationtime_click)
#Bind the '<Key>' event to the on_entry_type function
entry_Formationtime.bind('<Key>', on_entry_Formationtime_type)
#Bind the Enter key to the entry widget
entry_Formationtime_window=my_canvas.create_window(4*off_x,290,width=line_width-1,anchor='nw',window=entry_Formationtime)

##OptionMenus
    

# get the current settings for the dark.TMenubutton style
#menubutton_settings = my_style.lookup('dark.TMenubutton', None, default={})
# create a new style based on dark.TMenubutton with a red foreground color
my_style.configure("combat_mode.TMenubutton",**my_style.configure('dark.TMenubutton'))
my_style.configure('combat_time.TMenubutton', **my_style.configure('dark.TMenubutton'))
my_style.configure("combat_mode.TMenubutton",arrowcolor='white',font=('Helvetica',18),background='#191919',foreground='gray',bordercolor='white',border=2,padding=6)
my_style.configure('combat_time.TMenubutton', arrowcolor='white',font=('Helvetica',18),background='#191919',foreground='gray',bordercolor='white',border=2,padding=6)
my_style.map('combat_mode.TMenubutton',background=[('active','#191919')],bordercolor=[('active','withe')])
my_style.map('combat_time.TMenubutton',background=[('active','#191919')],bordercolor=[('active','withe')])
#combat mode
def combat_mode_selected(e):
    my_style.configure("combat_mode.TMenubutton",foreground='white')
    selection=selected_combat_mode.get()
selected_combat_mode = tb.StringVar(value="Select combat mode")
combat_modes = ["","Campaign", "King's Tower", "Celestial Sanctum", "Tower of Light", "The Brutal Citadel", "Infernal Fortress", "The Forsaken Necropolis", "The World Tree"]
combat_mode_menu = tb.OptionMenu(root,  selected_combat_mode,bootstyle='dark',style='combat_mode.TMenubutton', *combat_modes, command=combat_mode_selected)
combat_mode_menu['menu'].configure(font=('Helvetica',18), background='white')
#print(combat_mode_menu["menu"].keys())
combat_modes.pop(0)
combat_mode_menu_window=my_canvas.create_window(4*off_x,190,width=line_width-1,anchor='nw',window=combat_mode_menu)

#Combat time
def combat_time_selected(f):
    my_style.configure("combat_time.TMenubutton",foreground='white')
    selection=selected_combat_time.get()
selected_combat_time = tb.StringVar(value="Select combat time")
combat_times = ["","1 h", "3 h", "6 h", "infinite loop"]
combat_time_menu = tb.OptionMenu(root,  selected_combat_time,bootstyle='dark',style='combat_time.TMenubutton', *combat_times, command=combat_time_selected)
combat_time_menu['menu'].configure(font=('Helvetica',18),background='white', border=4,foreground='black')
#print(combat_mode_menu["menu"].keys())
combat_times.pop(0)
combat_time_menu_window=my_canvas.create_window(4*off_x,190-off_y-2*18,width=line_width-1,anchor='nw',window=combat_time_menu)

#LabelFrame Style
my_style.configure('primary.TLabelframe', bordercolor='white',border=4,borderwidth=2,labelmargins=4,labeloutside=False,padding=0, relief='solid')
my_style.configure('primary.TLabelframe.Label',font=('Helvetica',12,'bold'),foreground='white')

##Meters
meterdim=165
meter_height=button_y-off_y*5-10-meterdim


# Create 3 meters
meter_labelFrame=tb.LabelFrame(my_canvas,text='Kampfmodus: ', style='primary.TLabelframe')
meterstyle_list=['danger','primry','success']
meters=[]
meter_list=['restart_meter','stage_meter','Formation_meter']
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
    print(checked_indices)

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
tooltip1=ToolTip(entry_Formationtime,text='Here you specify the combat time per formation, e.g., 3 min for easy, 5 min for medium and 10 min for hard levels',bootstyle=(SECONDARY,INVERSE))
tooltip2=ToolTip(combat_time_menu,text='Here you specify the total running time of the battle mode, e.g., 1 h, 3 h, 6 h or in infinite loop.',bootstyle=(SECONDARY,INVERSE))
tooltip3=ToolTip(combat_mode_menu,text='Here you specify the battle mode that you want your teams to combat in.',bootstyle=(SECONDARY,INVERSE))







# create the entry box
entry_box = tb.Entry(root,font=("Helvetica",18),bootstyle="info")
#entry_box.grid(column=1,row=3,columnspan=5, pady=5,padx=5)
entry_box.bind("<Return>", lambda event: callback())






# start toolbutton style
#tb.Checkbutton(bootstyle="success-toolbutton")

# stop toolbutton style
#tb.Checkbutton(bootstyle="danger-toolbutton")

# success round toggle style
#way_checkbutton=tb.Checkbutton(bootstyle="success-round-toggle")
#way_checkbutton.grid(column=3,row=7, pady=5,padx=5)




# update the amount used directly




#combat_mode_menu.grid(column=3, row=5)


#global remaining_time

disable_combat_modes(root,combat_mode_menu,combat_modes)




#remaining_time = update_meter(root, meter, max_time, 1, Formation_val, remaining_time)

max_Formation_time=120
Formation_val=5
stage_val=645
max_stage_time=20*60
max_script_time=120*60
update_meters(root, Formation_meter, restart_meter, stage_meter, max_Formation_time, max_script_time, max_stage_time, Formation_val, stage_val)
#update_restart_meter(root, meter_restart, 120*60)#Meter variables where built in loop before
#update_stage_meter(root, meter_stage, 20*60, 5)
#update_Formation_meter(root, meter_Formation, 120, 5)



root.mainloop()