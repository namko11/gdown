#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def rapidshare_geturl(link, login, passwd):
	opera = browser()
	content = re.match('^http://[w\.]{,4}rapidshare.com/files/([0-9]+)/(.+)$', link)
	fileid = content.group(1)
	filename = content.group(2)
	content = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid='+fileid+'&filename='+filename+'&try=1&login='+login+'&password='+passwd)
	server = re.match('DL:(.+?),', content).group(1)
	return opera.get('https://'+server+'/cgi-bin/rsapi.cgi?sub=download&fileid='+fileid+'&filename='+filename+'&try=0&login='+login+'&password='+passwd, log=False, stream=True)	# return connection
def rapidshare_status(login, passwd):
	opera = browser()
	content = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=getaccountdetails&login=%s&password=%s&withpublicid=1' %(login, passwd))
	#login = re.search('accountid=(.+)\n', content).group(1)
	if 'Login failed.' in content:
		return 0
	return int(re.search('billeduntil=(.+)\n', content).group(1))
