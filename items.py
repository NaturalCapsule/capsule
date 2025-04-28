import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk


def create_menu_item(label_text, icon_path, on_hover_enter, on_hover_leave):
    box = Gtk.EventBox()
    box.set_above_child(False)
    
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox.set_border_width(8)
    
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 20, 20)
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        hbox.pack_start(icon, False, False, 2)
    except GLib.Error:
        pass
        
    label = Gtk.Label(label=label_text)
    label.set_xalign(0)
    hbox.pack_start(label, True, True, 2)
    
    if label_text != "Terminal" and label_text != "Exit" and label_text != "Open File Manager":
        arrow = Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.MENU)
        hbox.pack_end(arrow, False, False, 2)
        
    box.add(hbox)
    
    box.connect("enter-notify-event", on_hover_enter)
    box.connect("leave-notify-event", on_hover_leave)
    
    return box


def build_submenu_window(title):
    window = Gtk.Window(type=Gtk.WindowType.POPUP)
    window.set_decorated(False)
    window.set_resizable(False)
    window.set_skip_taskbar_hint(True)
    window.set_skip_pager_hint(True)
    window.get_style_context().add_class('Submenu')
    
    screen = window.get_screen()
    visual = screen.get_rgba_visual()
    if visual and screen.is_composited():
        window.set_visual(visual)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    window.add(vbox)
    
    window.connect("key-press-event", lambda w, e: w.destroy() if e.keyval == Gdk.KEY_Escape else None)
    
    return window, vbox


def create_submenu_item(label_text, icon_path=None, use_theme_icon=False, on_submenu_hover_enter = None, on_submenu_hover_leave = None):
    box = Gtk.EventBox()
    box.set_above_child(False)
    
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox.set_border_width(8)
    
    if icon_path:
        if use_theme_icon:
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon_path, 32, 0)
                scaled_pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.BILINEAR)
                icon = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
            except GLib.Error:
                icon = Gtk.Image.new_from_icon_name(icon_path, Gtk.IconSize.SMALL_TOOLBAR)
        else:
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 20, 20)
                icon = Gtk.Image.new_from_pixbuf(pixbuf)
            except GLib.Error:
                icon = Gtk.Image.new_from_icon_name(icon_path, Gtk.IconSize.MENU)
                
        hbox.pack_start(icon, False, False, 2)
        
    label = Gtk.Label(label=label_text)
    label.set_xalign(0)
    hbox.pack_start(label, True, True, 2)
    
    box.add(hbox)
    
    box.connect("enter-notify-event", on_submenu_hover_enter)
    box.connect("leave-notify-event", on_submenu_hover_leave)
    
    return box


def create_info_header(text, icon_path):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    box.set_border_width(8)
    
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 20, 20)
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        box.pack_start(icon, False, False, 0)
    except GLib.Error:
        pass
        
    label = Gtk.Label(label=text)
    label.set_xalign(0)
    box.pack_start(label, False, False, 0)
    
    return box

def create_info_item(text):
    label = Gtk.Label(label=text)
    label.set_xalign(0)
    label.set_margin_start(20)
    
    return label