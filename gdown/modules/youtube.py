# -*- coding: utf-8 -*-

import requests
import re
from urllib import unquote
from urlparse import parse_qs

from ..config import headers


def getUrl(link, username=None, passwd=None):
    """Returns direct file url."""
    opera = requests.session(headers=headers)
    content = opera.get(link).content
    content = unquote(re.search('url_encoded_fmt_stream_map=(.+?)&', content).group(1)).split()
    links = []
    for i in content:
        links.append(parse_qs(i))
    return opera.get(links[0]['url'][0]).url