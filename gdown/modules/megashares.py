# -*- coding: utf-8 -*-

import re

from ..module import browser


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is present (?).
    """
    fileid = re.match('http://d01.megashares.com/dl/(.+)/.+', link).group(1)
    link = 'http://d01.megashares.com/index.php?d01=%s' % (fileid)
    opera = browser()
    values = {'mymslogin_name': username, 'mymspassword': passwd, 'httpref': link, 'myms_login': 'Login'}
    content = opera.post('http://d01.megashares.com/myms_login.php', values).content
    link = re.search('show_download_button_1">\n    <a href="(.+)">', content).group(1)
    return opera.get(link).url
