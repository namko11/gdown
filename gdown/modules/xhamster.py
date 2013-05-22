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
    r = browser()
    content = r.get(link).content
    srv = re.search("'srv': '(.+)',", content).group(1)
    file_name = re.search("'file': '(.+)',", content).group(1)
    link = '%s/flv2/%s' % (srv, file_name)
    return r.get(link).url
