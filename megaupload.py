#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def megaupload_geturl(link, login, passwd):
	opera = browser()
	fileid = re.match('^http://[w\.]{,4}megaupload.com/\?d=(.+)$', link).group(1)
	values = {'c':'login', 'login':'1', 'setlang':'en', 'next':'d='+fileid, 'username':login, 'password':passwd}
	return opera.get('http://www.megaupload.com', values, log=False, stream=True)	# return connection
def megaupload_status(login, passwd):
	opera = browser()
	values = {'c':'login', 'login':'1', 'setlang':'en', 'next':'c=account', 'username':login, 'password':passwd}
	content = opera.get('http://www.megaupload.com', values)
	open('asd.log', 'w').write(content)
	if '<b>Premium</b>' in content:
		return time.time()+int(re.search('<b>Premium</b> <font style="font-size:12px;">\(([0-9]+) days remaining', content).group(1))*60*60
	return 0
