#!/usr/bin/env python

"""
inirama
-------

inirama -- Parse INI files

"""
import os

from setuptools import setup

from inirama import __version__, __project__, __license__


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name=__project__,
    version=__version__,
    license=__license__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=('Any'),

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen/inirama',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],

    py_modules=['inirama'],
    install_requires = read('requirements.txt').split(),
    test_suite = 'tests',
)
