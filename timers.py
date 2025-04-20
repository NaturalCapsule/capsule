import gi
gi.require_version('Gtk', '3.0')

from gi.repository import GLib
from updates import *

def RunTimers(cpu_temp, cpu_usage, ram_usage, ram_used, gpu_temp, gpu_usage, gpu_vram, gpu_speed, gpu_power):
    GLib.timeout_add(1000, update_cpu_temp, cpu_temp)
    GLib.timeout_add(1000, update_cpu_usage, cpu_usage)
    GLib.timeout_add(1000, update_ram_usage, ram_usage)
    GLib.timeout_add(1000, update_ram_used, ram_used)
    GLib.timeout_add(1000, update_nvidia_temp, gpu_temp)
    GLib.timeout_add(1000, update_nvidia_usage, gpu_usage)
    GLib.timeout_add(1000, update_nvidia_usedVram, gpu_vram)
    GLib.timeout_add(1000, update_nvidia_fanspeed, gpu_speed)
    GLib.timeout_add(1000, update_nvidia_powerdraw, gpu_power)