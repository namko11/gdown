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
	values = { 'txtuser':login, 'txtpass':passwd, 'txtcheck':'login', 'txtlogin':'' }
	opera.post('http://netload.in/index.php', values)
	content = opera.get('http://netload.in/index.php?id=2').content
	# error ??
	open('log.log', 'w').write(content)

	return 0
