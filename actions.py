import subprocess
import os
import shlex

def launch_app(widget, exec):
    if exec == 'kitty' or exec =='htop' or exec == 'alacritty' or exec == 'yazi' or exec == 'vim' or exec == 'nvim':
        subprocess.Popen(["kitty", "-e", "sh", "-c", exec])
    else:
        cmd = shlex.split(exec)
        subprocess.Popen(cmd, start_new_session = True, cwd = os.path.expanduser("~"))

def open_terminal(widget, term):
    if term is not None or term != '' or len(term) != 0:
        terminal = shlex.split(term)
        subprocess.Popen(terminal, shell = True, cwd=os.path.expanduser("~"))
    else:
        try:
            subprocess.Popen(
                ["kitty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~")
            )

        except FileNotFoundError:
            try:
                subprocess.Popen(["alacritty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~"))
            except FileNotFoundError:
                print("Tried Kitty and Alacritty and None of them opened, make sure its installed on your system!.")

def exit_(widget):
    subprocess.Popen(
        ["exit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~")
    )

def open_fileM(widget, fileM):
    if fileM is not None or fileM != '' or len(fileM) != 0:
        file_manager = shlex.split(fileM)
        subprocess.Popen(file_manager, shell = True, cwd=os.path.expanduser("~"))

    else:
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
    