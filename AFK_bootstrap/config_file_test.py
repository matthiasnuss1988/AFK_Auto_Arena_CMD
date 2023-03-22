import os
import sqlite3



def file_path(name):
    dir_path=os.path.dirname(os.path.realpath(__file__))
    path_to_name = os.path.join(dir_path, name)
    return path_to_name

def create_database_and_table(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS levels
                 (id INTEGER PRIMARY KEY, stage_mode TEXT, level TEXT)''')
    conn.commit()
    conn.close()

def is_database_empty(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM levels")
    count = c.fetchone()[0]
    conn.close()
    return count == 0

def initialize_levels(database_name):
    if is_database_empty(database_name):
        initial_data = {
            "Campaign": ["51-42", "51-43"],
            "King's Tower": ["1439"],
            "Celestial Sanctum": ["667"],
            "Tower of Light": ["991"],
            "The Brutal Citadel": ["982"],
            "Infernal Fortress": ["680"],
            "The Forsaken Necropolis": ["991"],
            "The World Tree": ["983"]
        }
        for stage_mode, levels in initial_data.items():
            for level in levels:
                append_level_to_database(stage_mode, level, database_name)

def is_valid_level_update(old_level, new_level):
    # Check if both the old level and new level are in the "chapter-level" format
    if '-' in old_level and '-' in new_level:
        old_chapter, old_lvl = old_level.split('-')
        new_chapter, new_lvl = new_level.split('-')
        if int(new_lvl) <= 60 and int(new_chapter) == int(old_chapter):
            return int(new_lvl) > int(old_lvl) and int(new_lvl) < 2000
        else:
            return False
    # Check if both the old level and new level are numeric
    elif old_level.isdigit() and new_level.isdigit():
        return int(new_level) > int(old_level) and int(new_level) < 2000
    else:
        return False
    
def append_level_to_database(stage_mode, new_level, database_name):
    latest_levels = get_latest_levels(database_name)
    old_level = latest_levels.get(stage_mode)

    if old_level is None or is_valid_level_update(old_level, new_level):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute("INSERT INTO levels (stage_mode, level) VALUES (?, ?)", (stage_mode, new_level))
        conn.commit()
        conn.close()
    else:
        print(f"Invalid level update for {stage_mode}: {old_level} -> {new_level}")

def get_latest_levels(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT stage_mode, MAX(id), level FROM levels GROUP BY stage_mode")
    latest_levels = {row[0]: row[2] for row in c.fetchall()}
    conn.close()
    return latest_levels

database_name= file_path('config.db')
create_database_and_table(database_name)
# Call the function after creating the database and table
initialize_levels(database_name)
append_level_to_database("Campaign", "51-42", database_name)


def return_valid_level(rec_level, latest_level):
    if rec_level.isdigit():
        rec_level_int = int(rec_level)
        latest_level_int = int(latest_level)
        if rec_level_int == latest_level_int or rec_level_int == latest_level_int + 1:
            return rec_level_int
        else:
            # Error guessing
            last_digit_of_latest_level = str(latest_level_int)[-1]

            if last_digit_of_latest_level +1 in rec_level:
                return latest_level_int + 1
            else:
                return latest_level_int
    else:
        return latest_level
    

def return_valid_chapter(rec_chapter,rec_level, latest_chapter, latest_level):
    if not latest_chapter or rec_level == 1:
        if rec_chapter == latest_chapter + 1:
            latest_chapter = rec_chapter
        elif latest_level == 40 or latest_level == 60:
            rec_chapter = latest_chapter + 1
        else:
            rec_chapter = latest_chapter
    return rec_chapter


def return_valid_stage(rec_level, latest_level, stage_mode):
        if stage_mode==1 and'-' in rec_level:
            rec_chapter, rec_lvl = map(int, recognized_level.split('-'))
        elif recognized_level.isdigit():
            rec_lvl = int(recognized_level)

        if stage_mode=1 and '-' in latest_level:
            latest_chapter, latest_lvl = map(int, latest_level.split('-'))
        elif latest_level.isdigit():
            latest_lvl = int(latest_level)
        valid_stage = return_valid_stage(rec_level, latest_level)
        if stage mode ==1
            rec_chapter = return_valid_chapter(rec_chapter,rec_level, latest_chapter, latest_level)
            valid_stage=string join (rec_chapter,'-' rec_level)
        

    return valid_stage

import json
import os

def read_bluestacks_config():
    bluestacks_config_path = "C:\\ProgramData\\BlueStacks\\Config\\Engine\\EngineUserSettings.json"

    if not os.path.exists(bluestacks_config_path):
        print("BlueStacks configuration file not found.")
        return None

    with open(bluestacks_config_path, "r") as config_file:
        config_data = json.load(config_file)

    width = config_data.get("width")
    height = config_data.get("height")
    dpi = config_data.get("dpi")

    return width, height, dpi


def capture_window_normalized(hwnd):
    # Read BlueStacks configuration values
    width, height, dpi = read_bluestacks_config()
    
    if width is None or height is None or dpi is None:
        print("Failed to read BlueStacks configuration values.")
        return None

    # Capture the window using the original capture_window function
    img_array = capture_window(hwnd)

    # Convert the numpy array to a PIL Image
    img = Image.fromarray(img_array)

    # Resize the captured image to the BlueStacks resolution
    img_resized = img.resize((width, height), Image.ANTIALIAS)

    # Set the updated DPI
    img_resized.info["dpi"] = (dpi, dpi)

    # Convert the resized PIL Image back to a numpy array
    img_array_resized = np.array(img_resized)

    return img_array_resized



higehr accuracy:

import json
import os
import ctypes
import win32gui
import win32ui
import win32con
import numpy as np
from PIL import Image


def read_bluestacks_config():
    bluestacks_config_path = "C:\\ProgramData\\BlueStacks\\Config\\Engine\\EngineUserSettings.json"

    if not os.path.exists(bluestacks_config_path):
        print("BlueStacks configuration file not found.")
        return None

    with open(bluestacks_config_path, "r") as config_file:
        config_data = json.load(config_file)

    width = config_data.get("width")
    height = config_data.get("height")
    dpi = config_data.get("dpi")

    return width, height, dpi

def capture_window(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    win32gui.BitBlt(save_dc.GetSafeHdc(), 0, 0, width, height, hwnd_dc, 0, 0, win32con.SRCCOPY)

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

    return np.array(img)

def capture_window_normalized(hwnd):
    # Read BlueStacks configuration values
    width, height, dpi = read_bluestacks_config()

    if width is None or height is None or dpi is None:
        print("Failed to read BlueStacks configuration values.")
        return None

    # Capture the window using the original capture_window function
    img_array = capture_window(hwnd)

    # Convert the numpy array to a PIL Image
    img = Image.fromarray(img_array)

    # Get the current screen resolution and DPI
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    hdc_screen = ctypes.windll.user32.GetDC(None)
    screen_dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc_screen, 88)  # 88 is LOGPIXELSX
    ctypes.windll.user32.ReleaseDC(None, hdc_screen)

    # Calculate the scaling factors based on the current screen resolution and DPI
    width_scaling_factor = screen_width / width
    height_scaling_factor = screen_height / height
    dpi_scaling_factor = screen_dpi / dpi

    # Resize the captured image based on the scaling factors
    img_resized = img.resize(
        (int(img.width * width_scaling_factor * dpi_scaling_factor),
         int(img.height * height_scaling_factor * dpi_scaling_factor)),
        Image.ANTIALIAS
    )

    # Set the updated DPI
    img_resized.info["dpi"] = (screen_dpi, screen_dpi)

        # Convert the resized PIL Image back to a numpy array
    img_array_resized = np.array(img_resized)

    return img_array_resized