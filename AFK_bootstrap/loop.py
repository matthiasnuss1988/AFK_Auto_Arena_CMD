import time
import win32gui, win32process, win32con, win32api,win32ui
import os
from tkinter import *
import sys
import pytesseract
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

import numpy as np
import json
import cv2
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))

window_title="BlueStacks App Player"

def get_image_path(image_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_folder = os.path.join(dir_path, "images")
    return os.path.join(image_folder, image_name)

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

def close_bluestacks():
    time.sleep(2)
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
    #os.kill(process_id , 9)

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

# def send_key_sequence(sequence, delay):
#     if sequence in key_sequences:
#         if not isinstance(keys, list) or not isinstance(delays, list) or len(keys) != len(delays):
#         raise ValueError("Both 'keys' and 'delays' should be lists of the same length.")
#             keys = key_sequences[sequence]
#             if isinstance(delay, (int, float)):  # Fixed delay between each key
#                 for key in keys:
#                     set_bluestacks_foreground()
#                     print(f'key {key}')
#                     pyautogui.typewrite(key, interval=delay)
#             elif isinstance(delay, (list, tuple)):  # List of delays
#                 for key, individual_delay in zip(keys, delay):
#                     set_bluestacks_foreground()
#                     print(f'key {key}')
#                     pyautogui.typewrite(key, interval=individual_delay)
#             else:
#                 raise ValueError("Invalid delay type. Must be a number or a list of numbers.")
#             print("seqence typed")
#         except Exception as e:
#             print(f"Error typing key {key}: {e}")
#     else:
#         print(f"Unknown modusValue: {key_sequences}")
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

def send_keys_to_bluestacks(sequence,delay=None):
    if not isinstance(sequence, list) and sequence in key_sequences:  # Sequence in dictionary
        keys = key_sequences[sequence]
    elif isinstance(sequence, list):  # List of keys
        keys = sequence
    elif isinstance(sequence, (str,int,float)):  # Single key
        keys = [sequence]
    else:
        raise ValueError("Invalid sequence input. Must be a single key, list of keys, or a key in the key_sequences dictionary.")
    
    if delay is None:
        delay = 0.1
    if not isinstance(delay, (int, float, list, tuple)) or (isinstance(delay, (list, tuple)) and len(keys) != len(delay)):
        raise ValueError("Invalid delay input. Must be a number or a list of numbers of the same length as 'keys'.")
    window_handle = win32gui.FindWindow(None, window_title)
    if isinstance(delay, (int, float)):  # Fixed delay between each key
        for key in keys:
            set_bluestacks_foreground(window_handle)
            #print(f'key {key}')
            pyautogui.press(key)
            time.sleep(delay)
    elif isinstance(delay, (list, tuple)):  # List of delays
        for key, individual_delay in zip(keys, delay):
            set_bluestacks_foreground(window_handle)
           # print(f'key {key}')
            pyautogui.press(key)
            time.sleep(individual_delay)
    else:
        raise ValueError("Invalid delay type. Must be a number or a list of numbers.")

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

def preprocess_image_for_ocr(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to remove noise
    #blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # Equalize the histogram to increase contrast
    equalized = cv2.equalizeHist(gray)
    # Apply adaptive thresholding to convert to binary image
    thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # Apply morphological transformations to remove noise and fill gaps
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    #opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
    # Invert the image to get black text on white background
    inverted = cv2.bitwise_not(thresh)
    # Convert to PIL image for pytesseract
    return inverted


def find_start_button_on_screen():
    while True:
        if pyautogui.locateOnScreen(get_image_path("start_button.png"),confidence=0.8)!=None:
            print("I can see it")
            #time.sleep(0.5)
            break
        #else:
            #print("I am unable to see it)")
           # time.sleep(0.5)

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

# def get_monitor_from_point(point):
#     monitor = win32api.MonitorFromPoint(point, win32con.MONITOR_DEFAULTTONEAREST)
#     monitor_info = win32api.GetMonitorInfo(monitor)
#     #print(monitor_info)
#     return monitor_info

# def image_recog(text):
#     counter=0
#     while True and counter<40:
#         counter+=1
#         with mss.mss() as sct:
#             window_handle = win32gui.FindWindow(None, window_title)
#             window_rect = win32gui.GetWindowRect(window_handle)
#             left, top, right, bottom = window_rect
#             monitor_info = get_monitor_from_point((left,top))
#             #print(window_rect)
#             monitor_number = int(monitor_info['Device'].split('DISPLAY')[-1])
#         stc=[810,195,-220,-100]
#         new_top=top+stc[0]
#         new_left=left+stc[1]
#         new_right=right+stc[2]
#         new_bottom=bottom+stc[3]
#         window_rect = {"top": new_top, "left": new_left, "width": new_right - new_left, "height": new_bottom - new_top, "monitor_number": monitor_number}
#         combos= ['st', 'ta', 'ar', 'rt','sta', 'tar', 'art']
#         myconfig=f" --psm 9 -l deu"
#         sct_img = sct.grab(window_rect)
#         img_np = np.array(sct_img)
#         image_pre=preprocess_image_for_ocr(img_np)
#         image_pre2 = np.array(image_pre)
#         cv2.imshow(f"Screenshot on monitor {monitor_number}", image_pre2)
#         cv2.waitKey(2000)
#         cv2.destroyAllWindows() 
#         pil_img = Image.fromarray(image_pre)
#         text = pytesseract.image_to_string(pil_img,config=myconfig)
#         #print(text)
#         for combo in combos:
#             if combo in text:
#                 print("Start button found")
#                 return
#         time.sleep(3)

# Fraction tower level coordinates
ft_cords=[265, 98, 40, 30]
#lxr#
start_cords=[230, 805, 80, 50]
campaign_cords=[285, 200, 80, 40]
start_search= ['st', 'ta', 'ar', 'rt', 'sta', 'tar', 'art']


def crop_screenshot(dim,p):
    bluestacks="BlueStacks App Player"
    window_handle = win32gui.FindWindow(None, bluestacks)
    img_np = cv2.cvtColor(capture_window(window_handle), cv2.COLOR_BGR2RGB)
    # Define a crop rectangle
    height, width, channels = img_np.shape
    # check that the crop rectangle is within the image dimensions
    if dim[0] < 0 or dim[1] < 0 or dim[0]+dim[2] > width or dim[1]+dim[3] > height:
        print("Invalid crop rectangle!")
    else:
        cropped_image = img_np[dim[1]:dim[1]+dim[3], dim[0]:dim[0]+dim[2]]
        #cv2.imshow("Screenshot", cropped_image)
        #cv2.waitKey(5000)
        #cv2.destroyAllWindows() 
    if p=='proc':
        image_pre = preprocess_image_for_ocr(cropped_image)
        #cv2.imshow("Processed window",   image_pre)
        #cv2.waitKey(5000)
    elif p=='org':
        image_pre=np.array(cropped_image )
        #cv2.imshow("Original window",   image_pre)
        #cv2.waitKey(10000)
    cv2.destroyAllWindows()
    return image_pre

def image_recog(dim,p,combos=None):
    counter = 0
    while True and counter < 40:
        counter += 1
        image_pre=crop_screenshot(dim,p)
        if combos=='digits':
            text = pytesseract.image_to_string(Image.fromarray(image_pre), config="--psm 11 -l deu")
            numeric_filter = filter(lambda x: x.isdigit() or x == "-", text)
            text = "".join(numeric_filter)
            return text
        elif combos!=None:
            text = pytesseract.image_to_string(Image.fromarray(image_pre), config="--psm 9 -l deu")
            for combo in combos:
                if combo in text:
                    print(f"{combo} found")
                    return text
        time.sleep(0.1)


def start_player(modus):
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
    #system("title " + MyCmdWindow)
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
        time.sleep(1)
        # Close all cmd windows
        def enum_windows_callback(hwnd, _):
            if 'cmd.exe' in win32gui.GetWindowText(hwnd):
                # get the process id of the window
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                # open the process with the SE_DEBUG_NAME privilege
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
                # terminate the process
                win32api.TerminateProcess(handle, -1)
                # close the handle
                win32api.CloseHandle(handle)
        win32gui.EnumWindows(enum_windows_callback, None)
        time.sleep(1)
        # Serach Start Button
        #start_time = time.time()
        send_keys_to_bluestacks(['q','f'],[0.5,0.5])
        image_recog(start_cords,'proc',start_search)
        #find_start_button_on_screen() 
        #end_time = time.time()
        #elapsed_time = end_time - start_time
        #print(f"Elapsed time: {elapsed_time:.2f} seconds")
        #find_start_button_on_screen() 
        time.sleep(1)
        send_keys_to_bluestacks(modus,2) 
    except OSError as e:
        print(f"Error starting the player: {e}")

def process_prefight(team, key_sequences):
    key_sequences['prefight'][4] = str(team)
    send_keys_to_bluestacks('prefight', 2.5)
    return time.time()

def process_afterfight():
    send_keys_to_bluestacks('afterfight', [2, 0.15, 2, 2])
    return time.time()

def makro(communication_data, script_start_event, stage_start_event, formation_start_event, restart_event, stop_event, my_lock):
    print('\tStart scripting\n')
    start_player(communication_data['stage_mode'])
    script_start_event.set()

    while not stop_event.is_set():
        total_time = 0
        num_iterations = 0
        num_teams = len(communication_data['formations'])
        print('1')
        if communication_data['stage_mode']==1:
            communication_data['stage_level']=image_recog(campaign_cords,'org','digits')
            send_keys_to_bluestacks('exept', 2.5)
        else:
            communication_data['stage_level']=image_recog(ft_cords,'org','digits')
        for team in communication_data['formations']:
            communication_data['formation_active']=team
            #time.sleep(1)
            iteration_start_time = process_prefight(team, key_sequences)
            if num_iterations == 0:
                print('2')
                stage_start_event.set()
            formation_start_event.set()
            while formation_start_event.is_set() and not stop_event.is_set() and not restart_event.is_set():
                time.sleep(0.2)
            iteration_end_time = process_afterfight()
            # Update the total time and number of iterations
            iteration_time = iteration_end_time - iteration_start_time
            total_time += iteration_time
            num_iterations += 1
            # Calculate the converging average
            average_time = total_time / num_iterations
            print('3')
            print(communication_data['stage_time'])
            with my_lock:
                communication_data['stage_time'] = total_time + average_time * (num_teams - num_iterations)
            print(communication_data['stage_time'])
            if stop_event.is_set():
                break
            elif restart_event.is_set():
                break
        stage_start_event.clear()
        if restart_event.is_set() and not stop_event.is_set():
            close_bluestacks()
            time.sleep(5)
            print('5')
            start_player(communication_data['stage_mode'])
            restart_event.clear()
    if stop_event.is_set():
        send_keys_to_bluestacks('quit', [1, 1, 1, 1, 1])
        script_start_event.clear()
        stage_start_event.clear()
        formation_start_event.clear()
        restart_event.clear()
