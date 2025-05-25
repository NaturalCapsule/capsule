import gi
import config
import widgets
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk
from timers import RunTimers, update_media_, update_time_, update_date_
from media import MediaPlayerMonitor

from actions import *
from sys_info import *
from items import *
from clicks import *
from effects import *


from app_info import get_app_info


class Capsule(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.POPUP)
        self.config = config
        self.apps_ = {}

        
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

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.main_box)
        
        self.open_submenus = {}
        self.menu_items = []
        self.current_selected_index = 0
        self.active_submenu = None


        self.build_menu()
        self.connect("key-press-event", self.on_key_press)
        
        RunTimers(widgets.cpu_temp, widgets.cpu_usage, widgets.ram_usage, widgets.used_ram, 
                  widgets.gpu_temp, widgets.gpu_usage, widgets.gpu_vram, widgets.gpu_speed, 
                  widgets.gpu_power)
        
        
        
        update_media_(widgets.title_label, widgets.media_image)
        update_time_(widgets.time_label)
        # update_date_(widgets.rounded_calendar)
        
            
        self.show_all()

    def on_focus_out(self, widget, event):
        self.destroy()
        Gtk.main_quit()
        return False

    def on_key_press_(self, widget, event):
        key = Gdk.keyval_name(event.keyval)

        # children = self.listbox.get_children()
        # if not children:
        #     return

        # current_row = self.listbox.get_focus_child()
        # if not current_row:
        #     current_row = children[0]

        # try:
        #     current_index = children.index(current_row)
        # except ValueError:
        #     current_index = 0

        if key == "Return":
            selected_row = widgets.listbox.get_selected_row()
            if selected_row:
                self.run_selected_program(selected_row)
            return True

        # if key == "j":
        #     new_index = (current_index - 1) % len(children)
        # elif key == "k":
        #     new_index = (current_index + 1) % len(children)
        # else:
        #     return

        # self.listbox.select_row(children[new_index])
        # children[new_index].grab_focus()

    def run_selected_program(self, row):
        event_box = row.get_child()
        box = event_box.get_child()

        try:
            label = box.get_children()[1]
            app_name = label.get_text()
        except IndexError:
            label = box.get_children()[0]
            app_name = label.get_text()

        print(f"Launching {app_name}...")
        launch_app(widget = None, exec=self.apps_.get(app_name))
        exit(0)


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

    def on_row_selected(self, listbox, row):
        for child in listbox.get_children():
            child.get_style_context().remove_class("App-List-selected-row")

        if row:
            row.get_style_context().add_class("App-List-selected-row")

    def on_search_changed(self, search_entry):
        widgets.listbox.invalidate_filter()

    def filter_func(self, row, data):
        
        if not row:
            return False

        event_box = row.get_child()
        if not event_box:
            return False

        hbox = event_box.get_child()
        if not hbox:
            return False

        label = None
        for child in hbox.get_children():
            if isinstance(child, Gtk.Label):
                label = child
                break

        if not label:
            return False

        query = widgets.search_entry.get_text().lower()
        return query in label.get_text().lower()

    def build_menu(self):
        self.media_box = create_menu_item("Media Control", "app_images/music.png", self.on_hover_enter, on_hover_leave)
        self.terminal_box = create_menu_item("Terminal", "app_images/terminal.png", self.on_hover_enter, on_hover_leave)
        self.exit_box = create_menu_item("Exit", "app_images/exit.png", self.on_hover_enter, on_hover_leave)
        self.file_manager_box = create_menu_item("Open File Manager", "app_images/folder.png", self.on_hover_enter, on_hover_leave)
        self.app_box = create_menu_item("Applications", "app_images/app.png", self.on_hover_enter, on_hover_leave)
        self.power_box = create_menu_item("Power Settings", "app_images/power.png", self.on_hover_enter, on_hover_leave)
        self.system_box = create_menu_item("Hardware Info", "app_images/info.png", self.on_hover_enter, on_hover_leave)
        self.timer_box = create_menu_item('Time & Date', 'app_images/clock.png', self.on_hover_enter, on_hover_leave)
        
        self.media_submenu = self.build_media_control_menu()
        self.media_box.submenu_func = self.media_submenu
        self.media_box.menu_id = "media"
        
        self.terminal_box.click_handler = lambda w, e, d=self.destroy, t=self.config.terminal: on_terminal_click(w, e, d, t)
        self.terminal_box.connect("button-press-event", lambda w, e, d = self.destroy, t = self.config.terminal: on_terminal_click(w, e, d, t))
        
        self.exit_box.click_handler = lambda w, e, a=self.destroy: on_exit_click(w, e, a)
        self.exit_box.connect("button-press-event", lambda w, e, a=self.destroy: on_exit_click(w, e, a))
        
        self.file_manager_box.click_handler = lambda w, e, d=self.destroy, m=self.config.file_manager: on_fileM_click(w, e, d, m)
        self.file_manager_box.connect("button-press-event", lambda w, e, d=self.destroy, m=self.config.file_manager: on_fileM_click(w, e, d, m))
        
        self.app_submenu = self.build_application_menu()
        self.app_box.submenu_func = self.app_submenu
        self.app_box.menu_id = "app"
        
        self.power_submenu = self.build_power_menu()
        self.power_box.submenu_func = self.power_submenu
        self.power_box.menu_id = "power"
        
        self.system_submenu = self.build_system_info_menu()
        self.system_box.submenu_func = self.system_submenu
        self.system_box.menu_id = "system"
        
        self.timer_submenu = self.build_time_menu()
        self.timer_box.submenu_func = self.timer_submenu
        self.timer_box.menu_id = "time"
        
        self.media_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.media_submenu, w, "media"))
        self.app_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.app_submenu, w, "app"))
        self.power_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.power_submenu, w, "power"))
        self.system_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.system_submenu, w, "system"))
        self.timer_box.connect("button-press-event", lambda w, e: self.toggle_submenu(self.timer_submenu, w, "time"))
        
        self.menu_items = [
            self.media_box,
            self.app_box,
            self.system_box,
            self.power_box,
            self.timer_box,
            self.terminal_box,
            self.file_manager_box,
            self.exit_box
        ]
        
        self.main_box.pack_start(self.media_box, False, False, 0)
        self.main_box.pack_start(self.app_box, False, False, 0)
        self.main_box.pack_start(self.system_box, False, False, 0)
        self.main_box.pack_start(self.power_box, False, False, 0)
        self.main_box.pack_start(self.timer_box, False, False, 0)
        
        self.main_box.pack_start(widgets.separator, False, False, 4)
        
        self.main_box.pack_start(self.terminal_box, False, False, 0)
        self.main_box.pack_start(self.file_manager_box, False, False, 0)
        self.main_box.pack_start(self.exit_box, False, False, 0)

    
    def on_hover_enter(self, widget, event):
        widget.get_style_context().add_class("menu-item-hover")
        widget.set_state_flags(Gtk.StateFlags.PRELIGHT, True)
        if widget in self.menu_items:
            self.current_selected_index = self.menu_items.index(widget)
        return False

    
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
            window, vbox = build_submenu_window("Media Control")

            text = '▶'
            media = MediaPlayerMonitor()
            if media.playback_status == 'Paused':
                text = '▶'
            elif media.playback_status == 'Playing':
                text = '❚❚'
            
            if text == '❚❚':
                reset = ' ↺'
            else:
                reset = '↺'
            
            items = [
                ("⏮", None, backward_func),
                (text, None, pause_play_func),
                ("⏭", None, fast_forward_func),
                ("<<", None, previous_track_func),
                (reset, None, reset_func),
                (">>", None, next_track_func),
            ]
            
            widgets.title_label.set_margin_start(20)
            widgets.title_label.set_margin_end(20)
            widgets.title_label.set_xalign(0)

            grid = Gtk.Grid()
            
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            vbox.pack_start(hbox, False, False, 0)
            
            hbox.pack_start(widgets.media_image, False, False, 10)
            hbox.pack_start(widgets.title_label, False, False, 0)
            vbox.pack_start(widgets.media_separator, False, False, 0)
            
            window.submenu_items = []
            
            window.current_selected_index = 0
            
            column = 0
            row = 0
            count = 0
            
            vbox.pack_start(grid, False, False, 0)
            
            for label_text, icon_path, action_func in items:
                item = create_submenu_item(label_text, icon_path, on_submenu_hover_enter=lambda w, e, a=self.active_submenu: on_submenu_hover_enter(w, e, a), on_submenu_hover_leave=on_submenu_hover_leave)
                item.action_func = action_func
                item.connect("button-press-event", lambda w, e, f=action_func: on_submenu_item_click(w, e, f))
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

            return window
            
        return create_submenu
        
        
    def build_application_menu(self):
        def create_submenu():
            window, vbox = build_submenu_window("Applications")
            
            widgets.listbox.connect("key-press-event", self.on_key_press_)
            widgets.search_entry.connect("changed", self.on_search_changed)
            widgets.search_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "view-app-grid-symbolic")
            
            widgets.listbox.set_filter_func(self.filter_func, None)
            widgets.listbox.connect("row-selected", self.on_row_selected)
            
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.get_style_context().add_class("Scroll-Window")
            scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scrolled_window.set_min_content_height(300)
            scrolled_window.set_max_content_height(500)
            scrolled_window.set_propagate_natural_height(True)
            
            
            window.submenu_items = []
            window.current_selected_index = 0
            
            
            scrolled_window.add(widgets.listbox)
            vbox.pack_start(widgets.search_entry, True, True, 0)
            vbox.pack_start(scrolled_window, True, True, 0)
            
            if not self.apps_:
                apps = get_app_info()
                for name, exec_cmd, icon in apps:
                    item = create_submenu_item(name, icon, use_theme_icon=True, on_submenu_hover_enter=lambda w, e, a=self.active_submenu: on_submenu_hover_enter(w, e, a), on_submenu_hover_leave=on_submenu_hover_leave)
                    item.exec_cmd = exec_cmd
                    item.connect("button-press-event", lambda w, e, cmd=exec_cmd: on_submenu_item_click(w, e, lambda w: launch_app(w, cmd)))
                    self.apps_[name] = exec_cmd
                    widgets.listbox.add(item)
                
            if self.config.show_app_info:
                info = Gtk.Label(label = 'Use Tab and Shift+Tab to navigate.')
                info.get_style_context().add_class('App-Info')
                vbox.pack_start(info, False, False, 0)
            
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
            
            return window
            
        return create_submenu
        
    def build_power_menu(self):
        def create_submenu():
            window, vbox = build_submenu_window("Power Settings")
            
            items = [
                ("Power Off         ⏻", None, shutdown_machine),
                ("Reboot               ⟳", None, reboot_machine),
                ("Lock                    🗝", None, lock_machine),
                ("Hibernate        ❄", None, hib_machine)
            ]
            
            window.submenu_items = []
            window.current_selected_index = 0
            
            for label_text, icon_path, action_func in items:
                item = create_submenu_item(label_text, icon_path, on_submenu_hover_enter=lambda w, e, a=self.active_submenu: on_submenu_hover_enter(w, e, a), on_submenu_hover_leave=on_submenu_hover_leave)
                item.action_func = action_func
                item.connect("button-press-event", lambda w, e, f=action_func: on_submenu_item_click(w, e, f))
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

                
            return window
            
        return create_submenu
        
    def build_system_info_menu(self):
        def create_submenu():
            window, vbox = build_submenu_window("Hardware Info")
            
            cpu_header = create_info_header("CPU", "app_images/cpu.png")
            cpu_header.get_style_context().add_class('sysInfo')

            vbox.pack_start(cpu_header, False, False, 0)
            
            cpu_name = create_info_item(f"CPU Name: {get_cpu_info()}")
            cpu_name.get_style_context().add_class('sysInfo')
            
            vbox.pack_start(cpu_name, False, False, 0)
            
            vbox.pack_start(widgets.cpu_temp, False, False, 0)
            widgets.cpu_temp.set_margin_start(20)
            widgets.cpu_temp.set_xalign(0)
            
            vbox.pack_start(widgets.cpu_usage, False, False, 0)
            widgets.cpu_usage.set_margin_start(20)
            widgets.cpu_usage.set_xalign(0)
            
            vbox.pack_start(widgets.sys_separator, False, False, 4)
            
            ram_header = create_info_header("RAM", "app_images/ram.png")
            ram_header.get_style_context().add_class('sysInfo')

            vbox.pack_start(ram_header, False, False, 0)
            
            vbox.pack_start(widgets.ram_usage, False, False, 0)
            widgets.ram_usage.set_margin_start(20)
            widgets.ram_usage.set_xalign(0)
            
            vbox.pack_start(widgets.used_ram, False, False, 0)
            widgets.used_ram.set_margin_start(20)
            widgets.used_ram.set_xalign(0)
            
            check = check_gpu()
            if check != '':
                vbox.pack_start(widgets.sys_separator_, False, False, 4)
                
                gpu_header = create_info_header("GPU", "app_images/gpu.png")
                gpu_header.get_style_context().add_class('sysInfo')

                vbox.pack_start(gpu_header, False, False, 0)
                
                gpu_name = create_info_item(f"GPU Name: {get_nvidia_name()}")
                gpu_name.get_style_context().add_class('sysInfo')
                
                vbox.pack_start(gpu_name, False, False, 0)
                
                vbox.pack_start(widgets.gpu_temp, False, False, 0)
                widgets.gpu_temp.set_margin_start(20)
                widgets.gpu_temp.set_xalign(0)
                
                vbox.pack_start(widgets.gpu_usage, False, False, 0)
                widgets.gpu_usage.set_margin_start(20)
                widgets.gpu_usage.set_xalign(0)
                
                vbox.pack_start(widgets.gpu_vram, False, False, 0)
                widgets.gpu_vram.set_margin_start(20)
                widgets.gpu_vram.set_xalign(0)
                
                vbox.pack_start(widgets.gpu_speed, False, False, 0)
                widgets.gpu_speed.set_margin_start(20)
                widgets.gpu_speed.set_xalign(0)
                
                vbox.pack_start(widgets.gpu_power, False, False, 0)
                widgets.gpu_power.set_margin_start(20)
                widgets.gpu_power.set_xalign(0)
                
            window.navigate = lambda direction: None
            window.activate_selected = lambda: None
                
            return window
            
        return create_submenu


    def build_time_menu(self):
        def create_submenu():
            window, vbox = build_submenu_window("Time & Date")
            vbox.pack_start(widgets.time_label, False, False, 0)
            vbox.pack_start(widgets.timer_separator, False, False, 0)
            # vbox.pack_start(widgets.date_label, False, False, 0)
            vbox.pack_start(widgets.rounded_calendar, False, False, 0)

            window.navigate = lambda direction: None
            window.activate_selected = lambda: None

            return window
        return create_submenu




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
    capsule = Capsule()
    Gtk.main()

show_menu()