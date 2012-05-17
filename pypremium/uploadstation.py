#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login', 'autoLogin':'on'}
	opera.post('http://www.uploadstation.com/login.php', values)
	return opera.get(link).url	# return connection	

def upload(login, passwd, filename):
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login', 'autoLogin':'on'}
	opera.post('http://uploadstation.com/login.php', values)
	content = opera.get('http://uploadstation.com/upload.php').content
	host = re.search('action="(http://upload.uploadstation.com/upload/[0-9]+/[0-9]+/)"', content).group(1)	
	content = opera.get('%s?callback=jsonp' %(host)).content	# get sessionId
	sessionId = re.search("sessionId:'(.+)'", content).group(1)
	content = opera.post('%s%s/' %(host, sessionId), files={'file':open(filename, 'rb')}).content
	open('log.log', 'w').write(content)
	return 0
