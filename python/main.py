import copy
import bluetooth
from pywinauto import Desktop
import time


def get_device_name(device_name):
    device_address = None
    nearby_devices = bluetooth.discover_devices()
    for device in nearby_devices:
        if device_name == bluetooth.lookup_name(device):
            device_address = device
            break
    if device_address is not None:
        print("Found esp32 device with address ", device_address)
    else:
        print("Could not find esp32 device nearby")
    return device_address


print("Establishing connection...")
esp_address = get_device_name("ESP32_busy_light")
#esp_address = "84:CC:A8:6D:33:CE"
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
try:
    socket.connect((esp_address, 1))
except:
    print("Connection cannot be established, make sure that the device is powered on and try again")
    time.sleep(2)
    exit()

socket.send("ready")
old_status = ""
while True:
    status = "free"
    time.sleep(5)
    for window in Desktop(backend="uia").windows():
        if window.window_text().startswith("Zoom Meeting"):
            # print("Zoom opened")
            status = "busy"
        elif window.window_text().startswith("Besprechung") or window.window_text().startswith("Meeting"):
            # print("Teams opened")
            status = "busy"

    if old_status != status:
        old_status = copy.deepcopy(status)
        print(status)
        socket.send(status)
socket.close()
