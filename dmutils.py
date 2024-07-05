# metadata
__version__ = '1.5'  
__author__  = 'Daemon Huang'  
__email__   = 'morningrocks@outlook.com' 
__date__    = '2024-07-03'
__license__ = 'MIT'

__all__ = [
    # class
    'DmGlobalVars',
    'DmLog',
    'DmArgs',
    'DateTrans',
    'xlsxDesigner',
    'xlsxMaker',
    'NuitkaMake',
    'Py2BAT',

    # descriptor
    'DmDescriptor',

    # context manager
    'CodeTimer',
    'ZipReader',
    'Zip2Reader',
    'ignored',

    # decorator
    'timethis',
    'teewrap',

    # function
    'is_root',
    'win_desktop_path',
    'sysc',
    'get_path',
    'get_all_path',
    'resource_path',
    'read_treezip',
    'level_x_path',
    'get_runtime_path',
    'join_path',
    'get_current_time',
    'mkdir',
    'dict2json',
    'json2dict',
    'json2jsone',
    'dict2jsone',
    'openjsone',
    'merge_dicts',
    'merge_all_dicts',
    'progressbar',
    'check_your_system',
    'traceback_get',
    'traceback_print',
    'exception_get',
    'exception_print',
    'print_aligned',
    'safe_remove',
    'dedent',
    'check_return_code',
    'quickmake',
    'print_k_v_aligned',
]


class DmDescriptor:
    """
    A descriptor for enabling class methods to be called without an instance.

    This descriptor allows class methods decorated with it to be called either from an instance
    or directly from the class. If called from the class, it attempts to execute the method without
    any arguments. If called from an instance, it passes the instance as the first argument to the method.

    Attributes:
        func (callable): The function that is wrapped by the descriptor.

    Usage:
        To use this descriptor, decorate a method in a class with an instance of `DmDescriptor`.

        Example:
            class MyClass:
                @DmDescriptor
                def my_method(cls):
                    # Implementation of the method

            # Calling the method on the class directly
            MyClass.my_method
    """
    ###### import ######
    # common
    ####################

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            # call from class
            try:
                return self.func()
            except TypeError:
                print(f"Warning! Make sure to use class level to call [{self.func.__name__}]")
                return
        else:
            # call from instance
            return self.func(instance)


def _dmimport(*, from_module=None, import_module):
    """
    Dynamically imports a module or specific attributes from a module.

    This function allows for dynamic importation of modules or specific attributes by specifying
    either the module name or a comma-separated list of attribute names. It gracefully handles
    import failures by returning `None` for failed imports or an error message and exception object
    for other errors.

    Args:
        from_module (str, optional): The name of the module to import from. If `None`, treats
            `import_module` as a module name.
        import_module (str): The name of the module or attributes to import. If `from_module` is
            `None`, this is treated as a module name. Otherwise, it's treated as a comma-separated
            list of attribute names.

    Returns:
        list: A list of imported modules or attributes. Returns `None` for failed imports or a list
            containing an error message and exception object for other errors.

    Raises:
        ModuleNotFoundError: If the specified module or any attributes cannot be found.
        Exception: For any other errors that occur during the import process.

    Example:
        >>> _dmimport(from_module="os", import_module="path, getenv")
        [<module 'posixpath'>, <function getenv>]
        >>> _dmimport(import_module="json")
        <module 'json'>
    """
    ###### import ######
    # common
    ####################

    try:
        if from_module:
            module = __import__(from_module, fromlist=[import_module])
            if ',' in import_module:
                attrs = import_module.split(',')
                return [getattr(module, attr.strip()) for attr in attrs]
            else:
                return getattr(module, import_module)
        else:
            if ',' in import_module:
                modules = import_module.split(',')
                return [__import__(module.strip()) for module in modules]
            else:
                return __import__(import_module)
    except ModuleNotFoundError:
        if ',' in import_module:
            return [None for _ in import_module.split(',')]
        else:
            return []
    except Exception as e:
        return [f"from_module={from_module}::import_module={import_module} error", e]


class DmGlobalVars:
    """
    Hold global variables and configurations for this module.

    Attributes:
        os (module): Dynamically imported `os` module for OS-related operations.
        time (module): Dynamically imported `time` module for time-related operations.
        dt (module): Dynamically imported `datetime.datetime` for date and time operations.
        platform (module): Dynamically imported `platform` module for platform-related information.
        textwrap (module): Dynamically imported `textwrap` module for text wrapping and formatting.

    Properties:
        SEP (str): The path separator specific to the operating system.
        CURRENTTIME (str): The current time formatted as "YYYY-MM-DD HH:MM:SS".
        CURRENTDATE (str): The current date in "YYYY-MM-DD" format.
        CURRENTWORKDIR (str): The current working directory.
        CURRENTYEAR (int): The current year.
        CURRENTWEEK (int): The current week number of the year.
        SYSTEM (str): The name of the operating system.
        URLS (dict): A dictionary of useful URLs.
        REGIONAL_URLS (dict): A dictionary containing regional URLs.
        BATHEADER (str): A batch script header for Windows that switches stdout to the Python console.
        NUITKA_HELP (str): Help text for Nuitka options.
    """
    def __init__(self):
        ###### import ######
        self.os         = _dmimport(import_module='os')
        self.time       = _dmimport(import_module='time')
        self.dt         = _dmimport(from_module='datetime', import_module='datetime')
        self.platform   = _dmimport(import_module='platform')
        self.textwrap   = _dmimport(import_module='textwrap')
        ####################

    @property
    def SEP(self):
        return self.os.sep
    
    @property
    def CURRENTTIME(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S", self.time.localtime())
    
    @property
    def CURRENTDATE(self):
        return self.CURRENTTIME.split(" ")[0]

    @property
    def CURRENTWORKDIR(self):
        return self.os.getcwd()
    
    @property
    def CURRENTYEAR(self):
        return int(self.dt.now().isocalendar()[0])
    
    @property
    def CURRENTWEEK(self):
        return int(self.dt.now().isocalendar()[1])
    
    @property
    def SYSTEM(self):
        return self.platform.system()

    @property
    def URLS(self):
        return {
            'Pytorch'       : 'https://pytorch.org/',
            'MXNet'         : 'https://github.com/apache/incubator-mxnet',
            'FashionMNIST'  : 'https://apache-mxnet.s3-accelerate.dualstack.amazonaws.com/gluon/dataset/fashion-mnist/train-labels-idx1-ubyte.gz',
            'PYPI'          : 'https://pypi.python.org/pypi/pip',
            'Conda'         : 'https://repo.continuum.io/pkgs/free/',
        }

    @property
    def REGIONAL_URLS(self):
        return {
            'cn': {
                'PYPI(douban)'    : 'https://pypi.douban.com/',
                'Conda(tsinghua)' : 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/',
            }
        }

    @property
    def BATHEADER(self):
        """
        Auto switch stdout to python console in windows BAT file
        """
        return self.textwrap.dedent("""
        1>2# : ^
        '''
        @echo off
        echo Switching stdout to python console!
        python "%~f0"
        exit /b
        rem ^
        '''
        # This is in python now!

        # also you can use this to enter python: @SETLOCAL ENABLEDELAYEDEXPANSION & python -x "%~f0" %* & EXIT /B !ERRORLEVEL!

        # @ prevents the script line from being printed
        # SETLOCAL ENABLEDELAYEDEXPANSION allows !ERRORLEVEL! to be evaluated after the python script runs
        # & allows another command to be run on the same line (similar to UNIX's ;)
        # python runs the python interpreter (Must be in %PATH%)
        # -x tells python to ignore the first line (Run python -h for details)
        # "%~f0" expands to the fully-qualified path of the currently executing batch script (Argument %0). It's quoted in case the path contains spaces
        # %* expands all arguments passed to the script, effectively passing them on to the python script
        # EXIT /B tells Windows Batch to exit from the current batch file only (Using just EXIT would cause the calling interpreter to exit)
        # !ERRORLEVEL! expands to the return code from the previous command after it is run. Used as an argument to EXIT /B, it causes the batch script to exit with the # return code received from the python interpreter

        # The batch code is in a multiline string ''' so this is invisible for python.
        # The batch parser doesn't see the python code, as it exits before.
        # The first line is the key.
        # It is valid for batch as also for python!
        # In python it's only a senseless compare 1>2 without output, the rest of the line is a comment by the #.
        # For batch 1>2# is a redirection of stream 1 to the file 2#.
        # The command is a colon : this indicates a label and labeled lines are never printed.
        # Then the last caret simply append the next line to the label line, so batch doesn't see the ''' line.
    """)

    @property
    def NUITKA_HELP(self):
        """
        Nuitka user guide record
        """
        return self.textwrap.dedent("""
        Options:
        --help                show this help message and exit
        --version             Show version information and important details for bug
                                reports, then exit. Defaults to off.
        --module              Create an extension module executable instead of a    
                                program. Defaults to off.
        --standalone          Enable standalone mode for output. This allows you to 
                                transfer the created binary to other machines without 
                                it using an existing Python installation. This also   
                                means it will become big. It implies these option: "--
                                follow-imports" and "--python-flag=no_site". Defaults 
                                to off.
        --onefile             On top of standalone mode, enable onefile mode. This  
                                means not a folder, but a compressed executable is    
                                created and used. Defaults to off.
        --python-debug        Use debug version or not. Default uses what you are   
                                using to run Nuitka, most likely a non-debug version. 
        --python-flag=FLAG    Python flags to use. Default is what you are using to 
                                run Nuitka, this enforces a specific mode. These are  
                                options that also exist to standard Python executable.
                                Currently supported: "-S" (alias "no_site"),
                                "static_hashes" (do not use hash randomization),      
                                "no_warnings" (do not give Python run time warnings), 
                                "-O" (alias "no_asserts"), "no_docstrings" (do not use
                                doc strings), "-u" (alias "unbuffered") and "-m".     
                                Default empty.
        --python-for-scons=PATH
                                If using Python3.3 or Python3.4, provide the path of a
                                Python binary to use for Scons. Otherwise Nuitka can  
                                use what you run Nuitka with or a Python installation 
                                from Windows registry. On Windows Python 3.5 or higher
                                is needed. On non-Windows, Python 2.6 or 2.7 will do  
                                as well.

        Control the inclusion of modules and packages in result:
            --include-package=PACKAGE
                                Include a whole package. Give as a Python namespace,
                                e.g. "some_package.sub_package" and Nuitka will then
                                find it and include it and all the modules found below
                                that disk location in the binary or extension module
                                it creates, and make it available for import by the
                                code. To avoid unwanted sub packages, e.g. tests you
                                can e.g. do this "--nofollow-import-to=*.tests".
                                Default empty.
            --include-module=MODULE
                                Include a single module. Give as a Python namespace,
                                e.g. "some_package.some_module" and Nuitka will then
                                find it and include it in the binary or extension
                                module it creates, and make it available for import by
                                the code. Default empty.
            --include-plugin-directory=MODULE/PACKAGE
                                Include also the code found in that directory,
                                considering as if they are each given as a main file.
                                Overrides all other inclusion options. You ought to
                                prefer other inclusion options, that go by names,
                                rather than filenames, those find things through being
                                in "sys.path". This option is for very special use
                                cases only. Can be given multiple times. Default
                                empty.
            --include-plugin-files=PATTERN
                                Include into files matching the PATTERN. Overrides all
                                other follow options. Can be given multiple times.
                                Default empty.
            --prefer-source-code
                                For already compiled extension modules, where there is
                                both a source file and an extension module, normally
                                the extension module is used, but it should be better
                                to compile the module from available source code for
                                best performance. If not desired, there is --no-
                                prefer-source-code to disable warnings about it.
                                Default off.

        Control the following into imported modules:
            --follow-imports    Descend into all imported modules. Defaults to on in
                                standalone mode, otherwise off.
            --follow-import-to=MODULE/PACKAGE
                                Follow to that module if used, or if a package, to the
                                whole package. Can be given multiple times. Default
                                empty.
            --nofollow-import-to=MODULE/PACKAGE
                                Do not follow to that module name even if used, or if
                                a package name, to the whole package in any case,
                                overrides all other options. Can be given multiple
                                times. Default empty.
            --nofollow-imports  Do not descend into any imported modules at all,
                                overrides all other inclusion options and not usable
                                for standalone mode. Defaults to off.
            --follow-stdlib     Also descend into imported modules from standard
                                library. This will increase the compilation time by a
                                lot and is also not well tested at this time and
                                sometimes won't work. Defaults to off.

        Onefile options:
            --onefile-tempdir-spec=ONEFILE_TEMPDIR_SPEC
                                Use this as a folder to unpack to in onefile mode.
                                Defaults to '%TEMP%/onefile_%PID%_%TIME%', i.e. user
                                temporary directory and being non-static it's removed.
                                Use e.g. a string like
                                '%CACHE_DIR%/%COMPANY%/%PRODUCT%/%VERSION%' which is a
                                good static cache path, this will then not be removed.
            --onefile-child-grace-time=GRACE_TIME_MS
                                When stopping the child, e.g. due to CTRL-C or
                                shutdown, etc. the Python code gets a
                                "KeyboardInterrupt", that it may handle e.g. to flush
                                data. This is the amount of time in ms, before the
                                child it killed in the hard way. Unit is ms, and
                                default 5000.

        Data files:
            --include-package-data=PACKAGE
                                Include data files for the given package name. DLLs
                                and extension modules are not data files and never
                                included like this. Can use patterns the filenames as
                                indicated below. Data files of packages are not
                                included by default, but package configuration can do
                                it. This will only include non-DLL, non-extension
                                modules, i.e. actual data files. After a ":"
                                optionally a filename pattern can be given as well,
                                selecting only matching files. Examples: "--include-
                                package-data=package_name" (all files) "--include-
                                package-data=package_name=*.txt" (only certain type) "
                                --include-package-data=package_name=some_filename.dat
                                (concrete file) Default empty.
            --include-data-files=DESC
                                Include data files by filenames in the distribution.
                                There are many allowed forms. With '--include-data-
                                files=/path/to/file/*.txt=folder_name/some.txt' it
                                will copy a single file and complain if it's multiple.
                                With '--include-data-
                                files=/path/to/files/*.txt=folder_name/' it will put
                                all matching files into that folder. For recursive
                                copy there is a form with 3 values that '--include-
                                data-files=/path/to/scan=folder_name=**/*.txt' that
                                will preserve directory structure. Default empty.
            --include-data-dir=DIRECTORY
                                Include data files from complete directory in the
                                distribution. This is recursive. Check '--include-
                                data-files' with patterns if you want non-recursive
                                inclusion. An example would be '--include-data-
                                dir=/path/some_dir=data/some_dir' for plain copy, of
                                the whole directory. All files are copied, if you want
                                to exclude files you need to remove them beforehand,
                                or use '--noinclude-data-files' option to remove them.
                                Default empty.
            --noinclude-data-files=PATTERN
                                Do not include data files matching the filename
                                pattern given. This is against the target filename,
                                not source paths. So to ignore a file pattern from
                                package data for "package_name" should be matched as
                                "package_name/*.txt". Or for the whole directory
                                simply use "package_name". Default empty.
            --list-package-data=LIST_PACKAGE_DATA
                                Output the data files found for a given package name.
                                Default not done.

        DLL files:
            --noinclude-dlls=PATTERN
                                Do not include DLL files matching the filename pattern
                                given. This is against the target filename, not source
                                paths. So ignore a DLL "someDLL" contained in the
                                package "package_name" it should be matched as
                                "package_name/someDLL.*". Default empty.
            --list-package-dlls=LIST_PACKAGE_DLLS
                                Output the DLLs found for a given package name.
                                Default not done.

        Control the warnings to be given by Nuitka:
            --warn-implicit-exceptions
                                Enable warnings for implicit exceptions detected at
                                compile time.
            --warn-unusual-code
                                Enable warnings for unusual code detected at compile
                                time.
            --assume-yes-for-downloads
                                Allow Nuitka to download external code if necessary,
                                e.g. dependency walker, ccache, and even gcc on
                                Windows. To disable, redirect input from nul device,
                                e.g. "</dev/null" or "<NUL:". Default is to prompt.
            --nowarn-mnemonic=MNEMONIC
                                Disable warning for a given mnemonic. These are given
                                to make sure you are aware of certain topics, and
                                typically point to the Nuitka website. The mnemonic is
                                the part of the URL at the end, without the HTML
                                suffix. Can be given multiple times and accepts shell
                                pattern. Default empty.

        Immediate execution after compilation:
            --run               Execute immediately the created binary (or import the
                                compiled module). Defaults to off.
            --debugger          Execute inside a debugger, e.g. "gdb" or "lldb" to
                                automatically get a stack trace. Defaults to off.
            --execute-with-pythonpath
                                When immediately executing the created binary or
                                module using '--run', don't reset 'PYTHONPATH'
                                environment. When all modules are successfully
                                included, you ought to not need PYTHONPATH anymore,
                                and definitely not for standalone mode.

        Compilation choices:
            --user-package-configuration-file=YAML_FILENAME
                                User provided Yaml file with package configuration.
                                You can include DLLs, remove bloat, add hidden
                                dependencies. Check User Manual for a complete
                                description of the format to use. Can be given
                                multiple times. Defaults to empty.
            --full-compat       Enforce absolute compatibility with CPython. Do not
                                even allow minor deviations from CPython behavior,
                                e.g. not having better tracebacks or exception
                                messages which are not really incompatible, but only
                                different or worse. This is intended for tests only
                                and should *not* be used.
            --file-reference-choice=MODE
                                Select what value "__file__" is going to be. With
                                "runtime" (default for standalone binary mode and
                                module mode), the created binaries and modules, use
                                the location of themselves to deduct the value of
                                "__file__". Included packages pretend to be in
                                directories below that location. This allows you to
                                include data files in deployments. If you merely seek
                                acceleration, it's better for you to use the
                                "original" value, where the source files location will
                                be used. With "frozen" a notation "<frozen
                                module_name>" is used. For compatibility reasons, the
                                "__file__" value will always have ".py" suffix
                                independent of what it really is.
            --module-name-choice=MODE
                                Select what value "__name__" and "__package__" are
                                going to be. With "runtime" (default for module mode),
                                the created module uses the parent package to deduce
                                the value of "__package__", to be fully compatible.
                                The value "original" (default for other modes) allows
                                for more static optimization to happen, but is
                                incompatible for modules that normally can be loaded
                                into any package.

        Output choices:
            --output-filename=FILENAME
                                Specify how the executable should be named. For
                                extension modules there is no choice, also not for
                                standalone mode and using it will be an error. This
                                may include path information that needs to exist
                                though. Defaults to '<program_name>' on this platform.
                                .exe
            --output-dir=DIRECTORY
                                Specify where intermediate and final output files
                                should be put. The DIRECTORY will be populated with
                                build folder, dist folder, binaries, etc. Defaults to
                                current directory.
            --remove-output     Removes the build directory after producing the module
                                or exe file. Defaults to off.
            --no-pyi-file       Do not create a ".pyi" file for extension modules
                                created by Nuitka. This is used to detect implicit
                                imports. Defaults to off.

        Debug features:
            --debug             Executing all self checks possible to find errors in
                                Nuitka, do not use for production. Defaults to off.
            --unstripped        Keep debug info in the resulting object file for
                                better debugger interaction. Defaults to off.
            --profile           Enable vmprof based profiling of time spent. Not
                                working currently. Defaults to off.
            --internal-graph    Create graph of optimization process internals, do not
                                use for whole programs, but only for small test cases.
                                Defaults to off.
            --trace-execution   Traced execution output, output the line of code
                                before executing it. Defaults to off.
            --recompile-c-only  This is not incremental compilation, but for Nuitka
                                development only. Takes existing files and simply
                                compile them as C again. Allows compiling edited C
                                files for quick debugging changes to the generated
                                source, e.g. to see if code is passed by, values
                                output, etc, Defaults to off. Depends on compiling
                                Python source to determine which files it should look
                                at.
            --xml=XML_FILENAME  Write the internal program structure, result of
                                optimization in XML form to given filename.
            --generate-c-only   Generate only C source code, and do not compile it to
                                binary or module. This is for debugging and code
                                coverage analysis that doesn't waste CPU. Defaults to
                                off. Do not think you can use this directly.
            --experimental=FLAG
                                Use features declared as 'experimental'. May have no
                                effect if no experimental features are present in the
                                code. Uses secret tags (check source) per experimented
                                feature.
            --low-memory        Attempt to use less memory, by forking less C
                                compilation jobs and using options that use less
                                memory. For use on embedded machines. Use this in case
                                of out of memory problems. Defaults to off.

        Backend C compiler choice:
            --clang             Enforce the use of clang. On Windows this requires a
                                working Visual Studio version to piggy back on.
                                Defaults to off.
            --mingw64           Enforce the use of MinGW64 on Windows. Defaults to off
                                unless MSYS2 with MinGW Python is used.
            --msvc=MSVC_VERSION
                                Enforce the use of specific MSVC version on Windows.
                                Allowed values are e.g. "14.3" (MSVC 2022) and other
                                MSVC version numbers, specify "list" for a list of
                                installed compilers, or use "latest".  Defaults to
                                latest MSVC being used if installed, otherwise MinGW64
                                is used.
            --jobs=N            Specify the allowed number of parallel C compiler
                                jobs. Defaults to the system CPU count.
            --lto=choice        Use link time optimizations (MSVC, gcc, clang).
                                Allowed values are "yes", "no", and "auto" (when it's
                                known to work). Defaults to "auto".
            --static-libpython=choice
                                Use static link library of Python. Allowed values are
                                "yes", "no", and "auto" (when it's known to work).
                                Defaults to "auto".

        Cache Control:
            --disable-cache=DISABLED_CACHES
                                Disable selected caches, specify "all" for all cached.
                                Currently allowed values are:
                                "all","ccache","bytecode","dll-dependencies". can be
                                given multiple times or with comma separated values.
                                Default none.
            --clean-cache=CLEAN_CACHES
                                Clean the given caches before executing, specify "all"
                                for all cached. Currently allowed values are:
                                "all","ccache","bytecode","dll-dependencies". can be
                                given multiple times or with comma separated values.
                                Default none.
            --disable-bytecode-cache
                                Do not reuse dependency analysis results for modules,
                                esp. from standard library, that are included as
                                bytecode. Same as --disable-cache=bytecode.
            --disable-ccache    Do not attempt to use ccache (gcc, clang, etc.) or
                                clcache (MSVC, clangcl). Same as --disable-
                                cache=ccache.
            --disable-dll-dependency-cache
                                Disable the dependency walker cache. Will result in
                                much longer times to create the distribution folder,
                                but might be used in case the cache is suspect to
                                cause errors. Same as --disable-cache=dll-
                                dependencies.
            --force-dll-dependency-cache-update
                                For an update of the dependency walker cache. Will
                                result in much longer times to create the distribution
                                folder, but might be used in case the cache is suspect
                                to cause errors or known to need an update.

        PGO compilation choices:
            --pgo               Enables C level profile guided optimization (PGO), by
                                executing a dedicated build first for a profiling run,
                                and then using the result to feedback into the C
                                compilation. Note: This is experimental and not
                                working with standalone modes of Nuitka yet. Defaults
                                to off.
            --pgo-args=PGO_ARGS
                                Arguments to be passed in case of profile guided
                                optimization. These are passed to the special built
                                executable during the PGO profiling run. Default
                                empty.
            --pgo-executable=PGO_EXECUTABLE
                                Command to execute when collecting profile
                                information. Use this only, if you need to launch it
                                through a script that prepares it to run. Default use
                                created program.

        Tracing features:
            --report=REPORT_FILENAME
                                Report module, data files, compilation, plugin, etc.
                                details in an XML output file. This is also super
                                useful for issue reporting. Default is off.
            --report-template=REPORT_DESC
                                Report via template. Provide template and output
                                filename "template.rst.j2:output.rst". For built-in
                                templates, check the User Manual for what these are.
                                Can be given multiple times. Default is empty.
            --quiet             Disable all information outputs, but show warnings.
                                Defaults to off.
            --show-scons        Run the C building backend Scons with verbose
                                information, showing the executed commands, detected
                                compilers. Defaults to off.
            --no-progressbar    Disable progress bars. Defaults to off.
            --show-progress     Obsolete: Provide progress information and statistics.
                                Disables normal progress bar. Defaults to off.
            --show-memory       Provide memory information and statistics. Defaults to
                                off.
            --show-modules      Provide information for included modules and DLLs
                                Obsolete: You should use '--report' file instead.
                                Defaults to off.
            --show-modules-output=PATH
                                Where to output '--show-modules', should be a
                                filename. Default is standard output.
            --verbose           Output details of actions taken, esp. in
                                optimizations. Can become a lot. Defaults to off.
            --verbose-output=PATH
                                Where to output from '--verbose', should be a
                                filename. Default is standard output.

        General OS controls:
            --disable-console   When compiling for Windows or macOS, disable the
                                console window and create a GUI application. Defaults
                                to off.
            --enable-console    When compiling for Windows or macOS, enable the
                                console window and create a console application. This
                                disables hints from certain modules, e.g. "PySide"
                                that suggest to disable it. Defaults to true.
            --force-stdout-spec=FORCE_STDOUT_SPEC
                                Force standard output of the program to go to this
                                location. Useful for programs with disabled console
                                and programs using the Windows Services Plugin of
                                Nuitka commercial. Defaults to not active, use e.g.
                                '%PROGRAM%.out.txt', i.e. file near your program.
            --force-stderr-spec=FORCE_STDERR_SPEC
                                Force standard error of the program to go to this
                                location. Useful for programs with disabled console
                                and programs using the Windows Services Plugin of
                                Nuitka commercial. Defaults to not active, use e.g.
                                '%PROGRAM%.err.txt', i.e. file near your program.

        Windows specific controls:
            --windows-icon-from-ico=ICON_PATH
                                Add executable icon. Can be given multiple times for
                                different resolutions or files with multiple icons
                                inside. In the later case, you may also suffix with
                                #<n> where n is an integer index starting from 1,
                                specifying a specific icon to be included, and all
                                others to be ignored.
            --windows-icon-from-exe=ICON_EXE_PATH
                                Copy executable icons from this existing executable
                                (Windows only).
            --onefile-windows-splash-screen-image=SPLASH_SCREEN_IMAGE
                                When compiling for Windows and onefile, show this
                                while loading the application. Defaults to off.
            --windows-uac-admin
                                Request Windows User Control, to grant admin rights on
                                execution. (Windows only). Defaults to off.
            --windows-uac-uiaccess
                                Request Windows User Control, to enforce running from
                                a few folders only, remote desktop access. (Windows
                                only). Defaults to off.

        macOS specific controls:
            --macos-target-arch=MACOS_TARGET_ARCH
                                What architectures is this to supposed to run on.
                                Default and limit is what the running Python allows
                                for. Default is "native" which is the architecture the
                                Python is run with.
            --macos-create-app-bundle
                                When compiling for macOS, create a bundle rather than
                                a plain binary application. Currently experimental and
                                incomplete. Currently this is the only way to unlock
                                disabling of console.Defaults to off.
            --macos-app-icon=ICON_PATH
                                Add icon for the application bundle to use. Can be
                                given only one time. Defaults to Python icon if
                                available.
            --macos-signed-app-name=MACOS_SIGNED_APP_NAME
                                Name of the application to use for macOS signing.
                                Follow "com.YourCompany.AppName" naming results for
                                best results, as these have to be globally unique, and
                                will potentially grant protected API accesses.
            --macos-app-name=MACOS_APP_NAME
                                Name of the product to use in macOS bundle
                                information. Defaults to base filename of the binary.
            --macos-app-mode=MODE
                                Mode of application for the application bundle. When
                                launching a Window, and appearing in Docker is
                                desired, default value "gui" is a good fit. Without a
                                Window ever, the application is a "background"
                                application. For UI elements that get to display
                                later, "ui-element" is in-between. The application
                                will not appear in dock, but get full access to
                                desktop when it does open a Window later.
            --macos-sign-identity=MACOS_APP_VERSION
                                When signing on macOS, by default an ad-hoc identify
                                will be used, but with this option your get to specify
                                another identity to use. The signing of code is now
                                mandatory on macOS and cannot be disabled. Default
                                "ad-hoc" if not given.
            --macos-sign-notarization
                                When signing for notarization, using a proper TeamID
                                identity from Apple, use the required runtime signing
                                option, such that it can be accepted.
            --macos-app-version=MACOS_APP_VERSION
                                Product version to use in macOS bundle information.
                                Defaults to "1.0" if not given.
            --macos-app-protected-resource=RESOURCE_DESC
                                Request an entitlement for access to a macOS protected
                                resources, e.g.
                                "NSMicrophoneUsageDescription:Microphone access for
                                recording audio." requests access to the microphone
                                and provides an informative text for the user, why
                                that is needed. Before the colon, is an OS identifier
                                for an access right, then the informative text. Legal
                                values can be found on https://developer.apple.com/doc
                                umentation/bundleresources/information_property_list/p
                                rotected_resources and the option can be specified
                                multiple times. Default empty.

        Linux specific controls:
            --linux-icon=ICON_PATH
                                Add executable icon for onefile binary to use. Can be
                                given only one time. Defaults to Python icon if
                                available.

        Binary Version Information:
            --company-name=COMPANY_NAME
                                Name of the company to use in version information.
                                Defaults to unused.
            --product-name=PRODUCT_NAME
                                Name of the product to use in version information.
                                Defaults to base filename of the binary.
            --file-version=FILE_VERSION
                                File version to use in version information. Must be a
                                sequence of up to 4 numbers, e.g. 1.0 or 1.0.0.0, no
                                more digits are allowed, no strings are allowed.
                                Defaults to unused.
            --product-version=PRODUCT_VERSION
                                Product version to use in version information. Same
                                rules as for file version. Defaults to unused.
            --file-description=FILE_DESCRIPTION
                                Description of the file used in version information.
                                Windows only at this time. Defaults to binary
                                filename.
            --copyright=COPYRIGHT_TEXT
                                Copyright used in version information. Windows only at
                                this time. Defaults to not present.
            --trademarks=TRADEMARK_TEXT
                                Copyright used in version information. Windows only at
                                this time. Defaults to not present.

        Plugin control:
            --enable-plugin=PLUGIN_NAME
                                Enabled plugins. Must be plug-in names. Use '--plugin-
                                list' to query the full list and exit. Default empty.
            --disable-plugin=PLUGIN_NAME
                                Disabled plugins. Must be plug-in names. Use '--
                                plugin-list' to query the full list and exit. Most
                                standard plugins are not a good idea to disable.
                                Default empty.
            --plugin-no-detection
                                Plugins can detect if they might be used, and the you
                                can disable the warning via "--disable-plugin=plugin-
                                that-warned", or you can use this option to disable
                                the mechanism entirely, which also speeds up
                                compilation slightly of course as this detection code
                                is run in vain once you are certain of which plugins
                                to use. Defaults to off.
            --plugin-list       Show list of all available plugins and exit. Defaults
                                to off.
            --user-plugin=PATH  The file name of user plugin. Can be given multiple
                                times. Default empty.
            --show-source-changes
                                Show source changes to original Python file content
                                before compilation. Mostly intended for developing
                                plugins. Default False.
        """)
    

def is_root():
    """
    Checks if the current user is the root user.

    Returns:
        bool: True if the current user is root, False otherwise.

    Usage:
        >>> if is_root():
        ...     print("Running as root.")
        ... else:
        ...     print("Not running as root.")
    """
    ###### import ######
    os = _dmimport(import_module='os')
    ####################

    return os.geteuid() == 0


def win_desktop_path():
    """
    Retrieves the path to the current user's desktop in Windows.

    Returns:
        str: The absolute path to the current user's desktop.

    Usage:
        >>> desktop_path = win_desktop_path()
        >>> print(desktop_path)
        This will print the path to the desktop of the current user, such as "C:\\Users\\Username\\Desktop".
    """
    ###### import ######
    winreg = _dmimport(import_module='winreg')
    ####################

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def sysc(command: str, cwd=None, outprint=True, printfunction=print):
    """
    Executes a system command and optionally prints its output in real-time.

    Args:
        command (str): The system command to be executed.
        cwd (str, optional): The working directory in which the command should be executed. Defaults to None, which uses the current working directory.
        outprint (bool, optional): Flag indicating whether to print the command's output in real-time. Defaults to True.
        printfunction (callable, optional): A custom print function to use for printing the command's output. Defaults to the built-in print function.

    Returns:
        tuple: A tuple containing two elements:
            - A list of strings, each representing a line of output from the command.
            - An integer representing the command's return code.

    Usage:
        >>> output, return_code = sysc("echo Hello, World!")
        >>> print(output)
        This will print ["Hello, World!"] and the command's output to stdout.

    Note:
        Combine win_command and bash_command into one unify function
        - use p.stdout to get output instead of p.communicate to have a real time output
        - use p.poll() to check if the process is still running or not
        - return output -> list and return code
    """
    ###### import ######
    subprocess = _dmimport(import_module='subprocess')
    ####################

    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        cwd=cwd
    )
    OUT = []
    while (line := p.stdout.readline()) != '' or (RC := p.poll()) is None:
        # if line:
        #     if outprint:
        #         printfunction(line.strip())
        #     OUT.append(line.strip())

        # add \r to overwrite the line for the case taht executing apt-get commands
        if line:
            stripped_line = line.strip()
            if outprint:
                printfunction('\r' + stripped_line if printfunction == print else stripped_line)
            OUT.append(stripped_line)

    return OUT, RC


def dedent(text: str):
    """dedent text, remove leading spaces from each line"""
    ###### import ######
    textwrap = _dmimport(import_module='textwrap')
    ####################

    return textwrap.dedent(text)


def check_return_code(rc: int, process: str, fprint=print, exit_on_fail=True):
    """check return code, if not 0, exit the program"""
    ###### import ######
    sys = _dmimport(import_module='sys')
    ####################

    if rc != 0:
        fprint(f"Execute [{process}] fail, exit.")
        if exit_on_fail:
            sys.exit(1)
    else:
        fprint(f"Execute [{process}] success.")


def win_command(command):
    """
    get windows command response
    deprecated in 1.0, please use `sysc` function
    """
    ###### import ######
    subprocess = _dmimport(import_module='subprocess')
    ####################

    sub = subprocess.Popen(f"{command}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    out, err = sub.communicate()
    return out, err


def bash_command(command):
    """
    get linux bash command response
    deprecated in 1.0, please use `sysc` function
    """
    ###### import ######
    subprocess = _dmimport(import_module='subprocess')
    ####################

    response = []
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        line = line.decode().strip()
        if line:
            response.append(line)
            print(line)
    return response


def get_path(path):
    """
    Generates absolute paths for all files under a given directory.

    Args:
        path (str): The root directory path from which to start generating file paths.

    Yields:
        str: The next absolute path to a file within the given directory or its subdirectories.

    Usage:
        >>> for file_path in get_path("/path/to/directory"):
        ...     print(file_path)
        This will print the absolute paths to all files within "/path/to/directory" and its subdirectories.
    """
    ###### import ######
    os = _dmimport(import_module='os')
    ####################

    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirname, filename)


def get_all_path(rootdir):
    """
    Recursively retrieves all file paths within a given directory.

    Args:
        rootdir (str): The root directory from which to start collecting file paths.

    Returns:
        list: A list of absolute paths to all files within the given directory and its subdirectories.

    Usage:
        >>> file_paths = get_all_path("/path/to/directory")
        >>> print(file_paths)
        This will print a list of absolute paths to all files within "/path/to/directory" and its subdirectories.
    """
    ###### import ######
    os = _dmimport(import_module='os')
    ####################

    path_list = []
    all_list = os.listdir(rootdir)
    for i in range(len(all_list)):
        com_path = os.path.join(rootdir, all_list[i])
        if os.path.isfile(com_path):
            path_list.append(com_path)
        if os.path.isdir(com_path):
            path_list.extend(get_all_path(com_path))
    return path_list


def resource_path(filepath):
    """
    Constructs an absolute path to a resource, intended for use in a PyInstaller bundle.

    This function dynamically imports the `sys` and `os` modules to determine the absolute path of a given file. 
    It is particularly useful when working with PyInstaller, where the file structure of a bundled application differs from that of a script during development.

    Args:
        filepath (str): The relative path to the file for which the absolute path is desired.

    Returns:
        str: The absolute path to the file.

    Usage:
        >>> abs_path = resource_path("data/config.json")
        >>> print(abs_path)
        This will print the absolute path to "config.json", which is useful when the script is bundled into an executable.

    Note:
        The function checks if the script is running in a bundled application by checking `sys.frozen`. 
        If so, it sets the base path to the directory of the executable; otherwise, it uses the directory of the script file.
    """
    ###### import ######
    sys = _dmimport(import_module='sys')
    os  = _dmimport(import_module='os')
    ####################

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    return os.path.join(application_path, filepath)


def level_x_path(path, level=3):
    """
    Recursively retrieves paths up to a specified depth level from a given root path.

    This function traverses a directory tree starting from a specified root path (`path`) and collects paths up to a specified depth level (`level`). 
    It dynamically imports the `os` module to handle file system paths and operations.

    Args:
        path (str): The root directory path from which to start the traversal.
        level (int, optional): The depth level to which the traversal should proceed. Defaults to 3.

    Returns:
        list: A list of paths collected up to the specified depth level.

    Usage:
        >>> paths = level_x_path("/path/to/directory", level=2)
        >>> print(paths)
        This will print a list of paths up to a depth of 2 levels from "/path/to/directory".
    """
    ###### import ######
    os  = _dmimport(import_module='os')
    ####################

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
            path_list.extend(level_x_path(com_path, level=level-1))
    return path_list


def get_runtime_path():
    """
    Returns the current working directory path.

    Returns:
        str: The path of the current working directory.

    Usage:
        >>> current_path = get_runtime_path()
        >>> print(current_path)
        This will print the absolute path of the current working directory.
    """
    ###### import ######
    os  = _dmimport(import_module='os')
    ####################

    return os.getcwd()


def join_path(path, file):
    """
    Joins a directory path and a file name into a single path.

    Args:
        path (str): The directory path.
        file_name (str): The name of the file.

    Returns:
        str: The combined path, which consists of the directory path and the file name.

    Usage:
        >>> combined_path = join_path("/path/to/directory", "file.txt")
        >>> print(combined_path)
        This will print "/path/to/directory/file.txt" on Unix-like systems or "\\path\\to\\directory\\file.txt" on Windows.
    """
    ###### import ######
    os  = _dmimport(import_module='os')
    ####################

    return os.path.join(path, file)


def get_current_time(format="%Y-%m-%d %H:%M:%S"):
    """
    Returns the current local time as a formatted string.

    Args:
        format (str, optional): The format string for strftime. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The current local time formatted according to the specified format string.

    Usage:
        >>> current_time = get_current_time()
        >>> print(current_time)
        This will print the current local time formatted as "YYYY-MM-DD HH:MM:SS".
    """
    ###### import ######
    time  = _dmimport(import_module='time')
    ####################

    return time.strftime(format, time.localtime())


class Tee:
    """
    A class that duplicates output to multiple file-like objects.

    Usage:
        >>> import sys
        >>> log_file = open("logfile.txt", "a")
        >>> tee = Tee(sys.stdout, log_file)
        >>> print("This message will go to stdout and logfile.txt", file=tee)

    Args:
        *files: Variable length argument list of file-like objects to which output will be duplicated.

    Methods:
        write(obj): Writes `obj` to all file-like objects passed during initialization.
        flush(): Flushes all file-like objects passed during initialization.
    """
    def __init__(self, *files):
        ###### import ######
        # common
        ####################
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)

    def flush(self):
        for file in self.files:
            file.flush()


def teewrap(run_time_log):
    """
    A decorator factory that logs the output of the decorated function to both stdout and a specified log file.

    This function returns a decorator that, when applied to another function, 
    will redirect the standard output (stdout) of that function to both the console and a specified log file. 
    It also configures a logger to log messages with a specific format to the same destinations.

    Usage:
        >>> @teewrap("path/to/runtime.log")
        ... def my_function():
        ...     print("This message will be logged to both stdout and the log file.")
        ...
        >>> my_function()

    Args:
        run_time_log (str): The path to the log file where the output and log messages should be written.
    """
    ###### import ######
    functools  = _dmimport(import_module='functools')
    sys        = _dmimport(import_module='sys')
    logging    = _dmimport(import_module='logging')
    ####################

    def decorator_log_to_file(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            f = open(run_time_log, 'w')
            tee = Tee(sys.stdout, f)
            stdout_original = sys.stdout 

            # Redirect stdout to tee(stdout and file)
            sys.stdout = tee

            # Create a new logger and configure it
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(tee)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s]%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            try:
                result = func(*args, **kwargs)
            finally:
                # Restore stdout and remove the handler
                sys.stdout = stdout_original
                logger.removeHandler(handler)
                f.close()
            return result
        return wrapper
    return decorator_log_to_file


def __logorder__(func):
    """builtin wrapper for dmlog class, do not use it directly"""
    ###### import ######
    logging    = _dmimport(import_module='logging')
    ####################

    def wrapper(self, msg):
        if self.showlog:
            if not self.savelog:
                if self.branch:
                    getattr(logging, func.__name__)(msg=f"[{self.branch}] - {msg}")
                else:
                    getattr(logging, func.__name__)(msg=f"{msg}")
            else:
                if self.branch:
                    getattr(self.logger, func.__name__)(msg=f"[{self.branch}] - {msg}")
                else:
                    getattr(self.logger, func.__name__)(msg=f"{msg}")
        else:
            ...
        return func(self, msg)
    return wrapper


class DmLog():
    """
    A simple logging system.

    Usage:
        >>> log = dmlog(branch="example", llevel="debug", showlog=True, savelog="path/to/logfile.log")
        >>> log.info("This is an info message.")
        >>> log.warning("This is a warning message.")
        >>> log.error("This is an error message.")
        >>> log.debug("This is a debug message.")

    Args:
        branch (str, optional): The log branch name. Defaults to None.
        llevel (str, optional): The log level as a string. Defaults to 'debug'.
        showlog (bool, optional): Whether to show logs in the console. Defaults to True.
        savelog (str or None, optional): The path to save the log file to. If None, logs are not saved. Defaults to None.
        format (str, optional): The format string for log messages. Defaults to '%(asctime)s [%(levelname)s]%(message)s'.
    """

    def __init__(self, branch=None, llevel='debug', showlog=True, savelog=None, format='%(asctime)s [%(levelname)s]%(message)s'):
        ###### import ######
        self.logging  = _dmimport(import_module='logging')
        self.os       = _dmimport(import_module='os')
        ####################

        self.level_relation = {
            'debug'  : self.logging.DEBUG,
            'info'   : self.logging.INFO,
            'warning': self.logging.WARNING,
            'error'  : self.logging.ERROR
        }
        self.showlog = showlog
        self.branch = branch
        self.savelog = savelog
        self.format = format

        if not savelog:
            self.logging.basicConfig(level=self.level_relation[llevel], format=self.format)
        else:
            if self.os.path.exists(savelog):
                self.os.remove(savelog)
            fh = self.logging.FileHandler(savelog)
            sh = self.logging.StreamHandler()
            ft = self.logging.Formatter(self.format)
            fh.setLevel(self.level_relation[llevel])
            sh.setLevel(self.level_relation[llevel])
            fh.setFormatter(ft)
            sh.setFormatter(ft)
            self.logger = self.logging.getLogger()
            self.logger.setLevel(self.level_relation[llevel])
            self.logger.addHandler(fh)
            self.logger.addHandler(sh)

    @__logorder__
    def info(self, msg):
        ...
    
    @__logorder__
    def debug(self, msg):
        ...
    
    @__logorder__
    def warning(self, msg):
        ...
    
    @__logorder__
    def error(self, msg):
        ...

    @__logorder__
    def exception(self, msg):
        ...


def timethis(func):
    """
    Decorator for measuring the execution time of a function.

    Args:
        func (Callable): The function to be wrapped by the decorator.

    Returns:
        Callable: The wrapped function with added timing functionality.

    Example:
        >>> @timethis
        ... def your_function(*args, **kwargs):
        ...     # function implementation
        ...
        This will print the execution time of `your_function` each time it is called.
    """
    ###### import ######
    time = _dmimport(import_module='time')
    ####################

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = round((time.time() - start), 3)
        print(f'{func.__name__} running time: {end}sec.')
        return result
    return wrapper


class CodeTimer(object):
    """
    A context manager for measuring the execution time of a code block.

    Args:
        keep_num (int, optional): The number of decimal places to round the running time to. Defaults to 3.

    Examples:
        >>> with CodeTimer():
        ...     # your code here
        ...
        Running time: X.XXXsec
    """
    def __init__(self, keep_num=3):
        ###### import ######
        self.time = _dmimport(import_module='time')
        ####################

        self.start = self.time.time()
        self.keep_num = keep_num

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.stop = self.time.time()
        self.cost = self.stop - self.start
        print(f'Running time: {round(self.cost, self.keep_num)}sec')


def mkdir(path):
    """
    Creates directories for the given path if they do not already exist.

    Args:
        path (str): The file system path where the directory (or directories) should be created.

    Note:
        This function dynamically imports the `os` module to ensure that directory creation is handled in a platform-independent manner.
    """
    ###### import ######
    os = _dmimport(import_module='os')
    ####################

    path = path.strip().rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def safe_remove(file_path):
    """
    Safely removes a file at the specified path.

    Args:
        file_path (str or Path): The path to the file to be removed. Can be a string or a `Path` object.

    Note:
        Before using this function, ensure that the file is intended to be permanently deleted.
    """
    ###### import ######
    PurePath = _dmimport(from_module="pathlib", import_module='PurePath')
    Path = _dmimport(from_module="pathlib", import_module='Path')
    ####################

    if not isinstance(file_path, Path):
        file_path = Path(PurePath(file_path))
    file_path.unlink(missing_ok=True)


def dict2json(target_dict, json_name, json_path) -> None:
    """
    Converts a dictionary to a JSON file and saves it to the specified path.

    Args:
        target_dict (dict): The dictionary to convert to JSON.
        json_name (str): The name of the JSON file to create, without the extension.
        json_path (str): The path where the JSON file will be saved.
    """
    ###### import ######
    os   = _dmimport(import_module='os')
    json = _dmimport(import_module='json')
    ####################

    file = join_path(json_path, f'{json_name}.json')
    if not os.path.exists(json_path):
        mkdir(json_path)
    content = json.dumps(target_dict, indent=4)
    with open(file, 'w') as json_file:
        json_file.write(content)


def json2dict(json_path) -> dict:
    """
    Converts a JSON file to a dictionary.

    Args:
        json_path (str): The file path of the JSON file to be converted.

    Returns:
        dict: The contents of the JSON file as a Python dictionary.

    Example:
        >>> my_dict = json2dict("path/to/myfile.json")
        >>> print(my_dict)
        This will print the contents of "myfile.json" as a dictionary.
    """
    ###### import ######
    json = _dmimport(import_module='json')
    ####################

    with open(json_path, 'r', encoding='UTF-8') as f:
        return json.load(f)
    

def json2jsone(json_path: str, jsone_path: str):
    """
    Encrypts a JSON file and saves it as a .jsone file.

    This function takes the path to a JSON file, encrypts its contents using Fernet symmetric encryption, 
    and saves the encrypted data to a specified path with a .jsone extension. It prints the path to the encrypted file and the decryption key upon completion.

    Args:
        json_path (str): The file path to the JSON file to be encrypted.
        jsone_path (str): The full path (including the file name) where the encrypted file (.jsone) will be saved.

    Note:
        - The function dynamically imports the `Fernet` class from the `cryptography.fernet` module for encryption and the `json` module for handling JSON data.
        - A new encryption key is generated each time the function is called. This key is required for decrypting the .jsone file.

    Example:
        >>> json2jsone("path/to/myfile.json", "path/to/myfile.jsone")
        This will encrypt "myfile.json" and save it as "myfile.jsone" in the specified path. 
        The path to the encrypted file and the decryption key are printed to the console.
    """
    ###### import ######
    Fernet = _dmimport(from_module='cryptography.fernet', import_module='Fernet')
    json   = _dmimport(import_module='json')
    ####################

    KEY = Fernet.generate_key()
    FERNET = Fernet(KEY)
    with open(json_path, encoding='UTF-8') as f:
        dict_original = json.load(f)
    dict_original = json.dumps(dict_original).encode()
    dict_encrypted = FERNET.encrypt(dict_original)

    with open(jsone_path, "wb") as f:
        f.write(dict_encrypted)

    print(f"Encrypted json to: {jsone_path}")
    print(f"Decrypt key: {KEY}")


def dict2jsone(target_dict, jsone_name, jsone_path):
    """
    Encrypts a dictionary and saves it as a .jsone file.

    This function takes a dictionary, encrypts it using Fernet symmetric encryption, 
    and saves the encrypted data to a file with a .jsone extension at the specified path. 
    It prints the path to the encrypted file and the decryption key upon completion.

    Args:
        target_dict (dict): The dictionary to encrypt.
        jsone_name (str): The name of the .jsone file to create, without the extension.
        jsone_path (str): The path where the .jsone file will be saved.

    Note:
        - The function dynamically imports the `Fernet` class from the `cryptography.fernet` module for encryption and the `json` module for serialization.
        - The encryption key is generated using `Fernet.generate_key()`.
        - The encrypted data and the key are printed to the console. The key is required for decryption.

    Example:
        >>> my_dict = {"key": "value"}
        >>> dict2jsone(my_dict, "encrypted_data", "/path/to/save")
        This will create an encrypted file named "encrypted_data.jsone" in "/path/to/save" and print the path and decryption key.
    """
    ###### import ######
    Fernet = _dmimport(from_module='cryptography.fernet', import_module='Fernet')
    json   = _dmimport(import_module='json')
    ####################

    KEY = Fernet.generate_key()
    FERNET = Fernet(KEY)
    jsone_file_path = join_path(jsone_path, f'{jsone_name}.jsone')
    dict_original = json.dumps(target_dict).encode()
    dict_encrypted = FERNET.encrypt(dict_original)

    with open(jsone_file_path, "wb") as f:
        f.write(dict_encrypted)

    print(f"Encrypted dict to: {jsone_file_path}")
    print(f"Decrypt key: {KEY}")


def openjsone(jsone_path, key) -> dict:
    """
    Opens and decrypts an encrypted JSON file, returning its contents as a dictionary.

    This function is designed to handle JSON files that have been encrypted using the Fernet symmetric encryption. 
    It requires the path to the encrypted JSON file and the Fernet key used for encryption. 
    The function decrypts the file and parses the JSON content into a Python dictionary.

    Args:
        jsone_path (str): The file path to the encrypted JSON file.
        key (bytes): The Fernet key used to encrypt the JSON file. This should be a byte string.

    Returns:
        dict: The decrypted and parsed contents of the JSON file.

    Example:
        >>> key = b'my_fernet_key'
        >>> jsone_path = 'path/to/encrypted_file.jsone'
        >>> content = openjsone(jsone_path, key)
        >>> print(content)
        This will print the decrypted content of the encrypted JSON file.

    Note:
        This function dynamically imports the `Fernet` class from the `cryptography.fernet` module and the `json` module for decryption and parsing, respectively.
    """
    ###### import ######
    Fernet = _dmimport(from_module='cryptography.fernet', import_module='Fernet')
    json   = _dmimport(import_module='json')
    ####################

    with open(jsone_path, "rb") as f:
        return json.loads(Fernet(key).decrypt(f.read()).decode('utf-8'))


class ZipReader:
    """
    A class for reading and extracting the contents of a specific file within a zip archive.

    This class is designed to open a zip file, search for a file within the zip archive that matches a given keyword, and read the contents of that file.

    Attributes:
        zipfile (module): The zipfile module, dynamically imported for handling zip files.
        content (list of str): The lines of the specified file within the zip archive, decoded to strings.

    Args:
        zippath (str): The path to the zip file.
        filekeyword (str): The keyword to identify the specific file within the zip archive.

    Examples:
        >>> with ZipReader(zippath="example.zip", filekeyword="targetfile.txt") as content:
        ...     for line in content:
        ...         print(line)
        This will print each line of the file named "targetfile.txt" (or contains "targetfile.txt" in its name) within "example.zip".
    """

    def __init__(self, zippath, filekeyword):
        ###### import ######
        self.zipfile =  _dmimport(import_module="zipfile")
        ####################

        with self.zipfile.ZipFile(zippath, "r") as z:
            for zipfile_path in z.namelist():
                if filekeyword in zipfile_path:
                    with z.open(zipfile_path, 'r') as file:
                        self.content = list(map(lambda x: x.decode(), file.readlines()))

    def __enter__(self):
        return self.content

    def __exit__(self, *_):
        ...


class Zip2Reader(object):
    """
    A class for reading the contents of a file within a zip file that is itself contained within another zip file.

    Attributes:
        zipfile (module): The zipfile module, dynamically imported.
        BytesIO (class): The BytesIO class from the io module, dynamically imported.
        content (list of str): The lines of the file specified by `filekeyword`, decoded to strings.

    Args:
        zippath (str): The path of the outer zip file.
        subziptype (str, optional): The file extension of the inner zip file. Defaults to 'zip'.
        filekeyword (str, optional): A keyword to identify the specific file within the inner zip file. Defaults to an empty string.

    Examples:
        >>> with Zip2Reader(zippath="path/to/outer.zip", subziptype="zip", filekeyword=".log") as content:
        ...     for line in content:
        ...         print(line)
        This will print each line of the .log file contained within the inner zip file.

    Note:
        The class uses context manager protocols (`__enter__` and `__exit__`) 
        to facilitate easy use with the `with` statement, ensuring resources are managed efficiently.
    """

    def __init__(self, zippath, subziptype='zip', filekeyword=''):
        ###### import ######
        self.zipfile =  _dmimport(import_module="zipfile")
        self.BytesIO = _dmimport(from_module='io', import_module='BytesIO')
        ####################

        with self.zipfile.ZipFile(zippath, "r") as mainzip:
            for mainzipcontent in [i for i in mainzip.namelist() if f".{subziptype}" in i]:
                subzip = self.BytesIO(mainzip.read(mainzipcontent))
                with self.zipfile.ZipFile(subzip, "r") as sz:
                    for subzipcontent in [i for i in sz.namelist() if filekeyword in i]:
                            with sz.open(subzipcontent, 'r') as target:
                                self.content = list(map(lambda x: x.decode(), target.readlines()))
    def __enter__(self):
        return self.content

    def __exit__(self, *_):
        ...


class DateTrans():
    """
    A class for transforming date strings into various formats and extracting date-related information.

    This class takes a date string as input and provides properties to access the 
    year, month, week number, quarter, and other date-related information in various formats.

    Attributes:
        dt (module): The datetime module, dynamically imported.
        time (module): The time module, dynamically imported.
        to_Tdate (date): The input date string converted to a date object.
        year (int): The year extracted from the input date.
        week (int): The ISO week number extracted from the input date.
        month (int): The month extracted from the input date.
        quarter (int): The quarter of the year extracted from the input date.
        weekday (int): The ISO weekday number extracted from the input date.
        yearweek (str): The year and ISO week number in 'YYYYWww' format.
        yearmonth (str): The year and month in 'YYYYMmm' format.
        yearquarter (str): The year and quarter in 'YYYYQq' format.
        timestamp (int): The Unix timestamp corresponding to the input date.

    Examples:
        >>> DTF = DateTransformer("2023-07-27")
        >>> DTF.year
        2023
        >>> DTF.month
        7
        >>> DTF.week
        30
        >>> DTF.quarter
        2
        >>> DTF.yearweek
        '2023W30'
        >>> DTF.yearmonth
        '2023M07'
        >>> DTF.yearquarter
        '2023Q2'
        >>> DTF.timestamp
        1690387200
        >>> DTF.weekday
        4
    """
    def __init__(self, datestring):
        ###### import ######
        self.dt         = _dmimport(from_module='datetime', import_module='datetime')
        self.time       = _dmimport(import_module='time')
        ####################

        datestring = datestring.replace('-','')
        _FormatDateString = self.dt.strptime(datestring,"%Y%m%d")
        _DateInformation = _FormatDateString.isocalendar()
        
        self.to_Tdate    = _FormatDateString.date()  # trnasform string to date type
        self.year        = int(_DateInformation[0])
        self.week        = int(_DateInformation[1])
        self.month       = int(_FormatDateString.month)
        self.quarter     = int(self.month // 4 + 1)
        self.weekday     = _FormatDateString.isoweekday()
        if len(str(self.week)) == 2:
            self.yearweek  = f"{self.year}W{self.week}"
        elif len(str(self.week)) == 1:
            self.yearweek  = f"{self.year}W0{self.week}"
        if len(str(self.month)) == 2:
            self.yearmonth = f"{self.year}M{self.month}"
        elif len(str(self.month)) == 1:
            self.yearmonth = f"{self.year}M0{self.month}"
        self.yearquarter = f"{self.year}Q{self.quarter}"
        self.timestamp     = int(self.time.mktime(self.time.strptime(datestring,"%Y%m%d")))


@_dmimport(from_module='contextlib', import_module='contextmanager')
def ignored(exception=Exception, func=lambda:None, **kwargs):
    """
    A context manager that ignores specified exceptions and optionally executes a callback function.

    This function allows code to be executed within a context block, ignoring specified exceptions. 
    If an exception is caught, an optional callback function can be executed with provided keyword arguments.

    Args:
        exception (Exception, optional): The exception type to ignore. Defaults to Exception.
        func (callable, optional): A callback function to execute if the exception is caught. Defaults to a lambda function that does nothing.
        **kwargs: Arbitrary keyword arguments passed to the callback function upon execution.

    Yields:
        None: This context manager does not provide a direct value upon entering the context.

    Examples:
        >>> with ignored(exception=ValueError, func=print, message="Error ignored"):
        ...     int("not a number")
        ...     print("This will not print if a ValueError is raised.")
        >>> # If a ValueError occurs, "Error ignored" will be printed to the console.

    Note:
        This context manager is useful for cases where certain exceptions can be safely ignored, and optional cleanup or logging actions need to be performed.
    """
    ###### import ######
    # common
    ####################

    try:
        yield
    except exception:
        func(**kwargs)


class xlsxDesigner():
    """
    Generate an openpyxl type xlsx design

    bgcolor  : str, background color
    hzalign  : str[left/general/right/center], alignment setting in cell,
    font     : str, font
    fontsize : font size
    fontbold : bool, bond font or not

    usage example refer to xlsxMaker.
    """

    #  some nice color for choice
    sggcolor = {
        'BlueAngel'  : 'B7CEEC',
        'MagicMint'  : 'AAF0D1',
        'CreamWhite' : 'FFFDD0',
        'PeachPink'  : 'F98B88',
        'PeriWinkle' : 'CCCCFF'
    }

    def __init__(self, bgcolor="BlueAngel", hzalign="left", font='Calibri', fontsize='10', fontbold=False):
        ###### import ######
        Border, Side, colors, Font, PatternFill, Alignment = _dmimport(from_module='openpyxl.styles', import_module='Border, Side, colors, Font, PatternFill, Alignment')
        ####################

        # border style
        self.border = Border(
            top    = Side(border_style='thin', color=colors.BLACK),
            bottom = Side(border_style='thin', color=colors.BLACK),
            left   = Side(border_style='thin', color=colors.BLACK),
            right  = Side(border_style='thin', color=colors.BLACK)
        )

        # font style
        self.font = Font(font, size=fontsize, bold=fontbold)

        # fill style
        self.fill = PatternFill('solid', fgColor=self.sggcolor.get(bgcolor, bgcolor))

        # alignment style
        self.alignment = Alignment(horizontal=hzalign, vertical='center') # left, general, right, center


class xlsxMaker():
    """
    A class for creating and manipulating xlsx files using the openpyxl library.

    This class provides methods to create sheets, write to cells, merge cells, and automatically adjust column widths in an Excel file.

    Attributes:
        wb (Workbook): An openpyxl Workbook object.

    Methods:
        create_sheet(sheetname='undefine'):
            Creates a new sheet in the workbook with the given name.

        auto_fit_width(excel_name: str, sheet_name: str):
            Automatically adjusts the width of all columns in the specified sheet.

        write2cell(sheet, design, row, column, value, fill=False):
            Writes a value to a specific cell and applies formatting from a design object.

        write2mergecell(sheet, design, start_row, end_row, start_column, end_column, value, fill=False):
            Writes a value to a range of merged cells and applies formatting from a design object.

        save(xlsxname, xlsxpath, allautowidth=True):
            Saves the workbook to a specified path and optionally adjusts column widths in all sheets.

    Examples:
        >>> xm = xlsxMaker()
        >>> xd = xlsxDesigner()
        >>> demo_sheet = xm.create_sheet('demo')
        >>> xm.write2cell(sheet=demo_sheet, design=xd, row=1, column=1, value="demo1")
        >>> xm.write2cell(sheet=demo_sheet, design=xd, row=2, column=1, value="demo2")
        >>> xm.write2cell(sheet=demo_sheet, design=xd, row=1, column=2, value="demo3")
        >>> xm.write2cell(sheet=demo_sheet, design=xd, row=2, column=2, value="demo4")
        >>> xm.save("demo", "./")
    """

    def __init__(self):
        ###### import ######
        self.openpyxl = _dmimport(import_module='openpyxl')
        ####################

        self.wb = self.openpyxl.Workbook()
        self.wb.remove(self.wb['Sheet'])
        self.GV = DmGlobalVars()

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
        wb = self.openpyxl.load_workbook(excel_name)
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
    
    def save(self, xlsxname, xlsxpath, allautowidth=True):
        self.wb.save(f"{xlsxpath}{self.GV.SEP}{xlsxname}.xlsx")
        if allautowidth:
            for sheet in self.wb.sheetnames:
                self.auto_fit_width(excel_name=f"{xlsxpath}{self.GV.SEP}{xlsxname}.xlsx", sheet_name=sheet)


class NuitkaMake():
    """
    A class to facilitate building Python applications with Nuitka.

    This class simplifies the process of using Nuitka to compile Python scripts into standalone executables. It provides methods to add command-line arguments for the Nuitka build process and to execute the build.

    Attributes:
        main (str): The path to the main Python file to be compiled.
        os (module): The operating system module, dynamically imported.
        GV (GlobalVars): An instance of the GlobalVars class, providing access to global variables.
        command (str): The Nuitka command to be executed, constructed dynamically based on provided arguments.

    Examples:
        >>> nm = NuitkaMake("main.py")
        >>> nm.ADD_ARG('onefile')
        >>> nm.ADD_ARG('standalone')
        >>> nm.ADD_ARG('remove-output')
        >>> nm.ADD_ARG('follow-imports')
        >>> nm.ADD_ARG(f'output-filename="{EXE}"')
        >>> nm.ADD_ARG(f'output-dir="{CWD}"')
        >>> nm.ADD_ARG(f'windows-icon-from-ico="{ICON}"')
        >>> nm.ADD_ARG('file-description="None"')
        >>> nm.ADD_ARG('copyright="None"')
        >>> nm.ADD_ARG(f'file-version="{VER}"')
        >>> nm.ADD_ARG(f'product-version="{VER}"')
        >>> nm.MAKE()

    The class supports building applications with various configurations, including setting output directories, file names, and version information.

    Methods:
        __init__(self, main):
            Initializes the NuitkaMake instance with the path to the main Python file.

        ADD_ARG(self, arg):
            Adds a command-line argument to the Nuitka command.

        MAKE(self):
            Executes the Nuitka build command.

        HELP(self):
            Prints help information for using Nuitka.
    """

    def __init__(self, main):
        """
        main is the main file you want to build

        full implementation sample:
        # demo1.
        CWD = GV().CURRENTWORKDIR
        (Path(CWD) / "demo").unlink(missing_ok=True)
        nm = NuitkaMake(f"{CWD}/demo.py")
        nm.ADD_ARG('onefile')
        nm.ADD_ARG(rf'include-data-dir={CWD}/bin=bin')
        nm.ADD_ARG('standalone')
        nm.ADD_ARG('remove-output')
        nm.ADD_ARG(f"output-dir={CWD}")
        nm.MAKE()
        sysc("mv demo.bin demo")

        # demo2.
        CWD  = CURRENTWORKDIR
        EXE  = 'autochain'
        os.system(f"del /f /s /q {EXE}.exe")
        nm = NuitkaMake("acexe.py")
        nm.ADD_ARG('onefile')
        nm.ADD_ARG('standalone')
        nm.ADD_ARG('remove-output')
        nm.ADD_ARG('follow-imports')
        nm.ADD_ARG(f'output-filename="{EXE}"')
        nm.ADD_ARG(f'output-dir="{CWD}"')
        nm.ADD_ARG('file-description="autochain"')
        nm.ADD_ARG('copyright="Copyright (C) 2024 NVIDIA. all right reserved."')
        nm.ADD_ARG(f'file-version="1.0"')
        nm.ADD_ARG(f'product-version="1.0"')
        nm.MAKE()
        """
        ###### import ######
        self.os = _dmimport(import_module='os')
        ####################

        self.GV = DmGlobalVars()

        match self.GV.SYSTEM:
            case 'Windows':
                self.command = 'python -m nuitka'
            case 'Linux':
                self.command = 'python3 -m nuitka'
            case _:
                raise TypeError('Unsupported system')
            
        self.main = main

    def ADD_ARG(self, arg):
        self.command = self.command.replace(f' {self.main}', '')
        self.command = f'{self.command} --{arg} {self.main}'
        print(f'Adding arg: --{arg}')

    def MAKE(self):
        print("Nuitka building start ...")
        with CodeTimer():
          self.os.system(self.command)
    
    def HELP(self):
        print(self.GV.NUITKA_HELP)


def quickmake(mainfile: str, onefile: bool = True, include_dir: str = None, include_packages=[], include_modules=[], output_dir=None):
    """
    Quickly builds an application with Nuitka in the current working directory.

    This function simplifies the process of building a Python application using Nuitka. 
    It supports building the application as a single file, including additional directories, packages, and modules in the build.

    Args:
        mainfile (str): The path to the main Python file to build.
        onefile (bool): If True, builds the application as a single executable file. Defaults to True.
        include_dir (str): Path to a directory to include in the build. Defaults to None.
        include_packages (list): A list of package names to include in the build. Defaults to an empty list.
        include_modules (list): A list of module names to include in the build. Defaults to an empty list.
    """
    ###### import ######
    Path = _dmimport(from_module="pathlib", import_module='Path')
    os   = _dmimport(import_module='os')
    ####################

    GV = DmGlobalVars()
    workdir = GV.CURRENTWORKDIR
    system = GV.SYSTEM
    mainfile_name, _ = os.path.splitext(os.path.basename(mainfile)) # ideally, _ is '.py' I think.

    safe_remove(f"{workdir}{GV.SEP}{mainfile_name}.exe")
    safe_remove(f"{workdir}{GV.SEP}{mainfile_name}.bin")
    safe_remove(f"{workdir}{GV.SEP}{mainfile_name}")
    # (Path(workdir) / f"{mainfile}{''.join('.exe' if system == 'Windows' else '')}").unlink(missing_ok=True)
    
    nm = NuitkaMake(mainfile)

    if onefile:
        nm.ADD_ARG('onefile')

    if include_dir:
        include_dir_path = Path(include_dir)
        nm.ADD_ARG(rf'include-data-dir={include_dir}={include_dir_path.name}')

    if include_packages:
        for package in include_packages:
            # example : nm.ADD_ARG('--include-package=mylibrary')
            nm.ADD_ARG(f'include-package={package}')
    
    if include_modules:
        for module in include_modules:
            # example : nm.ADD_ARG('--include-module=mylibrary.mymodule')
            nm.ADD_ARG(f'include-module={module}')

    nm.ADD_ARG('standalone')
    nm.ADD_ARG('remove-output')
    if not output_dir:
        nm.ADD_ARG(f"output-dir={workdir}")
    else:
        mkdir(output_dir)
        nm.ADD_ARG(f"output-dir={output_dir}")
    nm.MAKE()

    if system == 'Linux':
        src = f"{mainfile_name}.bin"
        dst = mainfile_name
        if os.path.exists(src):
            os.rename(src, dst)
        else:
            print(f"Error: The file {src} does not exist.")


class Py2BAT():
    """
    Converts a Python (.py) file to a Windows batch (.bat) file.

    This class facilitates the conversion of a Python script into a batch file that can be executed on Windows systems. 
    It allows specifying the name and output path for the generated batch file.

    Attributes:
        main (str): The path to the Python file to be converted.
        batname (str): The name of the generated batch file. Defaults to "Null".
        output_path (str): The directory where the batch file will be saved. Defaults to the runtime path.

    Examples:
        >>> Py2BAT("main.py", batname='test').MAKE()
        This will convert 'main.py' into a batch file named 'test.bat' in the default output path.

    Methods:
        MAKE():
            Generates the batch file from the specified Python file.
    """
    def __init__(self, main, batname="Null", output_path=get_runtime_path()):
        ###### import ######
        # common
        ####################

        self.main = main
        self.batname = batname
        self.output_path = output_path
        self.GV = DmGlobalVars()
        
    def MAKE(self):
        with CodeTimer():
            with open(f'{self.main}','r', encoding="utf8") as script:
                codes = script.readlines()
                with open(f"{self.output_path}{self.GV.SEP}{self.batname}.bat", 'w', encoding="utf8") as batch:
                    batch.write(self.GV.BATHEADER)
                    batch.writelines(codes)


def _progress_bar(function, estimated_time, tstep, progress_name, tqdm_kwargs={}, args=[], kwargs={}):
    """
    Tqdm wrapper for a long-running function

        function       : function to run
        estimated_time : how long you expect the function to take
        tstep          : time delta (seconds) for progress bar updates
        tqdm_kwargs    : kwargs to construct the progress bar
        args           : args to pass to the function
        kwargs         : keyword args to pass to the function
    
    ret:
        function(*args, **kwargs)
    
    >>> test = _progress_bar(
    ...        running_function,
    ...        estimated_time=5, 
    ...        tstep=1/5.0,
    ...        tqdm_kwargs={"bar_format":"{desc}{percentage:3.1f}%|{bar:25}|"},
    ...        args=(1, "foo"), 
    ...        kwargs={"spam":"eggs"}
    ...        )
    """
    ###### import ######
    tqdm = _dmimport(import_module="tqdm")
    threading = _dmimport(import_module="threading")
    ####################

    ret = [None]  # Mutable var so the function can store its return value
    pbar = tqdm.tqdm(total=estimated_time,**tqdm_kwargs)
    pbar.set_description(progress_name)


    def return_save(function, ret, *args, **kwargs):
        ret[0] = function(*args, **kwargs)
    
    class _progress_bar_build_in_print():
        @staticmethod
        def print_with_bar(msg):
            pbar.bar_format = tqdm_kwargs["bar_format"] + msg
        @staticmethod
        def print_in_line(msg):
            pbar.write(msg)
        print = print_with_bar
        write = print_in_line

    if '_progress_bar' in kwargs.keys():
        kwargs['_progress_bar'] = _progress_bar_build_in_print

    thread = threading.Thread(target=return_save, args=(function, ret) + tuple(args), kwargs=kwargs)
    actuall_time = 0
    thread.start()

    while thread.is_alive():
        thread.join(timeout=tstep)
        if actuall_time < estimated_time:
            pbar.update(tstep)
            actuall_time += tstep
        # for actual running time are longer than estimated_time
        if actuall_time + tstep > estimated_time:
            tstep = estimated_time - actuall_time
            pbar.update(tstep)
            actuall_time += tstep
    
    # for actual function running time is shorter than estimated_time
    while(actuall_time < estimated_time):
        if actuall_time + tstep > estimated_time:
            tstep = estimated_time - actuall_time
        pbar.update(tstep)
        actuall_time += tstep

    pbar.close()
    return ret[0]


def progressbar(
        estimated_time,
        tstep=0.1,
        progress_name='',
        tqdm_kwargs={
            "leave": False,
            "bar_format": "{desc}{percentage:3.0f}%|{bar:25}|"
        }
    ):
    """
    Decorate a function to add a progress bar

    >>> @progress_wrapped(estimated_time=8, tstep=0.2, progress_name='test')
    ... def arunning_function(*args, **kwargs):
            ...
        
    there provide a build in bar-print-function if your fucntion have a "_progress_bar" parameter

    your can assign _progress_bar to anthing

    it will be redirected to build in bar-print-function

    then you can use like this way

    - print message with bar

    >>> _progress_bar.print_with_bar(message)
    or
    >>> _progress_bar.print(message)


    - print message in another line but keep progress bar moving

    >>> _progress_bar.print_in_line(message)
    or
    >>> _progress_bat.write(message)

    DEMO:
    >>> class A():
    ...     @staticmethod
    ...     @progressbar(estimated_time=8, tstep=0.1, progress_name='this is a test')
    ...     def test_print(_progress_bar):
    ...         import time
    ...         _progress_bar.print("test1")
    ...         _progress_bar.write("test1")
    ...         time.sleep(2)
    ...         _progress_bar.print_with_bar("test2")
    ...         _progress_bar.print_in_line("test2")
    ...         time.sleep(2)
    ...         _progress_bar.print_with_bar("test3")
    ...         _progress_bar.print_in_line("test3")
    ... 
    ... test_bar = None
    ... A.test_print(_progress_bar=test_bar)
    """
    ###### import ######
    functools = _dmimport(import_module="functools")
    ####################

    # back up: tqdm_kwargs={"bar_format":"{desc}: {percentage:3.0f}%|{bar:25}| {n:.1f}/{total:.1f} [{elapsed}<{remaining}]"}
    def real_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return _progress_bar(function, estimated_time=estimated_time, tstep=tstep, progress_name=progress_name, tqdm_kwargs=tqdm_kwargs, args=args, kwargs=kwargs)
        return wrapper
    return real_decorator


def merge_dicts(dict1, dict2):
    """
    Merges two dictionaries into a single dictionary.

    This function merges two dictionaries into one by iterating over their keys. 
    If both dictionaries contain the same key, and the corresponding values are also dictionaries, 
    it recursively merges them. Otherwise, the value from the second dictionary overrides the one from the first. 
    The function is designed to be used with the `dict()` constructor to create a single, merged dictionary.

    Args:
        dict1 (dict): The first dictionary to merge.
        dict2 (dict): The second dictionary to merge.

    Yields:
        tuple: A tuple of (key, value) pairs that can be converted into a dictionary.

    Example:
        >>> dict1 = {'a': 1, 'b': {'x': 2}}
        >>> dict2 = {'b': {'y': 3}, 'c': 4}
        >>> merged_dict = dict(merge_dicts(dict1, dict2))
        >>> print(merged_dict)
        {'a': 1, 'b': {'x': 2, 'y': 3}, 'c': 4}

    Note:
        Use `dict(merge_dicts(dict1, dict2))` to obtain the merged dictionary.
    """
    ###### import ######
    # common
    ####################

    for k in set(dict1) | set(dict2):
    # for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def merge_all_dicts(dict_container:list):
    """
    Merges multiple dictionaries into one.

    This function takes a list of dictionaries and merges them into a single dictionary. 
    If the list contains only one dictionary, that dictionary is returned as is. 
    If the list is empty, an empty dictionary is returned.

    Args:
        dict_container (list): A list of dictionaries to be merged.

    Returns:
        dict: A single dictionary resulting from the merger of all dictionaries in `dict_container`.

    Example:
        >>> dict1 = {'a': 1, 'b': 2}
        >>> dict2 = {'b': 3, 'c': 4}
        >>> merge_all_dicts([dict1, dict2])
        {'a': 1, 'b': 3, 'c': 4}
    """
    ###### import ######
    # common
    ####################

    if len(dict_container) > 1:
        for idx in range(len(dict_container)):
            if idx == 0:
                temp = dict(merge_dicts(dict_container[0], dict_container[1]))
            elif idx == 1:
                continue
            else:
                temp = dict(merge_dicts(temp, dict_container[idx]))
        return temp
    elif len(dict_container) == 1:
        return dict_container[0]
    else:
        return {}


def print_aligned(string1, string2, align_width=10, print_func=print):
    """
    Prints two strings aligned, with the first string left-aligned to a specified width.

    This function prints two strings on the same line with the first string left-aligned to a specified width, 
    followed immediately by the second string. 
    It allows for a custom print function to be specified, enabling redirection of the output if needed.

    Args:
        string1 (str): The first string to print, which will be left-aligned.
        string2 (str): The second string to print, which follows the first string.
        align_width (int, optional): The width to which the first string will be aligned. Defaults to 10.
        print_func (Callable[[str], None], optional): A custom print function to use for printing. Defaults to the built-in print function.

    Returns:
        None
    """
    ###### import ######
    # common
    ####################
    
    print_func(f'{string1:<{align_width}}{string2}')


def print_k_v_aligned(src_dict: dict , print_func=print) -> None:
    """
    Prints each key-value pair in a dictionary aligned by the longest key.

    This function iterates through a dictionary, 
    aligning each key-value pair based on the length of the longest key. 
    It allows for a custom print function to be specified, enabling redirection of the output if needed.

    Args:
        src_dict (dict): The source dictionary whose key-value pairs are to be printed.
        print_func (Callable[[str], None], optional): A custom print function to use for printing. Defaults to the built-in print function.

    Returns:
        None
    """
    longest_key_length = max(len(key) for key in src_dict.keys())
    for key, value in src_dict.items():
        print_func(f"{key.ljust(longest_key_length)} : {value}")


def _test_connection(name, url, timeout=10):
    """Simple connection test"""
    ###### import ######
    socket = _dmimport(import_module="socket")
    time = _dmimport(import_module="time")
    try:
        urlopen, urlparse = _dmimport(from_module='urllib.request', import_module='urlopen, urlparse')
    except ImportError:
        urlopen, urlparse = _dmimport(from_module='urllib2', import_module='urlopen, urlparse')
    ####################

    urlinfo = urlparse(url)
    start = time.time()
    try:
        ip = socket.gethostbyname(urlinfo.netloc)
    except Exception as e:
        print('Error resolving DNS for {}: {}, {}'.format(name, url, e))
        return
    dns_elapsed = time.time() - start
    start = time.time()
    try:
        _ = urlopen(url, timeout=timeout)
    except Exception as e:
        print("Error open {}: {}, {}, DNS finished in {} sec.".format(name, url, e, dns_elapsed))
        return
    load_elapsed = time.time() - start
    print("Timing for {}: {}, DNS: {:.4f} sec, LOAD: {:.4f} sec.".format(name, url, dns_elapsed, load_elapsed))


def _check_network(region="cn", timeout=10):
    ###### import ######
    socket = _dmimport(import_module="socket")
    ####################

    GV = DmGlobalVars()
    print_aligned("[Network Test", "]", 15)
    if timeout > 0:
        print(f'Setting timeout: {timeout}')
        socket.setdefaulttimeout(10)
    for region in region.strip().split(','):
        r = region.strip().lower()
        if not r:
            continue
        if r in GV.REGIONAL_URLS:
            GV.URLS.update(GV.REGIONAL_URLS[r])
        else:
            import warnings
            warnings.warn(f'Region {r} do not need specific test, please refer to global sites.')
    for name, url in GV.URLS.items():
        _test_connection(name, url, timeout)


def _check_python():
    ###### import ######
    platform = _dmimport(import_module="platform")
    ####################

    print_aligned("[Python", "]", 15)
    print('Version      :', platform.python_version())
    print('Compiler     :', platform.python_compiler())
    print('Build        :', platform.python_build())
    print('Arch         :', platform.architecture())


def _check_pip():
    ###### import ######
    pip = _dmimport(import_module="pip")
    os = _dmimport(import_module="os")
    ####################

    print_aligned("[pip", "]", 15)
    try:
        print('Version      :', pip.__version__)
        print('Directory    :', os.path.dirname(pip.__file__))
    except ImportError:
        print('No corresponding pip install for current python.')


def _check_pytorch():
    ###### import ######
    torch = _dmimport(import_module="torch")
    ####################

    print_aligned("[Pytorch", "]", 15)
    if torch:
        print(torch)
        print('Version      :',torch.__version__)
        cudaenbale = torch.cuda.is_available()
        device = torch.device("cuda" if cudaenbale else "cpu") 
        if cudaenbale: 
            print('CUDA         :', torch.version.cuda)
            print('CUDNN        :', torch.backends.cudnn.version())
            print('GPU          :', torch.cuda.get_device_name(device))
    else:
        print('No Pytorch installed.')


def _check_mxnet():
    ###### import ######
    mxnet = _dmimport(import_module="mxnet")
    os    = _dmimport(import_module="os")
    ####################

    print_aligned("[Mxnet", "]", 15)
    if mxnet:
        def get_build_features_str():
            features = mxnet.runtime.Features()
            return '\n'.join(map(str, list(features.values())))
        
        print('Version      :', mxnet.__version__)
        mx_dir = os.path.dirname(mxnet.__file__)
        print('Directory    :', mx_dir)
        try:
            branch = mxnet.runtime.get_branch()
            commit_hash = mxnet.runtime.get_commit_hash()
            print('Branch       :', branch)
            print('Commit Hash  :', commit_hash)
        except AttributeError:
            commit_hash = os.path.join(mx_dir, 'COMMIT_HASH')
            if os.path.exists(commit_hash):
                with open(commit_hash, 'r') as f:
                    ch = f.read().strip()
                    print('Commit Hash   :', ch)
            else:
                print('Commit hash file "{}" not found. Not installed from pre-built package or built from source.'.format(commit_hash))
        print('Library      :', mxnet.libinfo.find_lib_path())
        try:
            print('Build features:')
            print(get_build_features_str())
        except (AttributeError, ModuleNotFoundError):
            print('No runtime build feature info available')
    else:
        print('No MXNet installed.')


def _check_os():
    ###### import ######
    platform = _dmimport(import_module="platform")
    sys      = _dmimport(import_module="sys")
    ####################

    print_aligned("[System", "]", 15)
    print('Platform     :', platform.platform())
    print('system       :', platform.system())
    print('node         :', platform.node())
    print('release      :', platform.release())
    print('version      :', platform.version())
    print('syspath      :')
    print('\n'.join(sys.path))


def _check_hardware():
    ###### import ######
    platform = _dmimport(import_module="platform")
    subprocess = _dmimport(import_module="subprocess")
    ####################
    
    print_aligned("[Hardware", "]", 15)
    print('machine      :', platform.machine())
    print('processor    :', platform.processor())
    
    if DmGlobalVars().SYSTEM == "linux":
        subprocess.call(['lscpu'])
    elif DmGlobalVars().SYSTEM == "windows":
        out, _ = sysc("wmic cpu get name")
        cpu = out.split('\n')[2]
        print('CPU          :', cpu)


def _check_environment():
    ###### import ######
    os = _dmimport(import_module="os")
    ####################

    print_aligned("[Env", "]", 15)
    for k,v in os.environ.items():
        # if k.startswith('MXNET_') or k.startswith('OMP_') or k.startswith('KMP_') or k == 'CC' or k == 'CXX':
            print('{}="{}"'.format(k,v))


def check_your_system():
    """Diagnoses the current system by running a series of checks."""
    _check_os()
    _check_hardware()
    _check_network()
    _check_python()
    _check_pip()
    _check_pytorch()
    #_check_environment()
    #_check_mxnet()


def traceback_get():
    """
    Retrieves the traceback string of the current exception.

    Returns:
        str: The traceback string of the current exception.
    """
    ###### import ######
    traceback = _dmimport(import_module="traceback")
    ####################

    return traceback.format_exc()


def traceback_print() -> None:
    """
    Prints the traceback of the current exception to stderr.

    Returns:
        None
    """
    ###### import ######
    traceback = _dmimport(import_module="traceback")
    ####################

    traceback.print_exc()


def exception_get(e):
    """
    Retrieves a detailed string representation of an exception.

    Args:
        e (Exception): The exception instance to be processed.

    Returns:
        str: A string that represents the detailed information of the exception, including its type and message.

    Example:
        try:
            # Code that might raise an exception
        except Exception as e:
            detailed_exception_info = exception_get(e)
            print(detailed_exception_info)  # Prints the detailed string representation of the exception
    """
    ###### import ######
    # common
    ####################

    return repr(e)


def exception_print(e) -> None:
    """
    Prints a detailed representation of an exception.

    Parameters:
        e (Exception): The exception to be printed.

    Example:
        try:
            # Code that may raise an exception
        except Exception as e:
            exception_print(e)  # Prints the detailed representation of the exception
    """
    ###### import ######
    # common
    ####################

    print(repr(e))


def read_treezip(treezip, factory_lst=[], product_lst=[], station_lst=[], type_lst=[]) -> list:
    """
    This module contains a function for reading and processing treezip files. 
    It is specifically designed to work with a custom format of tree files. 
    Using it with other formats may not yield the intended results.

    Function:
        read_treezip(treezip, factory_lst=[], product_lst=[], station_lst=[], type_lst=[]):
            Reads and processes a treezip file according to the specified filters.

            Parameters:
                treezip (FileType): The treezip file to be read. This should be in the custom 
                    format designed for this function.
                factory_lst (list, optional): A list of factory identifiers to filter the data. 
                    Defaults to an empty list, meaning no filtering on this criterion.
                product_lst (list, optional): A list of product identifiers to filter the data. 
                    Defaults to an empty list, meaning no filtering on this criterion.
                station_lst (list, optional): A list of station identifiers to filter the data. 
                    Defaults to an empty list, meaning no filtering on this criterion.
                type_lst (list, optional): A list of type identifiers to filter the data. 
                    Defaults to an empty list, meaning no filtering on this criterion.

            Returns:
                list: A list of processed data entries that match the specified filters. The 
                    structure and content of these entries depend on the custom tree file format.
    """
    ###### import ######
    zipfile = _dmimport(import_module="zipfile")
    shutil  = _dmimport(import_module="shutil")
    os      = _dmimport(import_module="os")
    ####################

    GV = DmGlobalVars()
    path_list = []
    shutil.copyfile(treezip, fr"{GV.CURRENTWORKDIR}{GV.SEP}tmptree.zip")
    print(f"copy file to {GV.CURRENTWORKDIR}{GV.SEP}tmptree.zip")
    treezip = fr"{GV.CURRENTWORKDIR}{GV.SEP}tmptree.zip" 

    if factory_lst and not product_lst and not station_lst:
        scenario = "FACTORY_ONLY"
    elif factory_lst and product_lst and not station_lst:
        scenario = "FACTORY_plus_PRODUCT"
    elif factory_lst and not product_lst and station_lst:
        scenario = "FACTORY_plus_STATION"
    elif factory_lst and product_lst and station_lst:
        scenario = "FACTORY_plus_PRODUCT_plus_STATION"
    elif not factory_lst and product_lst and not station_lst:
        scenario = "PRODUCT_ONLY"
    elif not factory_lst and product_lst and station_lst:
        scenario = "PRODUCT_plus_STATION"
    elif not factory_lst and not product_lst and station_lst:
        scenario = "STATION_ONLY"
    elif not factory_lst and not product_lst and not station_lst:
        scenario = "ALL"

    match scenario:
        case "ALL":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    with z.open(tree_file, 'r') as file:
                        abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                        if type_lst:
                            for abs_path in abs_path_list:
                                if any(log_type in abs_path for log_type in type_lst):
                                    path_list.append(abs_path)
                        else:
                            path_list.extend(abs_path_list)
        
        case "FACTORY_ONLY":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    factory_in_tree = tree_file.split('_')[0]
                    if factory_in_tree in factory_lst:
                        with z.open(tree_file, 'r') as file:
                            abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                        if type_lst:
                            for abs_path in abs_path_list:
                                if any(log_type in abs_path for log_type in type_lst):
                                    path_list.append(abs_path)
                        else:
                            path_list.extend(abs_path_list)
        
        case "PRODUCT_ONLY":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    with z.open(tree_file, 'r') as file:
                        abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                        for abs_path in abs_path_list:
                            try:
                                product_in_tree = abs_path.split(GV.SEP)[-1].split("_")[2]
                            except Exception:
                                continue
                            if any(product in product_in_tree for product in product_lst):
                                if type_lst:
                                    if any(log_type in abs_path for log_type in type_lst):
                                        path_list.append(abs_path)
                                else:
                                    path_list.append(abs_path)
        
        case "STATION_ONLY":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    with z.open(tree_file, 'r') as file:
                        abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                        for abs_path in abs_path_list:
                            try:
                                station_in_tree = abs_path.split(GV.SEP)[-1].split("_")[5]
                            except Exception:
                                continue
                            if any(station in station_in_tree for station in station_lst):
                                if type_lst:
                                    if any(log_type in abs_path for log_type in type_lst):
                                        path_list.append(abs_path)
                                else:
                                    path_list.append(abs_path)
        
        case "FACTORY_plus_PRODUCT":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    factory_in_tree = tree_file.split('_')[0]
                    if factory_in_tree in factory_lst:
                        with z.open(tree_file, 'r') as file:
                            abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                            for abs_path in abs_path_list:
                                try:
                                    product_in_tree = abs_path.split(GV.SEP)[-1].split("_")[2]
                                except Exception:
                                    continue
                                if any(product in product_in_tree for product in product_lst):
                                    if type_lst:
                                        if any(log_type in abs_path for log_type in type_lst):
                                            path_list.append(abs_path)
                                    else:
                                        path_list.append(abs_path)
        
        case "FACTORY_plus_STATION":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    factory_in_tree = tree_file.split('_')[0]
                    if factory_in_tree in factory_lst:
                        with z.open(tree_file, 'r') as file:
                            abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                            for abs_path in abs_path_list:
                                try:
                                    station_in_tree = abs_path.split(GV.SEP)[-1].split("_")[5]
                                except Exception:
                                    continue
                                if any(station in station_in_tree for station in station_lst):
                                    if type_lst:
                                        if any(log_type in abs_path for log_type in type_lst):
                                            path_list.append(abs_path)
                                    else:
                                        path_list.append(abs_path)
        
        case "FACTORY_plus_PRODUCT_plus_STATION":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    factory_in_tree = tree_file.split('_')[0]
                    if factory_in_tree in factory_lst:
                        with z.open(tree_file, 'r') as file:
                            abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                            for abs_path in abs_path_list:
                                try:
                                    product_in_tree = abs_path.split(GV.SEP)[-1].split("_")[2]
                                    station_in_tree = abs_path.split(GV.SEP)[-1].split("_")[5]
                                except Exception:
                                    continue
                                if any(station in station_in_tree for station in station_lst) and any(product in product_in_tree for product in product_lst):
                                    if type_lst:
                                        if any(log_type in abs_path for log_type in type_lst):
                                            path_list.append(abs_path)
                                    else:
                                        path_list.append(abs_path)
        
        case "PRODUCT_plus_STATION":
            with zipfile.ZipFile(treezip, "r") as z:
                for tree_file in reversed(z.namelist()):
                    with z.open(tree_file, 'r') as file:
                        abs_path_list = list(map(lambda x: x.decode().strip(), file.readlines()))
                        for abs_path in abs_path_list:
                            try:
                                product_in_tree = abs_path.split(GV.SEP)[-1].split("_")[2]
                                station_in_tree = abs_path.split(GV.SEP)[-1].split("_")[5]
                            except Exception:
                                continue
                            if any(station in station_in_tree for station in station_lst) and any(product in product_in_tree for product in product_lst):
                                if type_lst:
                                    if any(log_type in abs_path for log_type in type_lst):
                                        path_list.append(abs_path)
                                else:
                                    path_list.append(abs_path)
    os.remove(treezip)
    print("Parsing Tree File Successfully!")
    return path_list


class DmArgs():
    """
    A utility module providing a simplified interface for command-line argument parsing.

    This module offers a wrapper around argparse, making it easier to define and access command-line arguments in scripts and applications. 
    It streamlines the process of argument definition and parsing, allowing for a more concise and readable way to handle command-line inputs.

    Example Usage:
        args = dmargs("A brief description of the script")
        args.add_arg("-t", "--test", type=int, default=1, help="An example integer argument (default: %(default)s)")
        args = args()

        # Access the argument value
        test_value = args.test
        print(f"Test Argument Value: {test_value}")
    """

    def __init__(self, description: str = "") -> None:
        ###### import ######
        self.argparse = _dmimport(import_module="argparse")
        ####################

        description = dedent(description)
        self.parser = self.argparse.ArgumentParser(description=description, formatter_class=self.argparse.RawDescriptionHelpFormatter)

    def add_arg(self, *args, **kwargs) -> None:
        """
        - add_arg('-a', '--arg1', type=int, default=1, help="Description for arg1, (default: %(default)s)")
        - add_arg('-c', '--arg3', type=str, default='', choices=['str1', 'str2', 'str3', 'str4'], help='')
        - add_arg('-b', '--arg2', metavar='X', type=str, nargs='+', choices=['1', '2', '3'], help='')
        
        - add_arg('-f', '--flag', action="store_true", help="Enable some flag")
            Action: "store_true" means that if the -f or --flag is present in the command line,
            the corresponding variable is set to True. If not present, it defaults to False.
            This type of argument is typically used for enabling features or modes.

        - add_arg('-t', '--trial', action=argparse.BooleanOptionalAction, default=False, help='trial build or not, default False')
            Action: argparse.BooleanOptionalAction allows the argument to be used as a flag that
            can explicitly set the corresponding variable to True or False. If --trial is used,
            the variable is set to True. If --no-trial is used, it's set to False. If neither is
            specified, it defaults to the value provided by the default parameter.
        """
        self.parser.add_argument(*args, **kwargs)

    def add_subparser(self, *args, **kwargs) -> None:
        return self.parser.add_subparsers(*args, **kwargs)

    def add_argument_group(self, parser_inst, *args, **kwargs) -> None:
        parser_inst.add_argument_group(*args, **kwargs)

    def __call__(self, print_argv: bool=False, print_func=print):
        """
        Args:
            print_argv (bool, optional): Flag for printing out the args value. Defaults to False.
            print_func (_type_, optional): Print function. Defaults to print.
        """
        args = self.parser.parse_args()

        if print_argv:
            print_func("Args:")
            print_k_v_aligned(vars(args), print_func)

        return args


if __name__ == "__main__":
    LOG = DmLog(branch="dmutils")
    GV = DmGlobalVars()
    print_aligned("Version", f": {__version__}", print_func=LOG.info)
    print_aligned("Author", f": {__author__}", print_func=LOG.info)
    print_aligned("Email", f": {__email__}", print_func=LOG.info)   
    print_aligned("date", f": {__date__}", print_func=LOG.info)
    print_aligned("system", f": {GV.SYSTEM}", print_func=LOG.info)
    print_aligned("workdir", f": {GV.CURRENTWORKDIR}", print_func=LOG.info)
    safe_remove("./tmp.txt")
