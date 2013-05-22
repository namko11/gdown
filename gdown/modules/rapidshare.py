# -*- coding: utf-8 -*-

"""
gdown.modules.rapidshare
~~~~~~~~~~~~~~~~~~~

This module contains handlers for rapidshare.

"""

import re
from datetime import datetime

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is NOT present."""
    r = browser()
    content = re.match('^https?://[w\.]{,4}rapidshare.com/files/([0-9]+)/(.+)$', link)
    fileid = content.group(1)
    filename = content.group(2)
    content = r.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&try=1&login=%s&password=%s' % (fileid, filename, username, passwd)).content
    server = re.match('DL:(.+?),', content).group(1)
    return r.get('https://%s/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&try=0&login=%s&password=%s' % (server, fileid, filename, username, passwd)).url   # return connection


def accInfo(username, passwd):
    """Returns account info."""
    ''' List of errors:
    ERROR: Login failed. Password incorrect or account not found. (221a75e5)
    ERROR: Login failed. Account locked. Please contact us if you have questions. (b45c2518)
    ERROR: Login failed. Login data invalid. (0320f9f0)
    '''
    acc_info = acc_info_template()
    r = browser()
    content = r.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=getaccountdetails&login=%s&password=%s&withpublicid=1' % (username, passwd)).content
    if 'Login failed. Account locked.' in content:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Login failed. Password incorrect or account not found.' in content or 'Login failed. Login data invalid.' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'IP blocked' in content:   # ip blocked (too many wrong passwords)
        raise IpBlocked
    elif 'Login failed' in content:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
    elif 'billeduntil=' in content:
        # TODO: catch dates < now
        acc_info['expire_date'] = datetime.fromtimestamp(int(re.search('billeduntil=(.+)\n', content).group(1)))
        if acc_info['expire_date'] > datetime.utcnow():
            acc_info['status'] = 'premium'
        else:
            acc_info['status'] = 'free'
        return acc_info


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    r = browser()
    server_id = r.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=nextuploadserver').content
    content = r.post('https://rs%s.rapidshare.com/cgi-bin/rsapi.cgi?sub=upload' % (server_id), {'login': username, 'password': passwd}, files={'filecontent': open(filename, 'rb')}).content
    file_id = re.search('([0-9]+),[0-9]+,.+', content).group(1)
    return 'https://rapidshare.com/files/%s/%s' % (file_id, filename)
