# -*- coding: utf-8 -*-

"""
gdown.modules.kat
~~~~~~~~~~~~~~~~~~~

This module contains handlers for kat.

"""

import re
from simplejson import JSONDecoder

from ..module import browser, acc_info_template
#from ..exceptions import ModuleError, IpBlocked


def __login__(username, passwd):
    """Returns requests object after logging in."""
    r = browser()
    data = {'return_uri': 'https://kat.ph/', 'email': username, 'password': passwd}
    rc = r.post('https://kat.ph/auth/socialize/', data).content
    open('log.log', 'w').write(rc)
    # TODO: validate login
    return r


def rateGood(username, passwd, torrent_hash):
    """Vote good."""
    r = __login__(username, passwd)
    rc = JSONDecoder().decode(r.post('https://kat.ph/torrents/submitthnx/{}/'.format(torrent_hash)).content)
    if rc['method'] == 'ok':
        return True
    else:
        open('log.log', 'w').write(rc)
        return False


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = __login__(username, passwd)
    rc = r.get('https://kat.ph/').content
    username = re.search('<a href="/user/(.+)/">profile</a>', rc).group(1)
    rc = r.get('https://kat.ph/user/{}'.format(username)).content
    rating = re.search('<span title="Reputation" class="repValue positive">([0-9]+)</span>', rc).group(1)
    acc_info['points'] = rating
    acc_info['status'] = 'free'
    print username, rating
    return acc_info
