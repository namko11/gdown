# -*- coding: utf-8 -*-

"""
gdown.modules.crocko
~~~~~~~~~~~~~~~~~~~

This module contains handlers for crocko.

"""

import re
from datetime import datetime

from ..module import browser, acc_info_template


def getApikey(username, passwd):
    r = browser()
    content = re.search('<content type="text">(.+)</content>', r.post('http://api.crocko.com/apikeys', {'login': username, 'password': passwd}).content).group(1)
    if content == 'Invalid login or password':
        return False
    else:
        return content


def accInfo(username, passwd):
    """Returns account info."""
    # get apikey
    acc_info = acc_info_template()
    apikey = getApikey(username, passwd)
    if not apikey:
        acc_info['status'] = 'deleted'
        return acc_info  # invalid username or password (?)
    r = browser()
    content = r.get('http://api.crocko.com/account', headers={'Authorization': apikey}).content
    premium_end = re.search('<ed:premium_end>(.*?)</ed:premium_end>', content).group(1)
    if not premium_end:
        acc_info['status'] = 'free'
    else:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = datetime.fromtimestamp(premium_end)  # premium
    return acc_info


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    # get apikey
    apikey = getApikey(username, passwd)
    r = browser()
    content = r.post('http://api.crocko.com/files', headers={'Authorization': apikey}, files={'file': open(filename, 'rb')}).content  # upload
    return re.search('<link title="download_link" href="(.+)"', content).group(1)
