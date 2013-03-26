# -*- coding: utf-8 -*-

import requests
import os
from ..config import headers


def status(login, passwd):
    '''Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp'''
    opera = requests.session(headers=headers)
    content = opera.get('http://freakshare.com/login.html', {'user': login, 'pass': passwd, 'submit': 'Login'}).content
    if '<td><b>Member (premium)</b></td>' in content:
        return wazne
    elif '<td><b>Member (free)</b></td>' in content:
        return 0
    # NOT FINISHED!


def upload(login, passwd, filename):
    '''Returns uploaded file url'''
    file_size = os.path.getsize(filename)   # get file size
    opera = requests.session(headers=headers)
    # NOT FINISHED!

    host = opera.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = opera.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    opera.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return opera.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': login, 'password': passwd}).content[:-1]  # start upload
