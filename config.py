from configparser import ConfigParser

config = ConfigParser(interpolation = None)
config.read('config/config.ini')

use_blur = config.getboolean('Appearance', 'UseTransparentBlur')
show_app_info = config.getboolean('Appearance', 'ShowApplicationInfo')

terminal = config.get('Open Apps', 'terminal')
file_manager = config.get('Open Apps', 'FileManager')

display_time = config.get('Appearance', 'DisplayTime')
