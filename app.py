import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk

class App(Gtk.Menu):
    def __init__(self):
        super().__init__()
        self.build_menu()

    def build_menu(self):
        new_item = Gtk.MenuItem(label="New")
        new_submenu = Gtk.Menu()

        text_doc = Gtk.MenuItem(label="Text Document")
        folder = Gtk.MenuItem(label="Folder")

        new_submenu.append(text_doc)
        new_submenu.append(folder)
        new_item.set_submenu(new_submenu)

        refresh_item = Gtk.MenuItem(label="Refresh")

        self.append(new_item)
        self.append(refresh_item)

        self.show_all()

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
