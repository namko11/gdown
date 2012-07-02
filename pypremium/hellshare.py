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
		return -1
	content = opera.get('http://www.hellshare.com/members/').content
	if 'Inactive' in content:
		return 0
	else:
		open('log.log', 'w').write(content)
