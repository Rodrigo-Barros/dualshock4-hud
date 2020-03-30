#!/usr/bin/python3
import gi, cairo, evdev, os, sys
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GLib
from settings import config
from datetime import datetime
from time import sleep
from player import Dbus

load_config=0
bluetooth_id="1c:66:6d:55:e3:ea"

class messages():
    def __init__(self):
        #global battery
        battery = int(os.popen('cat /sys/class/power_supply/sony_controller_battery_%s/capacity' % bluetooth_id).read().strip() or -1)
        self.current_time = datetime.now().strftime("%H:%M")
        self.battery_status = {
            'full':'Full charge You ready to Play',
            'intermediate': 'Ok Good to Keep Playing',
            'half':'Baterry discharging, pay atention',
            'low':'Low Baterry'
        }
        self.plain_text  = '  Hora:%s Bateria:%s%% \n%s' % (self.current_time, battery,self.get_status_battery(battery))
        self.stylish_text = '<span font="%s" color="%s">%s</span>' % (config['bat_sts']['font']['size'], config['bat_sts']['font']['color'], self.plain_text)

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
        self.label.set_padding(0,10)
        self.label.set_margin_left(10)
        self.label.set_margin_right(10)
        self.move(config['bat_sts']["window"]["position"]["x"],config['bat_sts']["window"]["position"]["y"])
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
            self.background_color = config["bat_sts"]["background-color"]
            for i in range(3):
                self.background_color[i] = self.background_color[i]/256
        else:
            self.background_color = config["bat_sts"]["background-color"]


def get_cover_art_url(player_state="offline"):
    if player_state == "offline":
        return -1
    else:
        dbus = Dbus()
        dbus.get_player_props()
        return dbus.player_props["Metadata"]["mpris:artUrl"]

def log(msg):
    os.system("echo %s DEBUG: %s >> %s/log" % (datetime.now().strftime('%D %T'), msg, sys.path[0] ))

if __name__ == '__main__':
   
    command="python3 %s/player.py" % sys.path[0]
    Player=Dbus()
    old_cover_art = get_cover_art_url(Player.player_state)
    first_time_open_app = 1

    while True:

        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for controller in devices:
            controller_found=1
            sleep(config['scan-timeout'])
            if controller.active_keys() == config["notification"]["keys"]:
                current_cover_art = get_cover_art_url(Player.player_state)

                #Resolve o bug que exibe capas antigas na primeira inicialização
                if first_time_open_app==1:
                    first_time_open_app=0
                    os.system("%s update &" % command)
                    log("Baixando nova arte de capa")
                    continue

                if old_cover_art != current_cover_art:
                    log("Baixando nova arte de capa")
                    old_cover_art = current_cover_art
                    current_cover_art = get_cover_art_url(Player.player_state)
                    os.system("%s update &" % command)
                    sleep(config['scan-timeout'])
                elif current_cover_art == -1:
                    #bug com o anúncio do spotify
                    log("Nenhum Player Foi encontrado")
                    os.system("%s do_not_update &" % command)
                    sleep(config['scan-timeout'])
                else:
                    os.system("%s do_not_update &" % command)
                    log("Exibindo a arte de capa já baixada")
                    sleep(config['scan-timeout'])
                main()
            elif controller.active_keys() == [307, 316]:
                os.system("echo 'disconnect %s' | bluetoothctl >> /dev/null" % bluetooth_id)
                log("Desconectando o Controle")
            elif controller.active_keys() == [304, 316]:
                os.system("xdotool key XF86AudioPlay")
                log("Enviando Play/Pause para o Player")
        try:
            for event in controller.read_loop():

                if event.type == evdev.ecodes.ABS_RY or event.type == evdev.ecodes.ABS_RX or event.type == evdev.ecodes.EV_KEY:
                    
                    if event.code == 0:

                        if event.value <= 30 and controller.active_keys() == [316]:
                            #log("LS_X LEFT %s" % event.value)
                            log("Retornando para a música anterior")
                            os.system("xdotool key XF86AudioPrev")

                        if event.value >= 235 and controller.active_keys() == [316]:
                            #log("LS_X RIGHT %s" % event.value)
                            log("Passando para a próxima música")
                            os.system("xdotool key XF86AudioNext")

                    if event.code == 1:    
                        while event.value <= 100 and controller.active_keys() == [316]:
                            #log("LS_Y UP %s" % event.value)
                            log("Aumentando o volume")
                            sleep(config["scan-timeout"])
                            os.system("xdotool key XF86AudioRaiseVolume")
                            for event2 in controller.read_loop():
                                event.value = event2.value
                                break
                        while event.value >= 200 and controller.active_keys() == [316]:
                            sleep(config["scan-timeout"])
                            #log("LS_Y DOWN %s" % event.value)
                            log("Dimuinuindo o volume")
                            os.system("xdotool key XF86AudioLowerVolume")
                            for event2 in controller.read_loop():
                                event.value = event2.value
                                break
                    break
        except OSError:
            if controller_found == 1:
                    os.system("notify-send --hint int:transient:1 -i info 'Controle desligado'")
                    log("O controle foi desligado")
                    exit(0)
        except NameError:
            log("O controle nao foi encontrado")
            os.system("nnotify-send --hint int:transient:1 -i info 'O controle não foi encontrado'")
            log("O controle não foi encontrado")
            exit(1)
