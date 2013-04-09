# -*- coding: utf-8 -*-

"""
gdown.modules.extabit
~~~~~~~~~~~~~~~~~~~

This module contains handlers for extabit.

"""

from ..module import browser


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    #file_size = os.path.getsize(filename)  # get file size
    opera = browser()


    host = opera.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = opera.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    opera.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return opera.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': username, 'password': passwd}).content[:-1]  # start upload
