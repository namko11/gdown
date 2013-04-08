# -*- coding: utf-8 -*-

import re
from dateutil import parser

from ..core import decaptcha, decaptchaReportWrong
from ..module import browser, acc_info_template
from ..exceptions import ModuleError

recaptcha_public_key = '6LcTGLoSAAAAAHCWY9TTIrQfjUlxu6kZlTYP50_c'


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


def accInfo(username, passwd, captcha=False):
    """Returns account info."""
    # TODO: catch wrong captcha exception
    acc_info = acc_info_template()
    opera = browser()
    values = {'user[login]': username, 'user[pass]': passwd, 'user[memory]': '1', 'user[submit]': 'Login'}
    if captcha:
        recaptcha_challenge, recaptcha_response = decaptcha(recaptcha_public_key)
        values['recaptcha_challenge_field'] = recaptcha_challenge
        values['recaptcha_response_field'] = recaptcha_response
        values['user[captcha_type]'] = 'recaptcha'
        values['user[captcha_subtype]'] = ''
    content = opera.post('http://turbobit.net/user/login', values).content  # login
    if 'Incorrect login or password' in content or 'E-Mail address appears to be invalid. Please try again' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Limit of login attempts exceeded for your account. It has been temporarily locked.' in content:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Limit of login attempts exeeded.' in content or 'Please enter the captcha.' in content:
        return accInfo(username, passwd, captcha=True)
    try:
        content = re.search('<u>Turbo Access</u> [to ]{,3}(.*?)\.?					</div>', content).group(1)
    except:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
    if content == 'denied':
        acc_info['status'] = 'free'
        return acc_info
    else:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(content)
        return acc_info
