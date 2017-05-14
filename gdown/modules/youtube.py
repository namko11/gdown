# -*- coding: utf-8 -*-

"""
gdown.modules.youtube
~~~~~~~~~~~~~~~~~~~

This module contains handlers for youtube.

"""

import re
try:
    from urllib import unquote
    from urlparse import parse_qs
except:
    from urllib.parse import unquote
    from urllib.parse import parse_qs

from ..module import browser


def getUrl(link, username=None, passwd=None):
    """Returns direct file url (best quality)."""
    r = browser()
    content = r.get(link).text
    content = unquote(re.search('url_encoded_fmt_stream_map=(.+?)&', content).group(1)).split()
    links = []
    for i in content:
        links.append(parse_qs(i))
    return r.get(links[0]['url'][0]).url
