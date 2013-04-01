# -*- coding: utf-8 -*-

import requests
import re
from datetime import datetime, timedelta

from ..config import headers
from ..exceptions import AccountBlocked, AccountRemoved


def getUrl(link, username, passwd):  # not checked
    """Returns direct file url."""
    opera = requests.Session()
    opera.headers = headers
    values = {'id': username, 'pw': passwd, 'loginFormSubmit': 'Login'}
    opera.post('http://www.uploaded.net/io/login', values)
    return opera.get(link).url  # return connection


def expireDate(username, passwd):
    """Returns account premium expire date."""
    opera = requests.Session()
    opera.headers = headers
    values = {'id': username, 'pw': passwd}
    content = opera.post('http://uploaded.net/io/login', values).content
    if 'Account locked. Please contact Support.' in content:
        raise AccountBlocked
    elif 'User and password do not match!' in content or 'Benutzer wurde gelöscht' in content or 'Account has been deleted' in content:  # wrong password / acc deleted
        raise AccountRemoved
    content = opera.get('http://uploaded.net').content
    lang = re.search('<meta name="language" http-equiv="content-language" content="(.+)" />', content).group(1)
    if lang != 'en':
        content = opera.get('http://uploaded.net/language/en').content
        opera.get('http://uploaded.net/language/%s' % (lang))  # restore old language
    if re.search('<em>(.+)</em>', content).group(1) == 'Premium':
        if '<th>unlimited</th>          </tr>' in content:  # lifetime premium
            return datetime.max
        content = re.search('<th>([0-9]+.+)</th>[ 	]+</tr>', content).group(1)
        seconds = re.search('([0-9]+) second', content)
        minutes = re.search('([0-9]+) M|minute', content)
        hours = re.search('([0-9]+) hour', content)
        days = re.search('([0-9]+) day', content)
        weeks = re.search('([0-9]+) [wW]{1}eek', content)
        expire_date = datetime.utcnow()
        if seconds:
            expire_date += timedelta(seconds=int(seconds.group(1)))
        if minutes:
            expire_date += timedelta(minutes=int(minutes.group(1)))
        if hours:
            expire_date += timedelta(hours=int(hours.group(1)))
        if days:
            expire_date += timedelta(days=int(days.group(1)))
        if weeks:
            expire_date += timedelta(weeks=int(weeks.group(1)))
        return expire_date
    else:
        return datetime.min
