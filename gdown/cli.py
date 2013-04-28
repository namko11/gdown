#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""gdown (command-line interface to the gdown library)

Usage:
    gdown
    gdown -h | --help | --version

Options:
    -h --help  Show this screen.
    --version  Show version.

"""

from docopt import docopt

from . import __title__, __version__, __author__, __license__, __copyright__


def main():
    arguments = docopt(__doc__, version=__version__)
    print arguments
