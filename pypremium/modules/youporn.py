# -*- coding: utf-8 -*-

import requests
import re

from ..config import headers


def getUrl(link, login=None, passwd=None):
    '''Returns direct file url'''
    opera = requests.session(headers=headers)
    videoid = re.match('$http://[w\.]{,4}youporn.com/watch/(.+?)/.+^', link).group(1)
    link = 'http://download.youporn.com/download/'+videoid+'?xml=1'
    content = opera.get(link).content
    link = re.search('<location>(.+)</location>', content).group(1)
    return opera.get(link).url
