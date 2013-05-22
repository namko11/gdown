# -*- coding: utf-8 -*-

"""
gdown.modules.xvideos
~~~~~~~~~~~~~~~~~~~

This module contains handlers for xvideos.

"""

import re
try:
    from urllib import unquote
except:
    from urllib.parse import unquote

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    r = browser()
    content = r.get(link).content
    link = unquote(re.search('flv_url=(.*?)&amp;', content).group(1))
    return r.get(link).url
