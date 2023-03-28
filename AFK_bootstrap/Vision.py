
import os
import sys
import ctypes
import win32gui,win32ui,win32con,win32api,win32print
import numpy as np
import cv2
from PIL import Image
import pytesseract
from Shared_functions import *
import pyautogui
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
sys.path.append("C://Users//matth//AppData//Local//Packages//PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0//LocalCache//local-packages//Python311//site-packages//")
sys.path.append("C://Program Files//Tesseract-OCR")

# def search_for_apps(dict):
#     c_drive = "C:\\"
#     file_name = "bluestacks.conf"
#     path_player = None
#     bs_width = ''
#     bs_height = ''
#     bs_dpi = ''
#     total_dirs = 0
#     searched_dirs = 0

#     for root, dirs, files in os.walk(c_drive):
#         total_dirs += len(dirs)
#         if file_name in files:
#             file_path = os.path.join(root, file_name)
#             with open(file_path, 'r') as file:
#                 for line in file:
#                     if 'fb_height' in line:
#                         bs_height = line.split('=')[1].strip().replace('"', '')
#                     elif 'fb_width' in line:
#                         bs_width = line.split('=')[1].strip().replace('"', '')
#                     elif 'dpi' in line:
#                         bs_dpi = line.split('=')[1].strip().replace('"', '')
#             break

#         if path_player is None and 'HD-Player.exe' in files:
#             path_player = os.path.join(root, "HD-Player.exe")

#         searched_dirs += 1
#         percent_load_app= int((searched_dirs / total_dirs) * 100)
#         dict['percent_load_app']=percent_load_app
#         print(percent_load_app)

#     return int(bs_width), int(bs_height), int(bs_dpi), path_player

def search_for_apps(dict):
    c_drive = "C:\\"
    file_name = "bluestacks.conf"
    path_player = None
    bs_width = ''
    bs_height = ''
    bs_dpi = ''
    total_dirs = 0
    searched_dirs = 0

    for root, dirs, files in os.walk(c_drive):
        total_dirs += len(dirs)
        if file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    if 'fb_height' in line:
                        bs_height = line.split('=')[1].strip().replace('"', '')
                    elif 'fb_width' in line:
                        bs_width = line.split('=')[1].strip().replace('"', '')
                    elif 'dpi' in line:
                        bs_dpi = line.split('=')[1].strip().replace('"', '')
            searched_dirs += 1
            percent_load_app = int((searched_dirs / total_dirs) * 100)
            dict['percent_load_app']=percent_load_app
            continue

        if path_player is None and 'HD-Player.exe' in files:
            path_player = os.path.join(root, "HD-Player.exe")
            searched_dirs += 1
            percent_load_app = int((searched_dirs / total_dirs) * 100)
            dict['percent_load_app']=percent_load_app

        if path_player is not None and bs_width and bs_height and bs_dpi:
            searched_dirs += 1
            percent_load_app = int((searched_dirs / total_dirs) * 100)
            dict['percent_load_app']=percent_load_app
            break

        searched_dirs += 1
        percent_load_app = int((searched_dirs / total_dirs) * 100)
        dict['percent_load_app']=percent_load_app
        print(percent_load_app)
    return int(bs_width), int(bs_height), int(bs_dpi), path_player


def read_bluestacks_config():
    c_drive = "C:\\"
    file_name = "bluestacks.conf"
    bs_width=''
    bs_height=''
    bs_dpi=''
    for root, dirs, files in os.walk(c_drive):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            break
    else:
        print("BlueStacks configuration file not found.")
    with open(file_path, 'r') as file:
        for line in file:
            if 'fb_height' in line:
                bs_height = line.split('=')[1].strip().replace('"', '')
            elif 'fb_width' in line:
                bs_width = line.split('=')[1].strip().replace('"', '')
            elif 'dpi' in line:
                bs_dpi = line.split('=')[1].strip().replace('"', '')
    return int(bs_width), int(bs_height), int(bs_dpi)


#print(read_bluestacks_config())
bs_width=0
bs_height=0
bs_dpi=0

# def capture_window_normalized(hwnd):
#     # Read BlueStacks configuration values
#     width, height, dpi = read_bluestacks_config()
    
#     if width is None or height is None or dpi is None:
#         print("Failed to read BlueStacks configuration values.")
#         return None

#     # Capture the window using the original capture_window function
#     img_array = capture_window(hwnd)

#     # Convert the numpy array to a PIL Image
#     img = Image.fromarray(img_array)

#     # Resize the captured image to the BlueStacks resolution
#     img_resized = img.resize((width, height), Image.ANTIALIAS)

#     # Set the updated DPI
#     img_resized.info["dpi"] = (dpi, dpi)

#     # Convert the resized PIL Image back to a numpy array
#     img_array_resized = np.array(img_resized)

#     return img_array_resized


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

def get_monitor_info(window_handle):
    rect = win32gui.GetWindowRect(window_handle)
    monitor_handle = win32api.MonitorFromRect(rect, win32con.MONITOR_DEFAULTTONEAREST)
    monitor_info = win32api.GetMonitorInfo(monitor_handle)

    # Return the width, height, and DPI of the monitor
    width = monitor_info['Monitor'][2] - monitor_info['Monitor'][0]
    height = monitor_info['Monitor'][3] - monitor_info['Monitor'][1]
    hdc_screen = win32gui.GetDC(None)
    # Get the DPI for the window
    #print(monitor_info)
    dpi = win32print.GetDeviceCaps(hdc_screen, win32con.LOGPIXELSX)
    win32gui.ReleaseDC(None, hdc_screen)
    return width, height, dpi

def crop_screenshot(cords=None):
    bluestacks = "BlueStacks App Player"
    window_handle = win32gui.FindWindow(None, bluestacks)
    img_np = cv2.cvtColor(capture_window_normalized(window_handle), cv2.COLOR_BGR2RGB)
    if cords is not None:
        # Get the height and width of the image
        height, width, _ = img_np.shape

        # Get the relative coordinates
        x_rel, y_rel, w_rel, h_rel = cords

        # Convert the relative coordinates to absolute coordinates
        x_abs = int(x_rel * width)
        y_abs = int(y_rel * height)
        w_abs = int(w_rel * width)
        h_abs = int(h_rel * height)

        # Crop the image using absolute coordinates
        if 0 <= x_abs < width and 0 <= y_abs < height and x_abs + w_abs <= width and y_abs + h_abs <= height:
            img_crop = img_np[y_abs:y_abs + h_abs, x_abs:x_abs + w_abs]
        else:
            img_crop = img_np
            print("Invalid crop rectangle, return img instead")
    # if liveview is not None:
    #     cv2.imshow("Screenshot", img_crop)
    #     cv2.waitKey(5000)
    #     cv2.destroyAllWindows()
    return img_crop





def capture_window_normalized(hwnd):
    # Read BlueStacks configuration values
    #width, height, dpi = read_bluestacks_config()
    width, height, dpi = bs_width, bs_height, bs_dpi
    #print(f"Bluestacks window: {width, height, dpi}")
    if width is None or height is None or dpi is None:
        print("Failed to read BlueStacks configuration values.")
        return None
    # Capture the window using the original capture_window function
    img_array = capture_window(hwnd)

    # Convert the numpy array to a PIL Image
    img = Image.fromarray(img_array)

    # Get the current screen resolution and DPI
    # screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    # screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    # hdc_screen = ctypes.windll.user32.GetDC(None)
    # screen_dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc_screen, 88)  # 88 is LOGPIXELSX
    # ctypes.windll.user32.ReleaseDC(None, hdc_screen)
    # print(screen_width,screen_height,screen_dpi)
    screen_width,screen_height,screen_dpi=get_monitor_info(hwnd)
    # Calculate the scaling factors based on the current screen resolution and DPI
    width_scaling_factor = screen_width / width
    height_scaling_factor = screen_height / height
    dpi_scaling_factor = screen_dpi / dpi

    # Resize the captured image based on the scaling factors
    img_resized = img.resize(
        (int(img.width * width_scaling_factor *2.5* dpi_scaling_factor),
         int(img.height * height_scaling_factor *2.5*dpi_scaling_factor)),
        Image.LANCZOS
    )
    # Set the updated DPI
    img_resized.info["dpi"] = (screen_dpi, screen_dpi)

        # Convert the resized PIL Image back to a numpy array
    img_array_resized = np.array(img_resized)

    return img_array_resized


def image_process_for_ocr(img, process_for=None,liveview=None):
    if process_for is not None:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if process_for == 'conservative':
            #print(f"I use {process_for }")
            # Noise removal with a mild Gaussian blur
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            # Binarization using adaptive thresholding
            applied = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        elif process_for == 'text':
            #print(f"I use {process_for }")
            # Equalize the histogram to increase contrast
            equalized= cv2.equalizeHist(gray)
            # Apply adaptive thresholding to convert to binary image
            applied = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        elif process_for == 'digits':
            #print(f"I use {process_for }")
            applied=gray
            # Apply Gaussian blur to remove noise
            #blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            # Equalize the histogram to increase contrast
            #applied = cv2.equalizeHist(gray)
            # Apply adaptive thresholding to convert to binary image
            #applied = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            # Apply morphological transformations to remove noise and fill gaps
            #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            #opening = cv2.morphologyEx(equalized, cv2.MORPH_OPEN, kernel, iterations=1)
            #applied = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
    # Inversion to get black text/numbers on a white background
        img_process = np.array(cv2.bitwise_not(applied))
    else:
        #print(f"I use {process_for }")
        img_process=np.array(img)
    if liveview is not None:
        cv2.imshow("Screenshot", img_process)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
    return img_process     


def image_recog(rec_case, liveview=None,cords=None, rec_pattern=None, process_for=None, search=None, lang='deu'):
    if rec_case != 'custom' and (cords or rec_pattern or process_for or search):
        print("Warning: You provided additional inputs for a predefined rec_case. These inputs will be ignored. Use 'custom' rec_case if you want to provide custom inputs.")
        pass
  
    rec_pattern_configs = {
        'digits': f"--psm 11 -l {lang} -c tessedit_char_whitelist=0123456789-",
        'word': f"--psm 9 -l {lang}",
        'text': f"--psm 11 -l {lang}"
    }

    case_data = {
        #x_rel,y_rel_, w_rel, h_rel
        'startscreen': {'cords': [0.42, 0.854, 0.14, 0.04], 'search': ['start','st', 'ta', 'ar', 'rt', 'sta', 'tar', 'art'], 'rec_pattern': 'word', 'process_for': 'conservative'},
        'towers': {'cords': [0.485, 0.11, 0.075, 0.025], 'rec_pattern': 'digits', 'process_for': 'digits'},
        'campaign': {'cords': [0.501, 0.11, 0.1, 0.025], 'rec_pattern': 'digits', 'process_for': 'digits'},
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
            image_cropped = crop_screenshot(cords)
        else:
            image_cropped = crop_screenshot(cords)
        image_processed = image_process_for_ocr(image_cropped, process_for,liveview=liveview)
        detected = pytesseract.image_to_string(Image.fromarray(image_processed), config=config)
        #print(f"{detected} detected")
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
                image_processed = image_process_for_ocr(image_cropped, process_for,liveview=liveview)
                detected = pytesseract.image_to_string(Image.fromarray(image_processed), config=config)
                for item in search:
                    if item in detected:
                        #print(f"{detected} detected")
                        print(f"Start screen found")
                        return
                    time.sleep(0.1)
    else:
        print("Use case is not dfeined")
        return None
    

def find_on_screen(filename):
    x, y, width, height = bs_window.left, bs_window.top, bs_window.width, bs_window.height
    print(x, y, width, height)
    while True:
        if pyautogui.locateOnScreen(get_image_path(filename),confidence=0.8,grayscale=True,region=(x, y, width, height))!=None:
            print("Condition found")
            break
        #time.sleep(0.2)     

#image_recog(1, liveview="Yes",process_for ='digits')
#crop_screenshot([0.42, 0.854, 0.14, 0.04], liveview="Yes",duration=5000)
#window = gw.getWindowsWithTitle('BlueStacks App Player')[0]
# Get the window's x, y, width, and height
#x, y, width, height = window.left, window.top, window.width, window.height

def find_image(filename, threshold=0.8):
    bluestacks = "BlueStacks App Player"
    window_handle = win32gui.FindWindow(None, bluestacks)
    template = cv2.imread(get_image_path(filename))
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot=capture_window(window_handle)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return len(locations[0]) > 0

# bs_window = gw.getWindowsWithTitle('BlueStacks App Player')[0]
# start_time = time.time()
# #find_on_screen("victory.png")
# find_image("victory.png", threshold=0.8)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")

#print(find_image('victory.png', threshold=0.85))