#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from ..config import *

def getUrl(link, login, passwd):
	'''Returns direct file url
	IP validator is present'''
	opera = requests.session(headers=headers)
	values = { 'login':login, 'password':passwd, 'go':'1', 'submit':'enter' }
	opera.post('http://depositfiles.com/en/login.php', values)	# login
	content = opera.get(link).content	# get download page
	link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', content).group(1)
	return opera.get(link).url

def status(login, passwd):
	'''Returns account premium status:
	-999	unknown error
	-2		invalid password
	-1		account temporary blocked
	0		free account
	>0		premium date end timestamp'''
	opera = requests.session(headers=headers)
	values = { 'login':login, 'password':passwd, 'go':'1', 'submit':'enter' }
	opera.post('http://depositfiles.com/en/login.php', values)	# login
	#opera.get('http://depositfiles.com/gold/')
	#<div class="access">You have Gold access until: <b>2012-08-02 20:52:29</b></div>
	