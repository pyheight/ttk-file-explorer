import os
import concurrent.futures
from tkinter.filedialog import askdirectory
import threading
from functools import partial

import ttkbootstrap as ttk

from view.tab import Tab
from view.box import MessageBox as messagebox


from model.web_updater import is_valid_url
from model.builtin_transform import get_dict_key, is_disk
from model.config_loader import (
    update_read_json, 
    update_extensions_descs, 
    get_text, 
    get_image, 
    get_key, 
    get_tip, 
    get_type_text, 
    PathNavigator
)
from model.file_io import (
    get_shortcut_path, 
    open_with, 
    copy_file, 
    move_file, 
    recycle_file, 
    delete_file, 
    tree_askdirectory
)
from model.system_info import (
    HOME, 
    RECYCLE_BIN, 
    DISK, 
    LIBRARY, 
    RECYCLE_BIN_SHELL, 
    get_library_path, 
    get_disk_info, 
    get_node_path, 
    get_computer_info, 
    get_file_info, 
    get_recycle_bin_info, 
    get_disk_name, 
    get_disk_type, 
    get_basename, 
    get_type, 
    get_size
)


class ControllerTab(Tab):
    def __init__(self, master, style, tab_manager, use_path, navigator):
        super().__init__(master, style)
        self.tab_manager = tab_manager
        self.use_path = use_path
        self.navigator = navigator or PathNavigator()
        self.navigation_events = {
            'left': {
                'left': self.go_back,
                'right': self.go_forward,
                'recent': self.show_recent,
                'up': self.move_up,
            },
            'right': {
                'get_folder': self.get_folder,
                'search': self.search,
                'refresh': self.refresh,
            },
        }
        self.action_events = {
            'left': {
                'newly_built': self.newly_built,
                'shear': self.shear,
                'copy': self.copy,
                'paste': self.paste,
                'rename': self.rename,
                'copy_to': self.copy_to,
                'move_to': self.move_to,
                'recycle': self.recycle,
                'delete': self.delete,
                'attribute': self.attribute,
                'open': self.open,
                'open_with': self.open_with,
            },
            'right': {
                'more': self.more,
                'setting': self.setting,
                'layout': self.layout,
                'sort': self.sort,
                'options': self.options,    
            },
        }
        self.select_commands = {
            'select_all': self.select_all,
            'not_select': self.not_select,
            'invert_select': self.invert_select,
        }

        self.load_components()
        
        new_navigation_buts = {**self.navigation_buts['left'], 'search': self.navigation_buts['right']['search'], 'options': self.action_buts['right']['options']}
        new_action_buts = {**self.action_buts['left']}

        self.left_but_groups = { 
            'navigation': new_navigation_buts,
            'action': new_action_buts, 
        }   
        self.pending_future = None
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.ent_in_path = HOME
        self.layout_pack()
        self.bind_events()
        self.render_content(path=self.use_path, is_tab=False)

    def get_path_type(self, path):
        if path in (HOME, get_text(HOME), '\\', '\\/', ''):
            return HOME 
        elif path in (RECYCLE_BIN_SHELL, get_text(RECYCLE_BIN_SHELL)):
            return RECYCLE_BIN   
        elif is_disk(path):
            return DISK
        elif os.path.exists(path):
            library_path = get_library_path()  
            node_path = get_node_path()  
            return get_dict_key(library_path, path) or get_dict_key(node_path, path) or get_type(path)  
        else:
            return ''

    def render_content(self, event=None, path=HOME, text=None, image_text=None, is_shortcut=False, 
                       is_insert=False, is_back=False, is_up=False, is_tab=True):  
    
        path = path.strip()
        if is_shortcut and os.path.exists(path):
            try:
                path = get_shortcut_path(path)
            except Exception:
                pass

        if os.path.isfile(path) or is_valid_url(path):  
            open_with(path, 'open')
            if is_insert:
                self.insert_ent(self.ent_in_path)
                self.render_content(path=self.ent_in_path, is_shortcut=True, is_insert=True)
            self.show_bottom_info(path, 'open') 
            return

        self.insert_ent(get_text(path or HOME))  
        self.clear_widgets() 

        path_type = self.get_path_type(path)
        if path_type:  
            self.navigator.navigate_to(path)  
        
        if path_type == HOME:
            self.show_home_page()
            self.set_home_fra()
        elif os.path.isdir(path) or path_type == RECYCLE_BIN:
            if self.fill_view(path) is False:
                return
            else:
                self.master.after(0, self.set_table_view)
        else:  
            messagebox.error(f"{get_text('not_found')} {path}")
            if is_back:  
                self.go_back()  
            elif is_up:
                self.move_up()
            elif is_insert:
                self.insert_ent(self.ent_in_path)
                self.render_content(path=self.ent_in_path, is_shortcut=True, is_up=True)
            return

        if path_type == 'folder':  
            text = text or get_basename(path)  
        elif path_type == DISK:  
            text = get_disk_name(path)
            image_text = get_disk_type(path) 
        else:  
            text = text or get_text(path_type)

        if is_tab:  
            self.config_tab(text, image_text or path_type)  
        self.load_tree_view(path)
        self.show_info(path, image_text or path_type)  

    def config_tab(self, text, image_text=None):
        image = get_image(image_text, self.master.data.SIZE['tab'])
        text = get_text(text).ljust(15)
        current_tab_index = self.tab_manager.tab_bar.select()
        self.tab_manager.tab_bar.tab(current_tab_index, text=text, image=image)

    def config_but(self, path_type=None):  
        path_type = path_type or self.get_path_type(self.input_ent.get())
        navigation_but_states = {  
            'left': 'normal' if self.navigator.is_back() and self.get_path_type(self.navigator.backward_stack[0]) != '' else 'disabled',  
            'right': 'normal' if self.navigator.is_forward() and self.get_path_type(self.navigator.forward_stack[0]) != '' else 'disabled',  
            'up': 'normal' if path_type != HOME else 'disabled',
            'recent': 'normal',
            'search': 'normal' if path_type not in (HOME, RECYCLE_BIN) else 'disabled',
            'options': 'normal' if path_type != HOME else 'disabled',
        }  
        
        for button_group_name, buttons in self.left_but_groups.items():  
            for name, button in buttons.items():  
                if button_group_name == 'action':  
                    if path_type in (HOME, RECYCLE_BIN):  
                        state = 'disabled'  
                    elif self.table_view.selection():  
                        state = 'normal'  
                    elif name in ('newly_built', 'open_with', 'attribute', 'options'):  
                        state = 'normal'  
                    else: 
                        state = 'disabled'  
                else: 
                    state = navigation_but_states.get(name, 'disabled')  
    
                button.config(state=state) 

        if path_type not in (HOME, RECYCLE_BIN):
            self.action_buts['left']['paste'].config(state='normal' if self.master.data.clipboard else 'disabled')

    def insert_ent(self, text):
        self.input_ent.delete(0, 'end')
        self.input_ent.insert(0, text)

    def focus_node(self, path, parent_id=''):
        path = os.path.normpath(path)
        if path in (HOME, get_text(HOME)):
            self.select_item(self.home_node)
            return

        for node_id in self.tree_view.get_children(parent_id):
            if self.get_item(node_id) == path:
                self.select_item(node_id)
                return
            else:
                for node_child_id in self.tree_view.get_children(node_id):
                    if self.get_item(node_child_id) == path:
                        self.select_item(node_child_id)
                        return

        disk, _ = os.path.splitdrive(path)
        for disk_node_id in self.tree_view.get_children(self.disk_node):
            if self.get_item(disk_node_id).startswith(disk):
                self.select_item(disk_node_id)
                return

    def fill_view(self, path):
        def get_files(path):
            if self._check_not_recycle_bin():
                try:
                    files = os.listdir(path)
                    update_function = _update_directory_items
                    header_text = get_text('file_modify_date'), get_text('file_size')  
                except Exception as e:
                    messagebox.warning(str(e))
                    self.navigator.go_back()
                    self.move_up()
                    return False, None, None      
            else:
                files = get_recycle_bin_info() 
                update_function = _update_recycle_items
                header_text = get_text('file_recycle_date'), ''     

            return files, update_function, header_text

        def update_view():  
            self.clear_item()  
            for file in files: 
                update_function(file) 

        def _update_recycle_items(file_info):
            self.add_item(file_info['name'], file_info['rtime'], file_info['type'], text=file_info['path'])

        def _update_directory_items(file):  
            join_path = os.path.join(path, file)
            file_info = get_file_info(join_path)
            if file_info:
                self.add_item(file_info['name'], file_info['mtime'], file_info['type'], file_info['size'], text=join_path)

        files, update_function, header_texts = get_files(path)
        if files is False:
            return files
 
        self.table_view.heading(1, text=header_texts[0])  
        self.table_view.heading(3, text=header_texts[1]) 
        self.config_bottom(f"{len(files)} {get_text('items_number')}", '')

        if self.pending_future and not self.pending_future.done():  
            self.pending_future.cancel()  

        if self.master.data.use_thread is True:
            self.pending_future = self.executor.submit(update_view)
        else:
            update_view()

    def show_info(self, path, image_text=None, is_type=False):
        path_type = self.get_path_type(path)
        if path_type == DISK:
            disk_info = get_disk_info()[path]
            necessary_info = {
                'name': disk_info['disk_name'], 
                'type': disk_info['disk_type'],
            }
            more_info = {
                'disk_used': disk_info['disk_used'],
                'disk_free': disk_info['disk_free'],
                'disk_total': disk_info['disk_total'],
            }
            image_text = get_disk_type(path)
        elif os.path.exists(path):
            file_info = get_file_info(path)
            necessary_info = {
                'name': file_info['name'], 
                'type': file_info['type'],
            }
            more_info = {
                'size': file_info['size'],
                'mtime': file_info['mtime'], 
                'atime': file_info['atime'], 
                'ctime': file_info['ctime'],
            }
            is_type = True
        elif path_type == HOME:
            computer_info = get_computer_info()
            necessary_info = {
                'name': computer_info['node'], 
                'type': computer_info['version'], 
            }
            more_info = {
                'boot_time': computer_info['boot_time'],
                'processor': computer_info['processor'],
                'memory_total': computer_info['memory_total'],
                'logical': computer_info['logical'],
            }
        elif path_type == RECYCLE_BIN:
            necessary_info = {
                'name': get_text(RECYCLE_BIN), 
                'type': 'SHELL',
            }
            more_info = {}
        else:
            return

        self.config_but(path_type)
        self.config_info(
            necessary_info['name'], 
            necessary_info['type'], 
            more_info, 
            is_type,
            image_text=image_text or path_type,
        )

    def config_info(self, title, type_name, info_dict, is_type, image_text=None):
        image = get_image(image_text, self.master.data.SIZE['type']) or get_image('file', self.master.data.SIZE['type'])
        type_text = get_type_text(type_name) if is_type else type_name

        self.type_img_lab.config(image=image)
        self.title_lab.config(text=title)
        self.type_lab.config(text=type_text)

        for lab in self.info_bar_but:
            lab.destroy()

        self.info_bar_but.clear()

        for text, info in info_dict.items():
            if info:
                lab = ttk.Label(self.info_bar_fra, text=f"{get_text(text)}\n{info}", font=(self.master.data.FONT, 10), wraplength=180)
                lab.pack(padx=5, anchor='nw', pady=4)
                self.info_bar_but.append(lab)

    def show_bottom_info(self, path=None, message=None, info_text=None):  
        if info_text is None:
            name = get_basename(path)  
            size = get_size(path)
            info_text = f'{get_text(message)} {name}   {size}'  
        self.config_bottom(info_text=info_text)  

    def config_bottom(self, number_text=None, info_text=None):
        if number_text is not None:
            self.items_number_but.config(text=number_text)
        if info_text is not None:
            self.project_info_but.config(text=info_text)

    def add_node(self, text, value=None, image=None, parent='', open=False, tags=''):
        value = value or text
        image = image or text
        return self.tree_view.insert(
            parent, 
            'end', 
            text=get_text(text), 
            values=(value.replace('\\', '/'), image),
            image=get_image(image, self.master.data.SIZE['path']), 
            open=open,
            tags=('tree_view', tags))

    def add_item(self, name, time, type_, size='', text='', image=None, tags=''):
        image = get_image(type_, self.master.data.SIZE['files']) or get_image('file', self.master.data.SIZE['files'])
        self.table_view.insert(
            '', 
            'end', 
            image=image,
            text=text,
            values=(name, time, get_type_text(type_), size),
            tags=('table_view', tags))

    def get_item(self, node_id, option='path', parent=None):
        parent = parent or self.tree_view
        if option == 'path':
            value = parent.item(node_id, 'values')[0] if parent == self.tree_view else parent.item(node_id, 'text')
            return os.path.normpath(value)
        else:
            return parent.item(node_id, option)

    def clear_item(self, parent=None):  
        if isinstance(parent, str):
            children = self.tree_view.get_children(parent) 
            for child in children:    
                self.clear_item(child)    
                self.tree_view.delete(child)  
        else:
            parent = parent or self.table_view
            parent.delete(*parent.get_children())  

    def select_item(self, node_id, parent=None):
        parent = parent or self.tree_view
        parent.selection_set(node_id)

    def get_selected_paths(self, get_first_file=False):
        selected_items = self.table_view.selection()
        if selected_items:
            selected_paths = [self.get_item(item, parent=self.table_view) for item in selected_items]
            if get_first_file:
                return selected_paths[0]
            return selected_paths
        return None

    def select_all(self, event=None):
        for item in self.table_view.get_children():
            self.table_view.selection_add(item)

    def not_select(self, event=None):
        for item in self.table_view.selection():
            self.table_view.selection_remove(item)
        self.config_bottom(info_text='')

    def invert_select(self, event=None):
        for item in self.table_view.get_children():
            if item in self.table_view.selection():
                self.table_view.selection_remove(item)
            else:
                self.table_view.selection_add(item)

    def bind_events(self):
        def ent_out(event):
            get_path = self.input_ent.get()
            if get_path != '':
                self.render_content(path=get_path, is_shortcut=True, is_insert=True)
            else:
                self.render_content(path=HOME)

        def ent_in(event):
            self.ent_in_path = os.path.normpath(self.input_ent.get())        

        def select_node(event):
            node_id = event.widget.identify_row(event.y)
            if node_id != '':
                path = self.get_item(node_id)
                text = self.get_item(node_id, 'text')
                image = self.get_item(node_id, 'values')[1]
                if path and path != DISK and path != LIBRARY:
                    self.render_content(path=path, text=text, image_text=image)

        def show_menu(event):
            def add_command(text, image, command):  
                menu.add_command(  
                    label=get_text(text),  
                    command=command,  
                    image=get_image(image, self.master.data.SIZE['menu']),  
                    compound='left'  
                )  
          
            node_id = event.widget.identify_row(event.y)  
            if node_id:  
                menu = ttk.Menu(self.tree_view, tearoff=False)  
                path = self.get_item(node_id)  
                if path and path not in (DISK, LIBRARY):  
                    text = self.get_item(node_id, 'text')  
                    image = self.get_item(node_id, 'values')[1]  
                    self.render_content(path=path) 

                    open_in_tab_command = partial(self.tab_manager.add_tab, path=path, text=text, image_text=image)  
                    add_command('open_in_tab', 'add_tab', open_in_tab_command)  
          
                    if path not in (HOME, get_node_path()['user']):
                        view_attribute_command = partial(open_with, path=path, mode='properties')  
                        add_command('view_attribute', 'attribute', view_attribute_command)  
          
                menu.post(event.x_root, event.y_root)

        def select_out(event):
            item = self.table_view.identify('item', event.x, event.y)
            if item == '':
                self.not_select()

        def show_item_info(event=None):
            items = self.table_view.selection()
            path = self.input_ent.get()

            if items:
                item = items[-1]
                len_items = len(items)

                if self._check_not_recycle_bin():
                    path = self.get_item(item, parent=self.table_view)
                    self.show_info(path)                 
                else:           
                    path, rtime, type_, _ = self.get_item(item, 'values', parent=self.table_view)  
                    rpath = self.get_item(item, parent=self.table_view)
                    self.config_info(
                        path, 
                        type_, 
                        {'file_recycle_date': rtime, 'file_recycle_path': rpath}, 
                        is_type=False,
                        image_text=get_type(rpath),
                    )   
                    self.action_buts['left']['attribute'].config(state='disabled')

                if len_items == 1:
                    self.show_bottom_info(path, 'select')
                else:
                    info_text = f"{get_text('select')} {len_items} {get_text('items_number')}"
                    self.show_bottom_info(info_text=info_text)
            else:
                self.show_info(path)
                self.show_bottom_info(info_text='')

        def double_item(event):
            item = self.table_view.identify('item', event.x, event.y)
            if item != '':
                path = self.get_item(item, parent=self.table_view)
                if self._check_not_recycle_bin():
                    self.render_content(path=path, is_shortcut=True, is_up=True)

        def config_command(button_dict, event_dict, parent):  
            for side, buts in button_dict.items():  
                for name, but in buts.items():  
                    command = event_dict[side][name]
                    but.config(command=command)  

                    key = get_key(name)
                    if key:
                        # print(key, name)
                        parent.bind(key, command)

        config_command(self.navigation_buts, self.navigation_events, self.table_view)
        config_command(self.action_buts, self.action_events, self.table_view)

        for text, command in self.select_commands.items():
            key = get_key(text)
            if key:
                self.table_view.bind(key, command)

        self.input_ent.bind('<FocusOut>', ent_out)
        self.input_ent.bind('<FocusIn>', ent_in)
        self.input_ent.bind('<Return>', ent_out)
        self.tree_view.bind('<Button-1>', select_node)
        self.tree_view.bind('<Button-3>', show_menu)
        self.table_view.bind('<Button-1>', select_out)
        self.table_view.bind('<<TreeviewSelect>>', show_item_info)
        self.table_view.bind('<Double-1>', double_item)

    def go_back(self, event=None):  
        self._navigate(self.navigator.go_back)  
  
    def go_forward(self, event=None):  
        self._navigate(self.navigator.go_forward)  
  
    def _navigate(self, navigate_method):  
        path = navigate_method()  
        if path:  
            self.render_content(path=path, is_back=True)

    def show_recent(self, event=None):  
        def add_menu_items(stack, text):  
            for path in reversed(stack):  
                path_type = self.get_path_type(path)  
                if path_type != '':  
                    label = get_basename(path)  
                    image = get_image(text, self.master.data.SIZE['menu'])  
                    command = partial(self.render_content, path=path, is_back=True)  
                    self.recent_menu.add_command(label=label, command=command, image=image, compound='left')  
  
        current_path, backward_stack, forward_stack = self.navigator.get_history()  
        self.recent_menu = ttk.Menu(self, tearoff=False)  
  
        if current_path:  
            add_menu_items([current_path], 'correct')  
        if backward_stack:  
            self.recent_menu.add_separator()  
            add_menu_items(backward_stack, 'left')  
        if forward_stack:  
            self.recent_menu.add_separator()  
            add_menu_items(forward_stack, 'right')  
  
        x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()  
        self.recent_menu.tk_popup(x, y)

    def move_up(self, event=None):
        path = self.input_ent.get()
        up_path = os.path.dirname(path)
        if up_path == path or up_path == '':
            up_path = HOME
        self.render_content(path=up_path, is_up=True)

    def get_folder(self, event=None):
        d = tree_askdirectory(self.master.winfo_id, get_text('select_to_open'))
        if d and os.path.exists(d):
            self.render_content(path=d, is_shortcut=True)

    def search(self, event=None):
        # The default search function of the system is temporarily used
        file = self.input_ent.get()
        threading.Thread(target=os.startfile, args=(file, 'find',), daemon=True).start()

    def refresh(self, event=None):
        path = self.input_ent.get()
        self.render_content(path=path, is_up=True)
        # update_read_json()
        # update_extensions_descs()
        
    def newly_built(self, event=None, root_menu=None):
        def add_command(text):  
            label_text = get_type_text(text)  
            filename = label_text if text in ('folder', 'file') else label_text + text  
            image = get_image(text, self.master.data.SIZE['menu'])  
            command = partial(self.master.controller_window.newly_built, self.input_ent.get(), text, filename)  
            menu.add_command(label=label_text, image=image, compound='left', command=command)  
  
        def create_and_show_menu():  
            for file_type in self.master.data.newly_built_types:  
                if file_type:  
                    add_command(file_type)  
                else:  
                    menu.add_separator()  

            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()  
            menu.tk_popup(x, y)  
  
        if self._check_not_recycle_bin():
            menu = root_menu or ttk.Menu(self, tearoff=False)
            create_and_show_menu() 

    def _set_clipboard(self, mode):  
        files = self._get_files()
        if files:
            self.master.data.clipboard = {'mode': mode, 'files': files}  
            self.config_but()

    def shear(self, event=None):
        self._set_clipboard('shear') 

    def copy(self, event=None):
        self._set_clipboard('copy') 

    def paste(self, event=None):
        path = self.input_ent.get()
        clipboard_data = self.master.data.clipboard  
        if clipboard_data:  
            files = clipboard_data.get('files')  
            mode = clipboard_data.get('mode') 
            self.master.data.clipboard = None
            if files:
                if mode == 'shear':
                    move_file(files, path)
                elif mode == 'copy':
                    copy_file(files, path)
        self.config_but()

    def _check_not_recycle_bin(self):  
        if self.input_ent.get() == RECYCLE_BIN_SHELL:  
            return False  
        return True  

    def _get_files(self, get_first_file=False):  
        if self._check_not_recycle_bin():  
            return self.get_selected_paths(get_first_file)  
        return []

    def _ask_directory(self, function): 
        files = self._get_files()
        if files:
            d = askdirectory()  
            if d and os.path.exists(d):  
                function(files, os.path.normpath(d))  
            self.config_but()  

    def rename(self, event=None):
        file = self._get_files(True)
        if file:
            self.master.controller_window.rename(file)

    def copy_to(self, event=None):
        self._ask_directory(copy_file) 

    def move_to(self, event=None):
        self._ask_directory(move_file) 

    def recycle(self, event=None):
        files = self._get_files()
        if files:
            recycle_file(files)
            self.config_but()

    def delete(self, event=None):
        # Since fo.DeleteItem limitations, using a winshell library to delete files one by one
        files = self._get_files()
        if files:
            for file in files:
                try:
                    delete_file(file, self.master.winfo_id)
                except Exception:
                    pass

            self.config_but()

    def attribute(self, event=None):
        file = self._get_files(True)
        if not file:
            file = self.input_ent.get()
        if file:
            open_with(file, 'properties')

    def open(self, event=None):
        file = self._get_files(True)
        if file:
            self.render_content(path=file, is_shortcut=True, is_up=True)

    def open_with(self, event=None, root_menu=None):
        def add_command(text):
            command = partial(open_with, file, text)  
            label_text = get_text(text)
            menu.add_command(label=label_text, command=command, image=get_image(text, self.master.data.SIZE['menu']), compound='left')

        menu = root_menu or ttk.Menu(self, tearoff=False)
        if not root_menu:
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()

        file_command_texts = ['edit', 'print', 'runas']
        folder_command_texts = ['explore', 'cmd', 'PowerShell'] 

        file = self._get_files(True)
        if not file:
            file = self.input_ent.get()

        if os.path.isfile(file):
            texts = file_command_texts
        else:
            texts = folder_command_texts

        for text in texts:
            add_command(text)

        if not root_menu:
            menu.tk_popup(x, y)

    def more(self, event=None, root_menu=None):
        def add_command(text):
            # This feature is not developed.
            command = None
            label_text = get_text(text)
            menu.add_command(label=label_text, command=command, image=get_image(text, self.master.data.SIZE['menu']), compound='left')

        menu = root_menu or ttk.Menu(self, tearoff=False)
        if not root_menu:
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()

        texts = ['theme', 'demo', 'license', 'help', 'about']
        for text in texts:
            add_command(text)

        if not root_menu:
            menu.tk_popup(x, y)

    def setting(self, event=None):
        # This feature is not developed.
        pass

    def layout(self, event=None):
        # This feature is not developed.
        pass

    def sort(self, event=None):
        # This feature is not developed.
        pass

    def options(self, event=None):
        def add_command(text, command):
            label_text = get_tip(text)
            menu.add_command(label=label_text, command=command, image=get_image(text, self.master.data.SIZE['menu']), compound='left')

        menu = ttk.Menu(self, tearoff=False)
        for text, command in self.select_commands.items():
            add_command(text, command)

        x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()
        menu.tk_popup(x, y)
