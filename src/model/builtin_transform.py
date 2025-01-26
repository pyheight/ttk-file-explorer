import time
import logging
from datetime import datetime 
import json
import re
from dateutil import tz  

from model.profile_operation import detect_file_encoding


logger = logging.getLogger('logger')
date_format = '%Y/%m/%d %H:%M:%S'
local_tz = tz.gettz()  


def is_disk(path): 
    drive_pattern = r'^[A-Za-z]:[\\/]?$'  
    return bool(re.match(drive_pattern, path))  


def get_dict_key(d, find_value):
    return next((key for key, value in d.items() if value == find_value), None)


def convert_date_zone(date):
    local_date = date.astimezone(local_tz)   
    formatted_time = local_date.strftime(date_format) 

    return formatted_time


def convert_date_iso(date):
    if date:
        try:
            date = datetime.fromisoformat(date) 
            formatted_date = date.strftime(date_format)
        except ValueError as e:
            print(f"Error parsing date: {date}, Error: {e}")
            return None
        return formatted_date


def convert_time(time_, date_format=date_format):
    try:
        return time.strftime(date_format, time.localtime(int(time_)))
    except Exception:
        return ''


def convert_size(size):  
    def round_size(s):
        return round(s, 2)
    if size < 1024:    
        return f'{round_size(size)} B'    
    elif size < 1024 ** 2:    
        return f'{round_size(size / 1024)} KB'    
    elif size < 1024 ** 3:    
        return f'{round_size(size / (1024 ** 2))} MB'    
    elif size < 1024 ** 4:    
        return f'{round_size(size / (1024 ** 3))} GB'    
    else:  
        return f'{round_size(size / (1024 ** 4))} TB'


def get_dict_value(name, try_dict, default_dict):  
    def search_dict(d): 
        for name_, dict_ in d.items(): 
            if name in dict_:  
                get = dict_[name] 
                return get
        return ''  

    result = search_dict(try_dict)  
    if result != '':
        return result 

    return search_dict(default_dict)


def read_json_file(path, default_contents):
    try:
        with open(path, 'r', encoding=detect_file_encoding(path)) as f:
            get_contents = json.load(f)
    except Exception as e:
        logger.info(e)
        get_contents = default_contents

    return get_contents
