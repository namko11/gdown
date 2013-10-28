# -*- coding: utf-8 -*-

"""
gdown.core
~~~~~~~~~~~~~~~~~~~

This module implements the gdown's basic methods.

"""
import re
from random import random
from io import BytesIO

#from .config import deathbycaptcha_username, deathbycaptcha_password
from .config import decaptchercom_username, decaptchercom_password
from .module import browser
#from .deathbycaptcha import SocketClient as decaptcha
from .decaptchercom import client as decaptcha


def recaptcha(recaptcha_public_key):
    """Generates recaptcha & resolves.
    Returns (recaptcha_challenge_field, recaptcha_response_field).
    """
    r = browser()
    rc = r.get('http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cachestop=%s' % (recaptcha_public_key, random())).text
    recaptcha_challenge = re.search("challenge : '(.+)',", rc).group(1)
    captcha_img = BytesIO(r.get('http://www.google.com/recaptcha/api/image?c=%s' % (recaptcha_challenge)).content)

    client = decaptcha(decaptchercom_username, decaptchercom_password)  # TODO: choose good acc info
    captcha = client.decode(captcha_img)
    if captcha:
        return recaptcha_challenge, captcha['text']
    else:
        return False


def recaptchaReportWrong():
    """Reports wrong captcha to deathbycaptcha to save credit."""
    # TODO: write me ;-)
    pass
