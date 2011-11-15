#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	content = re.match('^http://[w\.]{,4}rapidshare.com/files/([0-9]+)/(.+)$', link)
	fileid = content.group(1)
	filename = content.group(2)
	content = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&try=1&login=%s&password=%s' %(fileid, filename, login, passwd)).content
	server = re.match('DL:(.+?),', content).group(1)
	return opera.get('https://'+server+'/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&try=0&login=%s&password=%s' %(fileid, filename, login, passwd)).url	# return connection
def status(login, passwd):
	opera = requests.session(headers=headers)
	content = opera.get('https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=getaccountdetails&login=%s&password=%s&withpublicid=1' %(login, passwd)).content
	#login = re.search('accountid=(.+)\n', content).group(1)
	if 'Login failed.' in content or '404 Not Found' in content:
		return 0
	return int(re.search('billeduntil=(.+)\n', content).group(1))
