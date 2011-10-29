#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def letitbit_geturl(link, login, passwd):
	link = re.search('http://[w\.]{,4}letitbit.net/download/([0-9]+)/(.+)/(.+)\.html', link)		# own | uid | name
	opera = browser()
	values = { 'act':'login', 'login':login, 'password':passwd }
	content = opera.get('http://letitbit.net/download.php?own='+link.group(1)+'&uid='+link.group(2)+'&name='+link.group(3)+'&page=1', values)	# login && get download page
	link = re.search('src="(http://.*letitbit.net/sms/check2_iframe.php\?ac_syml_uid.+)"', content).group(1)
	content = opera.get(link)								# get download iframe
	link = re.findall('href="(.+)" style', content)[0]	# get first link
	return opera.get(link, log=False, stream=True)
