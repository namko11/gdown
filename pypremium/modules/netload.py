# -*- coding: utf-8 -*-

import requests
import time
import re
from ..config import headers


def getUrl(link, login, passwd):
    '''Returns direct file url
    IP validator is present'''
    opera = requests.session(headers=headers)
    values = {'txtuser': login, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': ''}
    opera.post('http://netload.in/index.php', values)
    return opera.get(link).url  # return connection


def status(login, passwd):
    '''Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp'''
    opera = requests.session(headers=headers)
    values = {'txtuser': login, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': 'Login'}
    opera.post('http://netload.in/index.php', values)
    content = opera.get('http://netload.in/index.php?id=15').content
    if 'This account was locked' in content or'Sorry, please activate first your account.' in content:  # account not activated
        return -1
    elif 'not found in our records!' in content or 'Invalid User ID or password!' in content:
        return -2
    elif 'Please wait a moment before tryingto log in again!' in content:   # ip blocked
        print 'ip blocked'
        ip_blocked
        return -101
    content = opera.get('http://netload.in/index.php?id=2').content
    if 'No Bonus' in content or 'Kein Premium' in content:
        return 0
    else:
        content = re.search('<div style="float: left; width: 150px; color: #FFFFFF;"><span style="color: green">([0-9]*?)[ Tage,]{,7}([0-9]+) Stunden</span></div>', content)
        if content.group(1):
            content = time.time()+int(content.group(1))*24*60*60+int(content.group(2))*60*60
        else:
            content = time.time()+int(content.group(2))*60*60
        return content


def upload(login, passwd, filename):
    '''Returns uploaded file url'''
    opera = requests.session(headers=headers)
    host = opera.get('http://api.netload.in/getserver.php').content
    content = opera.post(host, {'user_id': login, 'user_password': passwd, 'modus': 'file_upload'}, files={'file': open(filename, 'rb')}).content
    return re.search('UPLOAD_OK;.+;[0-9]+;(.+);.+', content).group(1)
