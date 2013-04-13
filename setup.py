#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gdown

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'gdown',
    'gdown.modules',
]

requires = []

setup(
    name=gdown.__title__,
    version=gdown.__version__,
    #description='',
    long_description=open('README.rst').read(),
    author=gdown.__author__,
    author_email='piotr.staroszczyk@get24.org',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'gdown': 'gdown'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',  # not tested
        #'Programming Language :: Python :: 3.1',  # not tested
        #'Programming Language :: Python :: 3.2',  # not tested
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: Implementation :: CPython',  # not tested
        #'Programming Language :: Python :: Implementation :: IronPython',  # not tested
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
