import subprocess
import os
import shlex

def launch_app(widget, exec):
    cmd = shlex.split(exec)
    subprocess.Popen(cmd, start_new_session = True, cwd = os.path.expanduser("~"))

def open_terminal(widget):
    try:
        process = subprocess.Popen(
            ["kitty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~")
        )

    except FileNotFoundError:
        try:
            process = subprocess.Popen(["alacritty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~"))
        except FileNotFoundError:
            print("Tried Kitty and Alacritty and None of them opened, make sure its installed on your system!.")

def exit_(widget):
    subprocess.Popen(
        ["exit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~")
    )

def open_fileM(widget):
    try:
        subprocess.Popen(
            ["pcmanfm"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~")
        )
    except FileNotFoundError:
        try:
            subprocess.Popen(["thunar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~"))
        except FileNotFoundError:
            try:
                subprocess.Popen(["dolphin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~"))
            except FileNotFoundError:
                print("Tried pcmanfm, thunar and dolphin, None of them worked, make sure its installed on your system")

def previous_track_func(widget):
    os.system("playerctl previous")
    
def next_track_func(widget):
    os.system("playerctl next")

def reset_func(widget):
    os.system('playerctl position 0')

def pause_play_func(widget):
    os.system('playerctl play-pause')

def fast_forward_func(widget):
    os.system("playerctl position 10+")

def backward_func(widget):
    os.system("playerctl position 10-")

def shutdown_machine(widget):
    subprocess.Popen(['shutdown', 'now'])

def reboot_machine(widget):
    subprocess.Popen(['reboot'])

def lock_machine(widget):
    subprocess.Popen(['hyprlock'])

def hib_machine(widget):
    subprocess.Popen(['systemctl', 'hibernate'])
    