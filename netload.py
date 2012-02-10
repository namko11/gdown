#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'txtuser':login, 'txtpass':passwd, 'txtcheck':'login', 'txtlogin':'' }
	opera.post('http://netload.in/index.php', values)
	return opera.get(link).url	# return connection
def status(login, passwd):
	opera = requests.session(headers=headers)
	values = { 'txtuser':login, 'txtpass':passwd, 'txtcheck':'login', 'txtlogin':'Login' }
	opera.post('http://netload.in/index.php', values)
	content = opera.get('http://netload.in/index.php?id=2').content
	if 'This account was locked' in content:
		return -1
	elif 'No Bonus' in content:
		return 0
	else:
		return time.time() + int(re.search('<div style="float: left; width: 150px; color: #FFFFFF;"><span style="color: green">([0-9]+) Tage.+</span></div>', content).group(1))*60*60*24
