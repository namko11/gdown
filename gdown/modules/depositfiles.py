# -*- coding: utf-8 -*-

import re
from random import random
from StringIO import StringIO
from simplejson import JSONDecoder
from dateutil import parser

from ..module import browser, acc_info
from ..config import deathbycaptcha_username, deathbycaptcha_password
from ..exceptions import ModuleError
from ..deathbycaptcha import SocketClient as deathbycaptcha


recaptcha_public_key = '6LdRTL8SAAAAAE9UOdWZ4d0Ky-aeA7XfSqyWDM2m'


def decaptcha(public_key):
    """Generates captcha & resolves using deathbycaptcha.
    Returns (recaptcha_challenge_field, recaptcha_response_field)."""
    r = browser()
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
    r = browser()
    values = {'login': username, 'password': passwd, 'go': '1', 'submit': 'enter'}
    r.post('http://depositfiles.com/en/login.php', values)  # login
    rc = r.get(link).content   # get download page
    link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', rc).group(1)
    return r.get(link).url


def accInfo(username, passwd, captcha=False):
    """Returns account info."""
    r = browser()
    if captcha:
        recaptcha_challenge, recaptcha_response = decaptcha(recaptcha_public_key)
    else:
        recaptcha_challenge = ''
        recaptcha_response = ''

    data = {'login': username, 'password': passwd,
            'recaptcha_challenge_field': recaptcha_challenge,
            'recaptcha_response_field': recaptcha_response}
    rc = JSONDecoder().decode(r.post('http://dfiles.eu/api/user/login', data).content)

    # TODO: too many returns in one method
    if rc['status'] == 'OK':
        if rc['data']['mode'] == 'free':
            acc_info['status'] = 'free'
            return acc_info
        elif rc['data']['mode'] == 'gold':
            rc = r.get('http://dfiles.eu/gold/').content
            c = re.search('<div class="access">.+ <b>([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})</b></div>', rc)
            acc_info['status'] = 'premium'
            acc_info['expire_date'] = parser.parse(c.group(1))
            return acc_info
    elif rc['status'] == 'Error':
        if rc['error'] == 'CaptchaRequired':
            return accInfo(username, passwd, captcha=True)
        elif rc['error'] == 'CaptchaInvalid':
            decaptcha_wrong()  # add captcha_id
            return accInfo(username, passwd, captcha=True)
        elif rc['error'] == 'LoginInvalid':
            acc_info['status'] = 'deleted'
            return acc_info
    open('gdown.log', 'w').write(rc)
    raise ModuleError('Unknown error, full log in gdown.log')
