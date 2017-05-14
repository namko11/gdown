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
    r = browser()
    content = r.get(link).text
    link = re.search('<source src="(.+)" type="video/mp4">', content).group(1)
    return r.get(link).url
