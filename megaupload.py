#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	fileid = re.match('^http://[w\.]{,4}megaupload.com/\?d=(.+)$', link).group(1)
	values = {'c':'login', 'login':'1', 'setlang':'en', 'next':'d='+fileid, 'username':login, 'password':passwd}
	return opera.post('http://www.megaupload.com', values).url	# return connection
def status(login, passwd):
	opera = requests.session(headers=headers)
	values = {'c':'login', 'login':'1', 'setlang':'en', 'next':'c=account', 'username':login, 'password':passwd}
	content = opera.post('http://www.megaupload.com/?c=account', values).content
	status = re.search('<div class="account_txt">(.+) &nbsp;&nbsp;</div>', content).group(1)
	if status == 'Premium':
		return time.time()+int(re.search('<div class="account_txt"> ([0-9]+) days remaining  </div>', content).group(1))*60*60*24
	return 0
