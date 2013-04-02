# -*- coding: utf-8 -*-

import requests
import re
from time import sleep
from datetime import datetime
from dateutil import parser

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
        return datetime.min
    elif 'Premium till' in content:
        return parser.parse(re.search('Premium till ([0-9]{4}\-[0-9]{2}\-[0-9]{2})', content).group(1))
    elif '503 Service Temporarily Unavailable' in content:
        sleep(3)
        return expireDate(username, passwd)
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
