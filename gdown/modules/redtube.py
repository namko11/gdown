# -*- coding: utf-8 -*-

"""
gdown.modules.redtube
~~~~~~~~~~~~~~~~~~~

This module contains handlers for redtube.

"""

import re

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = browser()
    content = opera.get(link).content
    link = re.search('<source src="(.+)" type="video/mp4">', content).group(1)
    return opera.get(link).url
