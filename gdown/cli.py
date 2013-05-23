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

from . import __title__, __version__, __author__, __license__, __copyright__
from . import modules


# TODO: api
def accInfo(username, passwd):
    """Return account info."""
    pass


def main():
    args = docopt(__doc__, version=__version__)
    print args  # DEBUG
    module = getattr(modules, args['<module>'].lower(), None)
    if not module:
        print 'Sorry, {} module not found.'.format(args['<module>'])
    if args['<command>'].lower() == 'accinfo':
        if not hasattr(module, 'accInfo'):
            print 'Sorry, {} module does not support this command yet.'.format(args['<module>'])
        print module.accInfo(args['<username>'], args['<password>'])


if __name__ == '__main__':
    main()
