import evdev
from time import sleep
while True:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for controller in devices:
            print(controller.active_keys())
            sleep(.5)

