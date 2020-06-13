#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os.path
import warnings
import sys


try:
    from setuptools import setup, Command

    setuptools_available = True
except ImportError:
    from distutils.core import setup, Command

    setuptools_available = False
from distutils.spawn import spawn


# Get the version from picta_dl/version.py without importing the package
exec(compile(open("picta_dl/version.py").read(), "picta_dl/version.py", "exec"))

DESCRIPTION = "Picta video downloader"
LONG_DESCRIPTION = "Command-line program to download videos from Picta.cu Plataforma de Contenidos Audiovisuales and YouTube.com"


try:
    # This will create an exe that needs Microsoft Visual C++ 2008
    # Redistributable Package
    import PyInstaller
    from PyInstaller.utils.win32.versioninfo import (
        VarStruct,
        VarFileInfo,
        StringStruct,
        StringTable,
        StringFileInfo,
        FixedFileInfo,
        VSVersionInfo,
        SetVersion,
    )

    def version2tuple(commit=0):
        version_list = str(__version__).split(".")
        if len(version_list) > 3:
            _commit = int(version_list[3])
            del version_list[3]
        else:
            _commit = commit

        _year, _month, _day = [int(value) for value in version_list]
        return (_year, _month, _day, _commit)

    def version2str(commit=0):
        version_tuple = version2tuple(commit)
        return "%s.%s.%s.%s" % version_tuple

    class build_pyinstaller_exe(Command):

        description = "Build the executable"
        user_options = []
        version_file = VSVersionInfo(
            ffi=FixedFileInfo(
                filevers=version2tuple(),
                prodvers=version2tuple(),
                mask=0x3F,
                flags=0x0,
                OS=0x4,
                fileType=0x1,
                subtype=0x0,
                date=(0, 0),
            ),
            kids=[
                VarFileInfo([VarStruct("Translation", [0, 1200])]),
                StringFileInfo(
                    [
                        StringTable(
                            "000004b0",
                            [
                                StringStruct("CompanyName", "oleksis.fraga@gmail.com"),
                                StringStruct("FileDescription", DESCRIPTION),
                                StringStruct("FileVersion", version2str()),
                                StringStruct("InternalName", "picta-dl.exe"),
                                StringStruct(
                                    "LegalCopyright",
                                    "https://github.com/oleksis/youtube-dl/tree/picta-dl/LICENSE",
                                ),
                                StringStruct("OriginalFilename", "picta-dl.exe"),
                                StringStruct("ProductName", "Picta-DL"),
                                StringStruct("ProductVersion", version2str()),
                            ],
                        )
                    ]
                ),
            ],
        )

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self, version=version_file):
            spawn(
                [
                    "pyinstaller",
                    "-c",
                    "-F",
                    "--icon=assets/picta-dl.ico",
                    "--name=picta-dl",
                    "picta_dl/__main__.py",
                ],
                dry_run=self.dry_run,
            )
            SetVersion("./dist/picta-dl.exe", version)


except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == "pyinstaller":
        print("Cannot import pyinstaller", file=sys.stderr)
        exit(1)

pyinstaller_console = [
    {
        "script": "./picta_dl/__main__.py",
        "dest_base": "picta-dl",
        "version": __version__,
        "description": DESCRIPTION,
        "comments": LONG_DESCRIPTION,
        "product_name": "picta-dl",
        "product_version": __version__,
    }
]


if len(sys.argv) >= 2 and sys.argv[1] == "pyinstaller":
    make_executalble = True
    pyinstaller_cmd = {
        "pyinstaller": build_pyinstaller_exe,
    }
    params = dict()
else:
    make_executalble = False
    files_spec = [
        ("etc/bash_completion.d", ["picta-dl.bash-completion"]),
        ("etc/fish/completions", ["picta-dl.fish"]),
        ("share/doc/picta_dl", ["README.txt"]),
        ("share/man/man1", ["picta-dl.1"]),
    ]
    root = os.path.dirname(os.path.abspath(__file__))
    data_files = []
    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn(
                    "Skipping file %s since it is not present. Type  make  to build all automatically generated files."
                    % fn
                )
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {
        "data_files": data_files,
    }
    if setuptools_available:
        params["entry_points"] = {"console_scripts": ["picta-dl = picta_dl:main"]}
    else:
        params["scripts"] = ["bin/picta-dl"]


class build_lazy_extractors(Command):
    description = "Build the extractor lazy loading module"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        spawn(
            [
                sys.executable,
                "devscripts/make_lazy_extractors.py",
                "picta_dl/extractor/lazy_extractors.py",
            ],
            dry_run=self.dry_run,
        )


cmdclass = {"build_lazy_extractors": build_lazy_extractors}

if make_executalble:
    cmdclass.update(pyinstaller_cmd)


setup(
    name="picta_dl",
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/oleksis/youtube-dl/tree/picta-dl",
    author="Ricardo Garcia",
    author_email="ytdl@yt-dl.org",
    maintainer="Oleksis Fraga",
    maintainer_email="oleksis.fraga@gmail.com",
    license="Unlicense",
    packages=[
        "picta_dl",
        "picta_dl.extractor",
        "picta_dl.downloader",
        "picta_dl.postprocessor",
    ],
    # Provokes warning on most systems (why?!)
    # test_suite = 'nose.collector',
    # test_requires = ['nosetest'],
    classifiers=[
        "Topic :: Multimedia :: Video",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: IronPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    cmdclass=cmdclass,
    **params
)
