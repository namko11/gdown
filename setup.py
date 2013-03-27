#!/usr/bin/env python
import gdown

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'gdown',
]

requires = [
    'requests<1.0',
]

setup(
    name=gdown.__title__,
    version=gdown.__version__,
    #description='',
    long_description=open('README.rst').read(),
    author='Piotr Staroszczyk',
    author_email='piotr.staroszczyk@get24.org',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'gdown': 'gdown'},
    include_package_data=True,
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
