# -*- coding: utf-8 -*-

"""
gdown.core
~~~~~~~~~~~~~~~~~~~

This module implements the gdown's basic methods.

"""
import re
import sys
from random import random
from io import BytesIO

from .config import deathbycaptcha_username as decaptcha_username, deathbycaptcha_password as decaptcha_password
# from .config import decaptchercom_username, decaptchercom_password
from .module import browser
if sys.version_info[0] == 2 or '__pypy__' in sys.builtin_module_names:
    from .decaptchercom2 import SocketClient as decaptcha
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


def recaptcha(recaptcha_public_key):
    """Generates recaptcha & resolves.
    Returns (recaptcha_challenge_field, recaptcha_response_field).
    """
    r = browser()
    rc = r.get('http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cachestop=%s' % (recaptcha_public_key, random())).text
    recaptcha_challenge = re.search("challenge : '(.+)',", rc).group(1)
    captcha_img = r.get('http://www.google.com/recaptcha/api/image?c=%s' % (recaptcha_challenge)).content

    return recaptcha_challenge, captcha(captcha_img)


def recaptchaReportWrong():
    """Reports wrong captcha to deathbycaptcha to save credit."""
    # TODO: write me ;-)
    pass
