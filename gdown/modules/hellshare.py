# -*- coding: utf-8 -*-

import requests
import re
from datetime import datetime
from dateutil import parser

from ..config import headers
from ..exceptions import ModuleError, AccountRemoved


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = requests.session(headers=headers)
    opera.get('http://www.hellshare.com')
    opera.get('http://www.hellshare.com/?do=login-showLoginWindow')
    #   http://www.hellshare.com/members-auth/login
    values = {'login': 'Log in as registered user', 'username': username, 'password': passwd, 'perm_login': 'on'}
    content = opera.post('http://www.hellshare.com/?do=login-loginBoxForm-submit', values).content
    if 'Wrong user name or wrong password' in content:
        raise AccountRemoved
    content = opera.get('http://www.hellshare.com/members/').content
    if 'Active until: ' in content:
        expire_date = re.search('Active until: ([0-9]+\.[0-9]+\.[0-9]+)<br />', content).group(1)
        return parser.parse(expire_date)
    if 'Inactive' in content:
        return datetime.min
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
