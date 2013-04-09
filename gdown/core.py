# -*- coding: utf-8 -*-

"""
gdown.core
~~~~~~~~~~~~~~~~~~~

This module implements the gdown's basic methods.

"""
import re
from random import random
from StringIO import StringIO

from .config import deathbycaptcha_username, deathbycaptcha_password
from .module import browser
from .deathbycaptcha import SocketClient as deathbycaptcha


def decaptcha(recaptcha_public_key):
    """Generates recaptcha & resolves using deathbycaptcha.
    Returns (recaptcha_challenge_field, recaptcha_response_field).
    """
    r = browser()
    rc = r.get('http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cachestop=%s' % (recaptcha_public_key, random())).content
    recaptcha_challenge = re.search("challenge : '(.+)',", rc).group(1)
    captcha_img = StringIO(r.get('http://www.google.com/recaptcha/api/image?c=%s' % (recaptcha_challenge)).content)

    client = deathbycaptcha(deathbycaptcha_username, deathbycaptcha_password)
    captcha = client.decode(captcha_img)
    if captcha:
        return recaptcha_challenge, captcha['text']
    else:
        return False


def decaptchaReportWrong():
    """Reports wrong captcha to deathbycaptcha to save credit."""
    # TODO: write me ;-)
    pass
