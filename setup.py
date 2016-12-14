#!/usr/bin/env python

"""
tyler
-----
A simple tail written in python that can be used as a module for 
personal project or as a standalone program

Copyright 2016 Davide Mastromatteo
License: Apache 2.0
"""

from setuptools import setup
VERSION = "0.3"

setup(
    name='pytyler',
    version=VERSION,
    url='http://github.com/mastro35/tyler/',
    license='Apache-2.0',
    author='Davide Mastromatteo',
    author_email='dave35@me.com',
    description='a simple Python tail',
    long_description=__doc__,
    py_modules=['tyler'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    extras_require={'Win32 Optional Dependencies': ['pypiwin32>=219',
                                                    'pymssql>=2.1.3']
                   },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={'console_scripts': ['tyler=tyler:main',]}
)
