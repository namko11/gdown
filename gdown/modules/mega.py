# -*- coding: utf-8 -*-

"""
gdown.modules.mega
~~~~~~~~~~~~~~~~~~~

This module contains handlers for mega.

"""

import simplejson
#import re
#import os
#from dateutil import parser
from random import randint

from ..module import browser, acc_info_template
from ..exceptions import ModuleError
from ..utils import prepare_key, str_to_a32, stringhash


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    params = {'id': randint(0, 0xFFFFFFFF)}

    passwd_aes = prepare_key(str_to_a32(passwd))
    uh = stringhash(username, passwd_aes)
    data = simplejson.dumps([{'a': 'us', 'user': username, 'uh': uh}])
    rc = simplejson.loads(r.post('https://g.api.mega.co.nz/cs', data, params=params).content)[0]

    if isinstance(rc, int):  # error code returned
        if rc == -9:
            acc_info['status'] = 'deleted'
            return acc_info
        else:
            open('gdown.log', 'w').write(rc)
            raise ModuleError('Unknown error, full log in gdown.log')
    elif isinstance(rc, dict):
        params['sid'] = rc['sid']
        rc = __ask__({'a': 'ug'})
        print rc
    else:
        print rc
        print type(rc)
