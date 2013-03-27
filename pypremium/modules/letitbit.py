# -*- coding: utf-8 -*-
# TODO: use api (http://api.letitbit.net/reg/static/api.pdf)

import requests
import re
import time
from dateutil import parser

from ..config import headers


def status(login, passwd):
    """Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp
    """
    r = requests.session(headers=headers)
    data = {'act': 'login', 'login': login, 'password': passwd}
    rc = r.post('http://letitbit.net/index.php?lang=en', data).content
    #Only for registered users
    if 'Authorization data is invalid!' in rc or 'Login is indicated in wrong format!' in rc:
        return -2
    elif 'Account has been blocked. Please contact' in rc:
        return -1

    data = {'act': 'get_attached_passwords'}
    rc = r.post('http://letitbit.net/ajax/get_attached_passwords.php', data).content
    if 'There are no attached premium accounts found' in rc:
        return 0
    elif '<th>Premium account</th>' in rc:
        data = re.search('<td>([0-9]{4}\-[0-9]{2}\-[0-9]{2})</td>', rc).group(1)
        return time.mktime(parser.parse(data).timetuple())
    open('log.log', 'w').write(rc)  # DEBUG
    new_status
    return -999


def getUrl(link, login, passwd):
    """Returns direct file url."""
    link = re.search('http://[w\.]{,4}letitbit.net/download/([0-9]+)/(.+)/(.+)\.html', link)  # own | uid | name
    r = requests.session(headers=headers)
    values = {'act': 'login', 'login': login, 'password': passwd}
    rc = r.post('http://letitbit.net/download.php?own=%s&uid=%s&name=%s&page=1' % (link.group(1), link.group(2), link.group(3)), values).content  # login && get download page
    link = re.search('src="(http://.*letitbit.net/sms/check2_iframe.php\?ac_syml_uid.+)"', rc).group(1)
    rc = r.get(link).content  # get download iframe
    link = re.findall('href="(.+)" style', rc)[0]  # get first link
    return r.get(link).url
