# -*- coding: utf-8 -*-
import re
from datetime import datetime

from ..core import browser
from ..exceptions import AccountRemoved


def getApikey(username, passwd):
    opera = browser()
    content = re.search('<content type="text">(.+)</content>', opera.post('http://api.crocko.com/apikeys', {'login': username, 'password': passwd}).content).group(1)
    if content == 'Invalid login or password':
        return False
    else:
        return content


def expireDate(username, passwd):
    """Returns account premium expire date."""
    # get apikey
    apikey = getApikey(username, passwd)
    if not apikey:
        raise AccountRemoved  # invalid username or password (?)
    opera = browser()
    content = opera.get('http://api.crocko.com/account', headers={'Authorization': apikey}).content
    premium_end = re.search('<ed:premium_end>(.*?)</ed:premium_end>', content).group(1)
    if not premium_end:
        return datetime.min  # free
    else:
        return datetime.fromtimestamp(premium_end)  # premium


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    # get apikey
    apikey = getApikey(username, passwd)
    opera = browser()
    content = opera.post('http://api.crocko.com/files', headers={'Authorization': apikey}, files={'file': open(filename, 'rb')}).content  # upload
    return re.search('<link title="download_link" href="(.+)"', content).group(1)
