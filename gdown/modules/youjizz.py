# -*- coding: utf-8 -*-

"""
gdown.modules.youjizz
~~~~~~~~~~~~~~~~~~~

This module contains handlers for youjizz.

"""

import re

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = browser()
    content = opera.get(link).content
    link = re.search('so.addVariable\("file","(.+)"\);', content).group(1)
    return opera.get(link).url
