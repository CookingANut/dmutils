import os

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


setup_path = os.path.join(os.getcwd(), 'setup.py')
lib_path = get_all_path(os.path.join(os.getcwd(), 'dist'))[0]

os.system(f'python "{setup_path}" sdist')

need_install = input('Do you need install it now? y/n')
if need_install == 'y':
    os.system(f'pip3 install "{lib_path}"')
