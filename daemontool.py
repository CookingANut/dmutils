VERSION = '3.7'

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
import openpyxl
from openpyxl.styles import Border, Side, colors, Font, PatternFill, Alignment


def desktop_path():
    """return your desktop path"""
    if platform.system() == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]
    else:
        return "/home/"


def win_resonse(cmd):
    "get windows system command response, and run command in background"
    sub = subprocess.Popen(f"{cmd}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    out, err = sub.communicate()
    return out, err


def get_path(path):
    """generate all abs path under the given path"""
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirname, filename)


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
    """
    Use: 
    with ignored(func = func, **kwargs):
        xx 
    same as 
    try: 
        xx 
    except Exception
        func
    """
    try:
        yield
    except exception:
        func(**kwargs)


class xlsxDesigner():
    """
    for openpyxl only
    """

    sggcolor = {
        'blue angel' : 'B7CEEC',
        'magic mint' : 'AAF0D1',
        'cream white': 'FFFDD0',
        'peach pink' : 'F98B88',
        'periwinkle' : 'CCCCFF'
    }

    def __init__(self, bgcolor="blue angel", hz="left", fontsize='16'):

        self.border = Border(
            top    = Side(border_style='thin', color=colors.BLACK),
            bottom = Side(border_style='thin', color=colors.BLACK),
            left   = Side(border_style='thin', color=colors.BLACK),
            right  = Side(border_style='thin', color=colors.BLACK)
        )
        self.font = Font('Candara Light',size=fontsize)
        try:
            self.fill = PatternFill('solid', fgColor=self.sggcolor[bgcolor]) 
        except KeyError:
            self.fill = PatternFill('solid', fgColor=bgcolor)
        self.alignment = Alignment(horizontal=hz,vertical='center') # left, general, right, center


class xlsxMaker():
    """
    for openpyxl only
    """

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.wb.remove(self.wb['Sheet'])

    def create_sheet(self, sheetname='undefine'):
        return self.wb.create_sheet(sheetname)

    def _get_num_colnum_dict(self):
        num_str_dict = {}
        A_Z = [chr(a) for a in range(ord('A'), ord('Z') + 1)]
        AA_AZ = ['A' + chr(a) for a in range(ord('A'), ord('Z') + 1)]
        A_AZ = A_Z + AA_AZ
        for i in A_AZ:
            num_str_dict[A_AZ.index(i) + 1] = i
        return num_str_dict

    def auto_fit_width(self, excel_name:str, sheet_name:str):
        wb = openpyxl.load_workbook(excel_name)
        sheet = wb[sheet_name]
        max_column = sheet.max_column
        max_row = sheet.max_row
        max_column_dict = {}
        num_str_dict = self._get_num_colnum_dict()
        for i in range(1, max_column + 1):
            for j in range(1, max_row + 1):
                column = 0
                sheet_value = sheet.cell(row=j, column=i).value
                sheet_value_list = [k for k in str(sheet_value)]
                for v in sheet_value_list:
                    if v.isdigit() == True or v.isalpha() == True:
                        column += 1.1
                    else:
                        column += 2.2
                try:
                    if column > max_column_dict[i]:
                        max_column_dict[i] = column
                except Exception as e:
                    max_column_dict[i] = column
        for key, value in max_column_dict.items():
            sheet.column_dimensions[num_str_dict[key]].width = value + 2
        wb.save(excel_name)

    def wirte2cell(self, sheet, design, row, column, value, fill=False):
        sheet.cell(row=row, column=column).value       = value
        sheet.cell(row=row, column=column).border      = design.border
        sheet.cell(row=row, column=column).font        = design.font
        sheet.cell(row=row, column=column).alignment   = design.alignment
        if fill:
            sheet.cell(row=row, column=column).fill   = design.fill
    
    def write2mergecell(self, sheet, design, start_row, end_row, start_column, end_column, value, fill=False):
        self.wirte2cell(sheet, design, start_row, start_column, value, fill)
        sheet.merge_cells(start_row=start_row, start_column=start_column, end_row=end_row, end_column=end_column)
    
    def save(self, xlsxname, xlsxpath):
        self.wb.save(f"{xlsxpath}{SEP}{xlsxname}.xlsx")
        

SEP            =  os.sep
DESKTOP        =  desktop_path()
CURRENTTIME    =  get_current_time()
CURRENTWORKDIR =  get_runtime_path()
CURRENTYEAR    =  int(dt.now().isocalendar()[0])
CURRENTWEEK    =  int(dt.now().isocalendar()[1])


if __name__ == '__main__':
    daemontool_log = mylogging(branch='DAEMON SAYS')
    daemontool_log.info(f'daemontool - v{VERSION}')
