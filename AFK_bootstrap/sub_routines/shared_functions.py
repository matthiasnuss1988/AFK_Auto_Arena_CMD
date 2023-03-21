from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime, time

def calc_stripethickness(duration):
    if duration >180:
        stripethickness=0
    stripethickness = int(360/duration)
    return stripethickness 

def update_meter(root, my_meter, max_time, decr_sec, team_val): 
    global remaining_time
    remaining_time -= decr_sec
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    message_str = f"Team {team_val}: {minutes:02}:{seconds:02}"
    amount_used = max_time - remaining_time
    progress=amount_used*100/max_time
    formated_progress = "{:.1f}".format(progress)
    my_meter.configure(stripethickness=calc_stripethickness(max_time),amountused=formated_progress, subtext=message_str)
    if remaining_time > 0:
        root.after(1000, update_meter,max_time,1,team_val)

def disable_OptionMenue(option_menu,options):
    weekday_options = {
        'Monday': [3, 5, 6, 7, 8],
        'Tuesday': [3, 4, 6, 7, 8],
        'Wednesday': [4, 5, 7, 8],
        'Thursday': [3, 4, 5, 8],
        'Friday': [3, 4, 5, 6, 8],
        'Saturday': [3, 4, 5, 6, 7],
        'Sunday': [3, 4, 5],
    }

    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    d = datetime.now()
    day = weekday[d.weekday()]
    now = datetime.now()
    twoAM = time(2, 0, 0)
    options_to_disable = weekday_options.get(day, [])
    for i, trend in enumerate(options):
        if now.time() >= twoAM:
            if i in options_to_disable:
                option_menu['menu'].entryconfig(i, state='disabled')
            else:
                option_menu['menu'].entryconfig(i, foreground='blue')
        else:
           option_menu['menu'].entryconfig(i, state='disabled')
