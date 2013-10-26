# -*- coding: utf-8 -*-

"""
gdown.modules.kickass
~~~~~~~~~~~~~~~~~~~

This module contains handlers for kickass.

"""

import re
from simplejson import JSONDecoder

from ..core import decaptcha
from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def __login__(username, passwd):
    """Returns requests object after logging in."""
    r = browser()
    data = {'return_uri': 'http://kickass.to/', 'email': username, 'password': passwd}
    rc = r.post('http://kickass.to/auth/socialize/', data).content
    if any(i in rc for i in ('<title>Registration - KickassTorrents</title>', "You can't access your account because you were deleted", 'DELETED USER')):
        return False
    open('gdown.log', 'w').write(rc)
    # TODO: validate login
    return r


def rateGood(username, passwd, torrent_hash):
    """Vote good."""
    r = __login__(username, passwd)
    if r is False:
        return False
    rc = r.post('https://kickass.to/torrents/vote/like/%s/' % torrent_hash, data={'ajax': 1}).json()
    if rc['method'] == 'ok':
        return True
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = __login__(username, passwd)
    if r is False:
        acc_info['status'] = 'deleted'
    else:
        rc = r.get('http://kickass.to/').content
        username = re.search('<a href="/user/(.+)/">profile</a>', rc).group(1)
        rc = r.get('http://kickass.to/user/{}'.format(username)).content
        open('gdown.log', 'w').write(rc)
        rating = re.search('<span title="Reputation" class="repValue [positvenga]{8}">([0-9]+)</span>', rc).group(1)
        acc_info['points'] = rating
        acc_info['status'] = 'free'
    return acc_info


def signUp(email, passwd, username=None):
    """Creates new account."""
    if username is None:
        username = email.split('@')[0]
    r = browser()

    # TODO: /auth/check/{username}  | {"method":"ok","html":"fail"} | {"method":"ok","html":"ok"}

    # get recaptcha_public_key
    #rc = r.get('http://kickass.to/auth/register').content
    #recaptcha_public_key = re.search('Recaptcha\.create\("(.+?)"', rc).group(1)
    recaptcha_public_key = '6LfHpd8SAAAAAAIkr00VqbRkWColMiVepdfsHQZ0'  # always the same

    recaptcha_challenge, recaptcha_response = decaptcha(recaptcha_public_key)

    data = {'return_uri': 'http://kickass.to/user/{}'.format(username),
            'email': email, 'nickname': username, 'password': passwd,
            'recaptcha_challenge_field': recaptcha_challenge,
            'recaptcha_response_field': recaptcha_response,
            'tos': '1',
            'turing': 'iamhuman'}
    rc = r.post('http://kickass.to/auth/socialize/', data).content
    open('gdown.log', 'w').write(rc)
    return True
