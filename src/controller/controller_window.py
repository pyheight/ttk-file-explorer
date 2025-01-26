import os

import ttkbootstrap as ttk

from constants.information import (
    TITLE, 
    DESCRIPTION, 
    ABOUT_VERSION, 
    ICON_DATA
)
from model.file_io import create_file, new_shortcut, rename_file
from model.config_loader import get_text
from model.system_info import get_basename
from model.web_updater import get_update, open_web
from view.window import window
from view.box import MessageBox as messagebox


class ControllerWindow(window):
    def __init__(self, master):
        super().__init__(master)
        self.newly_built_master = None
        self.rename_master = None
        self.check_update_master = None

    def newly_built(self, path, file_type, filename):  
        def handle_creation(event=None):  
            target_name = name_ent.get().strip()  
            target_path = os.path.join(path, target_name)  
            try:  
                if file_type == '.lnk':  
                    if not os.path.exists(target_name):  
                        messagebox.showwarning(f'{get_text("not_found")} {target_name}', 'newly_built')  
                        return                      
                    new_shortcut(os.path.join(path, os.path.splitext(get_basename(target_path))[0] + file_type), target_path)  
                else:  
                    if os.path.exists(target_path):
                        messagebox.showwarning(get_text('name_exists'), 'newly_built')
                        return
                    create_file(target_path, file_type)  
            except Exception as e:  
                messagebox.showerror(str(e), 'newly_built')  
            else:  
                self.newly_built_master.destroy()  
  
        if self.newly_built_master:  
            self.newly_built_master.destroy()  
  
        self.newly_built_master = ttk.window.Toplevel(self.master)  
        self.config_window(self.newly_built_master, get_text('newly_built'), 450, 160)  
  
        texts = {  
            'tip': get_text('enter_name' if file_type != '.lnk' else 'enter_object_location'),  
            'setting': get_text('set_name' if file_type != '.lnk' else 'finish'), 
            'cancel': get_text('cancel'),
            'browse': get_text('browse'),
            'select_shortcut_target': get_text('select_shortcut_target'),
        }  
        name_ent = self.input_ui(self.newly_built_master, filename, handle_creation, texts, bool(file_type == '.lnk'))  

    def check_update(self, is_show=True):
        def download():
            self.check_update_master.destroy()
            try:
                open_web(update_info['download_url'])
            except Exception as e:  
                messagebox.showerror(str(e), 'update_reminder')    
                      
        update_info = get_update()
        if update_info: 
            update_info['cancel'] = get_text('on_next')
            update_info['setting'] = get_text('download_now')
            if self.check_update_master:  
                self.check_update_master.destroy() 
            self.check_update_master = ttk.window.Toplevel(self.master)  
            self.config_window(self.check_update_master, get_text('update_reminder'), 480, 300, is_transient=False, is_grab=False, resize_x=False) 
            self.content_ui(self.check_update_master, download, update_info, 390)
        elif update_info is False:
            if is_show:
                messagebox.showinfo(get_text('already_latest_version'), 'update_reminder')
        else:
            if is_show:
                messagebox.showwarning(get_text('failed_update'), 'update_reminder')

    def rename(self, path):
        def handle_renamed(event=None):  
            target_name = name_ent.get().strip()  
            target_path = os.path.join(os.path.dirname(path), target_name)  
            try:
                rename_file(path, target_path)  
            except Exception:  
                pass 
            else:  
                self.rename_master.destroy()  

        if self.rename_master:  
            self.rename_master.destroy()  
  
        self.rename_master = ttk.window.Toplevel(self.master)  
        self.config_window(self.rename_master, get_text('rename'), 450, 160)  

        texts = {  
            'tip': get_text('enter_name'),  
            'setting': get_text('rename'), 
            'cancel': get_text('cancel'),
        }  
        name_ent = self.input_ui(self.rename_master, os.path.basename(path), handle_renamed, texts)  
