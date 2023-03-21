
import datetime
import time
import math


def split_seconds(seconds):
    if seconds is None:
        return '--', '--', '--'
    else:
        hours = int(seconds) // 3600
        minutes = (int(seconds) % 3600) // 60
        seconds = int(seconds) % 60
        return hours, minutes, seconds

def calc_scale_meters(communication_data):
    list = [
        ('formation', communication_data['formation_time'], communication_data['formation_stripe']),
        ('stage', communication_data['stage_time'], communication_data['stage_stripe']),
        ('script', communication_data['script_time'], communication_data['script_stripe'])
    ]
    ref_value = 360 * 20
    for key, max_time, stripe in list:
        if key == 'stage':
            stripe = int(360/len(communication_data['formations']))
        elif max_time > ref_value / 3:
            stripe = 3
        else:
            stripe = int(ref_value / max_time)
        # Update the communication_data dictionary
        communication_data[f'{key}_stripe'] = stripe

    
      
   
    
 


def master_meter_timer(communication_data, callback, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event,my_lock):
    while not stop_event.is_set():
        # Script meter
        if not restart_event.is_set():
            if script_start_event.is_set():
                communication_data['script_runtime'] = communication_data['script_counter']
                next_restart = communication_data['restart_time'] - (communication_data['script_counter'] % communication_data['restart_time'])
                hrs, mins, secs = split_seconds(communication_data['script_runtime'])
                if next_restart <= 10:
                    communication_data['script_message'] = f"Restart in {next_restart} seconds"
                    if next_restart <= 1:
                        restart_event.set()
                else:
                    communication_data['script_message'] = f"Runtime: {hrs:02}:{mins:02}:{secs:02}"
                progress = (1 - (next_restart / communication_data['restart_time'])) * 100

                communication_data['script_progress'] = "{:.1f}".format(progress)
                communication_data['script_counter'] += 1
            else:
                communication_data.update({'script_counter': 0})

            # Stage meter
            if stage_start_event.is_set():
                communication_data['stage_remaining'] = communication_data['stage_time'] - communication_data['stage_counter']
                hrs, mins, secs = split_seconds(communication_data['stage_remaining'])
                communication_data['stage_message'] = f"Lvl. {communication_data['stage_level']}: {hrs:02}:{mins:02}:{secs:02}"
                if communication_data['stage_remaining'] >= 0:
                    #amount_used = communication_data['stage_time'] - communication_data['stage_remaining']
                    actual_percentage = communication_data['stage_counter'] * 100 / communication_data['stage_time']
                    progress_degrees = (actual_percentage * 360) / 100
                    stripes_needed = progress_degrees / communication_data['stage_stripe']
                    adjusted_stripes = math.floor(stripes_needed)
                    displayed_progress_percentage = (adjusted_stripes * communication_data['stage_stripe'] * 100) / 360
                    if actual_percentage == 100:
                        displayed_progress_percentage = 100
                    #progress = communication_data['stage_counter'] * 100 / communication_data['stage_meter_max']
                    communication_data['stage_progress'] = "{:.1f}".format(displayed_progress_percentage)
                    communication_data['stage_counter'] += 1
                    #print(progress)
                    # if communication_data['stage_remaining'] == 0:
                    #stage_start_event.clear()
            else:
                communication_data.update({'stage_counter': 0})

            # Formation meter
            if formation_start_event.is_set():
            
                communication_data['formation_remaining'] = communication_data['formation_time'] - communication_data['formation_counter']
                hrs, mins, secs = split_seconds(communication_data['formation_remaining'])
                communication_data['formation_message'] = f"Team {communication_data['formation_active']}: {mins:02}:{secs:02}"
                #print(communication_data['formation_remaining'])
                if communication_data['formation_remaining'] >= 0:
                    #amount_used = communication_data['formation_time'] - communication_data['formation_remaining
                    actual_percentage = communication_data['formation_counter'] * 100 / communication_data['formation_time']
                    progress_degrees = (actual_percentage * 360) / 100
                    stripes_needed = progress_degrees / communication_data['formation_stripe']
                    adjusted_stripes = math.floor(stripes_needed)
                    displayed_progress_percentage = (adjusted_stripes * communication_data['formation_stripe'] * 100) / 360
                    if actual_percentage == 100:
                        displayed_progress_percentage = 100
                    communication_data['formation_progress'] = "{:.1f}".format(displayed_progress_percentage)
                    #print(progress)
                    communication_data['formation_counter'] += 1
                    if communication_data['formation_remaining'] == 0:
                        formation_start_event.clear()
            else:
                communication_data.update({'formation_counter': 0})
            callback(communication_data)
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

