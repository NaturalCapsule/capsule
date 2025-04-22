from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')

use_blur = config.getboolean('Appearance', 'UseTransparentBlur')


terminal = config.get('Open Apps', 'terminal')
file_manager = config.get('Open Apps', 'FileManager')

