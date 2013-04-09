# -*- coding: utf-8 -*-

"""
gdown.modules.xhamster
~~~~~~~~~~~~~~~~~~~

This module contains handlers for xhamster.

"""

import re

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = browser()
    content = opera.get(link).content
    srv = re.search("'srv': '(.+)',", content).group(1)
    file_name = re.search("'file': '(.+)',", content).group(1)
    link = '%s/flv2/%s' % (srv, file_name)
    return opera.get(link).url
