#!/usr/bin/env python

from distutils.core import setup

from squawk import __version__ as version

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name = 'squawk',
    version = version,
    description = 'SQL query tool and library for static files',
    long_description = long_description,
    author = 'Samuel Stauffer',
    author_email = 'samuel@descolada.com',
    url = 'http://github.com/samuel/squawk',
    packages = ['squawk'],
    license = "BSD",
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
