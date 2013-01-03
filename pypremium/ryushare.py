#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os
from config import *
	
def status(login, passwd):
	opera = requests.session(headers=headers)
	content = opera.post('http://ryushare.com', {'op':'login', 'redirect':'http://ryushare.com/my-account.python', 'login':login, 'password':passwd, 'loginFormSubmit':'Login'}).content
	if 'Your account was banned by administrator.' in content:
		return -1
	elif 'Incorrect Login or Password' in content:
		return -2
	elif 'Your IP was blocked because too many logins fail.' in content:
		print 'ip blocked'
		ip_blocked
		return -101
	elif 'Premium account expire:' in content:
		return time.mktime(datetime.datetime.strptime(re.search('Premium account expire:</TD><TD><b>(.+)</b>', content).group(1), '%d %B %Y').timetuple())
	elif '<a class="logout" href="http://ryushare.com/logout">&nbsp;Logout</a>' in content:
		return 0
	else:
		open('log.log', 'w').write(content)
		print content
		new_status
		return -999
