#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login'}
	opera.post('http://www.uploadstation.com/login.php', values)
	return opera.get(link).url	# return connection	

def upload(login, passwd, filename):
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login'}
	opera.post('http://uploadstation.com/login.php', values)
	content = opera.get('http://uploadstation.com/upload.php').content
	host = re.search('action="(http://upload.uploadstation.com/upload/[0-9]+/[0-9]+/)"', content).group(1)
	#
	
	# jquery getJSON function(data)
	
	#
	content = opera.post(host, files={'file':open(filename, 'rb')}).content	# upload
	open('log.log', 'w').write(content)
	return 0
