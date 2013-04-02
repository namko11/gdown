# -*- coding: utf-8 -*-

import re

from ..core import browser


def getUrl(link, premium_key, username=None, passwd=None):
    """Returns direct file url."""
    fileid = re.match('http://[w\.]{,4}mediafire.com/\?(.+)', link).group(1)
    opera = browser()
    values = {'premium_key': premium_key, 'files': fileid}
    content = opera.post('http://www.mediafire.com/basicapi/premiumapi.php', values).content
    link = re.search('<url>(.+)</url>', content).group(1)
    return opera.get(link).url
