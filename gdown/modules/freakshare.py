# -*- coding: utf-8 -*-

"""
gdown.modules.freakshare
~~~~~~~~~~~~~~~~~~~

This module contains handlers for freakshare.

"""

import os

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    content = r.get('http://freakshare.com/login.html', {'user': username, 'pass': passwd, 'submit': 'Login'}).content
    if '<td><b>Member (premium)</b></td>' in content:
        acc_info['status'] = 'premium'
        return acc_info  # TODO: Finish it!
    elif '<td><b>Member (free)</b></td>' in content:
        acc_info['status'] = 'free'
        return acc_info
    # NOT FINISHED!


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    file_size = os.path.getsize(filename)   # get file size
    r = browser()
    # NOT FINISHED!

    host = r.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = r.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    r.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return r.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': username, 'password': passwd}).content[:-1]  # start upload
