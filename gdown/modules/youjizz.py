# -*- coding: utf-8 -*-

import re

from ..core import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = browser()
    content = opera.get(link).content
    link = re.search('so.addVariable\("file","(.+)"\);', content).group(1)
    return opera.get(link).url
