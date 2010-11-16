#!/usr/bin/env python

from distutils.core import setup

import os
execfile(os.path.join('squawk', 'version.py'))

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name = 'squawk',
    version = VERSION,
    description = 'SQL query tool and library for static files',
    long_description = long_description,
    author = 'Samuel Stauffer',
    author_email = 'samuel@descolada.com',
    url = 'http://github.com/samuel/squawk',
    packages = ['squawk', 'squawk/parsers'],
    license = "BSD",
    scripts = ['bin/squawk'],
    requires = ["pyparsing"],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
