# -*- coding: utf-8 -*-

"""
gdown
~~~~~~~~~~~~~~~~~~~~~

gdown is a simple library for managing sharing websites (like netload.in).

Usage:

    >>> from gdown import hotfile
    >>> hotfile.accInfo('login', 'password')
    {
        'email': 'sample@email.com',
        'id': 542,
        'status': 'premium',
        'expire_date': datetime.datetime(2014, 5, 28, 11, 16, 33)
    }
    >>> file_url = hotfile.getUrl('https://hotfile.com/dl/193966926/685bd36/chrome_frame_helper.dll.html', 'login', 'password')
    'http://s749.hotfile.com/get/f4ac4f6ae12e42973bca22b969c3b99915f9383b/51196253/1/4a70d63eb35925fa/b8fb34e/496034/chrome_frame_helper.dll'


:copyright: (c) 2013 by Piotr Staroszczyk.
:license: GNU GPLv3, see LICENSE for more details.

"""

__title__ = 'gdown'
__version__ = '0.0.1'
__author__ = 'Piotr Staroszczyk'
__license__ = 'GNU GPL v3'
__copyright__ = 'Copyright 2013 Piotr Staroszczyk'

from .modules import *
