#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from ..config import *

def getUrl(link, login, passwd):
	'''Returns direct file url
	IP validator is present (?)'''
	fileid = re.match('http://d01.megashares.com/dl/(.+)/.+', link).group(1)
	link = 'http://d01.megashares.com/index.php?d01='+fileid
	opera = requests.session(headers=headers)
	values = { 'mymslogin_name':login, 'mymspassword':passwd, 'httpref':link, 'myms_login':'Login' }
	content = opera.post('http://d01.megashares.com/myms_login.php', values).content
	link = re.search('show_download_button_1">\n	<a href="(.+)">', content).group(1)
	return opera.get(link).url
