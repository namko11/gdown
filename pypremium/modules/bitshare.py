#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os
from hashlib import md5
from ..config import *

def status(login, passwd):
	'''Returns account premium status:
	-999	unknown error
	-2		invalid password
	-1		account temporary blocked
	0		free account
	>0		premium date end timestamp'''
	opera = requests.session(headers=headers)
	 # api version (do not return expire date)
	content = opera.post('http://bitshare.com/api/openapi/login.php', {'user':login, 'password':md5(passwd).hexdigest()}).content	# get hashkey (login)
	if content == 'ERROR:Username is not matching to the provided password!':
		return -2
	elif content == 'ERROR:Due to an IP-Block because of security reasons you are not allowed to send more than 10 login requests per 10 minutes!':
		print 'ip bloked'
		ip_blocked
		return -101
	elif 'ERROR' in content:
		open('log.log', 'w').write(content)
		new_status
		return -999
	content = opera.post('http://bitshare.com/api/openapi/accountdetails.php', {'hashkey':content[8:]}).content
	content = re.search('SUCCESS:([0-9]+)#[0-9]+#[0-9]+#[0-9]+#.+', content).group(1)	# 0=noPremium | 1=premium
	if content == '1':
		return status_manual(login, passwd)		# check expire date
	elif content == '0':
		return 0
		
def status_manual(login, passwd):
	opera = requests.session(headers=headers)
	opera.get('http://bitshare.com/?language=EN')	# change language (regex)
	values = { 'user':login, 'password':passwd, 'rememberlogin':'1', 'submit':'Login' }
	content = opera.post('http://bitshare.com/login.html', values).content
	if '(<b>Premium</b>)' in content:
		content = opera.get('http://bitshare.com/myaccount.html').content
		content = re.search('Valid until: ([0-9]+\-[0-9]+\-[0-9]+)', content).group(1)
		content = time.mktime(datetime.datetime.strptime(content, '%Y-%m-%d').timetuple())
		return content
	#elif '(<b><a href="http://bitshare.com/myupgrade.html">Free</a></b>)' in content:		# no need to check this
	#	return 0
	#elif 'Wrong Username or Password!' in content:
	#	return -2
	else:
		open('log.log', 'w').write(content)
		new_status
		return -999

def getUrl(link, login, passwd):
	'''Returns direct file url
	IP validator is NOT present'''
	opera = requests.session(headers=headers)
	values = { 'user':login, 'password':passwd, 'rememberlogin':'1', 'submit':'Login' }
	opera.post('http://bitshare.com/login.html', values)
	return opera.get(link).url

def upload(login, passwd, filename):
	'''Returns uploaded file url'''
	file_size = int(os.path.getsize(filename))	# get file size
	opera = requests.session(headers=headers)
	hashkey = opera.post('http://bitshare.com/api/openapi/login.php', {'user':login, 'password':md5(passwd).hexdigest()}).content[8:]	# get hashkey (login)
	host = opera.post('http://bitshare.com/api/openapi/upload.php', {'action':'getFileserver'}).content[8:]								# get host
	content = ''
	while 'SUCCESS' not in content:
		content = opera.post(host, {'hashkey':hashkey, 'filesize':file_size}, files={'file':open(filename, 'rb')}).content					# upload
	return re.search('SUCCESS:(.+?)#\[URL', content).group(1)
