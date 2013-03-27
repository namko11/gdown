# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re

from ..config import headers
from ..exceptions import ModuleError, AccountBlocked, AccountRemoved


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = requests.session(headers=headers, config={'max_retries': 2})
    content = opera.post('https://rapidgator.net/auth/login', {'LoginForm[email]': username, 'LoginForm[password]': passwd, 'LoginForm[rememberMe]': '1'}).content
    if 'The code from a picture does not coincide' in content:
        raise AccountBlocked
    elif 'Error e-mail or password.' in content:
        raise AccountRemoved
    elif 'Account:&nbsp;<a href="/article/premium">Free</a>' in content:
        return 0
    elif 'Premium till' in content:
        return time.mktime(datetime.datetime.strptime(re.search('Premium till ([0-9]{4}\-[0-9]{2}\-[0-9]{2})', content).group(1), '%Y-%m-%d').timetuple())
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
