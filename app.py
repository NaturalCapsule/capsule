import gi
import config

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from timers import RunTimers, update_media_
from media import MediaPlayerMonitor

from actions import *
from sys_info import *

from app_info import get_app_info


class App(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.POPUP)
        self.config = config
        
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_decorated(False)
        self.set_resizable(False)
        if self.config.use_blur:
            self.set_app_paintable(True)
        self.get_style_context().add_class("window")
        
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        self.title_label = Gtk.Label()
        self.title_label.get_style_context().add_class("Media-Title")
        
        self.media_image = Gtk.Image()
        self.media_image.get_style_context().add_class("Media-Image")

        self.cpu_temp = Gtk.Label(label="CPU Temperature: Updating...")
        self.cpu_temp.get_style_context().add_class('sysInfo')

        self.cpu_usage = Gtk.Label(label="CPU Usage: Updating...")
        self.cpu_usage.get_style_context().add_class('sysInfo')

        self.ram_usage = Gtk.Label(label="RAM Usage: Updating...")
        self.ram_usage.get_style_context().add_class('sysInfo')
        
        self.used_ram = Gtk.Label(label="Used RAM: Updating...")
        self.used_ram.get_style_context().add_class('sysInfo')
        
        self.gpu_temp = Gtk.Label(label="GPU Temperature: Updating...")
        self.gpu_temp.get_style_context().add_class('sysInfo')

        self.gpu_usage = Gtk.Label(label="GPU Usage: Updating...")
        self.gpu_usage.get_style_context().add_class('sysInfo')

        self.gpu_vram = Gtk.Label(label="GPU VRAM: Updating...")
        self.gpu_vram.get_style_context().add_class('sysInfo')

        self.gpu_speed = Gtk.Label(label="GPU Speed: Updating...")
        self.gpu_speed.get_style_context().add_class('sysInfo')

        self.gpu_power = Gtk.Label(label="GPU Power: Updating...")
        self.gpu_power.get_style_context().add_class('sysInfo')
        
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.main_box)
        
        self.open_submenus = {}
        self.menu_items = []
        self.current_selected_index = 0
        self.active_submenu = None

        self.build_menu()
        self.connect("key-press-event", self.on_key_press)
        
        RunTimers(self.cpu_temp, self.cpu_usage, self.ram_usage, self.used_ram, 
                  self.gpu_temp, self.gpu_usage, self.gpu_vram, self.gpu_speed, 
                  self.gpu_power)
        
        update_media_(self.title_label, self.media_image)
        
        # if self.menu_items:
        #     self.select_menu_item(0)
            
        self.show_all()

    def on_focus_out(self, widget, event):
        self.destroy()
        Gtk.main_quit()
        return False
        
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            if self.open_submenus:
                for submenu_id in list(self.open_submenus.keys()):
                    self.open_submenus[submenu_id].destroy()
                    try:
                        del self.open_submenus[submenu_id]
                    except KeyError:
                        pass
                self.active_submenu = None
                return True
            else:
                self.destroy()
                Gtk.main_quit()
                return True
        elif event.keyval == Gdk.KEY_Up:
            if self.active_submenu and hasattr(self.active_submenu, 'navigate'):
                self.active_submenu.navigate('up')
            else:
                if self.current_selected_index > 0:
                    self.select_menu_item(self.current_selected_index - 1)
            return True
        elif event.keyval == Gdk.KEY_Down:
            if self.active_submenu and hasattr(self.active_submenu, 'navigate'):
                self.active_submenu.navigate('down')
            else:
                if self.current_selected_index < len(self.menu_items) - 1:
                    self.select_menu_item(self.current_selected_index + 1)
            return True
        elif event.keyval == Gdk.KEY_Left:
            if self.active_submenu:
                for submenu_id in list(self.open_submenus.keys()):
                    self.open_submenus[submenu_id].destroy()
                    try:
                        del self.open_submenus[submenu_id]
                    except KeyError:
                        pass
                self.active_submenu = None
                return True
        elif event.keyval == Gdk.KEY_Right:
            if not self.active_submenu and self.current_selected_index < len(self.menu_items):
                item = self.menu_items[self.current_selected_index]
                if hasattr(item, 'submenu_func') and item.submenu_func:
                    menu_id = item.menu_id
                    self.toggle_submenu(item.submenu_func, item, menu_id)
                    return True
        elif event.keyval == Gdk.KEY_Return:
            if self.active_submenu and hasattr(self.active_submenu, 'activate_selected'):
                self.active_submenu.activate_selected()
            elif self.current_selected_index < len(self.menu_items):
                item = self.menu_items[self.current_selected_index]
                if hasattr(item, 'click_handler'):
                    item.click_handler(item, None)
                elif hasattr(item, 'submenu_func') and item.submenu_func:
                    menu_id = item.menu_id
                    self.toggle_submenu(item.submenu_func, item, menu_id)
                    return True
        return False
        
    def select_menu_item(self, index):
        if 0 <= self.current_selected_index < len(self.menu_items):
            self.menu_items[self.current_selected_index].get_style_context().remove_class("menu-item-hover")
            self.menu_items[self.current_selected_index].unset_state_flags(Gtk.StateFlags.PRELIGHT)
        self.current_selected_index = index
        if 0 <= index < len(self.menu_items):
            self.menu_items[index].get_style_context().add_class("menu-item-hover")
            self.menu_items[index].set_state_flags(Gtk.StateFlags.PRELIGHT, True)

    def build_menu(self):
        self.media_box = self.create_menu_item("Media Control", "app_images/music.png")
        self.terminal_box = self.create_menu_item("Terminal", "app_images/terminal.png")
        self.exit_box = self.create_menu_item("Exit", "app_images/exit.png")
        self.file_manager_box = self.create_menu_item("Open File Manager", "app_images/folder.png")
        self.app_box = self.create_menu_item("Applications", "app_images/app.png")
        self.power_box = self.create_menu_item("Power Settings", "app_images/power.png")
        self.system_box = self.create_menu_item("Hardware Info", "app_images/info.png")
        
        self.media_submenu = self.build_media_control_menu()
        self.media_box.submenu_func = self.media_submenu
        self.media_box.menu_id = "media"
        
        self.terminal_box.click_handler = self.on_terminal_click
        self.terminal_box.connect("button-press-event", self.on_terminal_click)
        
        self.exit_box.click_handler = self.on_exit_click
        self.exit_box.connect("button-press-event", self.on_exit_click)
        
        self.file_manager_box.click_handler = self.on_fileM_click
        self.file_manager_box.connect("button-press-event", self.on_fileM_click)
        
        self.app_submenu = self.build_application_menu()
        self.app_box.submenu_func = self.app_submenu
        self.app_box.menu_id = "app"
        
        self.power_submenu = self.build_power_menu()
        self.power_box.submenu_func = self.power_submenu
        self.power_box.menu_id = "power"
        
        self.system_submenu = self.build_system_info_menu()
        self.system_box.submenu_func = self.system_submenu
        self.system_box.menu_id = "system"
        
        self.media_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.media_submenu, w, "media"))
        self.app_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.app_submenu, w, "app"))
        self.power_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.power_submenu, w, "power"))
        self.system_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.system_submenu, w, "system"))
        
        self.menu_items = [
            self.media_box,
            self.app_box,
            self.system_box,
            self.power_box,
            self.terminal_box,
            self.file_manager_box,
            self.exit_box
        ]
        
        self.main_box.pack_start(self.media_box, False, False, 0)
        self.main_box.pack_start(self.app_box, False, False, 0)
        self.main_box.pack_start(self.system_box, False, False, 0)
        self.main_box.pack_start(self.power_box, False, False, 0)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(separator, False, False, 4)
        
        self.main_box.pack_start(self.terminal_box, False, False, 0)
        self.main_box.pack_start(self.file_manager_box, False, False, 0)
        self.main_box.pack_start(self.exit_box, False, False, 0)

    def create_menu_item(self, label_text, icon_path):
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
        
        box.connect("enter-notify-event", self.on_hover_enter)
        box.connect("leave-notify-event", self.on_hover_leave)
        
        return box
    
    def on_hover_enter(self, widget, event):
        widget.get_style_context().add_class("menu-item-hover")
        widget.set_state_flags(Gtk.StateFlags.PRELIGHT, True)
        if widget in self.menu_items:
            self.current_selected_index = self.menu_items.index(widget)
        return False
        
    def on_hover_leave(self, widget, event):
        widget.get_style_context().remove_class("menu-item-hover")
        widget.unset_state_flags(Gtk.StateFlags.PRELIGHT)
        return False
        
    def on_terminal_click(self, widget, event):
        if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
            open_terminal(widget, self.config.terminal)
            self.destroy()
            Gtk.main_quit()

    def on_exit_click(self, widget, event):
        if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
            exit_(widget)
            self.destroy()
            Gtk.main_quit()

    def on_fileM_click(self, widget, event):
        if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
            open_fileM(widget, self.config.file_manager)
            self.destroy()
            Gtk.main_quit()

    def build_submenu_window(self, title):
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
        
        # window.connect("focus-out-event", lambda w, e: w.destroy())
        window.connect("key-press-event", lambda w, e: w.destroy() if e.keyval == Gdk.KEY_Escape else None)
        
        return window, vbox
    
    def toggle_submenu(self, submenu_func, parent_widget, menu_id):
        if menu_id in self.open_submenus and self.open_submenus[menu_id].get_visible():
            self.open_submenus[menu_id].destroy()
            try:
                del self.open_submenus[menu_id]
            except KeyError:
                pass
            self.active_submenu = None
        else:
            for id_key in list(self.open_submenus.keys()):
                if self.open_submenus[id_key] and self.open_submenus[id_key].get_visible():
                    self.open_submenus[id_key].destroy()
                    try:
                        del self.open_submenus[id_key]
                    except KeyError:
                        pass
                    
            self.show_submenu(submenu_func, parent_widget, menu_id)
        
    def show_submenu(self, submenu_func, parent_widget, menu_id):
        window_x, window_y = self.get_position()
        parent_alloc = parent_widget.get_allocation()
        
        x = window_x + parent_alloc.width
        y = window_y + parent_alloc.y
        
        submenu = submenu_func()
        submenu.move(x, y)
        
        self.open_submenus[menu_id] = submenu
        self.active_submenu = submenu
        
        submenu.connect("destroy", lambda w: self.on_submenu_destroyed(menu_id))
        
        submenu.connect("key-press-event", self.on_key_press)
        
        submenu.show_all()
    
    def on_submenu_destroyed(self, menu_id):
        if menu_id in self.open_submenus:
            del self.open_submenus[menu_id]
            self.active_submenu = None
            
    def build_media_control_menu(self):
        def create_submenu():
            window, vbox = self.build_submenu_window("Media Control")

            text = '▶'
            media = MediaPlayerMonitor()
            if media.playback_status == 'Paused':
                text = '▶'
            elif media.playback_status == 'Playing':
                text = '❚❚'
            
            items = [
                ("⏮", None, backward_func),
                (text, None, pause_play_func),
                ("⏭", None, fast_forward_func),
                ("<<", None, previous_track_func),
                ("↺", None, reset_func),
                (">>", None, next_track_func),
            ]
            
            self.title_label.set_margin_start(20)
            self.title_label.set_margin_end(20)
            self.title_label.set_xalign(0)

            grid = Gtk.Grid()
            
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            vbox.pack_start(hbox, False, False, 0)
            
            hbox.pack_start(self.media_image, False, False, 10)
            hbox.pack_start(self.title_label, False, False, 0)
            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            vbox.pack_start(separator, False, False, 0)
            
            window.submenu_items = []
            
            window.current_selected_index = 0
            
            column = 0
            row = 0
            count = 0
            
            vbox.pack_start(grid, False, False, 0)
            
            for label_text, icon_path, action_func in items:
                item = self.create_submenu_item(label_text, icon_path)
                item.action_func = action_func
                item.connect("button-press-event", lambda w, e, f=action_func: self.on_submenu_item_click(w, e, f))
                if count == 3:
                    column += 1
                    row = 0
                grid.attach(item, row, column, 1, 1)
                row += 1
                count += 1
                window.submenu_items.append(item)
                
            def navigate(direction):
                if direction == 'up' and window.current_selected_index > 0:
                    select_item(window.current_selected_index - 1)
                elif direction == 'down' and window.current_selected_index < len(window.submenu_items) - 1:
                    select_item(window.current_selected_index + 1)
                    
            def select_item(index):
                if 0 <= window.current_selected_index < len(window.submenu_items):
                    window.submenu_items[window.current_selected_index].get_style_context().remove_class("menu-item-hover")
                    window.submenu_items[window.current_selected_index].unset_state_flags(Gtk.StateFlags.PRELIGHT)
                
                window.current_selected_index = index
                if 0 <= index < len(window.submenu_items):
                    window.submenu_items[index].get_style_context().add_class("menu-item-hover")
                    window.submenu_items[index].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
                    
            def activate_selected():
                if 0 <= window.current_selected_index < len(window.submenu_items):
                    item = window.submenu_items[window.current_selected_index]
                    if hasattr(item, 'action_func'):
                        item.action_func(item)
                        window.destroy()
                        for w in Gtk.Window.list_toplevels():
                            w.destroy()
                        Gtk.main_quit()
            
            window.navigate = navigate
            window.activate_selected = activate_selected
            
            # if window.submenu_items:
            #     select_item(0)
                
            return window
            
        return create_submenu
        
    def build_application_menu(self):
        def create_submenu():
            window, vbox = self.build_submenu_window("Applications")
            
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.get_style_context().add_class("Scroll-Window")
            scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scrolled_window.set_min_content_height(300)
            scrolled_window.set_max_content_height(500)
            scrolled_window.set_propagate_natural_height(True)
            
            apps_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            scrolled_window.add(apps_box)
            
            window.submenu_items = []
            window.current_selected_index = 0
            
            apps = get_app_info()
            for name, exec_cmd, icon in apps:
                item = self.create_submenu_item(name, icon, use_theme_icon=True)
                item.exec_cmd = exec_cmd
                item.connect("button-press-event", lambda w, e, cmd=exec_cmd: self.on_submenu_item_click(w, e, lambda w: launch_app(w, cmd)))
                apps_box.pack_start(item, False, False, 0)
                window.submenu_items.append(item)
            
            vbox.pack_start(scrolled_window, True, True, 0)
            
            def navigate(direction):
                if direction == 'up' and window.current_selected_index > 0:
                    select_item(window.current_selected_index - 1)
                elif direction == 'down' and window.current_selected_index < len(window.submenu_items) - 1:
                    select_item(window.current_selected_index + 1)
                    
            def select_item(index):
                if 0 <= window.current_selected_index < len(window.submenu_items):
                    window.submenu_items[window.current_selected_index].get_style_context().remove_class("menu-item-hover")
                    window.submenu_items[window.current_selected_index].unset_state_flags(Gtk.StateFlags.PRELIGHT)
                
                window.current_selected_index = index
                if 0 <= index < len(window.submenu_items):
                    window.submenu_items[index].get_style_context().add_class("menu-item-hover")
                    window.submenu_items[index].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
                    adjustment = scrolled_window.get_vadjustment()
                    item_allocation = window.submenu_items[index].get_allocation()
                    if item_allocation.y < adjustment.get_value():
                        adjustment.set_value(item_allocation.y)
                    elif (item_allocation.y + item_allocation.height) > (adjustment.get_value() + adjustment.get_page_size()):
                        adjustment.set_value(item_allocation.y + item_allocation.height - adjustment.get_page_size())
                    
            def activate_selected():
                if 0 <= window.current_selected_index < len(window.submenu_items):
                    item = window.submenu_items[window.current_selected_index]
                    if hasattr(item, 'exec_cmd'):
                        launch_app(item, item.exec_cmd)
                        window.destroy()
                        for w in Gtk.Window.list_toplevels():
                            w.destroy()
                        Gtk.main_quit()
            
            window.navigate = navigate
            window.activate_selected = activate_selected
            
            # if window.submenu_items:
            #     select_item(0)
                
            return window
            
        return create_submenu
        
    def build_power_menu(self):
        def create_submenu():
            window, vbox = self.build_submenu_window("Power Settings")
            
            items = [
                ("Power Off         ⏻", None, shutdown_machine),
                ("Reboot               ⟳", None, reboot_machine),
                ("Lock                    🗝", None, lock_machine),
                ("Hibernate        ❄", None, hib_machine)
            ]
            
            window.submenu_items = []
            window.current_selected_index = 0
            
            for label_text, icon_path, action_func in items:
                item = self.create_submenu_item(label_text, icon_path)
                item.action_func = action_func
                item.connect("button-press-event", lambda w, e, f=action_func: self.on_submenu_item_click(w, e, f))
                vbox.pack_start(item, False, False, 0)
                window.submenu_items.append(item)
                
            def navigate(direction):
                if direction == 'up' and window.current_selected_index > 0:
                    select_item(window.current_selected_index - 1)
                elif direction == 'down' and window.current_selected_index < len(window.submenu_items) - 1:
                    select_item(window.current_selected_index + 1)
                    
            def select_item(index):
                if 0 <= window.current_selected_index < len(window.submenu_items):
                    window.submenu_items[window.current_selected_index].get_style_context().remove_class("menu-item-hover")
                    window.submenu_items[window.current_selected_index].unset_state_flags(Gtk.StateFlags.PRELIGHT)
                
                window.current_selected_index = index
                if 0 <= index < len(window.submenu_items):
                    window.submenu_items[index].get_style_context().add_class("menu-item-hover")
                    window.submenu_items[index].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
                    
            def activate_selected():
                if 0 <= window.current_selected_index < len(window.submenu_items):
                    item = window.submenu_items[window.current_selected_index]
                    if hasattr(item, 'action_func'):
                        item.action_func(item)
                        window.destroy()
                        for w in Gtk.Window.list_toplevels():
                            w.destroy()
                        Gtk.main_quit()
            
            window.navigate = navigate
            window.activate_selected = activate_selected
            
            # if window.submenu_items:
            #     select_item(0)
                
            return window
            
        return create_submenu
        
    def build_system_info_menu(self):
        def create_submenu():
            window, vbox = self.build_submenu_window("Hardware Info")
            
            cpu_header = self.create_info_header("CPU", "app_images/cpu.png")
            cpu_header.get_style_context().add_class('sysInfo')

            vbox.pack_start(cpu_header, False, False, 0)
            
            cpu_name = self.create_info_item(f"CPU Name: {get_cpu_info()}")
            cpu_name.get_style_context().add_class('sysInfo')
            
            vbox.pack_start(cpu_name, False, False, 0)
            
            vbox.pack_start(self.cpu_temp, False, False, 0)
            self.cpu_temp.set_margin_start(20)
            self.cpu_temp.set_xalign(0)
            
            vbox.pack_start(self.cpu_usage, False, False, 0)
            self.cpu_usage.set_margin_start(20)
            self.cpu_usage.set_xalign(0)
            
            separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            vbox.pack_start(separator1, False, False, 4)
            
            ram_header = self.create_info_header("RAM", "app_images/ram.png")
            ram_header.get_style_context().add_class('sysInfo')

            vbox.pack_start(ram_header, False, False, 0)
            
            vbox.pack_start(self.ram_usage, False, False, 0)
            self.ram_usage.set_margin_start(20)
            self.ram_usage.set_xalign(0)
            
            vbox.pack_start(self.used_ram, False, False, 0)
            self.used_ram.set_margin_start(20)
            self.used_ram.set_xalign(0)
            
            check = check_gpu()
            if check != '':
                separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                vbox.pack_start(separator2, False, False, 4)
                
                gpu_header = self.create_info_header("GPU", "app_images/gpu.png")
                gpu_header.get_style_context().add_class('sysInfo')

                vbox.pack_start(gpu_header, False, False, 0)
                
                gpu_name = self.create_info_item(f"GPU Name: {get_nvidia_name()}")
                gpu_name.get_style_context().add_class('sysInfo')
                
                vbox.pack_start(gpu_name, False, False, 0)
                
                vbox.pack_start(self.gpu_temp, False, False, 0)
                self.gpu_temp.set_margin_start(20)
                self.gpu_temp.set_xalign(0)
                
                vbox.pack_start(self.gpu_usage, False, False, 0)
                self.gpu_usage.set_margin_start(20)
                self.gpu_usage.set_xalign(0)
                
                vbox.pack_start(self.gpu_vram, False, False, 0)
                self.gpu_vram.set_margin_start(20)
                self.gpu_vram.set_xalign(0)
                
                vbox.pack_start(self.gpu_speed, False, False, 0)
                self.gpu_speed.set_margin_start(20)
                self.gpu_speed.set_xalign(0)
                
                vbox.pack_start(self.gpu_power, False, False, 0)
                self.gpu_power.set_margin_start(20)
                self.gpu_power.set_xalign(0)
                
            window.navigate = lambda direction: None
            window.activate_selected = lambda: None
                
            return window
            
        return create_submenu
        
        
    def create_submenu_item(self, label_text, icon_path=None, use_theme_icon=False):
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
        
        box.connect("enter-notify-event", self.on_submenu_hover_enter)
        box.connect("leave-notify-event", self.on_submenu_hover_leave)
        
        return box
    
    def on_submenu_hover_enter(self, widget, event):
        widget.get_style_context().add_class("menu-item-hover")
        widget.set_state_flags(Gtk.StateFlags.PRELIGHT, True)
        
        if self.active_submenu and hasattr(self.active_submenu, 'submenu_items'):
            if widget in self.active_submenu.submenu_items:
                self.active_submenu.current_selected_index = self.active_submenu.submenu_items.index(widget)
        
        return False
        
    def on_submenu_hover_leave(self, widget, event):
        widget.get_style_context().remove_class("menu-item-hover")
        widget.unset_state_flags(Gtk.StateFlags.PRELIGHT)
        return False
        
    def create_info_header(self, text, icon_path):
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
        
    def create_info_item(self, text):
        label = Gtk.Label(label=text)
        label.set_xalign(0)
        label.set_margin_start(20)
        
        return label
        
    def on_submenu_item_click(self, widget, event, callback):
        if event is None or event.type == Gdk.EventType.BUTTON_PRESS:
            callback(widget)
            for window in Gtk.Window.list_toplevels():
                window.destroy()
            Gtk.main_quit()


def show_menu():
    css_provider = Gtk.CssProvider()
    with open ('config/style.css', 'r') as f:
        css = f.read()
    css_provider.load_from_data(css.encode())
    
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    
    app = App()
    Gtk.main()

show_menu()