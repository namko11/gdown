# -*- coding: utf-8 -*-

import re
from datetime import datetime
from dateutil import parser

from ..core import browser, acc_info
from ..exceptions import ModuleError


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    opera = browser()
    opera.post('http://www.filefactory.com/member/login.php', {'email': username, 'password': passwd})  # login to get ff_membership cookie
    #host = opera.get('http://www.filefactory.com/servers.php?single=1').content  # get best server to upload
    host = 'http://upload.filefactory.com/upload.php'  # always returning the same url (?)
    viewhash = re.search('<viewhash>(.+)</viewhash>', opera.get('http://www.filefactory.com/upload/upload_flash_begin.php?files=1').content).group(1)  # get viewhash
    opera.post('%s/upload_flash.php?viewhash=%s' % (host, viewhash), {'Filename': filename, 'Upload': 'Submit Query'}, files={'file': open(filename, 'rb')}).content  # upload
    return 'http://www.filefactory.com/file/%s/n/%s' % (viewhash, filename)


def accInfo(username, passwd):
    """Returns account info."""
    opera = browser()
    content = opera.post('http://www.filefactory.com/member/login.php', {'redirect': '/', 'email': username, 'password': passwd, 'socialID': '', 'socialType': 'facebook'}).content
    if '<p class="greenText">Free member</p>' in content:
        acc_info['status'] = 'free'
        return acc_info
    elif 'The account you are trying to use has been deleted.' in content:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'The email or password you have entered is incorrect' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif '<span class="greenText">Premium until <time datetime=' in content:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(re.search('<span class="greenText">Premium until <time datetime="([0-9]{4}\-[0-9]{2}\-[0-9]{2})">', content).group(1))
        return acc_info
    elif "Congratulations! You're a FileFactory Lifetime member. We value your loyalty and support." in content:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = datetime.max
        return acc_info
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
