import ctypes
import sys
import threading

import pystray
from constants.information import TITLE, WEBSITE
from model.config_loader import get_text
from model.web_updater import open_web


class TrayMenu:
    def __init__(self, master, get_alpha, delete_window):
        self.master = master
        self.get_alpha = get_alpha
        self.delete_window = delete_window

    def load_menu(self):
        self.menu = (
            pystray.MenuItem(get_text('website'), self.show_website),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(get_text('window'), self.show_window, default=True),
            pystray.MenuItem(get_text('runas'), self.on_runas),
            pystray.MenuItem(get_text('quit'), self.on_quit),
            pystray.Menu.SEPARATOR,
        )
        self.menu_icon = pystray.Icon('', self.master.icon_img, TITLE, self.menu)
        threading.Thread(target=self.menu_icon.run, daemon=True).start()

    def show_website(self):
        open_web(WEBSITE)

    def show_window(self):
        if self.master.state() == 'normal':
            self.delete_window()
        else:
            self.master.deiconify()
            self.show_window_child()

    def show_window_child(self):
        alpha_now = self.get_alpha()
        if alpha_now >= self.master.alpha:
            return
        else:
            self.master.attributes('-alpha', alpha_now + 0.01)
            self.master.after(15, self.show_window_child)

    def on_runas(self):
        if ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, self.master.__file__, None, 1) == 42:
            self.on_quit(None)

    def on_quit(self, icon):
        self.delete_window(True)
        if icon:
            icon.stop()
