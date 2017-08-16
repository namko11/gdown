# -*- coding: utf-8 -*-

"""
gdown.core
~~~~~~~~~~~~~~~~~~~

This module implements the gdown's basic methods.

"""
# import re
import sys
import time
# from random import random
from io import BytesIO

from .config import deathbycaptcha_username as decaptcha_username, deathbycaptcha_password as decaptcha_password, twocaptcha_api_key
# from .config import decaptchercom_username, decaptchercom_password
from .module import browser
if sys.version_info[0] == 2 or '__pypy__' in sys.builtin_module_names:
    from .deathbycaptcha2 import SocketClient as decaptcha
else:
    from .deathbycaptcha import SocketClient as decaptcha
# from .decaptchercom import client as decaptcha


def captcha(img):
    client = decaptcha(decaptcha_username, decaptcha_password)
    captcha = client.decode(BytesIO(img))
    if captcha:
        return captcha['text']
    else:
        return False


def recaptcha(site_key, url):
    """Generates recaptcha & resolves.
    Returns (recaptcha_challenge_field, recaptcha_response_field).
    """
    recaptcha_answer = 'CAPCHA_NOT_READY'
    r = browser()
    rc = r.post('http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}'.format(twocaptcha_api_key, site_key, url)).text
    print(rc)
    captcha_id = rc.split('|')[1]
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        time.sleep(5)
        recaptcha_answer = r.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(twocaptcha_api_key, captcha_id)).text
        # print(recaptcha_answer)
    recaptcha_answer = recaptcha_answer.split('|')[1]

    return recaptcha_answer


def recaptchaReportWrong():
    """Reports wrong captcha to deathbycaptcha to save credit."""
    # TODO: write me ;-)
    pass
