# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from ..config import headers


def upload(username, passwd, filename):
    '''Returns uploaded file url'''
    opera = requests.session(headers=headers)
    opera.post('http://www.filefactory.com/member/login.php', {'email': username, 'password': passwd})  # login to get ff_membership cookie
    #host = opera.get('http://www.filefactory.com/servers.php?single=1').content  # get best server to upload
    host = 'http://upload.filefactory.com/upload.php'  # always returning the same url (?)
    viewhash = re.search('<viewhash>(.+)</viewhash>', opera.get('http://www.filefactory.com/upload/upload_flash_begin.php?files=1').content).group(1)  # get viewhash
    opera.post('%s/upload_flash.php?viewhash=%s' % (host, viewhash), {'Filename': filename, 'Upload': 'Submit Query'}, files={'file': open(filename, 'rb')}).content  # upload
    return 'http://www.filefactory.com/file/%s/n/%s' % (viewhash, filename)


def status(username, passwd):
    '''Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp'''
    opera = requests.session(headers=headers)
    content = opera.post('http://www.filefactory.com/member/login.php', {'redirect': '/', 'email': username, 'password': passwd, 'socialID': '', 'socialType': 'facebook'}).content
    if '<p class="greenText">Free member</p>' in content:
        return 0
    elif 'The account you are trying to use has been deleted.' in content:
        return -1
    elif 'The email or password you have entered is incorrect' in content:
        return -2
    elif '<span class="greenText">Premium until <time datetime=' in content:
        return time.mktime(datetime.datetime.strptime(re.search('<span class="greenText">Premium until <time datetime="([0-9]{4}\-[0-9]{2}\-[0-9]{2})">', content).group(1), '%Y-%m-%d').timetuple())
    elif "Congratulations! You're a FileFactory Lifetime member. We value your loyalty and support." in content:
        return 32503680000
    else:
        open('log.log', 'w').write(content)
        new_status
        return -999
