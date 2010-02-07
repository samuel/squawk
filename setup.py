#!/usr/bin/env python

from distutils.core import setup

from squawk import __version__ as version

setup(
    name = 'squawk',
    version = version,
    description = 'SQL query tool and library for static files',
    author = 'Samuel Stauffer',
    author_email = 'samuel@descolada.com',
    url = 'http://github.com/samuel/squawk',
    packages = ['squawk'],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
