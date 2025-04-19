import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from app_info import get_app_info
from actions import *

class App(Gtk.Menu):
    def __init__(self):
        super().__init__()
        self.build_menu()
        self.show_all()


    def build_menu(self):
        self.media_control_menu()
        self.terminal_menu()
        self.application_menu()

        self.append(self.media_item)
        self.append(self.terminal_item)
        self.append(self.app_menu_item)

    def terminal_menu(self):
        self.terminal_item = Gtk.MenuItem(label="Terminal")
        self.terminal_item.connect('activate', open_terminal)


    def media_control_menu(self):
        self.media_item = Gtk.MenuItem(label="Media Control")
        media_submenu = Gtk.Menu()

        pause_play = Gtk.MenuItem(label="Pause/Play")
        pause_play.connect('activate', pause_play_func)
        
        reset = Gtk.MenuItem(label="Reset")
        reset.connect('activate', reset_func)

        fast_forward = Gtk.MenuItem(label="Fast Forward")
        fast_forward.connect('activate', fast_forward_func)

        backward = Gtk.MenuItem(label="Backward")
        backward.connect('activate', backward_func)

        next_track = Gtk.MenuItem(label="Next Track")
        next_track.connect('activate', next_track_func)
        
        previous_track = Gtk.MenuItem(label="Previous Track")
        previous_track.connect('activate', previous_track_func)

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


    def application_menu(self):
        self.app_menu_item = Gtk.MenuItem(label="Applications")
        app_submenu = Gtk.Menu()
        self.app_menu_item.set_submenu(app_submenu)

        apps = get_app_info()
        for name, exec, icon in apps:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
                scaled_pixbuf = pixbuf.scale_simple(16, 16, GdkPixbuf.InterpType.BILINEAR)
                app_icon = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
            except GLib.Error:
                app_icon = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.SMALL_TOOLBAR)

            app_label = Gtk.Label(label=name)

            box.pack_start(app_icon, False, False, 0)
            box.pack_start(app_label, False, False, 0)
            box.show_all()

            menu_item = Gtk.MenuItem()
            menu_item.add(box)

            menu_item.connect("activate", launch_app, exec)

            app_submenu.append(menu_item)

        self.app_menu_item.show_all()


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
