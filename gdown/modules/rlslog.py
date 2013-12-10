# -*- coding: utf-8 -*-

"""
gdown.modules.rlslog
~~~~~~~~~~~~~~~~~~~

This module contains handlers for rlslog.

"""

import re
from time import sleep

from ..core import recaptcha, recaptchaReportWrong
from ..module import browser, random_word
from ..exceptions import ModuleError


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
    recaptcha_challenge, recaptcha_response = recaptcha(recaptcha_public_key)

    # post comment
    values = {'author': name, 'email': email, 'comment': body,
              'submit': 'Submit Comment', 'comment_post_ID': post_id,
              'recaptcha_challenge_field': recaptcha_challenge,
              'recaptcha_response_field': recaptcha_response}
    rc = r.post('http://www.rlslog.net/wp-comments-post.php', values).content
    if 'That reCAPTCHA response was incorrect.' in rc:
        recaptchaReportWrong()  # add captcha_id
        return comment(title, body, name, email)  # try again

    if 'You are posting comments too quickly.  Slow down.' in rc:
        print('sleeping')  # DEBUG
        sleep(360)  # less?
        return comment(title, body, name, email)
    elif 'Duplicate comment detected' in rc:
        return False
    elif 'error-page' in rc:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')


    return True
