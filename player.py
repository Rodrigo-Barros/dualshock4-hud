import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GLib, GdkPixbuf

import re
import dbus
import urllib.request
import sys
import os
from settings import config

script_path = sys.path[0]

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,Gtk.WindowType.POPUP)
        GLib.timeout_add(config["notification"]["timeout"] * 1000,Gtk.main_quit)
        self.move(950,15)
        self.resize(400,100)
        self.play_pause_icon = self.set_image("%s/icons/play.png" % script_path,130,130)
        self.play_pause_icon.set_hexpand(True)
        self.play_pause_icon.set_margin_top(10)

        self.label = Gtk.Label()
        self.label.set_label(self.format_metadata())
        self.label.set_hexpand(True)
        self.label.set_margin_bottom(10)
        self.label.set_line_wrap(True)
        
        self.art_album.set_padding(0,10)
        self.art_album.set_margin_left(10)

        self.grid = Gtk.Grid()
        self.grid.add(self.art_album)
        self.grid.attach(self.play_pause_icon,1,0,1,1)
        self.grid.attach_next_to(self.label,self.art_album,Gtk.PositionType.BOTTOM,2,1)

        self.add(self.grid)
        self.show_all()
    
    def set_image(self,path,width=60,height=60):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename=path, 
        width=width, 
        height=height, 
        preserve_aspect_ratio=True)
        return Gtk.Image.new_from_pixbuf(pixbuf)
    
    def format_metadata(self):
        try:
            dbus = Dbus()
            dbus.get_player_props()

            if (sys.argv[1]=="update"):
                print("Fazendo Download da arte de capa")
                urllib.request.urlretrieve(dbus.player_props["Metadata"]["mpris:artUrl"],"%s/artalbum" % script_path)
            self.art_album = self.set_image("%s/artalbum" % script_path,128,128)
            artist = dbus.player_props["Metadata"]["xesam:artist"][0]
            music = dbus.player_props["Metadata"]["xesam:title"]
            
            if dbus.player_props["PlaybackStatus"] == "Playing":
                return "%s - %s" % (artist,music)
            elif dbus.player_props["PlaybackStatus"] == "Paused":
                self.play_pause_icon=self.set_image("%s/icons/pause.png" % script_path,130,130)
                return "Pausado"
        except AttributeError:
            self.play_pause_icon=self.set_image("%s/icons/pause.png" % script_path,130,130)
            self.art_album = self.set_image("%s/icons/no-media.png" % script_path,112,112)
            return "Nenhum player Foi Encontrado"
        except ValueError:
            return "Anúncio ? | informação não disponível"


class Dbus:
    def __init__(self):
        bus = dbus.SessionBus()
        self.player_state="offline"
        for service in bus.list_names():
            if re.match('org.mpris.MediaPlayer2',service):
                self.player_state="online"
                self.player=dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
                self.property_interface = dbus.Interface(self.player, dbus_interface='org.freedesktop.DBus.Properties')
                self.player_dbus_request_name = service
                # stop at first entry with espcified pattern 
                break
      


    def get_player_props(self):
        player_props = {}
        for property, value in self.property_interface.GetAll('org.mpris.MediaPlayer2.Player').items():
            player_props[property] = value
        self.player_props = player_props
if __name__ == '__main__':
    Window()
    Gtk.main()