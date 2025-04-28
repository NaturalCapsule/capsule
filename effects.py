import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk

def on_submenu_hover_leave(widget, event):
    widget.get_style_context().remove_class("menu-item-hover")
    widget.unset_state_flags(Gtk.StateFlags.PRELIGHT)
    return False

def on_submenu_hover_enter(widget, event, active_submenu):
    widget.get_style_context().add_class("menu-item-hover")
    widget.set_state_flags(Gtk.StateFlags.PRELIGHT, True)
    
    if active_submenu and hasattr(active_submenu, 'submenu_items'):
        if widget in active_submenu.submenu_items:
            active_submenu.current_selected_index = active_submenu.submenu_items.index(widget)
    
    return False

def on_hover_leave(widget, event):
    widget.get_style_context().remove_class("menu-item-hover")
    widget.unset_state_flags(Gtk.StateFlags.PRELIGHT)
    return False