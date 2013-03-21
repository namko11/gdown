# -*- coding: utf-8 -*-

import requests
import re
from ..config import headers


def getUrl(link, login, passwd):
    '''Returns direct file url'''
    link = re.search('http://[w\.]{,4}letitbit.net/download/([0-9]+)/(.+)/(.+)\.html', link)  # own | uid | name
    opera = requests.session(headers=headers)
    values = {'act': 'login', 'login': login, 'password': passwd}
    content = opera.post('http://letitbit.net/download.php?own=%s&uid=%s&name=%s&page=1' % (link.group(1), link.group(2), link.group(3)), values).content  # login && get download page
    link = re.search('src="(http://.*letitbit.net/sms/check2_iframe.php\?ac_syml_uid.+)"', content).group(1)
    content = opera.get(link).content  # get download iframe
    link = re.findall('href="(.+)" style', content)[0]  # get first link
    return opera.get(link).url
