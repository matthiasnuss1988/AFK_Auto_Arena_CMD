import time
import win32gui, win32process, win32con, win32api
import os
import sys
from Vision import *
from Shared_functions import *
sys.path.append("C://Users//matth//AppData//Local//Packages//PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0//LocalCache//local-packages//Python311//site-packages//")
import pyautogui
import ctypes


pyautogui.FAILSAFE = False



os.chdir(os.path.dirname(os.path.abspath(__file__)))

window_title="BlueStacks App Player"
database_name = file_path('config.db')

key_sequences = {
    #1: ['h', 'x', 'y'],['y','h']
    1: ['f', 'x'],
    2: ['a', 'e', 'e', 'h'],
    3: ['a', 'e', 'h', 'h'],
    4: ['a', 'e', 'l', 'h'],
    5: ['a', 'e', 'b', 'h'],
    6: ['a', 'e', 'y', 'h'],
    7: ['a', 'e', '4', 'h'],
    8: ['a', 'e', '1', 'h'],
    'exept':['y','h'],
    'victory':['v','v','q','h','x'],
    'prefight': ['x','y','1','t',None,'k','v','a','v'],
    'afterfight': ['v','v','p','e'],
    'quit': ['q','v','q','v','q']
}


def enum_windows_callback(hwnd, _):
    # Close all cmd windows
    if 'cmd.exe' in win32gui.GetWindowText(hwnd):
        # get the process id of the window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        # open the process with the SE_DEBUG_NAME privilege
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
        # terminate the process
        win32api.TerminateProcess(handle, -1)
        # close the handle
        win32api.CloseHandle(handle)


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

def accurate_sleep(delay):
    end_time = time.perf_counter() + delay
    while time.perf_counter() < end_time:
        pass

# def capture_window(hwnd):
#     # Get the dimensions of the window
#     rect = win32gui.GetWindowRect(hwnd)
#     width = rect[2] - rect[0]
#     height = rect[3] - rect[1]
#     # Get the device context of the window
#     hwnd_dc = win32gui.GetWindowDC(hwnd)
#     mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
#     # Create a compatible DC to hold the bitmap
#     save_dc = mfc_dc.CreateCompatibleDC()
#     # Create a bitmap object and select it into the compatible DC
#     save_bitmap = win32ui.CreateBitmap()
#     save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
#     save_dc.SelectObject(save_bitmap)
#     time.sleep(0.1)
#     # Use BitBlt to copy the window content to the bitmap
#     SRCCOPY = 0xCC0020
#     result = ctypes.windll.gdi32.BitBlt(
#         save_dc.GetSafeHdc(), 0, 0, width, height,
#         hwnd_dc, 0, 0, SRCCOPY
#     )
#     # Check if BitBlt was successful
#     if not result:
#         print("Failed to capture window content!")
#         return None
#     # Create an image object from the bitmap and release the DCs
#     bmp_info = save_bitmap.GetInfo()
#     bmp_str = save_bitmap.GetBitmapBits(True)
#     img = Image.frombuffer(
#         "RGB",
#         (bmp_info["bmWidth"], bmp_info["bmHeight"]),
#         bmp_str,
#         "raw",
#         "BGRX",
#         0,
#         1,
#     )
#     win32gui.DeleteObject(save_bitmap.GetHandle())
#     save_dc.DeleteDC()
#     mfc_dc.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwnd_dc)
#     #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     return np.array(img)


def find_on_screen(filename):
    while True:
        if pyautogui.locateOnScreen(get_image_path(filename),confidence=0.8)!=None:
            print("Condition found")
            break
        time.sleep(0.2)       


def close_bluestacks():
    window_handle = win32gui.FindWindow(None, window_title)
    print(f"Closing BlueStacks")
    time.sleep(2)
    process_id = win32process.GetWindowThreadProcessId(window_handle)[1]
    print(f"Process ID for window {window_handle}: {process_id}")
    # open the process with the PROCESS_TERMINATE flag
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False,  process_id)
    # terminate the process
    win32api.TerminateProcess(handle, -1)
    # close the handle
    win32api.CloseHandle(handle)        


# def send_keys_to_bluestacks(keys, delays):
#     window_handle = win32gui.FindWindow(None, bluestacks)
#     time.sleep(2)
#     win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
#     win32gui.SetWindowPos(window_handle, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
#     ctypes.windll.user32.SetForegroundWindow(window_handle)
#     #win32gui.ShowWindow(window_handle, win32con.SW_SHOWNORMAL)
#     if not isinstance(keys, list) or not isinstance(delays, list) or len(keys) != len(delays):
#         raise ValueError("Both 'keys' and 'delays' should be lists of the same length.")

#     for key, delay in zip(keys, delays):
#         #win32gui.SetForegroundWindow(window_handle)
#         win32api.PostMessage(window_handle, win32con.WM_KEYDOWN, ord(key), 0)
#         time.sleep(0.05)  # Add a short pause between key down and key up events
#         win32api.PostMessage(window_handle, win32con.WM_KEYUP, ord(key), 0)
#         time.sleep(delay)
#         print(key)

def set_bluestacks_foreground(window_handle):
    # Search for the Bluestacks icon in the taskbar and click it
    foreground_window = win32gui.GetForegroundWindow()
    if foreground_window!=window_handle:
        #print("Bring Bluestacks to foreground")
        # bluestacks_icon = pyautogui.locateCenterOnScreen(get_image_path("ProductLogo.png"),confidence=0.6)
        # if bluestacks_icon:
        #     pyautogui.click(bluestacks_icon)
        #     return True
        # else:
        #     print("Bluestacks icon not found on taskbar")
        #     return False
        win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
        win32gui.SetWindowPos(window_handle, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        ctypes.windll.user32.SetForegroundWindow(window_handle)
    #print("Bluestacks allready in foreground")



def send_keys_to_bluestacks(window_handle, sequence, delay=None):
    if not isinstance(sequence, list) and sequence in key_sequences:  # Sequence in dictionary
        keys = key_sequences[sequence]
    elif isinstance(sequence, list):  # List of keys
        keys = sequence
    elif isinstance(sequence, (str,int,float)):  # Single key
        keys = [sequence]
    else:
        raise ValueError("Invalid sequence input. Must be a single key, list of keys, or a key in the key_sequences dictionary.")
    
    if delay is None:
        delay = 0.15

    if not isinstance(delay, (int, float, list, tuple)) or (isinstance(delay, (list, tuple)) and len(keys) != len(delay)):
        raise ValueError("Invalid delay input. Must be a number or a list of numbers of the same length as 'keys'.")

    if isinstance(delay, (int, float)):  # Fixed delay between each key
        for key in keys:
            set_bluestacks_foreground(window_handle)
            print(f'key {key}')
            pyautogui.press(key)
            accurate_sleep(delay)
    elif isinstance(delay, (list, tuple)):  # List of delays
        for key, individual_delay in zip(keys, delay):
            set_bluestacks_foreground(window_handle)
           # print(f'key {key}')
            pyautogui.press(key)
            accurate_sleep(individual_delay)
    else:
        raise ValueError("Invalid delay type. Must be a number or a list of numbers.")


def start_player(stage_mode):
    # if not is_admin():
    #    sys.exit()  
    #Search for HD-Player.exe file

    for root, dirs, files in os.walk("C:/"):
        if "HD-Player.exe" in files:
            path_player = os.path.join(root, "HD-Player.exe")
            break
    else:
        print("Error: HD-Player.exe not found")
        return
    
    cmd_args = ['--cmd', 'launchApp']
    package = '--package com.lilithgame.hgame.gp'
    arguments = [path_player] + cmd_args + [package]
    
    try:
        # Start the player as administrator
        commands = f'"{arguments[0]}" {" ".join(arguments[1:])}'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/k {commands}", None, win32con.SW_SHOWMINIMIZED)
        
        # Wait for the player's main window to appear
        while True:
            window_handle = win32gui.FindWindow(None, window_title)
            if window_handle != 0:
                print("Player started")
                break
            time.sleep(0.5)
            
        # Close all cmd windows
        win32gui.EnumWindows(enum_windows_callback, None)


        
        send_keys_to_bluestacks(window_handle,['q','f'],[0.5,0.5])

        # Detecet startscreen
        #start_time = time.time()
        image_recog('startscreen')
        #find_start_button_on_screen() 
        #end_time = time.time()
        #elapsed_time = end_time - start_time
        #print(f"Elapsed time: {elapsed_time:.2f} seconds")
        create_database_and_table(database_name)
        initialize_stages(database_name)
        #window_handle = win32gui.FindWindow(None, window_title)
        accurate_sleep(2)
        send_keys_to_bluestacks(window_handle, stage_mode,2) 
        return window_handle 
    except OSError as e:
        print(f"Error starting the player: {e}")
    return None

def process_prefight(window_handle,team, key_sequences):
    key_sequences['prefight'][4] = str(team)
    send_keys_to_bluestacks(window_handle,'prefight', 2.5)
    return time.time()

def process_afterfight(window_handle):
    send_keys_to_bluestacks(window_handle,'afterfight', [2, 0.15, 2, 2])
    return time.time()

def process_victory(window_handle):
    send_keys_to_bluestacks(window_handle,'victory', 2)
    return time.time()

def makro(communication_data, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event, my_lock):
    print('\tStart scripting\n')
    window_handle = start_player(communication_data['stage_mode'])
    script_start_event.set()
    
    # Initialize missed_iterations variable
    missed_iterations = 0

    while not stop_event.is_set():
        temp_dict = communication_data.copy()  # Copy communication_data to temp_dict in the outer while loop
        temp_dict['victories'] = 0
        total_time = 0
        num_iterations = 0
        num_teams = len(communication_data['formations'])

        if temp_dict['level_inc'] == 0:  # Perform image recognition only for the first iteration
            temp_dict['stage_level'] = image_recog(temp_dict['stage_mode'],liveview='Yes')
            first_stage=temp_dict['stage_level']
            print(f"No victory yet {first_stage}")
            if not first_stage:
                missed_iterations += 1
            #append_stages_to_database(temp_dict['stage_mode'], temp_dict['stage_level'], database_name)

        if temp_dict['level_inc'] !=0:
            if not first_stage:
                temp_dict['stage_level'] = image_recog(temp_dict['stage_mode'])
                first_stage=temp_dict['stage_level']
                print(f"After victory {first_stage}")
                if not first_stage:
                    missed_iterations += 1
            temp_dict['stage_level'] = str(int(first_stage) + int(temp_dict['level_inc']) - missed_iterations)  # Add increment to stage_level
            #append_stages_to_database(temp_dict['stage_mode'], temp_dict['stage_level'], database_name)

        print(temp_dict['stage_mode'], temp_dict['stage_level'], database_name)

        with my_lock:
            communication_data.update(temp_dict)  # Update the whole communication_data dictionary with temp_dict

        for team in communication_data['formations']:
            communication_data['formation_active'] = team
            iteration_start_time = process_prefight(window_handle, team, key_sequences)
            if num_iterations == 0:
                print(f"\tStart stage {communication_data['stage_level']}\n")
                stage_start_event.set()
            formation_start_event.set()
            while formation_start_event.is_set() and not stop_event.is_set() and not restart_event.is_set():
                victory_found = find_image("victory.png", threshold=0.84)
                if victory_found:
                    print("Victory detected")
                    temp_dict['victories'] +=1
                    with my_lock:
                        communication_data['victories'] +=1
                    if temp_dict['victories'] == 3:
                        append_stages_to_database(temp_dict['stage_mode'], temp_dict['stage_level'], database_name)
                        with my_lock:
                                communication_data['level_inc'] +=1
                        formation_start_event.clear()
                        break
                    time.sleep(3)  # Wait for the cooldown period
                time.sleep(0.15)
            print(f"\tTeam has finished\n")
            if temp_dict['victories']== 3:
                iteration_end_time = process_victory(window_handle)
            else:
                iteration_end_time = process_afterfight(window_handle)
            iteration_time = iteration_end_time - iteration_start_time
            total_time += iteration_time
            num_iterations += 1
            average_time = total_time / num_iterations
            temp_dict['stage_time'] = total_time + average_time * (num_teams - num_iterations)
            print(f"\tStage needs in average {temp_dict['stage_time']} seconds\n")
            if temp_dict['victories'] == 3:
                temp_dict['victories'] = 0
                break
            elif stop_event.is_set():
                break
            elif restart_event.is_set():
                break
        stage_start_event.clear()

        if restart_event.is_set() and not stop_event.is_set():
            close_bluestacks()
            script_start_event.clear()
            time.sleep(5)
            print('5')
            window_handle = start_player(communication_data['stage_mode'])
            script_start_event.set()
            restart_event.clear()

    if stop_event.is_set():
        send_keys_to_bluestacks(window_handle ,'quit', [1, 1, 1, 1, 1])
        script_start_event.clear()
        stage_start_event.clear()
        formation_start_event.clear()
        restart_event.clear()
