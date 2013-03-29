# -*- coding: utf-8 -*-

import requests
import re
from datetime import datetime
from dateutil import parser

from ..config import headers
from ..exceptions import ModuleError, AccountBlocked, AccountRemoved


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    opera = requests.session(headers=headers)
    opera.post('http://www.filefactory.com/member/login.php', {'email': username, 'password': passwd})  # login to get ff_membership cookie
    #host = opera.get('http://www.filefactory.com/servers.php?single=1').content  # get best server to upload
    host = 'http://upload.filefactory.com/upload.php'  # always returning the same url (?)
    viewhash = re.search('<viewhash>(.+)</viewhash>', opera.get('http://www.filefactory.com/upload/upload_flash_begin.php?files=1').content).group(1)  # get viewhash
    opera.post('%s/upload_flash.php?viewhash=%s' % (host, viewhash), {'Filename': filename, 'Upload': 'Submit Query'}, files={'file': open(filename, 'rb')}).content  # upload
    return 'http://www.filefactory.com/file/%s/n/%s' % (viewhash, filename)


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = requests.session(headers=headers)
    content = opera.post('http://www.filefactory.com/member/login.php', {'redirect': '/', 'email': username, 'password': passwd, 'socialID': '', 'socialType': 'facebook'}).content
    if '<p class="greenText">Free member</p>' in content:
        return datetime.min
    elif 'The account you are trying to use has been deleted.' in content:
        raise AccountBlocked
    elif 'The email or password you have entered is incorrect' in content:
        raise AccountRemoved
    elif '<span class="greenText">Premium until <time datetime=' in content:
        return parser.parse(re.search('<span class="greenText">Premium until <time datetime="([0-9]{4}\-[0-9]{2}\-[0-9]{2})">', content).group(1))
    elif "Congratulations! You're a FileFactory Lifetime member. We value your loyalty and support." in content:
        return datetime.max
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')