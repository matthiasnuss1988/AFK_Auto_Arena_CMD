from ppadb.client import Client

# Connect to the ADB server
adb = Client(host='127.0.0.1', port=5037)

# Get the list of connected devices
devices = adb.devices()
for device in devices:
    print(device.serial)

#     quit()
# device = devices[0]
# print(devices)
# device.shell('input touchscreen swipe 500 500 500 500 2000')
# image = device.screencap()

# with open('screen.png', 'wb') as f:
#     f.write(image)

# Set path to ADB executable
#adb_path = "C://Users//matth//Desktop//Neuer Ordner//adb//platform-tools//adb.exe"

# Start Bluestacks
#subprocess.call([adb_path, "shell", "am", "start", "-n", "com.bluestacks.home/com.bluestacks.home.HomeActivity"])
