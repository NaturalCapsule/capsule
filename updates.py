import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib
from sys_info import *

def update_cpu_temp(cpu_temp):
    temp = get_cpu_temp()
    cpu_temp.set_label(f"CPU Temp: {temp}C")
    return True


def update_cpu_usage(cpu_usage):
    usage = get_cpu_usage()
    cpu_usage.set_label(f"CPU Usage: {usage}%")
    return True

def update_ram_usage(ram_usage):
    usage = get_ram_usage()
    ram_usage.set_label(f"RAM Usage: {usage}%")
    return True

def update_ram_used(ram_used):
    used = get_used_ram()
    total = get_total_ram()
    ram_used.set_label(f"Total RAM: {used}GB/{total}GB")
    return True

def update_nvidia_temp(gpu_temp):
    temp = get_nvidia_temp()
    gpu_temp.set_label(f"GPU Temp: {temp}C")
    return True

def update_nvidia_usage(gpu_usage):
    usage = get_nvidia_gpu_usage()
    gpu_usage.set_label(f"GPU Usage: {usage}%")
    return True

def update_nvidia_fanspeed(gpu_speed):
    speed = get_nvidia_fanspeed()
    gpu_speed.set_label(f"GPU Usage: {speed}%")
    return True

def update_nvidia_usedVram(gpu_vram):
    used = get_nvidia_used_vram()
    total = get_nvidia_total_vram()
    gpu_vram.set_label(f"GPU VRAM: {used}MB/{total}GB")
    return True

def update_nvidia_powerdraw(gpu_power):
    power = get_nvidia_powerdraw()
    gpu_power.set_label(f"GPU Power Draw: {power}")
    return True