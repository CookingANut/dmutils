VERSION = '3.61'

import os
import logging
import platform
import time
import json
if platform.system() == "Windows":
    import winreg
import argparse
from datetime import datetime as dt
import zipfile
from contextlib import contextmanager
import subprocess


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
            if not self.savelog:
                if self.branch:
                    getattr(logging, func.__name__)(msg=f"[{self.branch}] - {msg}")
                else:
                    getattr(logging, func.__name__)(msg=f" {msg}")
            else:
                if self.branch:
                    getattr(self.logger, func.__name__)(msg=f"[{self.branch}] - {msg}")
                else:
                    getattr(self.logger, func.__name__)(msg=f" {msg}")
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
        'debug'  : logging.DEBUG,
        'info'   : logging.INFO,
        'warning': logging.WARNING,
        'error'  : logging.ERROR
    }

    format = '%(asctime)s [%(levelname)s]%(message)s'

    def __init__(self, branch=None, llevel='debug', showlog=True, savelog=None):
        self.showlog = showlog
        self.branch = branch
        self.savelog = savelog

        if not savelog:
            logging.basicConfig(level=self.level_relation[llevel], format=self.format)
        else:
            os.remove(savelog)
            fh = logging.FileHandler(savelog)
            sh = logging.StreamHandler()
            ft = logging.Formatter(self.format)
            fh.setLevel(self.level_relation[llevel])
            sh.setLevel(self.level_relation[llevel])
            fh.setFormatter(ft)
            sh.setFormatter(ft)

            self.logger = logging.getLogger()
            self.logger.setLevel(self.level_relation[llevel])
            self.logger.addHandler(fh)
            self.logger.addHandler(sh)

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

    @__logorder__
    def exception(self, msg):
        pass


def timethis(func):
    """A wrapper for counting functions time spent"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = round((time.time() - start), 3)
        print(f'{func.__name__} running time: {end}sec.')
        return result
    return wrapper


class CodeTimer(object):
    """
    Class for counting functions time spent\n
    use:
    with CodeTimer():
        code line;
        code line;
        ...
    """
    def __init__(self, keep_num=3):
        self.start = time.time()
        self.keep_num = keep_num

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.stop = time.time()
        self.cost = self.stop - self.start
        print(f'Time cost: {round(self.cost, self.keep_num)}sec')


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
    with open(json_path, 'r', encoding='UTF-8') as f:
        return json.load(f)


def parserinit(description, *args:dict):
    """
    add arguments for scripts
    use:
        args = parserinit(
        'Script description there',
        {'param': '-arg1', 'help': 'help1'},
        {'param': '-arg2', 'help': 'help2'},
        ....)
    then you can get arg by args.args1, args.args2 ...
    """
    parser = argparse.ArgumentParser(description=description)
    for arg in args:
        if 'param' and 'help' in arg.keys():
            parser.add_argument(arg['param'], help=arg['help'])
        else:
            raise KeyError("Wrong arguments, arg['param'] and arg['help] must need")
    return parser.parse_args()

def gettime(datestring, onlyweek=False, onlyyear=False):
    """
    Get date format

    Args:
        datestring (string): example, 20220928
        onlyweek (bool, optional):  return 39, Defaults to False.
        onlyyear (bool, optional):  return 2022 to False.

    Returns:
        "2022W39", (default)
    """
    FormatDateString = dt.strptime(datestring,"%Y%m%d")
    DateInformation = FormatDateString.isocalendar()
    year = DateInformation[0]
    week = DateInformation[1]

    if onlyweek == False and onlyyear == False:
        return f"{year}W{week}"
    elif onlyweek == True and onlyyear == False:
        return int(week)
    elif onlyweek == False and onlyyear == True:
        return int(year)
    else:
        print("can't make onlyweek and onlyyear all true!")
        return 0

class zipreader(object):
    """
    zipreader
    open a zip and return a file content

    args:
        zippath is the path of the zip file
        filekeyword is the file path in the zip you want to open

    use:
        with zipreader(zippath, filekeyword) as z:
        z is content list now
    """
    def __init__(self, zippath, filekeyword):
        with zipfile.ZipFile(zippath, "r") as z:
            for zipfile_path in z.namelist():
                if filekeyword in zipfile_path:
                    with z.open(zipfile_path, 'r') as file:
                        self.content = list(map(lambda x: x.decode(), file.readlines()))

    def __enter__(self):
        return self.content

    def __exit__(self, *_):
        pass

class DateTransformer():
    """
    Date string transformation
    """
    def __init__(self, datestring):
        datestring = datestring.replace('-','')
        _FormatDateString = dt.strptime(datestring,"%Y%m%d")
        _DateInformation = _FormatDateString.isocalendar()
        
        self.year        = int(_DateInformation[0])
        self.week        = int(_DateInformation[1])
        self.month       = int(_FormatDateString.month)
        self.quarter     = int(self.month // 4 + 1)
        self.yearweek    = f"{self.year}W{self.week}"
        self.yearmonth   = f"{self.year}M{self.month}"
        self.yearquarter = f"{self.year}Q{self.quarter}"

@contextmanager
def ignored(exception=Exception, func=lambda:None, **kwargs):
  try:
    yield
  except exception:
    func(**kwargs)

def win_resonse(cmd):
    sub = subprocess.Popen(f"{cmd}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    out, err = sub.communicate()
    return out, err

SEP            =  os.sep
DESKTOP        =  desktop_path()
CURRENTTIME    =  get_current_time()
CURRENTWORKDIR =  get_runtime_path()
CURRENTYEAR    =  int(dt.now().isocalendar()[0])
CURRENTWEEK    =  int(dt.now().isocalendar()[1])


if __name__ == '__main__':
    daemontool_log = mylogging(branch='DAEMON SAYS')
    daemontool_log.info(f'daemontool - v{VERSION}')


