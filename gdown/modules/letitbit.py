# -*- coding: utf-8 -*-
# TODO: use api (http://api.letitbit.net/reg/static/api.pdf)

import requests
import re
from datetime import datetime
from dateutil import parser

from ..config import headers
from ..exceptions import ModuleError, AccountBlocked, AccountRemoved


def expireDate(username, passwd):
    """Returns account premium expire date."""
    r = requests.Session()
    r.headers = headers
    data = {'act': 'login', 'login': username, 'password': passwd}
    rc = r.post('http://letitbit.net/index.php?lang=en', data).content
    #Only for registered users
    if 'Account has been blocked. Please contact' in rc:
        raise AccountBlocked
    elif 'Authorization data is invalid!' in rc or 'Login is indicated in wrong format!' in rc:
        raise AccountRemoved

    data = {'act': 'get_attached_passwords'}
    rc = r.post('http://letitbit.net/ajax/get_attached_passwords.php', data).content
    if 'There are no attached premium accounts found' in rc:
        return datetime.min
    elif '<th>Premium account</th>' in rc:
        data = re.search('<td>([0-9]{4}\-[0-9]{2}\-[0-9]{2})</td>', rc).group(1)
        return parser.parse(data)
    open('gdown.log', 'w').write(rc)
    raise ModuleError('Unknown error, full log in gdown.log')


def getUrl(link, username, passwd):
    """Returns direct file url."""
    link = re.search('http://[w\.]{,4}letitbit.net/download/([0-9]+)/(.+)/(.+)\.html', link)  # own | uid | name
    r = requests.Session()
    r.headers = headers
    values = {'act': 'login', 'login': username, 'password': passwd}
    rc = r.post('http://letitbit.net/download.php?own=%s&uid=%s&name=%s&page=1' % (link.group(1), link.group(2), link.group(3)), values).content  # login && get download page
    link = re.search('src="(http://.*letitbit.net/sms/check2_iframe.php\?ac_syml_uid.+)"', rc).group(1)
    rc = r.get(link).content  # get download iframe
    link = re.findall('href="(.+)" style', rc)[0]  # get first link
    return r.get(link).url
