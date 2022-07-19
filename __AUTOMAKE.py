# Description:scirpt for auto make one file library
# Author: Daemon Huang
# Date: 2022/07/19


import os
# os.system('pip install wheel')
# os.system('python -m pip install --upgrade pip')


class LibMaker():
    """
    auto make one library file
    """

    def __init__(self):
        self.setup_path = os.path.join(os.getcwd(), 'setup.py')
        self.dist_path = os.path.join(os.getcwd(), 'dist')
        self.egg_path = os.path.join(os.getcwd(), 'daemontool.egg-info')

    def create_setup(self):
        """create temp setup.py"""
        with open('./setup.py', 'w') as setup:
            setup.write('from setuptools import setup\n')
            setup.write('setup(\n')
            setup.write("    name='daemontool',\n")
            setup.write("    version='3.3',\n")
            setup.write("    author='Daemon Huang',\n")
            setup.write("    author_email='morningrocks@outlook.com',\n")
            setup.write("    url='',\n")
            setup.write("    install_requires=[],\n")
            setup.write("    python_requires='>=3',\n")
            setup.write("    py_modules=['daemontool'],\n")
            setup.write(")\n")
        print('temp setup.py creation completed!')

    def remove_old(self):
        # remove old dist folder
        # in windows need to use "{path}" to include the path, not '{path}'
        os.system(f'rd /s /q "{self.dist_path}"')

    def make_lib(self):
        # make lib:
        os.system(f'python "{self.setup_path}" sdist')
        os.system(f'del /f /s /q "{self.setup_path}"')
        os.system(f'rd /s /q "{self.egg_path}"')
        
    def if_install(self):
        # ask if need to install lib:
        lib_path = os.path.join(self.dist_path, os.listdir(self.dist_path)[0])
        lib_name = os.listdir(self.dist_path)[0]
        os.system(f'move "{lib_path}" .')
        os.system(f'rd /s /q "{self.dist_path}"')
        need_install = input('Do you need install it now? y/n ')
        if need_install == 'y':
            os.system(f'pip3 install "./{lib_name}"')

    def auto_build(self):
        self.create_setup()
        self.remove_old()
        self.make_lib()
        self.if_install()

    @classmethod
    def installation(cls):
        dist_path = os.path.join(os.getcwd(), 'dist')
        lib_path = os.path.join(dist_path, os.listdir(dist_path)[0])
        os.system(f'pip3 install "{lib_path}"')

if __name__ == '__main__':
    LibMaker().auto_build()



