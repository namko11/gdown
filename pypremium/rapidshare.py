#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import re
from config import *

def getUrl(link, login, passwd):
	'''Returns direct file url
	IP validator is NOT present'''
	opera = requests.session(headers=headers)
	content = re.match('^https?://[w\.]{,4}rapidshare.com/files/([0-9]+)/(.+)$', link)
	fileid = content.group(1)
	filename = content.group(2)
	content = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&try=1&login=%s&password=%s' %(fileid, filename, login, passwd)).content
	server = re.match('DL:(.+?),', content).group(1)
	return opera.get('https://'+server+'/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&try=0&login=%s&password=%s' %(fileid, filename, login, passwd)).url	# return connection
	
def status(login, passwd):
	'''Returns account premium status:
	-999	unknown error
	-2		invalid password
	-1		account temporary blocked
	0		free account
	>0		premium date end timestamp'''
	'''	errors:
	ERROR: Login failed. Password incorrect or account not found. (221a75e5)
	ERROR: Login failed. Account locked. Please contact us if you have questions. (b45c2518)
	ERROR: Login failed. Login data invalid. (0320f9f0)
	'''
	opera = requests.session(headers=headers)
	content = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=getaccountdetails&login=%s&password=%s&withpublicid=1' %(login, passwd)).content
	if 'Login failed. Account locked.' in content:
		return -1
	elif 'Login failed. Password incorrect or account not found.' in content or 'Login failed. Login data invalid.' in content:
		return -2
	elif 'IP blocked' in content:	# ip blocked (too many wrong passwords)
		print 'ip bloked'
		ip_blocked
		return -101
	elif 'Login failed' in content:
		print content
		new_status
		return -999
	elif 'billeduntil=' in content:
		return int(re.search('billeduntil=(.+)\n', content).group(1))

def upload(login, passwd, filename):
	'''Returns uploaded file url'''
	opera = requests.session(headers=headers)
	server_id = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=nextuploadserver').content
	content = opera.post('https://rs%s.rapidshare.com/cgi-bin/rsapi.cgi?sub=upload' %(server_id), {'login':login, 'password':passwd}, files={'filecontent':open(filename, 'rb')}).content
	file_id = re.search('([0-9]+),[0-9]+,.+', content).group(1)
	return 'https://rapidshare.com/files/%s/%s' %(file_id, filename)
