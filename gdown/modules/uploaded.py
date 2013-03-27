# -*- coding: utf-8 -*-

import requests
import time
import re

from ..config import headers


def getUrl(link, username, passwd):  # not checked
    '''Returns direct file url'''
    opera = requests.session(headers=headers)
    values = {'id': username, 'pw': passwd, 'loginFormSubmit': 'Login'}
    opera.post('http://www.uploaded.net/io/login', values)
    return opera.get(link).url  # return connection


def status(username, passwd):
    '''Returns account premium status:
    -999    unknown error
    -2      invalid password
    -1      account temporary blocked
    0       free account
    >0      premium date end timestamp'''
    opera = requests.session(headers=headers, config={'max_retries': 2})
    values = {'id': username, 'pw': passwd}
    content = opera.post('http://uploaded.net/io/login', values).content
    if 'User and password do not match!' in content or 'Benutzer wurde gelöscht' in content or 'Account has been deleted' in content:  # wrong password / acc deleted
        return -2
    elif 'Account locked. Please contact Support.' in content:
        return -1
    content = opera.get('http://uploaded.net').content
    lang = re.search('<meta name="language" http-equiv="content-language" content="(.+)" />', content).group(1)
    if lang != 'en':
        content = opera.get('http://uploaded.net/language/en').content
        opera.get('http://uploaded.net/language/%s' % (lang))  # restore old language
    if re.search('<em>(.+)</em>', content).group(1) == 'Premium':
        if '<th>unlimited</th>          </tr>' in content:  # lifetime premium
            return 32503680000
        content = re.search('<th>([0-9]+.+)</th>[ 	]+</tr>', content).group(1)
        # 2 weeks 6 days and 4 hours
        # 4 weeks 0 days and 8 hours
        # 36 weeks 6 days and 5 hours
        # 12 Stunden 58 Minuten und 4 Sekunden
        # 1 Woche 0 Tage und 19 Stunden
        # 6 Wochen 2 Tage und 19 Stunden
        # 7 Wochen 6 Tage und 0 Stunden
        # 5 semaines 2 jours et 21 heures
        seconds = re.search('([0-9]+) second', content)
        minutes = re.search('([0-9]+) M|minute', content)
        hours = re.search('([0-9]+) hour', content)
        days = re.search('([0-9]+) day', content)
        weeks = re.search('([0-9]+) [wW]{1}eek', content)
        i = time.time()
        if seconds:
            i += int(seconds.group(1))
        if minutes:
            i += int(minutes.group(1)) * 60
        if hours:
            i += int(hours.group(1)) * 60 * 60
        if days:
            i += int(days.group(1)) * 60 * 60 * 24
        if weeks:
            i += int(weeks.group(1)) * 7 * 24 * 60 * 60
        return i
    else:
        return 0
