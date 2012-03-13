#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
#import datetime
#import time
import re
import os
from config import *

def upload(login, passwd, filename):
	file_size = int(os.path.getsize(filename))
	opera = requests.session(headers=headers)
	content = re.match('(.+);(.+)', opera.post('http://www.share-online.biz/upv3_session.php', {'username':login, 'password':passwd}).content)																		# get upload_session and best server to upload
	upload_session = content.group(1)
	host = content.group(2)
	content = opera.post('http://%s' %(host), {'username':login, 'password':passwd, 'upload_session':upload_session, 'chunk_no':1, 'chunk_number':1, 'filesize':file_size, 'finalize':1}, files={'fn':open(filename, 'rb')}).content	# upload
	return re.match('(.+);[0-9]+;.+', content).group(1)
	