import winreg 

from constants.paths import TRANSLATION_PATH, KEY_PATH
from constants.keys import DEFAULT_KEYS_DICT
from constants.texts import DEFAULT_TEXTS_DICT
from constants.images import DEFAULT_DATA_DICT
from model.image_converter import tk_image
from model.builtin_transform import get_dict_value, read_json_file


def update_read_json():
    global translations_dict, keys_dict
    translations_dict = read_json_file(TRANSLATION_PATH, DEFAULT_TEXTS_DICT)
    keys_dict = read_json_file(KEY_PATH, DEFAULT_KEYS_DICT)


def format_type_text(text):
    if text.startswith('.'):
        text = text[1:]
    text = text.upper()
    space = ' ' if text.isascii() else ''
    text = f"{text}{space}{get_text('file')}"
    return text


def get_extensions_descs():  
    file_extensions = {}  
    file_descs = {} 
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, '') as root_key:  
        i = 0  
        while True:  
            try:  
                subkey_name = winreg.EnumKey(root_key, i)  
                data_dict = file_extensions if subkey_name.startswith('.') else file_descs

                try:  
                    with winreg.OpenKey(root_key, subkey_name) as subkey:  
                        try:  
                            desc = winreg.QueryValueEx(subkey, '')[0]
                        except FileNotFoundError:
                            desc = format_type_text(subkey_name)
                        data_dict[subkey_name] = desc   
                except FileNotFoundError: 
                    pass                       
                i += 1  
            except OSError:  
                break   
      
    return file_extensions, file_descs
  

update_read_json()


def get_text(name):
    text = get_dict_value(name, translations_dict, DEFAULT_TEXTS_DICT)
    return text if text else name


def update_extensions_descs():
    global file_extensions, file_descs
    file_extensions, file_descs = get_extensions_descs()


update_extensions_descs()


def get_type_text(file_type):
    if file_type in ('folder', 'file', '.lnk', '.exe', '.dll', '.ini', '.txt'):
        type_text = get_text(file_type)
    else:
        desc = file_extensions.get(file_type)
        if desc:
            type_text = file_descs.get(desc, None)
            if not type_text or type_text == file_type:
                type_text = format_type_text(file_type)
        else:
            type_text = format_type_text(file_type)
    return type_text


def get_key(name):  
    return get_dict_value(name, keys_dict, DEFAULT_KEYS_DICT)


def get_key_binding(binding):    
    stripped_binding = get_key(binding)  

    return f" ({stripped_binding.lstrip('<').rstrip('>').replace('-', '+')})" if stripped_binding else ''


def get_tip(name):
    text = str(get_text(name))
    key_binding = get_key_binding(name)
    
    return text + key_binding


def image_loader(master):
    global IL
    IL = ImageLoader(master)


def get_image(name, size=(15, 15)):
    return IL.get_image(name, size)


class ImageLoader:    
    def __init__(self, master):    
        self.master = master  
        self.master.images = {}    

    def get_image(self, name, size):
        theme_key = f'{name}_{size}'
        image = self.master.images.get(theme_key)  
      
        if not image:  
            for key in DEFAULT_DATA_DICT:  
                image_data = DEFAULT_DATA_DICT[key] 
                image_data = image_data.get(name)  
                if image_data:  
                    image = tk_image(image_data, size)
                    self.master.images[theme_key] = image
                    break  

        return image


class ViewConfigurator:
    def __init__(self, master):
        self.now_theme_names = master.style.theme_names()
        self.HIGHLIGHT_BG = master.highlight        
        self.IS_REVERSE = True
        self.SORTING_WAY = 'name'
        self.FONT = '微软雅黑'
        self.use_thread = False
        self.clipboard = None
        self.VIEW = {  
            'tree_view': {  
                'height': 31,  
                'font': (self.FONT, 10, 'normal', 'normal'),  
            },  
            'table_view': {  
                'height': 30,  
                'font': (self.FONT, 12, 'normal', 'normal'),  
            },  
        }
        
        self.IS_OPEN = {
            'favorites': True,
            'library': True,  
            'disk': True, 
            'library_cf': True,
            'disk_cf': True,    
            'quick_access_cf': True,
            'recent_file_cf': True,
        }

        self.SIZE = {
            'disk': (35, 35),
            'type': (94, 94),
            'tab': (18, 18),
            'navigation': (19, 19),
            'action': (21, 21),
            'path': (20, 20),
            'files': (23, 23),
            'menu': (20, 20),
        }

        self.newly_built_types = [  
            'folder',  
            'file',  
            '.lnk',
            '',
            '.bmp',  
            '.png',  
            '.doc',
            '.docx',  
            '.pdf',  
            '.ppt',
            '.pptx',  
            '.rtf',  
            '.txt',  
            '.xls',
            '.xlsx',  
            '.zip',  
        ] 


class PathNavigator:  
    def __init__(self):    
        self.forward_stack = []    
        self.backward_stack = []      
        self.current_path = None    
    
    def navigate_to(self, path):    
        if self.current_path and self.current_path != path:    
            if self.current_path not in self.backward_stack:    
                self.backward_stack.append(self.current_path)   
            self.forward_stack.clear()    
        self.current_path = path 
  
        # print(f'Navigated to: {self.current_path}')  
    
    def go_back(self):    
        if not self.is_back():    
            # print('Cannot go back further.')  
            return  
  
        self.forward_stack.append(self.current_path)  
        self.current_path = self.backward_stack.pop()  
        # print(f'Went back to: {self.current_path}')  
        return self.current_path  

    def go_forward(self):    
        if not self.is_forward():
            # print('Cannot go forward.')  
            return  
        self.backward_stack.append(self.current_path)  
        self.current_path = self.forward_stack.pop()  
        # print(f'Went forward to: {self.current_path}')  
        return self.current_path  

    def get_history(self):   
        return self.current_path, self.backward_stack, self.forward_stack  
  
    def is_back(self):  
        return bool(len(self.backward_stack) > 0) 
  
    def is_forward(self):  
        return bool(len(self.forward_stack) > 0) 
