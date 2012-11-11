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
	opera.get('http://www.hellshare.com')
	opera.get('http://www.hellshare.com/?do=login-showLoginWindow')
	#	http://www.hellshare.com/members-auth/login
	values = {'login':'Log in as registered user', 'username':login, 'password':passwd, 'perm_login':'on'}
	content = opera.post('http://www.hellshare.com/?do=login-loginBoxForm-submit', values).content
	if 'Wrong user name or wrong password' in content:
		return -2
	content = opera.get('http://www.hellshare.com/members/').content
	if 'Active until: ' in content:
		expire_date = re.search('Active until: ([0-9]+\.[0-9]+\.[0-9]+)<br />', content).group(1)
		expire_date = time.mktime(datetime.datetime.strptime(expire_date, '%d.%m.%Y').timetuple())
		return expire_date
	if 'Inactive' in content:
		return 0
	else:
		open('log.log', 'w').write(content)
