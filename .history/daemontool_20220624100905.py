import os
import logging
import winreg
import time
import json

def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def get_all_path(rootdir):
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
    return os.getcwd()


def join_path(path, file):
    return os.path.join(path, file)



def get_current_time(format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, time.localtime())


def logorder(func):
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

    @logorder
    def info(self, msg):
        pass
    
    @logorder
    def debug(self, msg):
        pass
    
    @logorder
    def warning(self, msg):
        pass
    
    @logorder
    def error(self, msg):
        pass


def timethis(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = round((time.time() - start), 3)
        print(f'{func.__name__} running time: {end}sec.')
        return result
    return wrapper


def mkdir(path):
    path = path.strip().rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f'{path} existed!')


def dict2json(target_dict, json_name, json_path):
    file = join_path(json_path, f'{json_name}.json')
    if not os.path.exists(json_path):
        mkdir(json_path)
    content = json.dumps(target_dict, indent=4)
    with open(file, 'w') as json_file:
        json_file.write(content)


def json2dict(json_path):
    with open(json_path,'r', encoding='UTF-8') as f:
        return json.load(f)



SEP = os.sep
DESKTOP = desktop_path()


if __name__ == '__main__':
    test_dict = {
        'keyone': 1,
        'keytwo': 2,
        'keythree': 3
    }
    path = DESKTOP + SEP + 'testfolder' + SEP + 'Hello'
    dict2json(test_dict, 'test', path)
    # print(json2dict(DESKTOP + SEP + 'testfolder' + SEP + 'Hello' + SEP + 'test.json'))