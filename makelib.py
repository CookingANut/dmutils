import os
import sys
from daemontool import __version__


command =  os.system
join    =  os.path.join
uppip   = 'python -m pip install --upgrade pip'

if sys.platform.startswith('win'):
    rm      = 'del /f /s /q '
    rm_rf   = 'rd /s /q '
    mv      = 'move '
    install = 'pip3 install '
else:
    rm      = 'rm '
    rm_rf   = 'rm -rf '
    mv      = 'mv '
    install = 'pip install '


class LibMaker():
    """
    auto make one library file
    """
    def __init__(self):
        self.setup_path = join(os.getcwd(), 'setup.py')
        self.dist_path  = join(os.getcwd(), 'dist')
        self.egg_path   = join(os.getcwd(), 'daemontool.egg-info')

    def __call__(self):
        self.auto_build()

    def create_setup(self):
        """create temp setup.py"""
        with open('./setup.py', 'w') as setup:
            writecode = lambda code: setup.write(code + '\n')
            writecode("from setuptools import setup")
            writecode("setup(")
            writecode("    name='daemontool',")
            writecode("    version='{}',".format(__version__))
            writecode("    author='Daemon Huang',")
            writecode("    author_email='morningrocks@outlook.com',")
            writecode("    url='',")
            writecode("    install_requires=['tqdm','openpyxl'],")
            writecode("    python_requires='>=3',")
            writecode("    py_modules=['daemontool'],")
            writecode(")")
        print('temp setup.py creation completed!')

    def remove_old(self):
        """remove old dist folder"""
        # in windows need to use "{path}" to include the path, not '{path}'
        command(f'{rm}"./*.tar.gz"')

    def make_lib(self):
        """make lib"""
        command(f'{install} wheel')
        command(f'{uppip}')
        command(f'python "{self.setup_path}" sdist')
        command(f'{rm}"{self.setup_path}"') # remove temp setup.py
        command(f'{rm_rf}"{self.egg_path}"') # remove egg-info folder
        
    def if_install(self):
        """ask if need to install lib"""
        lib_path = join(self.dist_path, os.listdir(self.dist_path)[0])
        lib_name = os.listdir(self.dist_path)[0]
        command(f'{mv}"{lib_path}" .') # move lib to workspace
        command(f'{rm_rf}"{self.dist_path}"') # remove dist folder
        # need_install = input('Do you need install it now? y/n ')
        # if need_install == 'y':
        command(f'{install}"./{lib_name}"')

    def auto_build(self):
        """auto run sequence"""
        self.create_setup()
        self.remove_old()
        self.make_lib()
        self.if_install()

    @classmethod
    def installation(cls):
        """"for installation used only"""
        lib_name = [x for x in os.listdir('.') if 'tar.gz' in x ][0]
        command(f'{install}"./{lib_name}"')

if __name__ == '__main__':
    LibMaker()()



