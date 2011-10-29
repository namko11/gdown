#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login, passwd):
	opera = browser()
	link = opera.get('http://api.hotfile.com/?action=getdirectdownloadlink&username='+login+'&password='+passwd+'&link='+link)
	return opera.get(link, log=False, stream=True)	# return connection
def status(login, passwd):
	opera = browser()
	content = opera.get('http://api.hotfile.com/?action=getuserinfo&username=%s&password=%s' %(login, passwd))
	if 'is_premium=1' in content:
		return time.mktime(datetime.datetime.strptime(re.search('premium_until=(.+?)&', content).group(1)[:-6],'%Y-%m-%dT%H:%M:%S').timetuple())
	return 0
