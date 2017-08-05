# -*- coding: utf-8 -*-

"""
gdown.modules.realdebrid
~~~~~~~~~~~~~~~~~~~

This module contains handlers for realdebrid.

"""

import re
import time
from dateutil import parser
from datetime import datetime
# from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    r.headers['x-requested-with'] = 'XMLHttpRequest'
    params = {'user': username,
              'pass': passwd,
              'pin_challenge': '',
              'pin_answer': 'PIN: 000000',
              'time': int(time.time() * 1000)}
    rc = r.get('https://real-debrid.com/ajax/login.php', params=params)
    open('gdown.log', 'w').write(rc.text)
    rc = rc.json()
    if rc['message'] == 'Too many attempts':
        # {"error":3,"message":"Too many attempts","captcha":1,"captcha_type":"recaptcha","recaptcha_public_key":"6LeK8voSAAAAAEnlRaMgmux_r2hEMtNAdlUbuPbs","pin":0}
        raise ModuleError('captcha')
    elif rc['message'] == 'Your login informations are incorrect !':
        acc_info['status'] = 'deleted'
    elif rc['message'] == 'PIN Code required':
        print('pin')
        acc_info['status'] = 'deleted'
    else:
        raise ModuleError('unknown error')
    return acc_info
