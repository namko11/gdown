# -*- coding: utf-8 -*-

"""
gdown.modules.shareonline
~~~~~~~~~~~~~~~~~~~

This module contains handlers for shareonline.

"""

import re
import os
from dateutil import parser

from ..module import browser, acc_info_template


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    file_size = int(os.path.getsize(filename))
    r = browser()
    content = re.match('(.+);(.+)', r.post('http://www.share-online.biz/upv3_session.php', {'username': username, 'password': passwd}).text)  # get upload_session and best server to upload
    upload_session = content.group(1)
    host = content.group(2)
    data = {'username': username, 'password': passwd, 'upload_session': upload_session, 'chunk_no': 1, 'chunk_number': 1, 'filesize': file_size, 'finalize': 1}
    content = r.post('http://%s' % (host), data, files={'fn': open(filename, 'rb')}).text  # upload
    return re.match('(.+);[0-9]+;.+', content).group(1)


def accInfo(username, passwd, proxy=False):
    r = browser(proxy)
    acc_info = acc_info_template()
    r.get('https://www.share-online.biz/lang/set/english')
    data = {'user': username,
            'pass': passwd}
    rc = r.post('https://www.share-online.biz/user/login', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'This account is disabled, please contact support' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Sammler        </p>' in rc:
        acc_info['status'] = 'free'
        return acc_info
    elif 'Premium        </p>' in rc or 'VIP-Special        </p>' in rc:
        acc_info['status'] = 'premium'
        expire_date = re.search("<span class='green'>([0-9\., :]+?)</span>", rc).group(1)  # this probably won't be "green" allways
        acc_info['expire_date'] = parser.parse(expire_date, dayfirst=True)
        return acc_info
    elif '* Login data invalid *' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    else:
        asddsadsa
