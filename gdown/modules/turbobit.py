# -*- coding: utf-8 -*-

import re
from datetime import datetime
from dateutil import parser

from ..core import browser
from ..exceptions import ModuleError, AccountRemoved


def getUrl(link, username, passwd):
    """Returns direct file url."""
    opera = browser()
    values = {'user[login]': username, 'user[pass]': passwd, 'user[memory]': '1', 'user[submit]': 'Login'}
    opera.post('http://turbobit.net/user/login', values)
    content = opera.get(link).content
    link = re.search("<h1><a href='(.+)'>", content).group(1)
    return opera.get(link).url  # return connection


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    #file_size = os.path.getsize(filename)  # get file size
    opera = browser()
    values = {'user[login]': username, 'user[pass]': passwd, 'user[memory]': '1', 'user[submit]': 'Login'}
    opera.post('http://turbobit.net/user/login', values).content  # login
    content = opera.get('http://turbobit.net/').content
    content = re.search('urlSite=(http://s[0-9]+.turbobit.ru/uploadfile)&userId=(.+)&', content)
    host = content.group(1)
    user_id = content.group(2)
    content = opera.post(host, {'Filename': filename, 'user_id': user_id, 'stype': 'null', 'apptype': 'fd1', 'id': 'null', 'Upload': 'Submit Query'}, files={'Filedata': open(filename, 'rb')}).content  # upload
    file_id = re.search('{"result":true,"id":"(.+)","message":"Everything is ok"}', content).group(1)
    return 'http://turbobit.net/%s.html' % (file_id)


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = browser()
    values = {'user[login]': username, 'user[pass]': passwd, 'user[memory]': '1', 'user[submit]': 'Login'}
    content = opera.post('http://turbobit.net/user/login', values).content  # login
    if 'Incorrect login or password' in content or 'E-Mail address appears to be invalid. Please try again' in content:
        raise AccountRemoved
    elif 'Limit of login attempts exeeded.' in content:
        # TODO: use deathbycaptcha
        print 'captcha'
        captcha
        return -999
    try:
        content = re.search('<u>Turbo Access</u> [to ]{,3}(.*?)\.?					</div>', content).group(1)
    except:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
    if content == 'denied':
        return datetime.min
    else:
        return parser.parse(content)
