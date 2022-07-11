# author: Daemon Huang
# date: 2022/7/11
# version: 3.1

# 2.0: WAR for winreg in linux system
# 3.0: add get_path and folder_level_X_path functions
# 3.1: update notes for all functions

import os
import logging
import platform
import time
import json
if platform.system() == "Windows":
    import winreg


def desktop_path():
    """return your desktop path"""
    if platform.system() == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]
    else:
        return "/home/"

def get_path(path):
    """generate all abs path under the given path"""
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirname, filename)

def folder_level_X_path(path, level=3):
    """return the level of the path under the given path"""
    path_list = []
    all_list = os.listdir(path)
    for i in range(len(all_list)):
        try:
            com_path = os.path.join(path, all_list[i])
        except NotADirectoryError:
            continue
        if level == 1:
            path_list.append(com_path)
        else:
            path_list.extend(folder_level_X_path(com_path, level=level-1))
    return path_list

def get_all_path(rootdir):
    """return all files abs paths in the given directory"""
    path_list = []
    all_list = os.listdir(rootdir)
    for i in range(len(all_list)):
        com_path = os.path.join(rootdir, all_list[i])
        if os.path.isfile(com_path):
            path_list.append(com_path)
        if os.path.isdir(com_path):
            path_list.extend(get_all_path(com_path))
    return path_list

def get_runtime_path():
    """return Current directory path"""
    return os.getcwd()

def join_path(path, file):
    """fake os.path.join method"""
    return os.path.join(path, file)

def get_current_time(format="%Y-%m-%d %H:%M:%S"):
    """
    return Current time format in string
    default format: %Y-%m-%d %H:%M:%S
    """
    return time.strftime(format, time.localtime())

def __logorder__(func):
    """A wrapper for mylogging"""
    def wrapper(self, msg):
        if self.showlog:
            if self.branch:
                getattr(logging, func.__name__)(msg=f"[{self.branch}] - {msg}")
            else:
                getattr(logging, func.__name__)(msg=f" {msg}")
        else:
            pass
        return func(self, msg)
    return wrapper

class mylogging():
    """
    A simpl logging system
    usage:  instense this class, ex log = mylogging()
            then log.info/log.warning/log.error/log.debug ...
    branch: is the log branch name in logging
    llevel: is the shown log level in logging
    showlog: the switch to enable log or not
    """

    level_relation = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }

    def __init__(self, branch=None, llevel='debug', showlog=True):
        self.showlog = showlog
        self.branch = branch
        logging.basicConfig(level=self.level_relation[llevel],format='%(asctime)s [%(levelname)s]%(message)s')

    @__logorder__
    def info(self, msg):
        pass
    
    @__logorder__
    def debug(self, msg):
        pass
    
    @__logorder__
    def warning(self, msg):
        pass
    
    @__logorder__
    def error(self, msg):
        pass

def timethis(func):
    """A wrapper for counting functions time spent"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = round((time.time() - start), 3)
        print(f'{func.__name__} running time: {end} sec.')
        return result
    return wrapper

def mkdir(path):
    """make directorys for the given path"""
    path = path.strip().rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f'{path} existed!')

def dict2json(target_dict, json_name, json_path):
    """"dict to json"""
    file = join_path(json_path, f'{json_name}.json')
    if not os.path.exists(json_path):
        mkdir(json_path)
    content = json.dumps(target_dict, indent=4)
    with open(file, 'w') as json_file:
        json_file.write(content)

def json2dict(json_path):
    """"json to dict"""
    with open(json_path,'r', encoding='UTF-8') as f:
        return json.load(f)


SEP = os.sep
DESKTOP = desktop_path()

if __name__ == '__main__':
    daemontool_log = mylogging(branch='DAEMON SAYS')
    daemontool_log.info('welcome to use daemontool!')