# -*- coding: utf-8 -*-

"""
gdown.modules.uploadstation
~~~~~~~~~~~~~~~~~~~

This module contains handlers for uploadstation.

"""

import re

from ..module import browser


def getUrl(link, username, passwd):
    """Returns direct file url."""
    r = browser()
    values = {'loginUserName': username, 'loginUserPassword': passwd, 'loginFormSubmit': 'Login', 'autoLogin': 'on'}
    r.post('http://www.uploadstation.com/login.php', values)
    return r.get(link).url  # return connection


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    r = browser()
    values = {'loginUserName': username, 'loginUserPassword': passwd, 'loginFormSubmit': 'Login', 'autoLogin': 'on'}
    r.post('http://uploadstation.com/login.php', values)
    content = r.get('http://uploadstation.com/upload.php').content
    host = re.search('action="(http://upload.uploadstation.com/upload/[0-9]+/[0-9]+/)"', content).group(1)
    content = r.get('%s?callback=jsonp' % (host)).content  # get sessionId
    sessionId = re.search("sessionId:'(.+)'", content).group(1)
    content = r.post('%s%s/' % (host, sessionId), files={'file': open(filename, 'rb')}).content
    open('log.log', 'w').write(content)
    return 0
