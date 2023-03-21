import sys
import os
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

main_script = 'C://Users//matth//Documents//GitHub//AFK_Auto_Arena_CMD//Neuer Ordner//AFK_Arena.py'  # Replace with the path to your main script

if not is_admin():
    print("Elevating script to admin")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{main_script}"', None, 1)
else:
    with open(main_script) as file:
        exec(file.read())