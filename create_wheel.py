from dmutil import (
    __version__, 
    progressbar, 
    sysc, 
    os, 
    sys,
    timethis
)

command =  sysc
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


class WheelMaker():
    """
    auto make one library file
    """
    def __init__(self):
        self.setup_path = join(os.getcwd(), 'setup.py')
        self.dist_path  = join(os.getcwd(), 'dist')
        self.egg_path   = join(os.getcwd(), 'dmutil.egg-info')

    def __call__(self):
        self.auto_build(_progress_bar=None)

    def create_setup(self, _progress_bar):
        """create temp setup.py"""
        _progress_bar.print('creating temp setup.py')
        with open('./setup.py', 'w') as setup:
            writecode = lambda code: setup.write(code + '\n')
            writecode("from setuptools import setup")
            writecode("setup(")
            writecode("    name='dmutil',")
            writecode("    version='{}',".format(__version__))
            writecode("    author='Daemon Huang',")
            writecode("    author_email='morningrocks@outlook.com',")
            writecode("    url='',")
            writecode("    install_requires=['tqdm','openpyxl', 'nuitka', 'cryptography'],")
            writecode("    python_requires='>=3.8',")
            writecode("    py_modules=['dmutil'],")
            writecode(")")
        _progress_bar.write('temp setup.py creation completed!')

    def remove_old(self,_progress_bar):
        """remove old dist folder"""
        # in windows need to use "{path}" to include the path, not '{path}'
        _progress_bar.print('removing old module')
        command(f'{rm}"./*.tar.gz"', printfunction=_progress_bar.write)
        _progress_bar.print('done')

    def make_lib(self, _progress_bar):
        """make lib"""
        _progress_bar.print('installing wheel')
        command(f'pip install wheel', printfunction=_progress_bar.write)
        _progress_bar.print('updating pip')
        command(f'{uppip}', printfunction=_progress_bar.write)
        _progress_bar.print('making wheel file')
        command(f'python "{self.setup_path}" sdist', printfunction=_progress_bar.write)
        _progress_bar.print('removing temp setup.py and egg-info folder')
        command(f'{rm}"{self.setup_path}"', printfunction=_progress_bar.write)
        command(f'{rm_rf}"{self.egg_path}"', printfunction=_progress_bar.write)
        
    def if_install(self, _progress_bar):
        """ask if need to install lib"""
        lib_path = join(self.dist_path, os.listdir(self.dist_path)[0])
        lib_name = os.listdir(self.dist_path)[0]
        _progress_bar.print('moving module to current location')
        command(f'{mv}"{lib_path}" .', printfunction=_progress_bar.write)
        _progress_bar.print('removing dist folder')
        command(f'{rm_rf}"{self.dist_path}"', printfunction=_progress_bar.write)
        # need_install = input('Do you need install it now? y/n ')
        # if need_install == 'y':
        _progress_bar.print('installing module')
        command(f'{install}"./{lib_name}"', printfunction=_progress_bar.write)
        _progress_bar.print('installation complete')

    @timethis
    @progressbar(estimated_time=4.5, tstep=0.1, progress_name='Wheel Creating Process')
    def auto_build(self, _progress_bar):
        """auto run sequence"""
        self.create_setup(_progress_bar)
        self.remove_old(_progress_bar)
        self.make_lib(_progress_bar)
        self.if_install(_progress_bar)
        _progress_bar.write("wheel creation completed.")

    @classmethod
    def installation(cls):
        """"for installation used only"""
        lib_name = [x for x in os.listdir('.') if 'tar.gz' in x ][0]
        command(f'{install}"./{lib_name}"')

if __name__ == '__main__':
    WheelMaker()()



