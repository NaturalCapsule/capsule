import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import threading
from sys_info import *

class RunTimers:
    def __init__(self, cpu_temp, cpu_usage, ram_usage, used_ram, gpu_temp=None, 
                 gpu_usage=None, gpu_vram=None, gpu_speed=None, gpu_power=None):
        self.cpu_temp = cpu_temp
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.used_ram = used_ram
        self.gpu_temp = gpu_temp
        self.gpu_usage = gpu_usage
        self.gpu_vram = gpu_vram
        self.gpu_speed = gpu_speed
        self.gpu_power = gpu_power
        
        self.prev_values = {}
        
        GLib.timeout_add(2000, self.update_all_stats)
    
    def update_all_stats(self):
        thread = threading.Thread(target=self.collect_info)
        thread.daemon = True
        thread.start()
        return True
    
    def collect_info(self):
        cpu_temp_val = get_cpu_temp()
        cpu_usage_val = get_cpu_usage()
        ram_usage_val = get_ram_usage()
        used_ram_val = get_used_ram()
        
        if hasattr(self, 'gpu_temp') and self.gpu_temp is not None:
            gpu_temp_val = get_nvidia_temp()
            gpu_usage_val = get_nvidia_gpu_usage()
            gpu_vram_val = get_nvidia_used_vram()
            gpu_speed_val = get_nvidia_fanspeed()
            gpu_power_val = get_nvidia_powerdraw()
        else:
            gpu_temp_val = gpu_usage_val = gpu_vram_val = gpu_speed_val = gpu_power_val = None
        
        GLib.idle_add(self.update_ui, 
                     cpu_temp_val, cpu_usage_val, ram_usage_val, used_ram_val,
                     gpu_temp_val, gpu_usage_val, gpu_vram_val, gpu_speed_val, gpu_power_val)
    
    def update_ui(self, cpu_temp_val, cpu_usage_val, ram_usage_val, used_ram_val,
                 gpu_temp_val, gpu_usage_val, gpu_vram_val, gpu_speed_val, gpu_power_val):
        if self.should_update('cpu_temp', cpu_temp_val, 2):
            self.cpu_temp.set_label(f"CPU Temperature: {cpu_temp_val}°C")
        
        if self.should_update('cpu_usage', cpu_usage_val, 0.01):
            self.cpu_usage.set_label(f"CPU Usage: {cpu_usage_val}%")
        
        if self.should_update('ram_usage', ram_usage_val, 0.01):
            self.ram_usage.set_label(f"RAM Usage: {ram_usage_val}%")
        
        if self.should_update('used_ram', used_ram_val, 0.01):
            self.used_ram.set_label(f"Used RAM: {used_ram_val}GB")
        
        if self.gpu_temp is not None:
            if self.should_update('gpu_temp', gpu_temp_val, 2):
                self.gpu_temp.set_label(f"GPU Temperature: {gpu_temp_val}°C")
            
            if self.should_update('gpu_usage', gpu_usage_val, 1):
                self.gpu_usage.set_label(f"GPU Usage: {gpu_usage_val}%")
            
            if self.should_update('gpu_vram', gpu_vram_val, 0.01):
                self.gpu_vram.set_label(f"GPU VRAM: {gpu_vram_val}MB/{get_nvidia_total_vram()}GB")
            
            if self.should_update('gpu_speed', gpu_speed_val, 2):
                self.gpu_speed.set_label(f"GPU Fan Speed: {gpu_speed_val} RPM")
            
            if self.should_update('gpu_power', gpu_power_val, 3):
                self.gpu_power.set_label(f"GPU Power: {gpu_power_val}")
        
        return False
    
    def should_update(self, key, new_value, threshold):
        if key not in self.prev_values:
            self.prev_values[key] = new_value
            return True
        
        try:
            if abs(float(new_value) - float(self.prev_values[key])) >= threshold:
                self.prev_values[key] = new_value
                return True
        except (ValueError, TypeError):
            if new_value != self.prev_values[key]:
                self.prev_values[key] = new_value
                return True
        
        return False