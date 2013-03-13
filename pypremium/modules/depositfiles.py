#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
#import datetime
import time
import re
from dateutil import parser

from ..config import *


def getUrl(link, login, passwd):
    """Returns direct file url
    IP validator is present
    """
    r = requests.session(headers=headers)
    values = {'login': login, 'password': passwd, 'go': '1', 'submit': 'enter'}
    r.post('http://depositfiles.com/en/login.php', values)  # login
    rc = r.get(link).content   # get download page
    link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', rc).group(1)
    return r.get(link).url


def status(login, passwd):
    """Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp
    """
    r = requests.session(headers=headers)
    manager_version = r.get('http://system.depositfiles.com/api/get_downloader_version.php').content
    manager_version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.8.1.20) DepositFiles/FileManager %s' % (manager_version)
    headers['User-Agent'] = manager_version

    r = requests.session(headers=headers)
    rc = r.post('http://dfiles.eu/en/login.php', {'go': 1, 'login': login, 'password': passwd}).content
    if '<div class="error_message">Your account has been blocked</div>' in rc:
        return -1
    elif '<div class="error_message">Your password or login is incorrect</div>' in rc:
        return -2
    elif 'Redirecting... If browser do not redirect you automaticaly' in rc:
        rc = r.get('http://dfiles.eu/gold/').content
        #rc = r.get('http://dfiles.eu/switch_lang.php?return_url=/gold&lang=en').content
        c = re.search('<div class="access">.+ <b>([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})</b></div>', rc)
        if c:
            return time.mktime(parser.parse(c.group(1)).timetuple())
        elif '<div class="access">' in rc:
            return 0
        open('log.log', 'w').write(content)
        print content
        new_status
        return -999

        '''
        if 'Your current status: FREE - member' in rc:
            return 0
        elif 'You have Gold access until' in rc:
            c = re.search('You have Gold access until: <b>([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})</b>', rc).group(1)
            return time.mktime(parser.parse(c).timetuple())
        else:
            open('log.log', 'w').write(rc)
        '''
    else:
        open('log.log', 'w').write(rc)
        print 'ip blocked'
        ip_blocked
        return -101
