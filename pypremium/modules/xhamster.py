# -*- coding: utf-8 -*-

import requests
import re

from ..config import headers


def getUrl(link, login=None, passwd=None):
    '''Returns direct file url'''
    opera = requests.session(headers=headers)
    content = opera.get(link).content
    srv = re.search("'srv': '(.+)',", content).group(1)
    link = srv+'/flv2/'+re.search("'file': '(.+)',", content).group(1)
    return opera.get(link).url
