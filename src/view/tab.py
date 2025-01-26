from functools import partial

import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame

from constants.texts import ACTION_BAR_TEXTS, NAVIGATION_BAR_TEXTS
from view.custom import CollapsibleFrame, DiskFrame
from model.config_loader import get_text, get_tip, get_image
from model.system_info import (
    HOME, 
    DISK, 
    LIBRARY, 
    get_library_path, 
    get_disk_info, 
    get_node_path, 
    get_disk_type
)


class AutoScrollbar(ttk.Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.pack_forget()
        else:
            self.pack(fill='y', side='right')
        ttk.Scrollbar.set(self, low, high)


class Tab(ttk.Frame):
    def __init__(self, master, style):
        super(Tab, self).__init__()
        self.master = master
        self.style = style
        self.info_bar_but = []
        self.home_fra = None
        self.input_ent = None
        self.navigation_buts = {'left': {}, 'right': {}}
        self.action_buts = {'left': {}, 'right': {}}

    def load_components(self):
        self.style.configure('Outline.TButton', relief='flat')  # 更改了所有使用Outline.TButton样式的按钮
        self.navigation_bar()
        self.bottom_bar()
        self.tree_view()
        self.action_bar()
        self.info_bar()
        self.table_view()

    def layout_pack(self):
        self.navigation_bar_fra.pack(fill='x', side='top', pady=5, padx=5)     
        self.bottom_bar_fra.pack(fill='x', side='bottom', padx=10)
        self.tree_view_fra.pack(fill='y', side='left', pady=5, padx=10)
        self.action_bar_fra.pack(fill='x', side='top', padx=5)   
        self.info_bar_fra.pack(fill='y', side='right', padx=10)
        self.content_fra.pack(fill='both', expand=True, pady=5)
        self.auto_scroll_fra.pack(fill='y', side='right', padx=2, pady=2)  
        self.auto_scroll.pack(fill='y', side='right') 
        self.table_view.pack(fill='both', side='left', expand=True)  
        
    def clear_widgets(self):
        self.home_fra.pack_forget()
        self.table_view_fra.pack_forget()

    def set_table_view(self, event=None, is_yview=True):
        self.table_view_fra.pack(fill='both', expand=True)
        self.content_fra.focus_set()
        self.table_view.focus_force()
        if is_yview:        
            self.table_view.yview('moveto', 0.0)
        self.auto_scroll.get()

    def set_home_fra(self):
        self.home_fra.pack(fill='both', expand=True)
        self.tree_view.focus_set()
        self.home_fra.focus_force()

    def create_but(self, frame, text, side, padx, size_name, state='normal'):
        but = ttk.Button(
            frame,
            image=get_image(text, self.master.data.SIZE[size_name]),
            style='Outline.TButton',
            state=state
        )
        but.pack(side=side, padx=padx)
        ToolTip(but, text=get_tip(text), bootstyle='info')
        return but

    def create_view(self, frame_name, style_name, selectmode, show, columns=None, height=None, padding=(2, 0, 2, 0)):
        def motion_row(event, widget):
            item = widget.identify_row(event.y)
            widget.tk.call(widget, 'tag', 'remove', 'highlight')
            widget.tk.call(widget, 'tag', 'add', 'highlight', item)

        def leave_row(event, widget):
            widget.tk.call(widget, 'tag', 'remove', 'highlight')

        self.style.configure(
            f'{style_name}.Treeview', 
            rowheight=self.master.data.VIEW[style_name]['height'], 
            padding=padding
        )
        view = ttk.Treeview(
            frame_name, 
            style=f'{style_name}.Treeview', 
            selectmode=selectmode, 
            show=show,
            columns=columns, 
            height=height
        )
        view.tag_configure(style_name, font=(self.master.data.VIEW[style_name]['font']))
        view.tag_configure('highlight', background=self.master.data.HIGHLIGHT_BG)
        view.bind('<Motion>', lambda event: motion_row(event, view))
        view.bind('<Leave>', lambda event: leave_row(event, view))
        return view

    def navigation_bar(self):
        self.navigation_bar_fra = ttk.Frame(self, height=40)
        for side, texts in NAVIGATION_BAR_TEXTS.items():
            for text in texts:
                but = self.create_but(self.navigation_bar_fra, text, side, 1, 'navigation')
                self.navigation_buts[side][text] = but
            if not self.input_ent:
                self.input_ent = ttk.Entry(self.navigation_bar_fra, font=(self.master.data.FONT, 10, 'bold'))
                self.input_ent.pack(side='left', fill='x', expand=True, padx=5)

    def action_bar(self):
        self.action_bar_fra = ttk.Frame(self, height=40)
        for side, texts in ACTION_BAR_TEXTS.items():
            for text in texts:
                but = self.create_but(self.action_bar_fra, text, side, 1, 'action')
                if side == 'left' and (text in ('newly_built', 'paste', 'delete')):
                    ttk.Separator(self.action_bar_fra, orient='vertical').pack(fill='y', padx=3, side='left')
                self.action_buts[side][text] = but

    def bottom_bar(self):
        self.bottom_bar_fra = ttk.Frame(self, height=30)
        self.items_number_but = ttk.Label(self.bottom_bar_fra, font=(self.master.data.FONT, 10))
        self.project_info_but = ttk.Label(self.bottom_bar_fra, font=(self.master.data.FONT, 10))
        self.sizegrip = ttk.Sizegrip(self.bottom_bar_fra, bootstyle='info')

        self.items_number_but.pack(side='left', padx=8)
        self.project_info_but.pack(side='left')
        self.sizegrip.pack(side='right')

        ToolTip(self.sizegrip, get_tip('sizegrip'), bootstyle='info')

    def info_bar(self):
        self.info_bar_fra = ttk.Frame(self, width=200)
        self.info_bar_fra.pack_propagate(0)
        self.type_img_lab = ttk.Label(self.info_bar_fra)
        self.title_lab = ttk.Label(self.info_bar_fra, font=(self.master.data.VIEW['table_view']['font'][0], 13), wraplength=175)
        self.type_lab = ttk.Label(self.info_bar_fra, font=(self.master.data.FONT, 10, 'bold'), wraplength=180)
        self.type_img_lab.pack(anchor='center', pady=10)
        self.title_lab.pack(anchor='center', padx=1)
        self.type_lab.pack(anchor='center', pady=5)

    def tree_view(self):
        self.tree_view_fra = ttk.Frame(self, width=200)
        self.tree_view = self.create_view(self.tree_view_fra, 'tree_view', 'browse', 'tree', padding=(10, 10, 10, 10))
        self.tree_view.pack(fill='both', expand=True)

    def table_view(self):
        self.content_fra = ttk.Frame(self)
        self.table_view_fra = ttk.Frame(self.content_fra)
        self.table_view = self.create_view(self.table_view_fra, 'table_view', 'extended', None, [0, 1, 2, 3], 70)
        self.table_view.heading(0, text=get_text('file_name'), anchor='w')
        self.table_view.heading(1, text=get_text('file_modify_date'), anchor='center')
        self.table_view.heading(2, text=get_text('file_type'), anchor='e')
        self.table_view.heading(3, text=get_text('file_size'), anchor='e')
        self.table_view.column('#0', anchor='w', width=40, stretch=False)
        self.table_view.column(1, anchor='center', width=140)
        self.table_view.column(2, anchor='e', width=62)
        self.table_view.column(3, anchor='e', width=40)

        self.auto_scroll_fra = ttk.Frame(self.table_view_fra)
        self.auto_scroll = AutoScrollbar(self.auto_scroll_fra, bootstyle='round')
        self.auto_scroll.config(command=self.table_view.yview)
        self.table_view.config(yscrollcommand=self.auto_scroll.set)

        self.home_fra = ScrolledFrame(self.content_fra, height=self.winfo_height(), padding=(5, 0, 15, 0), autohide=True, bootstyle='round')
        self.home_node = self.add_node(HOME)

        for name, path in get_node_path().items():
            if path:
                self.add_node(name, path)

        self.library_node = self.add_node(LIBRARY, open=self.master.data.IS_OPEN[LIBRARY])
        self.disk_node = self.add_node(DISK, open=self.master.data.IS_OPEN[DISK])

    def load_tree_view(self, focus_path):
        self.clear_item(self.library_node)
        self.clear_item(self.disk_node)

        for name, path in get_library_path().items():
            if path:
                self.add_node(name, path, parent=self.library_node)
        for disk, info in get_disk_info().items():
            self.add_node(info['disk_name'], disk, get_disk_type(disk), parent=self.disk_node)

        self.focus_node(focus_path)

    def show_home_page(self):
        def add_cf(text):
            cf = CollapsibleFrame(self.home_fra, get_text(text), self.master.data, open_text=text+'_cf')
            cf.pack(fill='both', expand=True, anchor='nw', pady=3)
            return cf

        def add_path_but(name, path):
            callback = partial(self.render_content, path=path, text=name, image_text=name)
            button = ttk.Button(
                self.library_cf.frame,
                text=get_text(name),
                image=get_image(name, self.master.data.SIZE['disk']),
                style='Outline.TButton',
                compound='top'
            )
            ToolTip(button, path, bootstyle='info')
            button.pack(side='left', padx=5, expand=True, fill='x')
            button.bind('<Button-1>', callback)

        def add_disk_but(disk, info):
            callback = partial(self.render_content, path=disk, text=info['disk_name'], image_text=DISK)
            free_space_text = f"{info['disk_free']} {get_text('usable')}, {get_text('total')} {info['disk_total']}"
            disk_but = DiskFrame(
                self.disk_cf.frame,
                get_image(get_disk_type(disk), self.master.data.SIZE[DISK]),
                info['disk_name'],
                info['disk_percent'],
                free_space_text,
                self.master.data.FONT,
                cursor='hand2'
            )
            disk_but.pack(anchor='nw', padx=5, ipady=2, side='left')
            disk_but.bind('<Button-1>', callback)
            for widget in disk_but.winfo_children():
                widget.bind('<Button-1>', callback)

        for widget in self.home_fra.winfo_children():
            widget.destroy()

        self.library_cf = add_cf(LIBRARY)
        self.disk_cf = add_cf(DISK)
        self.quick_access_cf = add_cf('quick_access')
        self.recent_file_cf = add_cf('recent_file')

        for name, path in get_library_path().items():
            if path:
                add_path_but(name, path)

        for disk, info in get_disk_info().items():
            add_disk_but(disk, info)

        self.config_bottom('', '')
