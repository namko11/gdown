# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os

from ..config import headers
from ..exceptions import ModuleError, IpBlocked, AccountBlocked, AccountRemoved


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is present."""
    opera = requests.session(headers=headers)
    link = opera.get('http://api.hotfile.com/?action=getdirectdownloadlink&username=%s&password=%s&link=%s' % (username, passwd, link)).content
    return opera.get(link).url  # return connection


def status(username, passwd):
    """Returns account premium status."""
    opera = requests.session(headers=headers)
    content = opera.get('http://api.hotfile.com/?action=getuserinfo&username=%s&password=%s' % (username, passwd)).content
    if 'is_premium=1' in content:   # premium
        return time.mktime(datetime.datetime.strptime(re.search('premium_until=(.+?)&', content).group(1)[:-6], '%Y-%m-%dT%H:%M:%S').timetuple())
    elif 'is_premium=0' in content:  # free
        return 0
    elif 'user account is suspended' in content:  # account suspended (permanent?)
        raise AccountBlocked
    elif 'invalid username or password' in content:  # invalid username/passwd
        raise AccountRemoved
    elif 'too many failed attemtps' in content:  # ip blocked
        raise IpBlocked
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    file_size = os.path.getsize(filename)   # get file size
    opera = requests.session(headers=headers)
    host = opera.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = opera.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    opera.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return opera.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': username, 'password': passwd}).content[:-1]  # start upload
