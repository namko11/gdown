#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
#import datetime
#import time
import re
from config import *

def upload(login, passwd, filename):
	opera = requests.session(headers=headers)
	opera.post('http://filefactory.com/member/login.php', {'email':login, 'password':passwd})																		# login to get ff_membership cookie
	#host = opera.get('http://www.filefactory.com/servers.php?single=1').content																					# get best server to upload
	host = 'http://upload.filefactory.com/upload.php'																												# always returning the same url (?)
	viewhash = re.search('<viewhash>(.+)</viewhash>', opera.get('http://www.filefactory.com/upload/upload_flash_begin.php?files=1').content).group(1)				# get viewhash
	opera.post('%s/upload_flash.php?viewhash=%s' %(host, viewhash), {'Filename':filename, 'Upload':'Submit Query'}, files={'file':open(filename, 'rb')}).content	# upload
	return 'http://www.filefactory.com/file/%s/n/%s' %(viewhash, filename)
	