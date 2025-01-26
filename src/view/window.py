import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame

from constants.paths import ICON_PATH
from model.file_io import tree_askdirectory


class window:
    def __init__(self, master):
        self.master = master

    def config_window(self, master, title, width, height, is_transient=True, is_grab=True, resize_x=True, is_topmost=False):
        rel_x = self.master.winfo_rootx()  
        rel_y = self.master.winfo_rooty()  
        rel_width = self.master.winfo_width()  
        rel_height = self.master.winfo_height()  
      
        x = rel_x + (rel_width // 2) - (width // 2)  
        y = rel_y + (rel_height // 2) - (height // 2) - 20
      
        master.geometry(f'{width}x{height}+{x}+{y}')  
        master.minsize(width, height)
        if is_transient:
            master.transient(self.master)
        if is_grab:
            master.grab_set() 
        try:
            master.iconbitmap(ICON_PATH)
        except FileNotFoundError:
            master.iconphoto(False, self.master.icon_photo)
        master.title(title)
        master.resizable(resize_x, False)
        master.protocol('WM_DELETE_WINDOW', master.destroy)
        master.wm_attributes('-topmost', is_topmost)

    def button_bar_ui(self, master, texts, cancel_func, setting_func):
        bottom_fra = ttk.Frame(master, height=40)
        cancel_but = ttk.Button(bottom_fra, text=texts['cancel'], bootstyle='toolbutton', command=cancel_func)
        setting_but = ttk.Button(bottom_fra, text=texts['setting'], command=setting_func)
        cancel_but.pack(side='right', padx=17, ipadx=15)
        setting_but.pack(side='right', ipadx=15)
        bottom_fra.pack(fill='x', pady=15, side='bottom')
        return setting_but

    def input_ui(self, master, filename, func, texts, is_browse=False):
        def insert_filename():  
            name_ent.insert(0, filename)  
            dot_index = filename.rfind('.')  
            if dot_index != -1:  
                name_ent.selection_range(0, dot_index)  
            else:  
                name_ent.selection_range(0, 'end')  

        def on_change(*args):
            if not name_var.get().strip():
                setting_but.config(state='disabled')
            else:
                setting_but.config(state='normal')

        def name_ent_out(event):
            if not name_ent.get().strip():
                name_ent.insert(0, filename)

        def browse():
            d = tree_askdirectory(self.master.winfo_id, texts['select_shortcut_target'])
            if d:
                name_ent.delete(0, 'end')
                name_ent.insert(0, d) 

        name_var = ttk.StringVar()
        tip_lab = ttk.Label(master, text=texts['tip'], font=(self.master.data.FONT, 11, 'bold'))
        middle_fra = ttk.Frame(master)
        name_ent = ttk.Entry(middle_fra, font=(self.master.data.FONT, 12), textvariable=name_var)
        setting_but = self.button_bar_ui(master, texts, master.destroy, func)
        tip_lab.pack(pady=15, padx=15, anchor='nw')

        if is_browse:
            ask_but = ttk.Button(middle_fra, text=texts['browse'], command=browse)
            ask_but.pack(side='right', padx=5, ipadx=5)
            setting_but.config(state='disabled')
        else:
            insert_filename()
            name_ent.bind('<FocusOut>', name_ent_out)   

        name_ent.pack(fill='x', padx=5)
        middle_fra.pack(fill='x', padx=10)
        name_ent.focus_set()
        name_ent.bind('<Return>', func)         
        name_var.trace('w', on_change)
        
        return name_ent

    def content_ui(self, master, func, texts, wraplength, is_title=True, is_time=True):
        def update_wraplength(event):
            text_lab.config(wraplength=master.winfo_width()-40)
        content_fra = ScrolledFrame(master, height=master.winfo_height(), padding=(15, 15, 15, 15), autohide=True, bootstyle='round')
        if is_title:
            title_lab = ttk.Label(content_fra, text=texts['title'], font=(self.master.data.FONT, 11, 'bold'), wraplength=wraplength)
            title_lab.pack(anchor='center')
        if is_time:
            time_lab = ttk.Label(content_fra, text=texts['time'], font=(self.master.data.FONT, 10, 'bold'), wraplength=wraplength)
            time_lab.pack(anchor='center')

        text_lab = ttk.Label(content_fra, text=texts['text'], font=(self.master.data.FONT, 10), wraplength=wraplength)
        text_lab.pack(anchor='nw')
        self.button_bar_ui(master, texts, master.destroy, func)
        content_fra.pack(fill='both', expand=True)
        master.bind('<Configure>', update_wraplength)
