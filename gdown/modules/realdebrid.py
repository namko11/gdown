# -*- coding: utf-8 -*-

"""
gdown.modules.realdebrid
~~~~~~~~~~~~~~~~~~~

This module contains handlers for realdebrid.

"""

# import re
import time
# from dateutil import parser
# from datetime import datetime
# from bs4 import BeautifulSoup

from ..core import recaptcha
from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False, captcha_response=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    r.headers['x-requested-with'] = 'XMLHttpRequest'
    params = {'user': username,
              'pass': passwd,
              'pin_challenge': '',
              'pin_answer': 'PIN: 000000',
              'time': int(time.time() * 1000)}
    if captcha_response:
        params['captcha_response'] = captcha_response
    rc = r.get('https://real-debrid.com/ajax/login.php', params=params)
    open('gdown2.log', 'w').write(rc.text)
    rc = rc.json()
    if rc['message'] == 'Too many attempts':
        # {"error":3,"message":"Too many attempts","captcha":1,"captcha_type":"recaptcha","recaptcha_public_key":"6LeK8voSAAAAAEnlRaMgmux_r2hEMtNAdlUbuPbs","pin":0}
        # raise ModuleError('captcha')
        ans = recaptcha(rc['recaptcha_public_key'], 'https://real-debrid.com/ajax/login.php')
        return accInfo(username=username, passwd=passwd, proxy=proxy, captcha_response=ans)
    elif rc['message'] == 'Your login informations are incorrect !':
        acc_info['status'] = 'deleted'
    elif rc['message'] == 'PIN Code required':
        print('PIN')
        acc_info['status'] = 'deleted'
    elif rc['message'] == 'OK':
        del r.headers['x-requested-with']
        rc = r.get('https://real-debrid.com').text
        open('gdown2.log', 'w').write(rc)
        if 'Premium :<span class="fidelity">Free</span>' in rc:
            acc_info['status'] = 'free'
        else:
            raise ModuleError('unknown status')
    else:
        raise ModuleError('unknown error')
    return acc_info
