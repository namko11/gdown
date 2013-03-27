# -*- coding: utf-8 -*-
import requests
import re

from ..config import headers
from ..exceptions import AccountRemoved


def getApikey(username, passwd):
    opera = requests.session(headers=headers)
    content = re.search('<content type="text">(.+)</content>', opera.post('http://api.crocko.com/apikeys', {'login': username, 'password': passwd}).content).group(1)
    if content == 'Invalid login or password':
        return False
    else:
        return content


def status(username, passwd):
    """Returns account premium status."""
    # get apikey
    apikey = getApikey(username, passwd)
    if not apikey:
        raise AccountRemoved  # invalid username or password (?)
    opera = requests.session(headers=headers)
    content = opera.get('http://api.crocko.com/account', headers={'Authorization': apikey}).content
    premium_end = re.search('<ed:premium_end>(.*?)</ed:premium_end>', content).group(1)
    if not premium_end:
        return 0  # free
    else:
        return premium_end  # premium


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    # get apikey
    apikey = getApikey(username, passwd)
    opera = requests.session(headers=headers)
    content = opera.post('http://api.crocko.com/files', headers={'Authorization': apikey}, files={'file': open(filename, 'rb')}).content  # upload
    return re.search('<link title="download_link" href="(.+)"', content).group(1)
