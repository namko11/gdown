#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os
from hashlib import md5
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'user':login, 'password':passwd, 'rememberlogin':'1', 'submit':'Login' }
	opera.post('http://bitshare.com/login.html', values)
	return opera.get(link).url

def upload(login, passwd, filename):
	file_size = int(os.path.getsize(filename))	# get file size
	opera = requests.session(headers=headers)
	hashkey = opera.post('http://bitshare.com/api/openapi/login.php', {'user':login, 'password':md5(passwd).hexdigest()}).content[8:]	# get hashkey (login)
	host = opera.post('http://bitshare.com/api/openapi/upload.php', {'action':'getFileserver'}).content[8:]								# get host
	content = ''
	while 'SUCCESS' not in content:
		content = opera.post(host, {'hashkey':hashkey, 'filesize':file_size}, files={'file':open(filename, 'rb')}).content					# upload
	return re.search('SUCCESS:(.+?)#\[URL', content).group(1)
