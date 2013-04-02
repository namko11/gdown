# -*- coding: utf-8 -*-

import re
from datetime import datetime
from dateutil import parser

from ..core import browser
from ..exceptions import ModuleError, IpBlocked, AccountBlocked, AccountRemoved


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = browser()
    content = opera.post('http://ryushare.com', {'op': 'login', 'redirect': 'http://ryushare.com/my-account.python', 'login': username, 'password': passwd, 'loginFormSubmit': 'Login'}).content
    if 'Your account was banned by administrator.' in content:
        raise AccountBlocked
    elif 'Incorrect Login or Password' in content:
        raise AccountRemoved
    elif any(i in content for i in ('Your IP was blocked because too many logins fail.', 'Your IP was had too many fail login!!!')):
        raise IpBlocked
    elif 'Premium account expire:' in content:
        return parser.parse(re.search('Premium account expire:</TD><TD><b>(.+)</b>', content).group(1))
    elif '<a class="logout" href="http://ryushare.com/logout">&nbsp;Logout</a>' in content:
        return datetime.min
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
