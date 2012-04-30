#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	link = opera.get('http://api.hotfile.com/?action=getdirectdownloadlink&username=%s&password=%s&link=%s' %(login, passwd, link)).content
	return opera.get(link).url	# return connection
	
def status(login, passwd):
	opera = requests.session(headers=headers)
	content = opera.get('http://api.hotfile.com/?action=getuserinfo&username=%s&password=%s' %(login, passwd)).content
	if 'is_premium=1' in content:
		return time.mktime(datetime.datetime.strptime(re.search('premium_until=(.+?)&', content).group(1)[:-6],'%Y-%m-%dT%H:%M:%S').timetuple())
	elif 'is_premium=0' in content:
		return time.time()
	elif 'invalid username or password' in content:
		return -1
	elif 'too many failed attemtps' in content:
		print 'ip blocked'
		asd
	print content

def upload(login, passwd, filename):
	file_size = os.path.getsize(filename)	# get file size
	opera = requests.session(headers=headers)
	host = opera.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]																				# get server to upload
	upload_id = opera.post('http://%s/segmentupload.php?action=start' %(host), {'size':file_size}).content[:-1]													# start upload
	opera.post('http://%s/segmentupload.php?action=upload' %(host), {'id':upload_id, 'offset':0}, files={'segment':open(filename, 'rb')}).content				# upload
	return opera.post('http://%s/segmentupload.php?action=finish' %(host), {'id':upload_id, 'name':filename, 'username':login, 'password':passwd}).content[:-1]	# start upload
	