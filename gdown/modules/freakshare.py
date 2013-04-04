# -*- coding: utf-8 -*-

import os

from ..module import browser, acc_info_template


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    opera = browser()
    content = opera.get('http://freakshare.com/login.html', {'user': username, 'pass': passwd, 'submit': 'Login'}).content
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
    opera = browser()
    # NOT FINISHED!

    host = opera.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = opera.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    opera.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return opera.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': username, 'password': passwd}).content[:-1]  # start upload
