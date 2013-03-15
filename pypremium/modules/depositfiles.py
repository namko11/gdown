#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
#import datetime
import time
import re
from random import random
from StringIO import StringIO
from simplejson import JSONDecoder
from dateutil import parser

from ..config import headers, deathbycaptcha_username, deathbycaptcha_password
from ..deathbycaptcha import SocketClient as deathbycaptcha


recaptcha_public_key = '6LdRTL8SAAAAAE9UOdWZ4d0Ky-aeA7XfSqyWDM2m'


def decaptcha(public_key):
    """Generates captcha & resolves using deathbycaptcha.
    Returns (recaptcha_challenge_field, recaptcha_response_field)."""
    r = requests.session(headers=headers)
    rc = r.get('http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cachestop=%s' % (recaptcha_public_key, random())).content
    recaptcha_challenge = re.search("challenge : '(.+)',", rc).group(1)
    captcha_img = StringIO(r.get('http://www.google.com/recaptcha/api/image?c=%s' % (recaptcha_challenge)).content)

    client = deathbycaptcha(deathbycaptcha_username, deathbycaptcha_password)
    captcha = client.decode(captcha_img)
    if captcha:
        return recaptcha_challenge, captcha['text']
    else:
        print 'decaptcha failed (?)'
        return False


def decaptcha_wrong():
    """Reports wrong captcha resolve to save credit."""
    pass


def getUrl(link, username, passwd):
    """Returns direct file url
    IP validator is present
    """
    r = requests.session(headers=headers)
    values = {'login': username, 'password': passwd, 'go': '1', 'submit': 'enter'}
    r.post('http://depositfiles.com/en/login.php', values)  # login
    rc = r.get(link).content   # get download page
    link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', rc).group(1)
    return r.get(link).url


def status(username, passwd, captcha=False):
    """Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp
    """
    r = requests.session(headers=headers)
    if captcha:
        recaptcha_challenge, recaptcha_response = decaptcha(recaptcha_public_key)
    else:
        recaptcha_challenge = ''
        recaptcha_response = ''

    data = {'login': username, 'password': passwd,
            'recaptcha_challenge_field': recaptcha_challenge,
            'recaptcha_response_field': recaptcha_response}
    rc = JSONDecoder().decode(r.post('http://dfiles.eu/api/user/login', data).content)

    if rc['status'] == 'OK':
        if rc['data']['mode'] == 'free':
            return 0
        elif rc['data']['mode'] == 'gold':
            rc = r.get('http://dfiles.eu/gold/').content
            c = re.search('<div class="access">.+ <b>([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})</b></div>', rc)
            return time.mktime(parser.parse(c.group(1)).timetuple())
    elif rc['status'] == 'Error':
        if rc['error'] == 'CaptchaRequired':
            return status(username, passwd, captcha=True)
        elif rc['error'] == 'LoginInvalid':
            return -2
    open('log.log').write(rc)
    new_status
    return -999
