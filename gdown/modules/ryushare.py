# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re

from ..config import headers
from ..exceptions import ModuleError, IpBlocked, AccountBlocked, AccountRemoved


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = requests.session(headers=headers)
    content = opera.post('http://ryushare.com', {'op': 'login', 'redirect': 'http://ryushare.com/my-account.python', 'login': username, 'password': passwd, 'loginFormSubmit': 'Login'}).content
    if 'Your account was banned by administrator.' in content:
        raise AccountBlocked
    elif 'Incorrect Login or Password' in content:
        raise AccountRemoved
    elif any(i in content for i in ('Your IP was blocked because too many logins fail.', 'Your IP was had too many fail login!!!')):
        raise IpBlocked
    elif 'Premium account expire:' in content:
        return time.mktime(datetime.datetime.strptime(re.search('Premium account expire:</TD><TD><b>(.+)</b>', content).group(1), '%d %B %Y').timetuple())
    elif '<a class="logout" href="http://ryushare.com/logout">&nbsp;Logout</a>' in content:
        return 0
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
