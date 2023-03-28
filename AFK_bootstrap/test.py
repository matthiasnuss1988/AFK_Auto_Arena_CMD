import os 
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
    return bs_width, bs_height, bs_dpi
        

print(read_bluestacks_config())
