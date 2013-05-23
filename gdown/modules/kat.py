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
    if '<title>Registration - KickassTorrents</title>' in rc or "You can't access your account because you were deleted" in rc:
        return False
    open('log.log', 'w').write(rc)
    # TODO: validate login
    return r


def rateGood(username, passwd, torrent_hash):
    """Vote good."""
    r = __login__(username, passwd)
    if r is False:
        return False
    rc = JSONDecoder().decode(r.post('https://kat.ph/torrents/submitthnx/{}/'.format(torrent_hash)).content)
    print rc
    if rc['method'] == 'ok':
        return True
    else:
        open('log.log', 'w').write(rc)
        return False


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = __login__(username, passwd)
    if r is False:
        acc_info['status'] = 'deleted'
    else:
        rc = r.get('https://kat.ph/').content
        username = re.search('<a href="/user/(.+)/">profile</a>', rc).group(1)
        rc = r.get('https://kat.ph/user/{}'.format(username)).content
        open('log.log', 'w').write(rc)
        rating = re.search('<span title="Reputation" class="repValue [positvenga]{8}">([0-9]+)</span>', rc).group(1)
        acc_info['points'] = rating
        acc_info['status'] = 'free'
    return acc_info
