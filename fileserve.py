#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login'}
	opera.post('http://www.fileserve.com/login.php', values)
	return opera.get(link).url	# return connection
	
def status(login, passwd, proxy=None):
	if proxy: proxy = {'http':proxy, 'https':proxy}
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login'}
	content = opera.post('http://www.fileserve.com/login.php', values, proxies=proxy).content	# sprawdz haslo
	if 'Invalid login. Please check username or password.' in content:		return -1
	content = opera.get('http://www.fileserve.com/dashboard.php', proxies=proxy).content
	#earnings = re.search('</h5><h3><span>\$ </span><span style="font-size:20px;font-weight:normal;">(.+)</span></h3>', content).group(1)
	try: premium = re.search('<td><h5>(.+) EST</h5></td>', content).group(1)
	except: 	return 0
	premium = premium.replace(' January ', '.01.')
	premium = premium.replace(' February ', '.02.')
	premium = premium.replace(' March ', '.03.')
	premium = premium.replace(' April ', '.04.')
	premium = premium.replace(' May ', '.05.')
	premium = premium.replace(' June ', '.06.')
	premium = premium.replace(' July ', '.07.')
	premium = premium.replace(' August ', '.08.')
	premium = premium.replace(' September ', '.09.')
	premium = premium.replace(' October ', '.10.')
	premium = premium.replace(' November ', '.11.')
	premium = premium.replace(' December ', '.12.')
	premium = time.mktime(datetime.datetime.strptime(premium,'%d.%m.%Y').timetuple())
	return premium
