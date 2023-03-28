
import datetime
import time
import math
import os
import threading
from Database import *

lock = threading.Lock()
database_name = file_path('config.db')

def get_dir_path():
    dir_path=os.path.dirname(os.path.realpath(__file__))
    return dir_path

def get_image_path(image_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_folder = os.path.join(dir_path, "images")
    return os.path.join(image_folder, image_name)

def split_seconds(seconds):
    if seconds is None:
        return '--', '--'
    else:
        hours = int(seconds) // 3600
        minutes = (int(seconds) % 3600) // 60
        seconds = int(seconds) % 60
        return hours, minutes, seconds

def calc_scale_meters(communication_data):
    local_dict=communication_data.copy()
    list = [
        ('formation', local_dict['formation_time'], local_dict['formation_stripe']),
        ('stage', local_dict['stage_time'], local_dict['stage_stripe']),
        ('script', local_dict['script_time'], local_dict['script_stripe'])
    ]
    ref_value = 360 * 20
    for key, max_time, stripe in list:
        if key == 'stage':
            stripe = int(360/len(local_dict['formations']))
        elif max_time > ref_value / 3:
            stripe = 3
        else:
            stripe = int(ref_value / max_time)
        # Update the communication_data dictionary
        local_dict[f'{key}_stripe'] = stripe
        communication_data.update(local_dict)

def master_meter_timer(communication_data, callback, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event,my_lock):
    while not stop_event.is_set():
        local_dict=communication_data.copy()
        # Script meter
        if not restart_event.is_set():
            if script_start_event.is_set():
                local_dict['script_runtime'] = local_dict['script_counter']
                next_restart = local_dict['restart_time'] - (local_dict['script_counter'] % local_dict['restart_time'])
                hrs, mins, secs = split_seconds(local_dict['script_runtime'])
                if next_restart <= 10:
                    local_dict['script_message'] = f"Restart in {next_restart} seconds"
                    if next_restart == 0:
                        restart_event.set()
                else:
                    local_dict['script_message'] = f"Runtime: {hrs:02}:{mins:02}:{secs:02}"
                progress = (1 - (next_restart / local_dict['restart_time'])) * 100

                local_dict['script_progress'] = "{:.1f}".format(progress)
                local_dict['script_counter'] += 1
            else:
                local_dict.update({'script_counter': 0})

            # Stage meter
            if stage_start_event.is_set():
                local_dict['stage_remaining'] = local_dict['stage_time'] - local_dict['stage_counter']
                #hrs, mins, secs = split_seconds(local_dict['stage_remaining'])
                #local_dict['stage_message'] = f"Stage: {local_dict['stage_level']}: {hrs:02}:{mins:02}:{secs:02}"
                local_dict['stage_message'] = f"Stage: {get_latest_stage(database_name).get(get_combat_mode(local_dict['stage_mode']))}: ({local_dict['victories']}/3)"
                if local_dict['stage_remaining'] >= 0:
                    #amount_used = local_dict['stage_time'] - local_dict['stage_remaining']
                    actual_percentage = local_dict['stage_counter'] * 100 / local_dict['stage_time']
                    progress_degrees = (actual_percentage * 360) / 100
                    stripes_needed = progress_degrees / local_dict['stage_stripe']
                    adjusted_stripes = math.floor(stripes_needed)
                    displayed_progress_percentage = (adjusted_stripes * local_dict['stage_stripe'] * 100) / 360
                    if actual_percentage == 100:
                        displayed_progress_percentage = 100
                    #progress = local_dict['stage_counter'] * 100 / local_dict['stage_meter_max']
                    local_dict['stage_progress'] = "{:.1f}".format(displayed_progress_percentage)
                    local_dict['stage_counter'] += 1
                    #print(progress)
                    # if local_dict['stage_remaining'] == 0:
                    #stage_start_event.clear()
            else:
                local_dict.update({'stage_counter': 0})

            # Formation meter
            if formation_start_event.is_set():
                local_dict['formation_remaining'] = local_dict['formation_time'] - local_dict['formation_counter']
                hrs, mins, secs = split_seconds(local_dict['formation_remaining'])
                local_dict['formation_message'] = f"Team {local_dict['formation_active']}: {mins:02}:{secs:02}"
                #print(local_dict['formation_remaining'])
                if local_dict['formation_remaining'] >= 0:
                    #amount_used = local_dict['formation_time'] - local_dict['formation_remaining
                    actual_percentage = local_dict['formation_counter'] * 100 / local_dict['formation_time']
                    progress_degrees = (actual_percentage * 360) / 100
                    stripes_needed = progress_degrees / local_dict['formation_stripe']
                    adjusted_stripes = math.floor(stripes_needed)
                    displayed_progress_percentage = (adjusted_stripes * local_dict['formation_stripe'] * 100) / 360
                    if actual_percentage == 100:
                        displayed_progress_percentage = 100
                    local_dict['formation_progress'] = "{:.1f}".format(displayed_progress_percentage)
                    #print(progress)
                    local_dict['formation_counter'] += 1
                    if local_dict['formation_remaining'] == 0:
                        formation_start_event.clear()
            else:
                local_dict.update({'formation_counter': 0})
            callback(local_dict)
            with lock:
                # Update the original dictionary with the changes made in the thread's copy
                communication_data.update(local_dict)
            time.sleep(1)


# def update_meters(qo,qi,formation_meter,stage_meter,script_meter,root):
#     communication_data = qo.get()
#     communication_data = qi.get()
#     print(communication_data)
#     time.sleep(20)
#     if communication_data['script_start']:
#         script_meter_timer(qo,qi,script_meter,root)
#         communication_data['script_start']=False
#     if communication_data['stage_start']:
#         stage_meter_timer(qo,qi, stage_meter,root)
#         communication_data['stage_start']=False
#     if communication_data['formation_start']:
#         formation_meter_timer(qo,qi, formation_meter,root)
#         communication_data['formation_start']=False
#     qo.put(communication_data)
#     if  communication_data['btn_stop']:
#             update_meters.after_cancel(communication_data['update_id'])
#             return
#     root.after(1000, update_meters,qo,qi,formation_meter,stage_meter,script_meter,root)


    
        



# def update_meter_timers(root, formation_meter, script_meter, stage_meter, formation_time, script_time, teamlist, restart_time):
#     global counter
#     update_formation_meter(formation_meter, formation_time,teamlist,counter)
#     update_script_meter(script_meter, script_time,restart_time,counter)
#     update_stage_meter(stage_meter, teamlist, formation_time,counter)
#     counter += 1
#     root.after(1000, update_meter_timers, root, formation_meter, script_meter, stage_meter, formation_time, script_time, teamlist,restart_time)
    
# def formation_meter_timer(formation_meter, formation_time, teamlist,counter):
#     formation_active=teamlist[0]
#     remaining_time = formation_time - counter
#     hrs, mins, secs = split_seconds(remaining_time)
#     message_str = f"Team {formation_active}: {mins:02}:{secs:02}"
#     if remaining_time >= 0:
#         amount_used = formation_time - remaining_time
#         progress = amount_used * 100 / formation_time
#         formated_progress = "{:.1f}".format(progress)
#         formation_meter.configure(stripethickness=calc_stripethickness(formation_time), amountused=formated_progress, subtext=message_str) 

# def stage_meter_timer(stage_meter, teamlist,formation_time, counter):
#     formation_active=teamlist[0]
#     number_of_teams=len(teamlist)
#     stage_time=formation_time*number_of_teams
#     remaining_time = stage_time - counter
#     hrs, mins, secs = split_seconds(remaining_time)
#     message_str = f"Stage {formation_active}/{number_of_teams}: {mins:02}:{secs:02}"
#     #later ->message_str = f"Stage {stage value form image recognition}: {mins:02}:{secs:02}"
#     if remaining_time >= 0:
#         amount_used = stage_time - remaining_time
#         progress = amount_used * 100 / stage_time
#         formated_progress = "{:.1f}".format(progress)
#         stage_meter.configure(stripethickness=calc_stripethickness(stage_time), amountused=formated_progress, subtext=message_str)
        
# def script_meter_timer(script_meter, script_time, restart_time, counter):
#     remaining_time = script_time - counter
#     until_restart = restart_time - counter
#     hrs, mins, secs = split_seconds(until_restart)
#     message_str = f"Next restart: {hrs:02}:{mins:02}:{secs:02}"
#     if remaining_time >= 0:
#         amount_used = script_time - remaining_time
#         progress = amount_used * 100 / script_time
#         formated_progress = "{:.1f}".format(progress)
#         script_meter.configure(stripethickness=calc_stripethickness(script_time), amountused=formated_progress, subtext=message_str)



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

    d = datetime.datetime.now()
    day = days_of_week[d.weekday()]
    current_time= d.time()
    setpoint = datetime.time(2, 0, 0)
    

    # get the current time
    #setpoint = (datetime.datetime.now() + datetime.timedelta(hours=1)).time()
    if  current_time >= setpoint:
            #print("Now: "+str(day)+" "+str(current_time)+" is past "+ str(setpoint))
            combat_modes_to_disable =  weekday_options.get(day, [])
    else:
            previous_day = days_of_week[days_of_week.index(day)-1]
            #print("Now: "+str(day)+" "+str(current_time)+" is before "+ str(setpoint)+" but we set previous day "+str(previous_day))
            combat_modes_to_disable =  weekday_options.get(previous_day, [])
    for i, combat_mode in enumerate(combat_modes):
        combat_mode_menu['menu'].entryconfig(i, state='normal')
        if i in combat_modes_to_disable:
            combat_mode_menu['menu'].entryconfig(i, state='disabled')
        else:
            combat_mode_menu['menu'].entryconfig(i, foreground='black')       

    root.after(60000, disable_combat_modes, root, combat_mode_menu, combat_modes) 

