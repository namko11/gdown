# -*- coding: utf-8 -*-

"""
gdown.modules.pornhub
~~~~~~~~~~~~~~~~~~~

This module contains handlers for pornhub.

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
    content = r.get(link).text
    link = unquote(re.search('to.addVariable\("video_url","(.+)"\);', content).group(1))
    return r.get(link).url
