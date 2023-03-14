from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime, time

def split_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds

def calc_stripethickness(duration):
    if duration >180:
        stripethickness=0
    stripethickness = int(360/duration)
    return stripethickness 

counter=0
def update_meters(root, formation_meter, restart_meter, stage_meter, max_formation_time, max_script_time, max_stage_time, formation_val,stage_val):
    global counter
    counter += 1
    update_formation_meter(formation_meter, max_formation_time, formation_val,counter)
    update_restart_meter(restart_meter, max_script_time,counter)
    update_stage_meter(stage_meter, max_stage_time, stage_val, counter)
    root.after(1000, update_meters, root, formation_meter, restart_meter, stage_meter, max_formation_time, max_script_time, max_stage_time, formation_val, stage_val)
    
def update_formation_meter(formation_meter, max_formation_time, formation_val,counter):
    remaining_time = max_formation_time - counter
    hrs, mins, secs = split_seconds(remaining_time)
    message_str = f"formation {formation_val}: {mins:02}:{secs:02}"
    if remaining_time >= 0:
        amount_used = max_formation_time - remaining_time
        progress = amount_used * 100 / max_formation_time
        formated_progress = "{:.1f}".format(progress)
        formation_meter.configure(stripethickness=calc_stripethickness(max_formation_time), amountused=formated_progress, subtext=message_str)
        
def update_restart_meter(restart_meter, max_script_time,counter):
    remaining_time = max_script_time - counter
    hrs, mins, secs = split_seconds(remaining_time)
    message_str = f"Restart: {hrs:02}:{mins:02}:{secs:02}"
    if remaining_time >= 0:
        amount_used = max_script_time - remaining_time
        progress = amount_used * 100 / max_script_time
        formated_progress = "{:.1f}".format(progress)
        restart_meter.configure(stripethickness=calc_stripethickness(max_script_time), amountused=formated_progress, subtext=message_str)

def update_stage_meter(stage_meter, max_stage_time, stage_val, counter):
    remaining_time = max_stage_time - counter
    hrs, mins, secs = split_seconds(remaining_time)
    message_str = f"Stage {stage_val}: {mins:02}:{secs:02}"
    if remaining_time >= 0:
        amount_used = max_stage_time - remaining_time
        progress = amount_used * 100 / max_stage_time
        formated_progress = "{:.1f}".format(progress)
        stage_meter.configure(stripethickness=calc_stripethickness(max_stage_time), amountused=formated_progress, subtext=message_str)



def disable_combat_modes(root, combat_mode_menu, combat_modes):
    weekday_options = {#starts at 0
        'Monday': [2, 4, 5, 6, 7],
        'Tuesday': [2, 3, 5, 6, 7],
        'Wednesday': [3, 4, 5, 6],
        'Thursday': [2 ,3, 4, 7],
        'Friday': [3, 5, 6, 7],
        'Saturday': [2, 3, 4],
        'Sunday': []
    }
    #["","Feldzug", "Königsturm", "Himmlisches Heiligtum", "Turm des Lichtes", "Die Brutale Zitadelle", "Höllische Festung", "Die Verlassene Nekropolis", "Der Weltenbaum"]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    d = datetime.now()
    day = days_of_week[d.weekday()]
    current_time= d.time()
    setpoint = time(2, 0, 0)
    # get the current time
    #setpoint = (datetime.datetime.now() + datetime.timedelta(hours=1)).time()
    if  current_time >= setpoint:
            print("Now: "+str(day)+" "+str(current_time)+" is past "+ str(setpoint))
            combat_modes_to_disable =  weekday_options.get(day, [])
    else:
            previous_day = days_of_week[days_of_week.index(day)-1]
            print("Now: "+str(day)+" "+str(current_time)+" is before "+ str(setpoint)+" but we set previous day "+str(previous_day))
            combat_modes_to_disable =  weekday_options.get(previous_day, [])
    for i, combat_mode in enumerate(combat_modes):
        combat_mode_menu['menu'].entryconfig(i, state='normal')
        if i in combat_modes_to_disable:
            combat_mode_menu['menu'].entryconfig(i, state='disabled')
        else:
            combat_mode_menu['menu'].entryconfig(i, foreground='black')       
    root.after(60000, disable_combat_modes, root, combat_mode_menu, combat_modes) 