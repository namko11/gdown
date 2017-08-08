# -*- coding: utf-8 -*-

"""
gdown.modules.nitroflare
~~~~~~~~~~~~~~~~~~~

This module contains handlers for nitroflare.

"""

import re
# from datetime import datetime, timedelta
# from time import sleep
# from decimal import Decimal

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    # cloudflare challenge
