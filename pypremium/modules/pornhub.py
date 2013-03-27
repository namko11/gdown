# -*- coding: utf-8 -*-

import requests
import re
from urllib import unquote

from ..config import headers


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = requests.session(headers=headers)
    content = opera.get(link).content
    link = unquote(re.search('to.addVariable\("video_url","(.+)"\);', content).group(1))
    return opera.get(link).url
