import os
from daemontool import get_all_path


setup_path = os.path.join(os.getcwd(), 'setup.py')
dist_path = os.path.join(os.getcwd(), 'dist')
print(os.path.join(dist_path, os.listdir(dist_path)[0]))

# in windows need to use "{path}" to include the path, not '{path}'
os.system(f'rd /s /q "{dist_path}"')
os.system(f'python "{setup_path}" sdist')

lib_path = get_all_path(dist_path)[0]
need_install = input('Do you need install it now? y/n')
if need_install == 'y':
    os.system(f'pip3 install "{lib_path}"')

