import os
import logging
import configparser
import importlib.util 

import chardet


cfg_config = configparser.ConfigParser()
logger = logging.getLogger('logger')


def remove_file(path):
    if os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            pass


def get_config_option(path, section, option, get_option=None):
    if os.path.isfile(path):
        try:
            cfg_config.read(path, encoding=detect_file_encoding(path))
            if cfg_config.has_section(section) and cfg_config.has_option(section, option):
                get_option = cfg_config.get(section, option)
        except Exception as e:
            logger.info(e)
    return get_option


def get_user_module(path):
    spec = importlib.util.spec_from_file_location("user_module", path)
    user_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_module)
    return user_module


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def create_file(path, get_str=''):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:  
            f.write(get_str)
    return path
