import subprocess
import time
import win32gui
import win32process
import os
import sys
sys.path.append("C://Users//matth//AppData//Local//Packages//PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0//LocalCache//local-packages//Python311//site-packages//")
import pyautogui
import pygetwindow as gw




# def detect_startscreen(window_handle):xyhxy
#     # Use the handle to create a Window object
#     window = gw.win32wrapper.Win32Window(window_handle)

#     # Start a while loop that runs every 5 seconds
#     print('Start looking for startscreen_image')
#     while True:
#         # Get the position and size of the Blue Stacks window
#         left, top, width, height = window.topleft + window.size

#         # Use pyautogui.screenshot to take a screenshot of the Blue Stacks window
#         screenshot = pyautogui.screenshot(region=(left, top, width, height))

#         # Use pyautogui.locateOnScreen to find the image on the screen
#         image_pos = pyautogui.locateOnScreen('startscreen_0.png', region=screenshot)

#         # Check if the image was found
#         if image_pos is not None:
#             # The image was found, exit the while loop
#             print('Image found at:', image_pos)
#             break
#         print('Image not found.')
#         # Wait for 5 seconds before running the search again
#         time.sleep(2)
def close_bluestacks():
    time.sleep(2)
    window_handle = win32gui.FindWindow(None, "BlueStacks App Player")
    print(f"here1")
    time.sleep(2)
    process_id = win32process.GetWindowThreadProcessId(window_handle)[1]
    print(f"Process ID for window {window_handle}: {process_id}")
    os.kill(process_id , 9)
    time.sleep(5)

def modus_player(modusValue):
    # Send hotkeys based on the modusValue
    key_sequences = {
        1: ['h', 'x', 'y'],
        2: ['a', 'e', 'e'],
        3: ['a', 'e', 'h'],
        4: ['a', 'e', 'l'],
        5: ['a', 'e', 'b'],
        6: ['a', 'e', 'y'],
        7: ['a', 'e', '4'],
        8: ['a', 'e', '1']
    }
    print('intermediate')
    if modusValue in key_sequences:
        # Set the BlueStacks window to be the active window
        window_handle = set_bluestacks_foreground()
        if window_handle:
            try:
                for key in key_sequences[modusValue]:
                    set_bluestacks_foreground()
                    pyautogui.typewrite(key, interval=2.5)
                print("Finished 1")
                time.sleep(5)
            except Exception as e:
                print(f"Error typing key {key}: {e}")
            print("Finished 2")
            time.sleep(2)
            close_bluestacks()
            return window_handle
        else:
            return None
    else:
        print(f"Unknown modusValue: {modusValue}")
        return None


def start_player():
    str_path_player = r'"C:\Program Files\BlueStacks_nxt\HD-Player.exe"'
    str_attr2 = ' --cmd launchApp'
    str_attr3 = ' --package com.lilithgame.hgame.gp'
    str_arguments = str_path_player + str_attr2 + str_attr3
    subprocess.Popen(str_arguments)
    print('Waiting')
    time.sleep(10)
    print('Now I start typing')
    time.sleep(5)
    modus_player(1)

def set_bluestacks_foreground():
    try:
        # Find the window handle of the BlueStacks App Player window
        window_handle = win32gui.FindWindow(None, "BlueStacks App Player")
        # Get the handle of the current foreground window
        foreground_window = win32gui.GetForegroundWindow()
        # Check if the BlueStacks window is already in the foreground
        if foreground_window == window_handle:
            return window_handle
        else:
            try:
                # Set the BlueStacks window in the foreground
                win32gui.SetForegroundWindow(window_handle)
                return window_handle
            except Exception as e:
                print(f"Error BlueStacks could not be set to foreground: {e}")
                return None
    except Exception as e:
        print(f"Error BlueStacks or foreground window not found: {e}")
        return None

start_player()



