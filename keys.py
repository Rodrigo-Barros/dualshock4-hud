import evdev
import os
from time import sleep

# button list
# button name              code/axis     max    min
# home                        316         -      -          
# ABS_RX                       3         255     0
# ABS_RY                       4          0     255
# ABS_X                        0         255     0
# ABS_Y                        1          0     255        


while True:
    #original keys file
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for controller in devices:
            print(controller.active_keys())
            sleep(.3)
    continue
    device = evdev.InputDevice('/dev/input/event21')
    home_button_pressed=0
    print("init")
    for event in device.read_loop():

        if event.type == evdev.ecodes.ABS_RY or event.type == evdev.ecodes.ABS_RX or event.type == evdev.ecodes.EV_KEY:
            
            #print( evdev.categorize(event).event )
            #print("%s %s" %(evdev.categorize(event),event.value))
            
            #Left Stick

            if event.code == 0:

                if event.value <= 30 and device.active_keys() == [316]:
                    print("LS_X LEFT %s" % event.value)
                    os.system("xdotool key XF86AudioPrev")

                if event.value >= 235 and device.active_keys() == [316]:
                    os.system("xdotool key XF86AudioNext")
                    print("LS_X RIGHT %s" % event.value)
                    

            if event.code == 1:    
                while event.value <= 100 and device.active_keys() == [316]:
                    print("LS_Y UP %s" % event.value)
                    sleep(.1)
                    os.system("xdotool key XF86AudioRaiseVolume")
                    for event2 in device.read_loop():
                        event.value = event2.value
                        break
                while event.value >= 200 and device.active_keys() == [316]:
                    sleep(.1)
                    print("LS_Y DOWN %s" % event.value)
                    os.system("xdotool key XF86AudioLowerVolume")
                    for event2 in device.read_loop():
                        event.value = event2.value
                        break
            break



            if event.code == 316:
                print("botao central pressionado")
                #continue

            while device.active_keys() == [316] and event.code==1 and event.value <= 10:
                sleep(.1)
                #home_button_pressed=0
                os.system("xdotool key XF86AudioRaiseVolume")

            while device.active_keys() == [316] and event.code==1 and event.value >= 245:
                sleep(.1)
                os.system("xdotool key XF86AudioLowerVolume")
            continue


            if home_button_pressed==1 and event.code==1 and event.value <= 10: 
                home_button_pressed=0
                os.system("xdotool key XF86AudioRaiseVolume")
                print("aumentar volume")
                #exit(0)
            if home_button_pressed==1 and event.code==1 and event.value >= 245: 
                home_button_pressed=0
                os.system("xdotool key XF86AudioLowerVolume")
                print("diminuir volume")
                #exit(0)

        continue

        if event.type != 3 and event.type != 0:
            print( evdev.categorize(event).event )
            print("%s %s" %(evdev.categorize(event),event.value))
            print("\n")
            exit(0)


            
        
