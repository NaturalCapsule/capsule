import gi
import os
import hashlib
import urllib.request
import time
import config

gi.require_version('Gdk', '3.0')
from gi.repository import GdkPixbuf, GLib

from media import MediaPlayerMonitor
from sys_info import *
from raduis_image import create_radius_pixbuf

media = MediaPlayerMonitor()

title_name, player_name = None, None


def update_cpu_temp(cpu_temp):
    temp = get_cpu_temp()
    cpu_temp.set_label(f"CPU Temp: {temp}C")
    return True

def update_time(time_label):
    t = time.localtime()
    time__ = config.display_time
    fmt_time = time.strftime(time__, t)
    # fmt_time = time.strftime("  %H:%M", t)
    # fmt_time = time.strftime("%H:%M:%S", t)
    # d
    time_label.set_text(f"{fmt_time}")
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
    gpu_speed.set_label(f"GPU Fan Speed: {speed}RPM")
    return True

def update_nvidia_usedVram(gpu_vram):
    used = get_nvidia_used_vram()
    total = get_nvidia_total_vram()
    gpu_vram.set_label(f"GPU VRAM: {used}GB/{total}GB")
    return True

def update_nvidia_powerdraw(gpu_power):
    power = get_nvidia_powerdraw()
    gpu_power.set_label(f"GPU Power Draw: {power}")
    return True

def get_cached_filename(title):
    hashed = hashlib.md5(title.encode()).hexdigest()
    return f"/tmp/{hashed}.jpg"


def safe_set_label(label, text):
    GLib.idle_add(label.set_text, text)

def safe_set_image(image_widget, pixbuf):
    GLib.idle_add(image_widget.set_from_pixbuf, pixbuf)

def update_media(title_label, image):
    global title_name, player_name
    media.monitor()
    thumbnail = None
    
    current_player = media.current_player or ''
    current_title = media.title_ or ''
    should_update = False

    if player_name != current_player:
        print(f"Player changed: {player_name} → {current_player}")
        player_name = current_player
        should_update = True

    if title_name != current_title:
        print(f"Title changed: {title_name} → {current_title}")
        title_name = current_title
        should_update = True

    if current_player:
        try:
            if should_update:
                print(f"title: {current_title}\nartist: {media.artist}")
                
                safe_set_label(title_label, current_title)
                
                media_ = f'{current_title}\nBy\n{media.artist}'
                height, width = 120, 120
                if 'file:///' in media.art_url:
                    thumbnail = media.art_url.replace('file:///', '/')
                    height, width = 120, 120
                elif 'https://' in media.art_url or 'http://' in media.art_url:
                    thumbnail = get_cached_filename(current_title)
                    if not os.path.exists(thumbnail):
                        print(f"Downloading thumbnail to cache: {thumbnail}")
                        urllib.request.urlretrieve(media.art_url, thumbnail)
                    else:
                        print(f"Using cached thumbnail: {thumbnail}")
                    height, width = 120, 120

                if thumbnail and os.path.exists(thumbnail):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, height, width)
                    circular_pixbuf = create_radius_pixbuf(pixbuf)

                    print("Setting images safely...")
                    safe_set_image(image, circular_pixbuf)
                    safe_set_label(title_label, media_)
                    image.show()


        except Exception as e:
            print(f"Exception in update_image: {e}")

    else:
        safe_set_label(title_label, '')
        image.hide()

    return True