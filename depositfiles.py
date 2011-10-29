#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login, passwd):
	opera = browser()
	values = { 'login':login, 'password':passwd, 'go':'1', 'submit':'enter' }
	opera.get('http://depositfiles.com/en/login.php', values)	# login
	content = opera.get(link)	# get download page
	link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', content).group(1)
	return opera.get(link, log=False, stream=True)
