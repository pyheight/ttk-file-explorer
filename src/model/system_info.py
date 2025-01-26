import os
import ctypes
import psutil 
import platform
import win32api
import win32file  
from uuid import UUID
from ctypes import wintypes
from win32com.shell import shell

import winshell

from constants.settings import ENCOD
from model.builtin_transform import convert_size, convert_time, convert_date_zone


class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', wintypes.DWORD),
        ('Data2', wintypes.WORD),
        ('Data3', wintypes.WORD),
        ('Data4', wintypes.BYTE * 8)
    ]

    def __init__(self, uuidstr):
        uuid = UUID(uuidstr)
        ctypes.Structure.__init__(self)
        self.Data1, self.Data2, self.Data3, \
            self.Data4[0], self.Data4[1], rest = uuid.fields
        for i in range(2, 8):
            self.Data4[i] = rest >> (8-i-1)*8 & 0xff


FOLDERID_DOWNLOAD = '{374DE290-123F-4565-9164-39C4925E467B}'
SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
SHGetKnownFolderPath.argtypes = [
    ctypes.POINTER(GUID), wintypes.DWORD,
    wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
]


HOME = 'home'
RECYCLE_BIN_SHELL = 'shell:RecycleBinFolder'
RECYCLE_BIN = 'recycle_bin'
DISK = 'disk'
LIBRARY = 'library'


def get_system_encoding():  
    try:
        GetACP = ctypes.windll.kernel32.GetACP  
        GetACP.restype = ctypes.c_int  
        code_page = GetACP()  
        code_page_name = 'cp{}'.format(code_page)  
    except Exception:
        code_page_name = ENCOD
    return code_page_name  


def get_expanduser_path(folder):
    path = os.path.normpath(os.path.join(os.path.expanduser('~'), folder))
    return path if os.path.exists(path) else None


def get_path(folder_id, folder=None):  
    try:  
        return shell.SHGetFolderPath(0, folder_id, None, 0)  
    except Exception:  
        return get_expanduser_path(folder)


def get_download_path():
    pathptr = ctypes.c_wchar_p()
    guid = GUID(FOLDERID_DOWNLOAD)
    if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
        return get_expanduser_path('Downloads')
    return pathptr.value


def get_node_path():
    path = {
        'user': get_expanduser_path(''),
        'favorites': get_path(6, 'Favorites'),
        'recycle_bin': RECYCLE_BIN_SHELL,
    }

    return path


def get_library_path():
    path = { 
        'desktop': get_path(0, 'Desktop'),
        'documents': get_path(5, 'Documents'), 
        'downloads': get_download_path(),  
        'pictures': get_path(39, 'Pictures'), 
        'music': get_path(13, 'Music'), 
        'videos': get_path(14, 'Videos'), 
    } 

    return path


def get_disk_name(path):
    # f-string expression part cannot include a backslash    
    return f"{win32api.GetVolumeInformation(path)[0]} ({path}".rstrip('\\') + ')' 


def get_disk_type(path):  
    disk, tail = os.path.splitdrive(path)  
    disk_type = win32file.GetDriveType(disk)  
    if disk_type == win32file.DRIVE_REMOVABLE:
        return 'USB'
    elif disk_type == win32file.DRIVE_CDROM:
        return 'CD'
    elif is_system_disk(path):
        return 'system_disk'
    else:
        return 'disk'


def is_system_disk(path): 
    system_root = win32api.GetEnvironmentVariable("SystemRoot")  
    system_disk = os.path.splitdrive(system_root)[0] 
    disk, _ = os.path.splitdrive(path)  
    return disk.lower() == system_disk.lower()  


def get_disk_info():  
    info = {}  
    disks = psutil.disk_partitions()  
    for disk in disks:
        disk_mountpoint = disk.mountpoint 
        try:
            disk_usage = psutil.disk_usage(disk_mountpoint)

            info[disk_mountpoint] = {  
                'disk_name': get_disk_name(disk_mountpoint), 
                'disk_type': disk.fstype,
                'disk_total': convert_size(disk_usage.total),  
                'disk_used': convert_size(disk_usage.used),  
                'disk_free': convert_size(disk_usage.free),  
                'disk_percent': disk_usage.percent,
            }  
        except Exception:
            pass

    return info   


def get_computer_info():
    info = {
        'node': platform.node(),
        'version': f'{platform.system()} {platform.version()} {platform.architecture()[0]}',
        'boot_time': convert_time(psutil.boot_time()),
        'processor': platform.processor(),
        'memory_total': convert_size(psutil.virtual_memory().total),
        'logical': psutil.cpu_count(logical=True),
    }

    return info


def get_extension(path):
    basename = os.path.basename(path)
    if basename.startswith('.'): 
        new_basename = basename[1:]
        if '.' in new_basename:
            return get_extension(new_basename)
        else:
            return basename
    else:  
        return os.path.splitext(path)[1]


def get_basename(path):
    return os.path.basename(path) or path


def get_type(path):
    return 'folder' if os.path.isdir(path) else get_extension(path)   


def get_size(path):
    return convert_size(os.path.getsize(path)) if os.path.isfile(path) else ''


def get_file_info(path):
    path = os.path.normpath(path)
    try:
        file_stat = os.stat(path)
    except Exception:
        return None
    info = {
        'name': get_basename(path),
        'type': get_type(path),        
        'size': get_size(path),
        'mtime': convert_time(file_stat.st_mtime), 
        'atime': convert_time(file_stat.st_atime), 
        'ctime': convert_time(file_stat.st_ctime),
    }  

    return info


def get_recycle_bin_info():
    recycle_bin = winshell.recycle_bin()  
    info = []
    for item in recycle_bin: 
        path = item.original_filename()
        info.append({
            'path': path,
            'name': os.path.basename(path),
            'type': 'folder' if os.path.isdir(path) else get_extension(path), 
            'rtime': convert_date_zone(item.recycle_date()),
        })

    return info
