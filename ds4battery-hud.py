#!/usr/bin/python3
import gi, cairo, evdev, os, time, sys
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GLib
from settings import config
from datetime import datetime

load_config=0

class messages():
    def __init__(self):
        global battery
        battery = int(os.popen('cat /sys/class/power_supply/sony_controller_battery_1c:66:6d:55:e3:ea/capacity').read().strip() or -1)
        self.current_time = datetime.now().strftime("%H:%M")
        self.battery_status = {
            'full':'Full charge You ready to Play',
            'intermediate': 'Ok Good to Keep Playing',
            'half':'Baterry discharging, pay atention',
            'low':'Low Baterry'
        }
        self.plain_text  = '  Hora:%s Bateria:%s%% \n%s' % (self.current_time, battery,self.get_status_battery(battery))
        self.stylish_text = '<span font="%s" color="%s">%s</span>' % (config['font']['size'], config['font']['color'], self.plain_text)

    def get_status_battery(self,level):
        if level == 100:
            return self.battery_status['full']
        elif level >= 50:
            return self.battery_status['intermediate']
        elif level <= 50:
            return self.battery_status['half']
        elif level < 50:
            return self.battery_status['low']

class main(Gtk.Window):
    def __init__(self):
        self.convert_background()
        Gtk.Window.__init__(self,Gtk.WindowType.POPUP)
        self.label = Gtk.Label()
        self.label.set_markup(messages().stylish_text)
        self.move(config["window"]["position"]["x"],config["window"]["position"]["y"])
        self.resize(200,100)
        self.connect("destroy", Gtk.main_quit)
        self.connect("draw",self.draw)
        GLib.timeout_add(config["notification"]["timeout"] * 1000, self.destroy_window)
        self.add(self.label)
        self.set_app_paintable(True)

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual and self.screen.is_composited():
            self.set_visual(self.visual)

        self.set_app_paintable(True)
        self.show_all()

        Gtk.main()
    
    def draw(self,widget,context):
        context.set_source_rgba(self.background_color[0] or 0, self.background_color[1] or 0, self.background_color[2] or 0, self.background_color[3] or 0)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER) 

    def destroy_window(self):
        Gtk.main_quit()
        self.destroy()

    def convert_background(self):
        global load_config
        if load_config == 0:
            load_config = 1
            self.background_color = config["background-color"]
            for i in range(3):
                self.background_color[i] = (1/255) * self.background_color[i]
        else:
            self.background_color = config["background-color"]
        

if __name__ == '__main__':
    while True:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for controller in devices:
            if controller.active_keys() == config["notification"]["keys"]:
                main()
            elif controller.active_keys() == [307, 316]:
                os.system("echo 'power off' | bluetoothctl")
        if devices == []:
            #print("%s DEBUG: O controle nao foi encontrado" % datetime.now().strftime('%T'))
            os.system("echo %s DEBUG: O controle nao foi encontrado >> %s/log" % (datetime.now().strftime('%T'),sys.path[0] ))
            exit(1)
        time.sleep(config["scan-timeout"])

    
