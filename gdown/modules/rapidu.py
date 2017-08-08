# -*- coding: utf-8 -*-

"""
gdown.modules.rapidu
~~~~~~~~~~~~~~~~~~~

This module contains handlers for rapidu.

"""

import re
from datetime import datetime, timedelta

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.post('https://rapidu.net/ajax.php?a=getUserLogin', {'login': username, 'pass': passwd, 'remember': 0, '_go': ''}, verify=False).json()
    if rc['message'] == 'error':
        acc_info['status'] = 'deleted'
        return acc_info
    elif rc['message'] == 'success':
        rc = r.get('https://rapidu.net', verify=False).text
        open('gdown.log', 'w').write(rc)
        if 'Account: <b>Free</b>' in rc or 'Konto: <b>Free</b>' in rc:
            acc_info['status'] = 'free'
            return acc_info
        else:
            days = re.search('A?c?c?o?u?n?t?K?o?n?t?o?: <b>Premium \(([0-9]+) dz?i?e?ń?a?y?s?n?i?\)</b>', rc).group(1)  # TODO: this is just wrong
            acc_info['status'] = 'premium'
            acc_info['expire_date'] = datetime.utcnow() + timedelta(days=int(days))
            acc_info['transfer'] = re.search('class="tipsyS"><b>(.+?)</b>', rc).group(1)
            return acc_info
    else:
        print(rc)
        open('gdown.log', 'w').write(rc)  # this won't work - json.dumps first
        ModuleError('Unknown error, full log in gdown.log')
