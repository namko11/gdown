#!/usr/bin/env python
import pypremium

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = [
    'requests<1.0',
]

setup(
    name=pypremium.__title__,
    version=pypremium.__version__,
    #description='',
    long_description=open('README.rst').read(),
    author='oczkers',
    author_email='oczkers@gmail.com',
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',
        #'Programming Language :: Python :: 3.1',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)
