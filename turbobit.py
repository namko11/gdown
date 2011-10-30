#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'user[login]':login, 'user[pass]':passwd, 'user[memory]':'1', 'user[submit]':'Zaloguj się' }
	opera.post('http://turbobit.net/user/login', values)
	content = opera.get(link).content
	link = re.search("<h1><a href='(.+)'>", content).group(1)
	return opera.get(link).url	# return connection
