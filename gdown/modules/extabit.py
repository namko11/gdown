# -*- coding: utf-8 -*-

"""
gdown.modules.extabit
~~~~~~~~~~~~~~~~~~~

This module contains handlers for extabit.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'email': username, 'pass': passwd, 'remember': '1', 'auth_submit_login.x': '38', 'auth_submit_login.y': '26', 'auth_submit_login': 'Enter'}
    rc = r.post('http://extabit.com/login.jsp', data).content

    alert = re.search('\$.jGrowl\("(.+)", \{life: [0-9]+\} \);', rc)
    if alert:
        if any(i in alert.group(1) for i in ('Account not activated.', 'Your account has been suspended for violating terms of service')):
            acc_info['status'] = 'blocked'
            return acc_info
        elif 'Username or password is incorrect.' in alert.group(1):
            acc_info['status'] = 'deleted'
            return acc_info
        elif 'Too many tries, try again in 30 minutes' in alert.group(1):
            raise IpBlocked
        else:
            open('gdown.log', 'w').write(rc)
            raise ModuleError('Unknown alert, full log in gdown.log')

    status = re.search('Premium is active till ([0-9]{2}\.[0-9]{2}\.[0-9]{4})  </span>', rc)
    status2 = re.search('You have <strong>([0-9]+)</strong> downloads </span>', rc)
    if status:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(status.group(1), dayfirst=True)
    elif status2:
        acc_info['status'] = 'premium'
        acc_info['points'] = status2.group(1)
    else:  # TODO: change this to elif and catch unknown error
        acc_info['status'] = 'free'

    return acc_info


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    #file_size = os.path.getsize(filename)  # get file size
    r = browser()

    host = r.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = r.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    r.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return r.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': username, 'password': passwd}).content[:-1]  # start upload
