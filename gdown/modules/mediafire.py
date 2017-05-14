# -*- coding: utf-8 -*-

"""
gdown.modules.mediafire
~~~~~~~~~~~~~~~~~~~

This module contains handlers for mediafire.

"""

import re

from ..module import browser


def getUrl(link, premium_key, username=None, passwd=None):
    """Returns direct file url."""
    fileid = re.match('http://[w\.]{,4}mediafire.com/\?(.+)', link).group(1)
    r = browser()
    values = {'premium_key': premium_key, 'files': fileid}
    content = r.post('http://www.mediafire.com/basicapi/premiumapi.php', values).text
    link = re.search('<url>(.+)</url>', content).group(1)
    return r.get(link).url
