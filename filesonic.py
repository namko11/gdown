#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	fileid = re.match('^http://[w\.]{,4}filesonic.[plcom]{2,3}/file/([0-9]+)/?.*$', link).group(1)
	values = { 'u':login, 'p':passwd, 'ids':fileid, 'redirect':'true' }
	return opera.post('http://api.filesonic.com/link?method=getDownloadLink', values).url	# return connection
def status(login, passwd):
	opera = requests.session(headers=headers)
	values = { 'u':login, 'p':passwd }
	content = opera.post('http://api.filesonic.com/user?method=getInfo', values).content
	if 'Your account has been deleted' in content: 	return -1
	elif 'Login failed. Please check username or password' in content:	return -1
	#login = re.search('email":"(.+?)"', content).group(1)
	status = re.search('"is_premium":(.+?),', content).group(1)
	if status != 'true':		return 0
	else:						return time.mktime(datetime.datetime.strptime(re.search('premium_expiration":"(.+?)"', content).group(1),'%Y-%m-%d %H:%M:%S').timetuple())
