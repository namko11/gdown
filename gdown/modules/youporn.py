# -*- coding: utf-8 -*-

import requests
import re

from ..config import headers


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = requests.Session()
    opera.headers = headers
    videoid = re.match('$http://[w\.]{,4}youporn.com/watch/(.+?)/.+^', link).group(1)
    link = 'http://download.youporn.com/download/%s?xml=1' % (videoid)
    content = opera.get(link).content
    link = re.search('<location>(.+)</location>', content).group(1)
    return opera.get(link).url
