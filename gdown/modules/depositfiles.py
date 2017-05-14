# -*- coding: utf-8 -*-

"""
gdown.modules.depositfiles
~~~~~~~~~~~~~~~~~~~

This module contains handlers for depositfiles.

"""

import re
from dateutil import parser

from ..core import recaptcha, recaptchaReportWrong
from ..module import browser, acc_info_template
from ..exceptions import ModuleError


recaptcha_public_key = '6LdRTL8SAAAAAE9UOdWZ4d0Ky-aeA7XfSqyWDM2m'


def getUrl(link, username, passwd):
    """Returns direct file url
    IP validator is present
    """
    r = browser()
    values = {'login': username, 'password': passwd, 'go': '1', 'submit': 'enter'}
    r.post('http://depositfiles.com/en/login.php', values)  # login
    rc = r.get(link).text   # get download page
    link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', rc).group(1)
    return r.get(link).url


def accInfo(username, passwd, captcha=False, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    if captcha:
        recaptcha_challenge, recaptcha_response = recaptcha(recaptcha_public_key)
    else:
        recaptcha_challenge = ''
        recaptcha_response = ''

    data = {'login': username, 'password': passwd,
            'recaptcha_challenge_field': recaptcha_challenge,
            'recaptcha_response_field': recaptcha_response}
    rc = r.post('http://dfiles.eu/api/user/login', data).json()

    # TODO: too many returns in one method
    if rc['status'] == 'OK':
        if rc['data']['mode'] == 'free':
            acc_info['status'] = 'free'
            return acc_info
        elif rc['data']['mode'] == 'gold':
            rc = r.get('http://dfiles.eu/gold/').text
            c = re.search('<div class="access">.+ <b>([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})</b></div>', rc)
            acc_info['status'] = 'premium'
            acc_info['expire_date'] = parser.parse(c.group(1))
            return acc_info
    elif rc['status'] == 'Error':
        if rc['error'] == 'CaptchaRequired':
            return accInfo(username, passwd, captcha=True, proxy=proxy)
        elif rc['error'] == 'CaptchaInvalid':
            recaptchaReportWrong()  # add captcha_id
            return accInfo(username, passwd, captcha=True, proxy=proxy)
        elif rc['error'] == 'LoginInvalid':
            acc_info['status'] = 'deleted'
            return acc_info
    open('gdown.log', 'w').write(rc)
    raise ModuleError('Unknown error, full log in gdown.log')
