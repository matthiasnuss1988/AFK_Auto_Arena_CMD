import logging
import tkinter as tk
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def loop():
    global counter
    time.sleep(2.5)
    # Do some stuff
    time.sleep(1)
    # Do some other stuff
    time.sleep(3)
    print("hello")
    logging.debug(f"Processing iteration {counter}")
    counter += 1
    if stop_flag.get():
        root.after(10, loop)

def start_loop():
    global stop_flag, counter
    stop_flag = tk.BooleanVar(value=True)
    counter = 0
    loop()

def stop_loop():
    global stop_flag
    if stop_flag is not None:
        stop_flag.set(False)
        #stop_button.config(state=tk.DISABLED)

root = tk.Tk()

stop_flag = None

start_button = tk.Button(root, text="Start", command=start_loop)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_loop)
stop_button.pack()

root.mainloop()