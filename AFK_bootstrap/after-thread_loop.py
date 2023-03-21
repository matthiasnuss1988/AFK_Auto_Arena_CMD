import threading
import time
from loop_process import long_duration_loop
global loop_result, stop_event,t

def start_loop():
    global loop_result,stop_event,t
    stop_event = threading.Event()
    loop_result = None
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    def update_label(j):
        label.config(text="Inner loop index:"+str(j))
        root.update()
    def run_loop():
        loop_result = long_duration_loop(stop_event, update_label)
    t = threading.Thread(target=run_loop)
    t.start()
def stop_loop():
    global stop_event
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    stop_event.set()
    for t in threading.enumerate():
        if t != threading.main_thread():
            t.join()
    stop_event.clear()

import tkinter as tk
root = tk.Tk()
label = tk.Label(root, text="Inner loop index: 0")
label.pack()
start_button = tk.Button(root, text="Start", command=start_loop)
start_button.pack()
stop_button = tk.Button(root, text="Stop", command=stop_loop)
stop_button.pack()
root.mainloop()
