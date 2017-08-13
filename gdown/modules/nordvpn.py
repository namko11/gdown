# -*- coding: utf-8 -*-

"""
gdown.modules.nordvpn
~~~~~~~~~~~~~~~~~~~

This module contains handlers for nordvpn.

"""

# import re
# import time
import json
import hashlib
# from dateutil import parser
from datetime import datetime, timedelta
# from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    r.headers['User-Agent'] = 'NordVPN_Client_5.56.780.0'
    rc = r.get('https://api.nordvpn.com/token/token/%s' % username).json()
    user_hash = hashlib.sha512(rc['salt'].encode() + passwd.encode()).hexdigest()
    user_hash = hashlib.sha512(user_hash.encode() + rc['key'].encode()).hexdigest()
    rc2 = r.get('https://api.nordvpn.com/token/verify/%s/%s' % (rc['token'], user_hash)).json()
    # print(rc2)  # DEBUG
    if rc2 is True:
        r.headers['nToken'] = rc['token']
        rc = r.get('https://api.nordvpn.com/user/databytoken').json()
        # print(rc)  # DEBUG
        acc_info['transfer'] = '%s/%s' % (rc['devices']['current'], rc['devices']['max'])
        if rc['expires'] > 0:
            acc_info['status'] = 'premium'
            acc_info['expire_date'] = datetime.utcnow() + timedelta(seconds=rc['expires'])
        else:
            acc_info['status'] = 'free'
    elif rc2['status'] == 401:
        acc_info['status'] = 'deleted'
    else:
        open('gdown.log', 'w').write(json.dumps(rc2))
        raise ModuleError('Unknown status')
    return acc_info
