import ttkbootstrap as ttk

from view.tray_menu import TrayMenu
from controller.controller_tab import ControllerTab
from controller.controller_window import ControllerWindow
from model.config_loader import (
    get_text, 
    get_image,     
    get_key, 
    get_tip, 
    image_loader, 
    ViewConfigurator
)


class TabManager(ttk.Frame):
    def __init__(self, master, style):
        super(TabManager, self).__init__()
        self.master = master
        self.style = style
        self.TrayMenu = TrayMenu
        self.close_tab_data = []
        self.current_tab = None
        self.select_index = None 

        self.master.winfo_id = self.master.winfo_id()
        self.master.data = ViewConfigurator(self.master)
        self.master.controller_window = ControllerWindow(self.master)
        image_loader(self.master)

        self.tab_bar = ttk.Notebook(self, padding=(5, 5, 5, 5))
        self.tab_bar.pack(fill='both', expand=True)
        self.add_tab() 
        self.bind_events()
        
    def add_tab(self, event=None, path='home', text='home', image_text=None, direct_image=None, navigator=None): 
        controller_tab = ControllerTab(self.master, self.style, self, path, navigator)
        image = direct_image or get_image(image_text or text, self.master.data.SIZE['tab'])  
        text = get_text(text).ljust(15)  
        self.tab_bar.add(controller_tab, text=text, image=image, compound='left') 
        self.tab_bar.select(controller_tab)  

    def copy_tab(self, event=None):  
        self.update_current_tab()
        if self.current_tab is not None:
            get_frame = self.get_frame()
            self.add_tab(path=get_frame.input_ent.get(), text=self.get_tab_option('text'), direct_image=self.get_tab_option('image'), navigator=get_frame.navigator)

    def close_tab(self, event=None):  
        self.update_current_tab()
        if self.current_tab is not None:
            if len(self.tab_bar.tabs()) > 1:
                self.forget(self.current_tab)    

    def close_other_tabs(self, event=None):
        self.update_current_tab()
        self.forget_tabs(self.tab_bar.tabs())

    def close_left_tabs(self, event=None):
        self.update_current_tab_index()
        tabs_left = [tab for index, tab in enumerate(self.tab_bar.tabs()) if index < self.select_index]  
        self.forget_tabs(tabs_left)

    def close_right_tabs(self, event=None):
        self.update_current_tab_index()
        tabs_right = [tab for index, tab in enumerate(self.tab_bar.tabs()) if index > self.select_index]  
        self.forget_tabs(tabs_right)

    def readd_tab(self, event=None):
        if len(self.close_tab_data) > 0:
            data = self.close_tab_data[0]
            self.add_tab(path=data['path'], text=data['text'], direct_image=data['direct_image'], navigator=data['navigator'])
            self.close_tab_data.pop(0)

    def show_menu(self, event):
        def add_command(text, command):
            menu.add_command(label=get_tip(text), command=command, image=get_image(text, self.master.data.SIZE['tab']), compound='left') 
        
        menu = ttk.Menu(self.tab_bar, tearoff=False)  

        add_command('add_tab', self.add_tab)  
        add_command('copy_tab', self.copy_tab)

        self.update_current_tab_index()
        tabs = self.tab_bar.tabs()
        if len(tabs) > 1:
            menu.add_separator()
            add_command('close_tab', self.close_tab) 
            add_command('close_other_tabs', self.close_other_tabs)

        if self.select_index > 0:  
            add_command('close_left_tabs', self.close_left_tabs)
        if self.select_index < len(tabs) - 1:
            add_command('close_right_tabs', self.close_right_tabs)

        if len(self.close_tab_data) > 0:
            menu.add_separator()
            add_command('readd_tab', self.readd_tab)
            
        menu.post(event.x_root, event.y_root)

    def bind_events(self):
        def bind(text, command):  
            self.master.bind(get_key(text), command)  

        bindings = {  
            'add_tab': self.add_tab,  
            'close_tab': self.close_tab,  
            'copy_tab': self.copy_tab,  
            'close_other_tabs': self.close_other_tabs,  
            'close_left_tabs': self.close_left_tabs,  
            'close_right_tabs': self.close_right_tabs,  
            'readd_tab': self.readd_tab  
        }
        for text, command in bindings.items():  
            bind(text, command)  
        self.tab_bar.bind("<Button-3>", self.show_menu) 

    def get_tab_option(self, option, tab=None):
        tab = tab or self.current_tab
        return self.tab_bar.tab(tab, option)

    def update_current_tab(self):
        self.current_tab = self.tab_bar.select()

    def update_current_tab_index(self):
        self.update_current_tab()
        self.select_index = self.tab_bar.index(self.current_tab) 

    def get_frame(self, tab=None):
        tab = tab or self.current_tab
        return self.tab_bar.winfo_toplevel().nametowidget(tab) 

    def forget_tabs(self, tabs):
        for tab in tabs:  
            if tab != self.current_tab:
                self.forget(tab)

    def forget(self, tab):
        get_frame = self.get_frame(tab)
        self.close_tab_data.append(
            {
                'path': get_frame.input_ent.get(), 
                'text': self.get_tab_option('text', tab), 
                'direct_image': self.get_tab_option('image', tab),
                'navigator': get_frame.navigator,
            }
        )
        self.tab_bar.forget(tab)
