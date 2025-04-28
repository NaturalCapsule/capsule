import gi
gi.require_version('Gtk', '3.0')
from actions import *

from gi.repository import Gtk, Gdk

def on_exit_click(widget, event, destroy):
    if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
        exit_(widget)
        destroy()
        Gtk.main_quit()

def on_fileM_click(widget, event, destroy, file_manager):
    if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
        open_fileM(widget, file_manager)
        destroy()
        Gtk.main_quit()

def on_terminal_click(widget, event, destroy, terminal):
    if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
        open_terminal(widget, terminal)
        destroy()
        Gtk.main_quit()

def on_submenu_item_click(widget, event, callback):
    if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
        callback(widget)
        for window in Gtk.Window.list_toplevels():
            window.destroy()
        Gtk.main_quit()
