#!/usr/bin/env python

"""
inirama
-------

inirama -- Parse INI files

"""
import os
from sys import version_info

from setuptools import setup


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


install_requires = read('requirements.txt').split()
if version_info < (2, 7):
    install_requires.append('ordereddict')


setup(
    name="Inirama",
    version="0.4.0",
    license="BSD",
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
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

    install_requires=install_requires,
    py_modules=['inirama'],
    test_suite = 'tests',
)
