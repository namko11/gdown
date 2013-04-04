# -*- coding: utf-8 -*-
# TODO: use api (http://api.letitbit.net/reg/static/api.pdf)

import re
from dateutil import parser

from ..module import browser, acc_info
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    r = browser()
    data = {'act': 'login', 'login': username, 'password': passwd}
    rc = r.post('http://letitbit.net/index.php?lang=en', data).content
    #Only for registered users
    if 'Account has been blocked. Please contact' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Authorization data is invalid!' in rc or 'Login is indicated in wrong format!' in rc:
        acc_info['status'] = 'deleted'
        return acc_info

    data = {'act': 'get_attached_passwords'}
    rc = r.post('http://letitbit.net/ajax/get_attached_passwords.php', data).content
    if 'There are no attached premium accounts found' in rc:
        acc_info['status'] = 'free'
        return acc_info
    elif '<th>Premium account</th>' in rc:
        data = re.search('<td>([0-9]{4}\-[0-9]{2}\-[0-9]{2})</td>', rc).group(1)
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(data)
        return acc_info
    open('gdown.log', 'w').write(rc)
    raise ModuleError('Unknown error, full log in gdown.log')


def getUrl(link, username, passwd):
    """Returns direct file url."""
    link = re.search('http://[w\.]{,4}letitbit.net/download/([0-9]+)/(.+)/(.+)\.html', link)  # own | uid | name
    r = browser()
    values = {'act': 'login', 'login': username, 'password': passwd}
    rc = r.post('http://letitbit.net/download.php?own=%s&uid=%s&name=%s&page=1' % (link.group(1), link.group(2), link.group(3)), values).content  # login && get download page
    link = re.search('src="(http://.*letitbit.net/sms/check2_iframe.php\?ac_syml_uid.+)"', rc).group(1)
    rc = r.get(link).content  # get download iframe
    link = re.findall('href="(.+)" style', rc)[0]  # get first link
    return r.get(link).url
