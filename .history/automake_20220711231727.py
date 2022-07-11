import os

def automake():
    """auto make python file lib"""
    # remove old dist folder
    # in windows need to use "{path}" to include the path, not '{path}'
    setup_path = os.path.join(os.getcwd(), 'setup.py')
    dist_path = os.path.join(os.getcwd(), 'dist')
    os.system(f'rd /s /q "{dist_path}"')

    # make lib:
    os.system(f'python "{setup_path}" sdist')

    # ask if need to install lib:
    lib_path = os.path.join(dist_path, os.listdir(dist_path)[0])
    need_install = input('Do you need install it now? y/n ')
    if need_install == 'y':
        os.system(f'pip3 install "{lib_path}"')


if __name__ == '__main__':
    automake()
