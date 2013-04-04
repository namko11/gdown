# -*- coding: utf-8 -*-

import re
from time import sleep
from dateutil import parser

from ..module import browser, acc_info
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    opera = browser()
    content = opera.post('https://rapidgator.net/auth/login', {'LoginForm[email]': username, 'LoginForm[password]': passwd, 'LoginForm[rememberMe]': '1'}).content
    if 'The code from a picture does not coincide' in content:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Error e-mail or password.' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Account:&nbsp;<a href="/article/premium">Free</a>' in content:
        acc_info['status'] = 'free'
        return acc_info
    elif 'Premium till' in content:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(re.search('Premium till ([0-9]{4}\-[0-9]{2}\-[0-9]{2})', content).group(1))
        return acc_info
    elif '503 Service Temporarily Unavailable' in content:
        sleep(3)
        return accInfo(username, passwd)
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
