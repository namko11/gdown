# -*- coding: utf-8 -*-

"""
gdown.decaptchercom
~~~~~~~~~~~~~~~~~~~

This module implements basic api for decaptcher.com.

"""

import requests


class client(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def decode(self, captcha_img):
        """Resolves captcha."""
        values = {'function': 'picture2', 'username': self.username, 'password':self.password, 'pict_to': '0', 'pict_type': '0'}
        files = {'pict': captcha_img}
        rc = requests.post('http://poster.de-captcher.com/', values, files=files).text.split('|')
        #0|1246040|1484|0|0|42398666 9022
        return {'status': rc[0], 'text': rc[5]}
