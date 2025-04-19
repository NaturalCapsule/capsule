import os
from pathlib import Path
from configparser import ConfigParser

desktop_dirs = [
    Path("~/.local/share/applications").expanduser(),
    Path("/usr/share/applications")
]

apps = []

def get_app_info():
    for directory in desktop_dirs:
        if not directory.exists():
            continue
        for file in directory.glob("*.desktop"):
            config = ConfigParser(strict=False)
            config.read(file, encoding="utf-8")
            try:
                name = config.get("Desktop Entry", "Name")
                exec_cmd = config.get("Desktop Entry", "Exec", fallback="")
                icon = config.get("Desktop Entry", "Icon", fallback="")
                apps.append((name, exec_cmd, icon))
            except:
                continue
    return apps

# apps = get_app_info()
# Print them
# for name, exec_cmd, icon in apps:
#     print(f"{name} | Exec: {exec_cmd} | Icon: {icon}")