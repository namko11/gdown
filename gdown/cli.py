#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""gdown (command-line interface to the gdown library)

Usage:
    gdown <command> <module> [(-u <username> -p <password>)]

Options:
    -h --help  Show this screen.
    --version  Show version.

"""

from docopt import docopt
from clint.textui import colored

#from . import __title__, __version__, __author__, __license__, __copyright__
#from . import modules
import modules
__version__ = '0.0.1'


def accInfo(username, passwd):
    """Return account info."""
    pass


def main():
    args = docopt(__doc__, version=__version__)
    print args  # DEBUG
    if args['<command>'].lower() == 'accinfo':
        if hasattr():  # module has attribute?
            #accInfo(username, passwd)
            pass
        else:
            print 'Sorry, %s module does not support this command yet.' % args['<module>']


if __name__ == '__main__':
    main()
