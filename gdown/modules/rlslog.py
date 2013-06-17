# -*- coding: utf-8 -*-

"""
gdown.modules.rlslog
~~~~~~~~~~~~~~~~~~~

This module contains handlers for rlslog.

"""

import re

from ..core import decaptcha, decaptchaReportWrong
from ..module import browser, random_word


recaptcha_public_key = '6LfEHroSAAAAAHMm1oJ-Wk-Wmk1n8nutKcpM_mJ6'


def comment(title, body, name=random_word(), email=None):
    """Posts comment."""
    if not email:
        email = name+'@gmail.com'
    title = title.replace(' ', '-')
    title = title.replace(':', '')
    url = 'http://www.rlslog.net/{}/'.format(title)
    r = browser()
    rc = r.get(url).content
    post_id = re.search('name="comment_post_ID" value="([0-9]+)"', rc).group(1)
    #recaptcha_public_key = re.search('http://api.recaptcha.net/challenge?k=(.+)"', rc).group(1)
    recaptcha_challenge, recaptcha_response = decaptcha(recaptcha_public_key)

    # post comment
    values = {'author': name, 'email': email, 'comment': body,
              'submit': 'Submit Comment', 'comment_post_ID': post_id,
              'recaptcha_challenge_field': recaptcha_challenge,
              'recaptcha_response_field': recaptcha_response}
    rc = r.post('http://www.rlslog.net/wp-comments-post.php', values).content
    if 'That reCAPTCHA response was incorrect.' in rc:
        decaptchaReportWrong()  # add captcha_id
        return comment(title, name, email, body)  # try again

    return True
