import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from app_info import get_app_info
from actions import *
from sys_info import *
from timers import RunTimers



class App(Gtk.Menu):
    def __init__(self):
        super().__init__()
        self.build_menu()
        self.show_all()


    def build_menu(self):
        self.media_control_menu()
        self.terminal_menu()
        self.application_menu()
        self.power_menu()
        self.system_info_menu()


        self.append(self.media_item)
        self.append(self.app_menu_item)
        self.append(self.system_item)
        self.append(self.power_item)
        self.append(Gtk.SeparatorMenuItem())
        
        self.append(self.terminal_item)

        RunTimers(self.cpu_temp, self.cpu_usage, self.ram_usage, self.used_ram, self.gpu_temp, self.gpu_usage, self.gpu_vram, self.gpu_speed, self.gpu_power)


    def terminal_menu(self):
        self.terminal_item = Gtk.MenuItem()

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)


        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/terminal.png', 20, 20)
        app_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        app_label = Gtk.Label(label="Terminal")

        self.terminal_item.connect('activate', open_terminal)


        box.pack_start(app_icon, False, False, 0)
        box.pack_start(app_label, False, False, 0)
        box.show_all()
        self.terminal_item.add(box)

    def media_control_menu(self):
        media_submenu = Gtk.Menu()
        self.media_item = Gtk.MenuItem()

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/music.png', 20, 20)
        app_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        app_label = Gtk.Label(label="Media Control")


        box.pack_start(app_icon, False, False, 0)
        box.pack_start(app_label, False, False, 0)
        box.show_all()
        self.media_item.add(box)


        pause_play = Gtk.MenuItem(label="Pause/Play")
        pause_play.connect('activate', pause_play_func)
        
        reset = Gtk.MenuItem()
        reset.connect('activate', reset_func)


        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/reset.png', 20, 20)
        reset_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        reset_label = Gtk.Label(label = "Reset")


        box.pack_start(reset_icon, False, False, 0)
        box.pack_start(reset_label, False, False, 0)
        box.show_all()
        reset.add(box)

        fast_forward = Gtk.MenuItem()
        fast_forward.connect('activate', fast_forward_func)
        
        box_ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/fast-forward.png', 20, 20)
        fast_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        fast_label = Gtk.Label(label = "Fast Forward")


        box_.pack_start(fast_icon, False, False, 0)
        box_.pack_start(fast_label, False, False, 0)
        box_.show_all()
        fast_forward.add(box_)


        backward = Gtk.MenuItem()
        backward.connect('activate', backward_func)

        box__ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/fast-backward.png', 20, 20)
        back_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        back_label = Gtk.Label(label = "Fast Backward")


        box__.pack_start(back_icon, False, False, 0)
        box__.pack_start(back_label, False, False, 0)
        box__.show_all()
        backward.add(box__)


        next_track = Gtk.MenuItem()
        next_track.connect('activate', next_track_func)

        box___ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/next.png', 20, 20)
        next_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        next_label = Gtk.Label(label = "Next Track")


        box___.pack_start(next_icon, False, False, 0)
        box___.pack_start(next_label, False, False, 0)
        box___.show_all()
        next_track.add(box___)


        previous_track = Gtk.MenuItem()
        previous_track.connect('activate', previous_track_func)

        box____ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/previous.png', 20, 20)
        previous_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        previous_label = Gtk.Label(label = "Previous Track")


        box____.pack_start(previous_icon, False, False, 0)
        box____.pack_start(previous_label, False, False, 0)
        box____.show_all()
        previous_track.add(box____)

        media_submenu.append(pause_play)
        media_submenu.append(reset)
        media_submenu.append(fast_forward)
        media_submenu.append(backward)
        media_submenu.append(next_track)
        media_submenu.append(previous_track)

        self.media_item.set_submenu(media_submenu)


    def application_menu(self):
        app_submenu = Gtk.Menu()
        self.app_menu_item = Gtk.MenuItem()
        self.app_menu_item.set_submenu(app_submenu)


        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/app.png', 20, 20)
        app_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        app_label = Gtk.Label(label="Applications")


        box.pack_start(app_icon, False, False, 0)
        box.pack_start(app_label, False, False, 0)
        box.show_all()
        self.app_menu_item.add(box)

        apps = get_app_info()
        for name, exec, icon in apps:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
                scaled_pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.BILINEAR)
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

    def power_menu(self):
        self.power_item = Gtk.MenuItem()
        power_submenu = Gtk.Menu()
        self.power_item.set_submenu(power_submenu)


        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/power.png', 20, 20)
        app_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        app_label = Gtk.Label(label="Power Settings")


        box.pack_start(app_icon, False, False, 0)
        box.pack_start(app_label, False, False, 0)
        box.show_all()
        self.power_item.add(box)


        power_off = Gtk.MenuItem()
        power_off.connect('activate', shutdown_machine)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/power_off.png', 20, 20)
        power_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        power_label = Gtk.Label(label = "Power Off")


        box.pack_start(power_icon, False, False, 0)
        box.pack_start(power_label, False, False, 0)
        box.show_all()
        power_off.add(box)

        reboot = Gtk.MenuItem()
        reboot.connect('activate', reboot_machine)


        box_ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/reboot.png', 20, 20)
        reboot_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        reboot_label = Gtk.Label(label = "Reboot")


        box_.pack_start(reboot_icon, False, False, 0)
        box_.pack_start(reboot_label, False, False, 0)
        box_.show_all()
        reboot.add(box_)


        lock = Gtk.MenuItem()
        lock.connect('activate', lock_machine)


        box__ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/lock.png', 20, 20)
        lock_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        lock_label = Gtk.Label(label = "Lock")


        box__.pack_start(lock_icon, False, False, 0)
        box__.pack_start(lock_label, False, False, 0)
        box__.show_all()
        lock.add(box__)

        hib = Gtk.MenuItem()
        hib.connect('activate', hib_machine)

        box___ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/hibernate.png', 20, 20)
        hib_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        hib_label = Gtk.Label(label = "Hibernate")


        box___.pack_start(hib_icon, False, False, 0)
        box___.pack_start(hib_label, False, False, 0)
        box___.show_all()
        hib.add(box___)

        power_submenu.append(power_off)
        power_submenu.append(reboot)
        power_submenu.append(lock)
        power_submenu.append(hib)


        self.power_item.set_submenu(power_submenu)


    def system_info_menu(self):
        self.system_item = Gtk.MenuItem()
        system_submenu = Gtk.Menu()
        self.system_item.set_submenu(system_submenu)


        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/info.png', 20, 20)
        app_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        app_label = Gtk.Label(label="Hardware Info")


        box.pack_start(app_icon, False, False, 0)
        box.pack_start(app_label, False, False, 0)
        box.show_all()
        self.system_item.add(box)

        cpu_item = Gtk.MenuItem()
        cpu_item.set_sensitive(False)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/cpu.png', 20, 20)
        cpu_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        cpu_label = Gtk.Label(label="CPU: ")


        box.pack_start(cpu_icon, False, False, 0)
        box.pack_start(cpu_label, False, False, 0)
        box.show_all()
        cpu_item.add(box)
        
        cpu_name = Gtk.MenuItem()
        cpu_name.set_sensitive(False)
        cpu_name.set_label(f"CPU Name: {get_cpu_info()}")
        
        self.cpu_temp = Gtk.MenuItem()
        self.cpu_temp.set_sensitive(False)
        
        self.cpu_usage = Gtk.MenuItem()
        self.cpu_usage.set_sensitive(False)


        ram_item = Gtk.MenuItem()
        ram_item.set_sensitive(False)

        box_ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/ram.png', 20, 20)
        ram_icon = Gtk.Image.new_from_pixbuf(pixbuf)

        ram_label = Gtk.Label(label="RAM: ")


        box_.pack_start(ram_icon, False, False, 0)
        box_.pack_start(ram_label, False, False, 0)
        box_.show_all()
        ram_item.add(box_)

        self.ram_usage = Gtk.MenuItem()
        self.ram_usage.set_sensitive(False)
        
        self.used_ram = Gtk.MenuItem()
        self.used_ram.set_sensitive(False)

        check = check_gpu()

        if check != '':

            gpu_item = Gtk.MenuItem()
            gpu_item.set_sensitive(False)

            box__ = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('app_images/gpu.png', 20, 20)
            gpu_icon = Gtk.Image.new_from_pixbuf(pixbuf)

            gpu_label = Gtk.Label(label = "GPU: ")


            box__.pack_start(gpu_icon, False, False, 0)
            box__.pack_start(gpu_label, False, False, 0)
            box__.show_all()
            gpu_item.add(box__)


            gpu_name = Gtk.MenuItem(label=f"GPU Name: {get_nvidia_name()}")
            gpu_name.set_sensitive(False)
            
            self.gpu_temp = Gtk.MenuItem()
            self.gpu_temp.set_sensitive(False)

            self.gpu_usage = Gtk.MenuItem()
            self.gpu_usage.set_sensitive(False)
            
            self.gpu_vram = Gtk.MenuItem()
            self.gpu_vram.set_sensitive(False)


            self.gpu_speed = Gtk.MenuItem()
            self.gpu_speed.set_sensitive(False)

            self.gpu_power = Gtk.MenuItem()
            self.gpu_power.set_sensitive(False)


        system_submenu.append(cpu_item)
        system_submenu.append(cpu_name)
        system_submenu.append(self.cpu_temp)
        system_submenu.append(self.cpu_usage)
        system_submenu.append(Gtk.SeparatorMenuItem())
        system_submenu.append(ram_item)
        system_submenu.append(self.ram_usage)
        system_submenu.append(self.used_ram)
        if check != '':
            system_submenu.append(Gtk.SeparatorMenuItem())
            system_submenu.append(gpu_item)
            system_submenu.append(gpu_name)
            system_submenu.append(self.gpu_temp)
            system_submenu.append(self.gpu_usage)
            system_submenu.append(self.gpu_vram)
            system_submenu.append(self.gpu_speed)
            system_submenu.append(self.gpu_power)


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