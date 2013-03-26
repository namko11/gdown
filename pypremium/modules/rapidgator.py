# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re

from ..config import headers


def status(login, passwd):
    '''Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp'''
    opera = requests.session(headers=headers, config={'max_retries': 2})
    content = opera.post('https://rapidgator.net/auth/login', {'LoginForm[email]': login, 'LoginForm[password]': passwd, 'LoginForm[rememberMe]': '1'}).content
    if 'Error e-mail or password.' in content:
        return -2
    elif 'The code from a picture does not coincide' in content:
        return -1
    elif 'Account:&nbsp;<a href="/article/premium">Free</a>' in content:
        return 0
    elif 'Premium till' in content:
        return time.mktime(datetime.datetime.strptime(re.search('Premium till ([0-9]{4}\-[0-9]{2}\-[0-9]{2})', content).group(1), '%Y-%m-%d').timetuple())
    else:
        open('log.log', 'w').write(content)
        #print content
        new_status
        return -999
