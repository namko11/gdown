#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
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
	return 0
