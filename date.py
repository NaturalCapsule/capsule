import calendar
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class RoundedCalendarLabel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        
        self.apply_css()
        
        self.create_calendar()
        
    def apply_css(self):
        css_provider = Gtk.CssProvider()
        with open ('config/style.css', 'r') as f:
            css = f.read()
        css_provider.load_from_data(css.encode())
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
    def create_calendar(self):
        today = datetime.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day
        
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_halign(Gtk.Align.CENTER)
        header_label = Gtk.Label(label=f"{calendar.month_name[current_month]} {current_year}")
        header_label.get_style_context().add_class("month-header")
        header_box.pack_start(header_label, False, False, 0)
        self.pack_start(header_box, False, False, 0)
        
        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        weekday_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        weekday_box.set_halign(Gtk.Align.CENTER)
        for day in weekdays:
            label = Gtk.Label(label=day)
            label.get_style_context().add_class("weekday-header")
            label.set_size_request(30, -1)
            weekday_box.pack_start(label, False, False, 0)
        self.pack_start(weekday_box, False, False, 0)
        
        first_day_of_month = datetime(current_year, current_month, 1)
        first_weekday = first_day_of_month.weekday()
        first_weekday = (first_weekday + 1) % 7
        days_in_month = (datetime(current_year, current_month + 1, 1) - first_day_of_month).days
        
        day_counter = 1
        for week in range(6):
            week_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            week_box.set_halign(Gtk.Align.CENTER)
            
            for day_of_week in range(7):
                if week == 0 and day_of_week < first_weekday:
                    label = Gtk.Label()
                    label.set_size_request(30, 25)
                elif day_counter <= days_in_month:
                    label = Gtk.Label(label=str(day_counter))
                    label.set_size_request(30, 25)
                    
                    if day_counter == current_day:
                        label.get_style_context().add_class("current-day")
                    else:
                        label.get_style_context().add_class("calendar-day")
                    
                    day_counter += 1
                else:
                    label = Gtk.Label()
                    label.set_size_request(30, 25)
                
                week_box.pack_start(label, False, False, 0)
            
            self.pack_start(week_box, False, False, 0)
            
            if day_counter > days_in_month:
                break
    
    def update_calendar(self):
        for child in self.get_children():
            self.remove(child)
        
        self.create_calendar()
        self.show_all()
        return True