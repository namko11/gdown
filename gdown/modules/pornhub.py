# -*- coding: utf-8 -*-

"""
gdown.modules.pornhub
~~~~~~~~~~~~~~~~~~~

This module contains handlers for pornhub.

"""

import re
from urllib import unquote

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = browser()
    content = opera.get(link).content
    link = unquote(re.search('to.addVariable\("video_url","(.+)"\);', content).group(1))
    return opera.get(link).url
