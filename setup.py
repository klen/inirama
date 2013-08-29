#!/usr/bin/env python

"""
inirama
-------

inirama -- Parse INI files

"""
import os

from setuptools import setup


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="Inirama",
    version="0.5.0",
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

    py_modules=['inirama'],
    test_suite = 'tests',
)
