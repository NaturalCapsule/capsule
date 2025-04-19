import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk

class App(Gtk.Menu):
    def __init__(self):
        super().__init__()
        self.build_menu()
        self.show_all()


    def build_menu(self):
        self.media_control_menu()
        refresh_item = Gtk.MenuItem(label="Refresh")

        self.append(self.media_item)
        self.append(refresh_item)


    def media_control_menu(self):
        self.media_item = Gtk.MenuItem(label="Media Control")
        media_submenu = Gtk.Menu()

        pause_play = Gtk.MenuItem(label="Pause/Play")
        pause_play.connect('activate', self.pause_play_func)
        
        
        reset = Gtk.MenuItem(label="Reset")
        reset.connect('activate', self.reset_func)

        fast_forward = Gtk.MenuItem(label="Fast Forward")
        fast_forward.connect('activate', self.fast_forward_func)

        backward = Gtk.MenuItem(label="Backward")
        backward.connect('activate', self.backward_func)

        next_track = Gtk.MenuItem(label="Next Track")
        next_track.connect('activate', self.next_track)
        
        previous_track = Gtk.MenuItem(label="Previous Track")
        previous_track.connect('activate', self.previous_track)

        # label = Gtk.MenuItem(label="Advanced Options")
        # label.set_sensitive(False)

        # media_submenu.append(label)

        # media_submenu.append(Gtk.SeparatorMenuItem())



        media_submenu.append(pause_play)
        media_submenu.append(reset)
        media_submenu.append(fast_forward)
        media_submenu.append(backward)
        media_submenu.append(next_track)
        media_submenu.append(previous_track)
        
        self.media_item.set_submenu(media_submenu)

    def previous_track(self, widget):
        os.system("playerctl previous")
        
    def next_track(self, widget):
        os.system("playerctl next")

    def reset_func(self, widget):
        os.system('playerctl position 0')

    def pause_play_func(self, widget):
        os.system('playerctl play-pause')
    
    def fast_forward_func(self, widget):
        os.system("playerctl position 10+")

    def backward_func(self, widget):
        os.system("playerctl position 10-")


def show_menu():
    menu = App()

    display = Gdk.Display.get_default()
    seat = display.get_default_seat()
    device = seat.get_pointer()
    screen, x, y = device.get_position()

    menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

    def exit_on_close(*args):
        Gtk.main_quit()

    menu.connect("selection-done", exit_on_close)

show_menu()
Gtk.main()
