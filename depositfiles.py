#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'login':login, 'password':passwd, 'go':'1', 'submit':'enter' }
	opera.post('http://depositfiles.com/en/login.php', values)	# login
	content = opera.get(link).content	# get download page
	link = re.search('<a href="(.+)" onClick="download_started\(\);" class="hide_download_started">Download the file', content).group(1)
	return opera.get(link).url
