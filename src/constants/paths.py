import os
import sys

BEGINNING_PATH = os.path.dirname(sys.argv[0])

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS  
else:  
    base_path = BEGINNING_PATH

ICON_PATH = os.path.join(base_path, 'images', 'icon.ico')
LOADING_PATH = os.path.join(base_path, 'images', 'loading.gif')
SETTINGS_PATH = os.path.join(BEGINNING_PATH, 'config', 'settings.ini')
CLIPBOARD_PATH = os.path.join(BEGINNING_PATH, 'config', 'clipboard.ini')
LOG_PATH = os.path.join(BEGINNING_PATH, 'config', 'application.log')

SKIN_PATH = os.path.join(BEGINNING_PATH, 'config', 'skin.py')
LAYOUT_PATH = os.path.join(BEGINNING_PATH, 'config', 'layout.ini')
TRANSLATION_PATH = os.path.join(BEGINNING_PATH, 'config', 'translations.json')
KEY_PATH = os.path.join(BEGINNING_PATH, 'config', 'keys.json')
