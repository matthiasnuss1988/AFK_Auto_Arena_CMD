import os
import win32api
import win32con
import win32gui
import time
import sys
from win32con import SW_SHOWNORMAL
import json
import pyautogui
import win32gui,  win32con, win32api,win32ui
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
import ctypes
import ctypes.wintypes
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
key_sequences = {
    1: ['h', 'x', 'y'],
    2: ['a', 'e', 'e'],
    3: ['a', 'e', 'h'],
    4: ['a', 'e', 'l'],
    5: ['a', 'e', 'b'],
    6: ['a', 'e', 'y'],
    7: ['a', 'e', '4'],
    8: ['a', 'e', '1'],
    'prefight': ['h','x','y','1','t',None,'k','v','a','v'],
    'afterfight': ['v','v','p','e']
}
def send_keys_to_bluestacks(keys, delays):
    window_handle = win32gui.FindWindow(None, bluestacks)
    time.sleep(2)
    win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
    win32gui.SetWindowPos(window_handle, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    ctypes.windll.user32.SetForegroundWindow(window_handle)
    #win32gui.ShowWindow(window_handle, win32con.SW_SHOWNORMAL)
    if not isinstance(keys, list) or not isinstance(delays, list) or len(keys) != len(delays):
        raise ValueError("Both 'keys' and 'delays' should be lists of the same length.")

    for key, delay in zip(keys, delays):
        #win32gui.SetForegroundWindow(window_handle)
        win32api.PostMessage(window_handle, win32con.WM_KEYDOWN, ord(key), 0)
        time.sleep(0.05)  # Add a short pause between key down and key up events
        win32api.PostMessage(window_handle, win32con.WM_KEYUP, ord(key), 0)
        time.sleep(delay)
        print(key)

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
start=[230, 805, 80, 40]









# Fraction tower level coordinates
ft_cords=[265, 98, 40, 30]








#lxr#
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
        cv2.imshow("Screenshot", cropped_image)
        cv2.waitKey(5000)
        cv2.destroyAllWindows() 
    if p=='proc':
        image_pre = preprocess_image_for_ocr(cropped_image)
        #cv2.imshow("Processed window",   image_pre)
        #cv2.waitKey(5000)
    elif p=='org':
        image_pre=np.array(cropped_image )
        cv2.imshow("Original window",   image_pre)
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
            print(text)
            return text
        elif combos!=None:
            text = pytesseract.image_to_string(Image.fromarray(image_pre), config="--psm 9 -l deu")
            for combo in combos:
                if combo in text:
                    print(f"{combo} found")
                    return text
        time.sleep(0.1)
        




bluestacks="BlueStacks App Player"
# if not is_admin():
#     sys.exit() 
#Get the path to the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to Bluestacks relative to the script directory
for root, dirs, files in os.walk("C:/"):
    if "HD-Player.exe" in files:
        bluestacks_path  = os.path.join(root, "HD-Player.exe")
        break

# Open Bluestacks with administrator privileges
win32api.ShellExecute(0, 'runas', bluestacks_path, '', '', 1)
print("waiting")
time.sleep(1)
print("now")
# Send keys to Bluestacks
#send_keys_to_bluestacks(['X','Y', 'Y'], [2, 2, 2])
##pyautogui.typewrite(['x','y','y','1'],interval=2)
config ={"Campaign":"",
         "King's Tower":"",
         "Celestial Sanctum":"",
         "Tower of Light":"",
         "The Brutal Citadel":"",
         "Infernal Fortress":"",
         "The Forsaken Neckropolis":"",
         "The World Tree":""
         }
with open ('config.json','w') as f:
    json.dump(config,f)

with open ('config.json','r') as f:
    config=json.load(f)
    config["Campaign"]='51-12'
    config["King's Tower"]='1439'
    config["Celestial Sanctum"]='667'
    config["Tower of Light"]='991'
    config["The Brutal Citadel"]='982'
    config["Infernal Fortress"]='680'
    config["The Forsaken Neckropolis"]='991'
    config["The World Tree"]='983'

with open ('config.json','w') as f:
    json.dump(config,f)
image_recog(ft_cords,'org','digits')
# counter=0
# if pyautogui.mouse.click():
#              new_top=top+stc[0]
# #         new_left=left+stc[1]
# #         new_right=right+stc[2]
# #         new_bottom=bottom+stc[3]
#      if counter==0:
#          xl, yl = pyautogui.position()
#      if counter==1:
#          xr, yr = pyautogui.position()
#      if counter==2:
#          xt, yt = pyautogui.position()
#      if counter==3:
#          xb, yb = pyautogui.position()
#      if counter==4:
#          il, il = pyautogui.position()
#      if counter==5:
#          ir, ir = pyautogui.position()
#      if counter==6:
#          it, it = pyautogui.position()
#      if counter==7:
#          ib, b = pyautogui.position()
#     rect_t=it-xt
#     rect_l= il-xl
#     rect_r= xr-xl
    
#     counter+=1

#     window_top
# window_down
# window_left
# window_right
# rect_top
# rect_down
# rect_left
# rect_right
a_string='991%,'
numeric_filter = filter(str.isdigit, a_string)
numeric_string = "".join(numeric_filter)
print(numeric_string)