# -*- coding: utf-8 -*-

"""
gdown.modules.shareonline
~~~~~~~~~~~~~~~~~~~

This module contains handlers for shareonline.

"""

import re
import os

from ..module import browser


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
