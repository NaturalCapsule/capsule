import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
separator.get_style_context().add_class('Separators')

sys_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
sys_separator.get_style_context().add_class('Separators')

sys_separator_ = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
sys_separator_.get_style_context().add_class('Separators')

media_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
media_separator.get_style_context().add_class('Separators')

timer_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
timer_separator.get_style_context().add_class('Separators')


search_entry = Gtk.SearchEntry()
search_entry.get_style_context().add_class('App-Search')
search_entry.set_placeholder_text('Search...')

listbox = Gtk.ListBox()
listbox.get_style_context().add_class('App-List')

listbox.set_hexpand(False)
listbox.set_vexpand(False)


title_label = Gtk.Label()
title_label.get_style_context().add_class("Media-Title")

media_image = Gtk.Image()
media_image.get_style_context().add_class("Media-Image")

cpu_temp = Gtk.Label(label="CPU Temperature: Updating...")
cpu_temp.get_style_context().add_class('sysInfo')

cpu_usage = Gtk.Label(label="CPU Usage: Updating...")
cpu_usage.get_style_context().add_class('sysInfo')

ram_usage = Gtk.Label(label="RAM Usage: Updating...")
ram_usage.get_style_context().add_class('sysInfo')

used_ram = Gtk.Label(label="Used RAM: Updating...")
used_ram.get_style_context().add_class('sysInfo')

gpu_temp = Gtk.Label(label="GPU Temperature: Updating...")
gpu_temp.get_style_context().add_class('sysInfo')

gpu_usage = Gtk.Label(label="GPU Usage: Updating...")
gpu_usage.get_style_context().add_class('sysInfo')

gpu_vram = Gtk.Label(label="GPU VRAM: Updating...")
gpu_vram.get_style_context().add_class('sysInfo')

gpu_speed = Gtk.Label(label="GPU Speed: Updating...")
gpu_speed.get_style_context().add_class('sysInfo')

gpu_power = Gtk.Label(label="GPU Power: Updating...")
gpu_power.get_style_context().add_class('sysInfo')


time_label = Gtk.Label(label = 'Loading Time...')
time_label.get_style_context().add_class('Clock')