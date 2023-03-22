import time
import win32gui, win32process, win32con, win32api,win32ui
import os
from tkinter import *
import sys
import pytesseract
from shared_functions import *
sys.path.append("C://Users//matth//AppData//Local//Packages//PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0//LocalCache//local-packages//Python311//site-packages//")
sys.path.append("C://Program Files//Tesseract-OCR")
# for root, dirs, files in os.walk("C:/"):
#     if "tesseract.exe" in files:
#         path_tesseract = os.path.join(root, "tesseract.exe")
#         break
# else:
#     print("Error: HD-Player.exe not found")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#pytesseract.pytesseract.tesseract_cmd = r'{path_tesseract}'
import pyautogui
import ctypes
pyautogui.FAILSAFE = False
import numpy as np
import json
import cv2
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))

window_title="BlueStacks App Player"
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

def capture_window(hwnd):
    # Get the dimensions of the window
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    # Get the device context of the window
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # Create a compatible DC to hold the bitmap
    save_dc = mfc_dc.CreateCompatibleDC()
    # Create a bitmap object and select it into the compatible DC
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)
    time.sleep(0.1)
    # Use BitBlt to copy the window content to the bitmap
    SRCCOPY = 0xCC0020
    result = ctypes.windll.gdi32.BitBlt(
        save_dc.GetSafeHdc(), 0, 0, width, height,
        hwnd_dc, 0, 0, SRCCOPY
    )
    # Check if BitBlt was successful
    if not result:
        print("Failed to capture window content!")
        return None
    # Create an image object from the bitmap and release the DCs
    bmp_info = save_bitmap.GetInfo()
    bmp_str = save_bitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        "RGB",
        (bmp_info["bmWidth"], bmp_info["bmHeight"]),
        bmp_str,
        "raw",
        "BGRX",
        0,
        1,
    )
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return np.array(img)


def crop_screenshot(cords=None, liveview=None):
    bluestacks = "BlueStacks App Player"
    window_handle = win32gui.FindWindow(None, bluestacks)
    img_np = cv2.cvtColor(capture_window(window_handle), cv2.COLOR_BGR2RGB)
    img_np_resized = cv2.resize(img_np, (1920, 1080))
    # Check if cords are provided and valid

    if cords is not None:
        x, y, w, h = cords
        height, width, _ = img_np_resized.shape
        if 0 <= x < width and 0 <= y < height and x + w <= width and y + h <= height:
            img_crop = img_np[y:y + h, x:x + w]
        else:
            img_crop = img_np_resized
            print("Invalid crop rectangle, return img instead")
    else:
        img_crop = img_np_resized

    if liveview is not None:
        cv2.imshow("Screenshot", img_crop)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
    return img_crop


def image_process_for_ocr(img, process_for=None):
    if process_for is not None:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if process_for == 'conservative':
            # Noise removal with a mild Gaussian blur
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            # Binarization using adaptive thresholding
            applied = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        elif process_for == 'text':
            # Equalize the histogram to increase contrast
            equalized = cv2.equalizeHist(gray)
            # Apply adaptive thresholding to convert to binary image
            applied = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        elif process_for == 'digits':
            # Apply Gaussian blur to remove noise
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            # Equalize the histogram to increase contrast
            equalized = cv2.equalizeHist(blurred)
            # Apply adaptive thresholding to convert to binary image
            thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            # Apply morphological transformations to remove noise and fill gaps
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            applied = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
    # Inversion to get black text/numbers on a white background
        img_process = np.array(cv2.bitwise_not(applied))
    else:
        img_process=np.array(img)
    return img_process     


def image_recog(rec_case, cords=None, rec_pattern=None, process_for=None, search=None, lang='deu'):
    if rec_case != 'custom' and (cords or rec_pattern or process_for or search):
        print("Warning: You provided additional inputs for a predefined rec_case. These inputs will be ignored. Use 'custom' rec_case if you want to provide custom inputs.")
        pass
  
    rec_pattern_configs = {
        'digits': f"--psm 11 -l {lang} -c tessedit_char_whitelist=0123456789-",
        'word': f"--psm 9 -l {lang}",
        'text': f"--psm 11 -l {lang}"
    }

    case_data = {
        'startscreen': {'cords': [230, 805, 80, 50], 'search': ['st', 'ta', 'ar', 'rt', 'sta', 'tar', 'art'], 'rec_pattern': 'text', 'process_for': 'text'},
        'towers': {'cords': [265, 98, 40, 30], 'rec_pattern': 'digits', 'process_for': process_for},
        'campaign': {'cords': [285, 200, 80, 40], 'rec_pattern': 'digits', 'process_for': process_for},
        'victory': {'rec_pattern': 'digits', 'process_for': process_for}
    }

    if isinstance(rec_case, int):
        if rec_case == 1:
            rec_case = 'campaign'
        elif 2 <= rec_case <= 8:
            rec_case = 'towers'

    if rec_case != 'custom':
        cords = case_data[rec_case].get('cords', cords)
        rec_pattern = case_data[rec_case].get('rec_pattern', rec_pattern)
        process_for = case_data[rec_case].get('process_for', process_for)
        search = case_data[rec_case].get('search', search)

    config = rec_pattern_configs[rec_pattern]

    if rec_case!='startscreen':
        if rec_case == 'custom':
            image_cropped = crop_screenshot(cords, liveview='yes')
        else:
            image_cropped = crop_screenshot(cords,liveview='yes')
        image_processed = image_process_for_ocr(image_cropped, process_for)
        detected = pytesseract.image_to_string(Image.fromarray(image_processed), config=config)
        print(f"{detected} detected")
        if rec_case != 'custom':
            # Numeric filter
            numeric_filter = filter(lambda x: x.isdigit() or x == "-", detected)
            return "".join(numeric_filter)
        else:
            return detected
    elif rec_case == 'startscreen':
            counter = 0
            while True and counter < 40:
                counter += 1
                image_cropped = crop_screenshot(cords)
                image_processed = image_process_for_ocr(image_cropped, process_for)
                detected = pytesseract.image_to_string(Image.fromarray(image_processed), config=config)
                for item in search:
                    if item in detected:
                        print(f"{detected} detected")
                        print(f"Start screen found detected")
                        return detected
                time.sleep(0.1)
    else:
        print("Use case is not dfeined")
        return None


def find_start_button_on_screen():
    while True:
        if pyautogui.locateOnScreen(get_image_path("start_button.png"),confidence=0.8)!=None:
            print("Found start button")
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
            #print(f'key {key}')
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
    if not is_admin():
       sys.exit()  
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
        start_time = time.time()
        image_recog('startscreen')
        #find_start_button_on_screen() 
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        #window_handle = win32gui.FindWindow(None, window_title)
        accurate_sleep(1)
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

def makro(communication_data, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event, my_lock):
    print('\tStart scripting\n')
    window_handle = start_player(communication_data['stage_mode'])
    script_start_event.set()

    while not stop_event.is_set():
        total_time = 0
        num_iterations = 0
        num_teams = len(communication_data['formations'])
        communication_data['stage_level']=image_recog(communication_data['stage_mode'])
        temp_dict=communication_data
        print(f"Image recognition: stage mode {temp_dict['stage_mode']} delivers {temp_dict['stage_level']}")
        send_keys_to_bluestacks(window_handle ,'exept', 2.5)

        for team in communication_data['formations']:
            communication_data['formation_active']=team
            #time.sleep(1)
            iteration_start_time = process_prefight(window_handle, team, key_sequences)

            if num_iterations == 0:
                print(f"\tStart stage {temp_dict['stage_level']}\n")
                stage_start_event.set()
            formation_start_event.set()

            while formation_start_event.is_set() and not stop_event.is_set() and not restart_event.is_set():
                time.sleep(0.2)

            print(f"\tTeam has finished\n")
            iteration_end_time = process_afterfight(window_handle)

            # Calculate stage time needed
            iteration_time = iteration_end_time - iteration_start_time
            total_time += iteration_time
            num_iterations += 1
            average_time = total_time / num_iterations
            with my_lock:
                communication_data['stage_time'] = total_time + average_time * (num_teams - num_iterations)
            print(f"\tStage needs in average {communication_data['stage_time']} seconds\n")

            if stop_event.is_set():
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
