# -*- coding: utf-8 -*-

"""
gdown.modules.youporn
~~~~~~~~~~~~~~~~~~~

This module contains handlers for youporn.

"""

import re

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    r = browser()
    videoid = re.match('$http://[w\.]{,4}youporn.com/watch/(.+?)/.+^', link).group(1)
    link = 'http://download.youporn.com/download/%s?xml=1' % (videoid)
    content = r.get(link).content
    link = re.search('<location>(.+)</location>', content).group(1)
    return r.get(link).url
