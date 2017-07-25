# -*- coding: utf-8 -*-

"""
gdown.modules.uploaded
~~~~~~~~~~~~~~~~~~~

This module contains handlers for uploaded.

"""

import re
from datetime import datetime, timedelta
from time import sleep
from decimal import Decimal

from ..module import browser, acc_info_template


def getUrl(link, username, passwd):  # not checked
    """Returns direct file url."""
    r = browser()
    values = {'id': username, 'pw': passwd, 'loginFormSubmit': 'Login'}
    r.post('http://www.uploaded.net/io/login', values)
    return r.get(link, stream=True).url  # return connection


def get(link, username, passwd):
    """Returns file content."""
    # TODO: return file-object with filename etc.
    r = browser()
    values = {'id': username, 'pw': passwd, 'loginFormSubmit': 'Login'}
    r.post('http://www.uploaded.net/io/login', values)
    return r.get(link).text


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    values = {'id': username, 'pw': passwd}
    content = r.post('http://uploaded.net/io/login', values).text
    if 'Account locked. Please contact Support.' in content:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'User and password do not match!' in content or 'Benutzer wurde gelöscht' in content or 'Account has been deleted' in content:  # wrong password / acc deleted
        acc_info['status'] = 'deleted'
        return acc_info
    content = r.get('http://uploaded.net/me').text
    if '<button type="submit">Login</button>' in content:  # ip blocked(?), waiting 30s
        sleep(30)
        return accInfo(username, passwd, proxy=proxy)
    lang = re.search('<meta name="language" http-equiv="content-language" content="(.+)" />', content).group(1)
    if lang != 'en':
        content = r.get('http://uploaded.net/language/en').text
        r.get('http://uploaded.net/language/%s' % (lang))  # restore old language

    balance = re.search('title="Request payout" onclick="location.href=\'/affiliate\'">([0-9]*?)\.?([0-9]+),([0-9]+) &([a-zA-Z]+);</em>', content)
    acc_info['balance_currency'] = balance.group(4)
    acc_info['balance'] = Decimal(balance.group(1) + balance.group(2) + '.' + balance.group(3))

    if re.search('<em>(.+)</em>', content).group(1) == 'Premium':
        # transfer
        acc_info['transfer'] = re.search('<th colspan="2"><b class="cB">(.+?)</b></th>', content).group(1)
        content = content.replace(' ', '').replace('	', '')
        acc_info['status'] = 'premium'
        if 'unlimited</th>' in content:  # lifetime premium
            acc_info['expire_date'] = datetime.max
            return acc_info
        content = re.search('<th>\n?([0-9]+.+)</th>\n?</tr>', content).group(1)
        seconds = re.search('([0-9]+)second', content)
        minutes = re.search('([0-9]+)M|minute', content)
        hours = re.search('([0-9]+)hour', content)
        days = re.search('([0-9]+)day', content)
        weeks = re.search('([0-9]+)[wW]{1}eek', content)
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
        acc_info['expire_date'] = expire_date

        return acc_info
    else:
        # TODO: detect (blind guess now)
        acc_info['status'] = 'free'
        return acc_info
