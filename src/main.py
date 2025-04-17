"""
Copyright 2025 pyheight  
 
Licensed under the Apache License, Version 2.0 (the "License");  
you may not use this software except in compliance with the License.  
You may obtain a copy of the License at  
 
    http://www.apache.org/licenses/LICENSE-2.0  
 
Unless required by applicable law or agreed to in writing, software  
distributed under the License is distributed on an "AS IS" BASIS,  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and  
limitations under the License.  
 
Project home page: https://github.com/pyheight/ttk-file-explorer  
Contact: pyheight@qq.com
 
This copyright and license notice applies to all files in this project,  
unless otherwise indicated.  
"""

import atexit
import ctypes
import importlib
import os
import logging
import sys
import threading
from tkinter import messagebox
from math import sin, radians

import ttkbootstrap as ttk
from ttkbootstrap.style import ThemeDefinition
from ttkbootstrap.icons import Icon

from __init__ import testing
from constants.settings import (
    WIDTH, 
    HEIGHT, 
    ALPHA, 
    THEME
)
from constants.information import (
    TITLE, 
    DESCRIPTION, 
    ABOUT_VERSION, 
    ICON_DATA
)
from constants.paths import (
    ICON_PATH, 
    LOADING_PATH, 
    CLIPBOARD_PATH, 
    LOG_PATH,
    TRANSLATION_PATH, 
    SETTINGS_PATH, 
    KEY_PATH, 
    SKIN_PATH
)
from model.image_converter import (
    decode_image, 
    photo_image, 
    open_image
)
from model.profile_operation import (
    create_file, 
    get_config_option, 
    remove_file, 
    get_user_module
)


class TtkFileExplorer:
    def __init__(self, master):
        self.master = master
        self.master.__file__ = __file__
        self.master.theme_type = 'light'
        self.master.highlight = '#a0a8b0'
        self.master.icon_img = decode_image(ICON_DATA, (72, 72))
        self.master.icon_photo = photo_image(self.master.icon_img)
        self.theme_name = get_config_option(SETTINGS_PATH, 'style_theme', 'theme_use', THEME)
        self.alpha = get_config_option(SETTINGS_PATH, 'window', 'alpha', '')
        self.master.alpha = float(self.alpha) if self.alpha.isdigit() else ALPHA

    def setup_logging(self):
        self.master.logger = logging.getLogger('logger')
        self.master.logger.setLevel(logging.DEBUG if testing else logging.INFO) 
        file_handler = logging.FileHandler(create_file(LOG_PATH))
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if testing:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.master.logger.addHandler(console_handler)             
        file_handler.setFormatter(formatter)
        self.master.logger.addHandler(file_handler)

    def get_alpha(self):
        return float(self.master.attributes('-alpha'))

    def delete_window(self, is_destroy=False):
        try:
            alpha_now = self.get_alpha()
            if alpha_now <= 0.1:
                if is_destroy:
                    self.master.destroy()
                    self.master.quit()
                else:
                    self.master.withdraw()
                return
            else:
                self.master.attributes('-alpha', alpha_now - 0.1)
                self.master.after(30, self.delete_window, is_destroy)
        except Exception:
            pass

    def config_window(self):
        def drag(event):
            x = self.master.winfo_pointerx() - self.master._offset_x
            y = self.master.winfo_pointery() - self.master._offset_y
            self.master.geometry(f'+{x}+{y}')

        def start_drag(event):
            self.master._offset_x = event.x
            self.master._offset_y = event.y

        def stop_drag(event):
            self.master._offset_x = None
            self.master._offset_y = None

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 75
            self.master.scaling(scale)
        except Exception:
            pass

        x = int((self.master.winfo_screenwidth() // 2) - (WIDTH // 2))
        y = int((self.master.winfo_screenheight() // 2) - (HEIGHT // 2))
        
        self.master.overrideredirect(True)
        self.master.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
        self.master.lift()
        try:
            self.master.iconbitmap(ICON_PATH)
        except FileNotFoundError:
            self.master.iconphoto(False, self.master.icon_photo)
        self.master.title(TITLE)
        self.master.minsize(850, 425)
        self.master.protocol('WM_DELETE_WINDOW', self.delete_window)
        self.master.bind('<ButtonPress-1>', start_drag)
        self.master.bind('<ButtonRelease-1>', stop_drag)
        self.master.bind('<B1-Motion>', drag)

    def set_theme(self):
        # This feature is not currently available.
        
        def load_standard_theme():
            STANDARD_THEMES = ttk.themes.standard.STANDARD_THEMES
            self.master.theme_type = STANDARD_THEMES[self.theme_name]['type']
            self.master.highlight = STANDARD_THEMES[self.theme_name]['colors']['primary']

        def load_user_theme():
            USER_THEMES = get_user_module(SKIN_PATH).USER_THEMES
            colors = USER_THEMES[self.theme_name]['colors']
            self.master.highlight = colors['primary']
            self.master.theme_type = USER_THEMES[self.theme_name]['type']
            definition = ThemeDefinition(self.theme_name, colors, self.master.theme_type)
            self.master.style.register_theme(definition)
            self.master.style.theme_use(self.theme_name)

        try:
            self.ttk_style = ttk.Style(self.theme_name)
            load_standard_theme()
        except Exception:
            try:
                load_user_theme()
            except Exception as e:
                self.master.logger.info(e)
                self.ttk_style = ttk.Style(THEME)

    def init_page(self):
        def update_image(frame_number=0):
            image = animation_frames[frame_number]
            try:
                about_img_lab.configure(image=image)
            except Exception:
                return
            about_img_lab.image = image
            frame_number += 1
            if frame_number >= len(animation_frames):
                frame_number = 0
            self.master.after(15, update_image, frame_number)

        self.loading_fra = ttk.Frame(self.master)
        loading_child_fra = ttk.Frame(self.loading_fra)
        about_lab = ttk.Label(loading_child_fra, text=f' {TITLE}', image=self.master.icon_photo, compound='left', font=('小白体', 25, 'bold'))
        about_text_lab = ttk.Label(loading_child_fra, text=f'  {DESCRIPTION}', font=('微软雅黑', 20))
        about_bottom_lab = ttk.Label(self.loading_fra, text=ABOUT_VERSION, font=('微软雅黑', 13, 'bold'))
        about_img_lab = ttk.Label(self.loading_fra)

        loading_child_fra.pack(expand=True)
        about_lab.pack(pady=40)
        about_text_lab.pack()
        about_img_lab.pack()
        about_bottom_lab.pack(side='bottom', pady=40)
        self.loading_fra.pack(fill='both', expand=True)

        try:
            animation = open_image(LOADING_PATH)
            animation_frames = []    
            try:        
                while True:
                    animation.seek(len(animation_frames))
                    frame = animation.copy()
                    animation_frames.append(photo_image(frame))
            except Exception:
                pass
            update_image()
        except Exception:
            pass      

    def load_main(self):
        # Implicit import of modules is done in this thread

        def clean_up():
            remove_file(CLIPBOARD_PATH)

        def restart(e):
            if messagebox.askretrycancel(TITLE, e):
                if 'not all arguments converted during string formatting' in e:
                    remove_file(TRANSLATION_PATH)
                elif 'bad event type or keysym' in e:
                    remove_file(KEY_PATH)
                os.execl(sys.executable, sys.executable, self.master.__file__)
            else:
                self.delete_window(True)

        def new_settings():
            self.master.unbind('<ButtonPress-1>')
            self.master.unbind('<ButtonRelease-1>')
            self.master.unbind('<B1-Motion>')
            self.loading_fra.destroy()
            set_alpha()
            threading.Thread(target=self.master.controller_window.check_update, args=(False,), daemon=True).start()
            
        def set_alpha():
            alpha_now = self.get_alpha()
            if alpha_now > self.master.alpha:
                self.master.attributes('-alpha', alpha_now - 0.05)
                self.master.after(30, set_alpha)

        def animate(angle=0):
            def get_x():           
                return -960 * sin(radians(angle))  

            place_kwargs = {
                'relx': 0.5, 
                'rely': 0.5, 
                'anchor': 'center', 
                'relwidth': 1, 
                'relheight': 1
            }

            self.loading_fra.place(x=get_x(), **place_kwargs)
            tab_manager_fra.place(x=960 + get_x(), **place_kwargs)

            if angle < 89:
                self.master.after(5, animate, angle + 1)
            else:
                new_settings()

        try:
            tab_manager_module = importlib.import_module('controller.tab_manager')
            tab_manager_fra = tab_manager_module.TabManager(self.master, self.ttk_style)
            self.master.overrideredirect(False)
            tray_menu = tab_manager_fra.TrayMenu(self.master, self.get_alpha, self.delete_window)
            tray_menu.load_menu()
            self.master.after(250, animate)
            atexit.register(clean_up)
        except Exception as e:
            self.master.logger.exception("An error occurred:")
            restart(str(e))


def main():
    try:
        import pyi_splash
        pyi_splash.update_text('UI loaded...')   
        pyi_splash.close()
    except Exception:
        pass

    Icon.icon = ICON_DATA
    window = ttk.window.Window()
    file_explorer = TtkFileExplorer(window)
    file_explorer.setup_logging()    
    file_explorer.set_theme()
    file_explorer.config_window()
    file_explorer.init_page()
    loading_thread = threading.Thread(target=file_explorer.load_main, daemon=True)  
    loading_thread.start() 
    window.mainloop()


if __name__ == '__main__':
    main()
