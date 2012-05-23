#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os
from hashlib import md5
from config import *

def status(login, passwd):
	opera = requests.session(headers=headers)
	''' # api version (do not return expire date)
	hashkey = opera.post('http://bitshare.com/api/openapi/login.php', {'user':login, 'password':md5(passwd).hexdigest()}).content[8:]	# get hashkey (login)
	content = opera.post('http://bitshare.com/api/openapi/accountdetails.php', {'hashkey':hashkey}).content
	content = re.search('SUCCESS:([0-9]+)#[0-9]+#[0-9]+#[0-9]+#.+', content).group(1)	# 0=noPremium | 1=premium
	'''
	opera.get('http://bitshare.com/?language=EN')	# change language (regex)
	values = { 'user':login, 'password':passwd, 'rememberlogin':'1', 'submit':'Login' }
	content = opera.post('http://bitshare.com/login.html', values).content
	if '(<b>Premium</b>)' in content:
		content = opera.get('http://bitshare.com/myaccount.html').content
		content = re.search('Valid until: ([0-9]+\-[0-9]+\-[0-9]+)', content).group(1)
		content = time.mktime(datetime.datetime.strptime(content, '%Y-%m-%d').timetuple())
		return content
	elif 'Free' in content:
		return 0
	elif 'Wrong Username or Password!' in content:
		return -1
	else:
		open('log.log', 'w').write(content)
		new_status

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
