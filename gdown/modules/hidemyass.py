# -*- coding: utf-8 -*-

"""
gdown.modules.hidemyass
~~~~~~~~~~~~~~~~~~~

This module contains handlers for hidemyass.

"""

import re
import json
from dateutil import parser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


# def _token(corelation_id):
#     data = {"correlationId": corelation_id,
#             "operationName": "securityToken",
#             "payload": [],
#             "serviceName": "MetaService"}
#     rc = r.post('https://id.hidemyass.com/service/single/MetaService/securityToken', data=json.dumps(data)).json()
#     return rc['operationResult']


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)

    # r.get('https://my.hidemyass.com/')
    r.headers['Referer'] = 'https://my.hidemyass.com/'
    r.headers['Origin'] = 'https://my.hidemyass.com'
    r.get('https://id.hidemyass.com/public/services-schema.json')
    # token
    data = {"correlationId": 1,
            "operationName": "securityToken",
            "payload": [],
            "serviceName": "MetaService"}
    rc = r.post('https://id.hidemyass.com/service/single/MetaService/securityToken', data=json.dumps(data)).json()
    token = rc['operationResult']

    data = {"correlationId": 5,
            "operationName": "login",
            "payload": [
                {
                    "email": username,
                    "password": passwd,
                    "rememberMe": False,
                    "captcha_response": "NOTREQUIRED"
                }, {
                    "allowAuthenticated": True,
                    "extraLoginTicket": False
                }
            ],
            "securityToken": token,
            "serviceName": "LoginService"
            }
    rc = r.post('https://id.hidemyass.com/service/single/LoginService/login', data=json.dumps(data)).json()
    print(rc)

    # token
    data = {"correlationId": 1,
            "operationName": "securityToken",
            "payload": [],
            "serviceName": "MetaService"}
    rc = r.post('https://id.hidemyass.com/service/single/MetaService/securityToken', data=json.dumps(data)).json()
    token = rc['operationResult']

    data = {"correlationId": 2,
            "operationName": "getCurrentUserData",
            "payload": [],
            "securityToken": token,
            "serviceName": "AccountService"}
    rc = r.post('https://id.hidemyass.com/service/single/AccountService/getCurrentUserData', data=json.dumps(data)).content
    print(rc)

    # token with different correlationId and subdomain (my. instead of id.)
    data = {"correlationId": 123,
            "operationName": "securityToken",
            "serviceName": "SecurityController",
            "payload": []}
    rc = r.post('https://my.hidemyass.com/SecurityController/securityToken', data=json.dumps(data)).json()
    token2 = rc['operationResult']
    print(rc)

    data = {"correlationId": 124,
            "operationName": "accountInfo",
            "serviceName": "AccountController",
            "payload": [],
            "securityToken": token2}
    rc = r.post('https://my.hidemyass.com/AccountController/accountInfo', data=json.dumps(data)).content
    print(rc)

    data = {"correlationId": 127,
            "operationName": "licenseInfoList",
            "serviceName": "LicenseController",
            "payload": [],
            "securityToken": token2}
    rc = r.post('https://my.hidemyass.com/LicenseController/licenseInfoList', data=json.dumps(data))
    print(rc.content)

    # data = {"correlationId": 3,
    #         "operationName": "getInitializationData",
    #         "payload": [],
    #         "securityToken": token,
    #         "serviceName": "RegistrationService"}
    # rc = r.post('https://id.hidemyass.com/service/single/RegistrationService/getInitializationData', data=json.dumps(data)).content
    # print(rc)
