#!/usr/bin/env python

""".

Inirama
-------

inirama -- Parse INI files

"""
import os
import re

from setuptools import setup


def _read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

_meta = _read('inirama.py')
_version = re.search(r'^__version__\s*=\s*"(.*)"', _meta, re.M).group(1)
_license = re.search(r'^__license__\s*=\s*"(.*)"', _meta, re.M).group(1)
_project = re.search(r'^__project__\s*=\s*"(.*)"', _meta, re.M).group(1)


setup(
    name=_project,
    version=_version,
    license=_license,
    description=_read('DESCRIPTION'),
    long_description=_read('README.rst'),
    platforms=('Any'),
    keywords="config parser ini",

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen/inirama',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],

    py_modules=['inirama'],
    test_suite='tests',
)
