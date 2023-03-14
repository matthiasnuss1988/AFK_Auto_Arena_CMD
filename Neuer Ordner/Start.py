import tkinter as tk

def add_five():
    num = int(entry.get())
    result = num + 5
    label.config(text="Result: " + str(result))

root = tk.Tk()
root.title("Add 5")

# Create GUI elements
label = tk.Label(root, text="Enter a number:")
entry = tk.Entry(root)
button = tk.Button(root, text="Add 5", command=add_five)

# Add GUI elements to window
label.pack()
entry.pack()
button.pack()
tk.mainloop()