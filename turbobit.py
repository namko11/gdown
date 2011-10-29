#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def turbobit_geturl(link, login, passwd):
	opera = browser()
	values = { 'user[login]':login, 'user[pass]':passwd, 'user[memory]':'1', 'user[submit]':'Zaloguj się' }
	opera.get('http://turbobit.net/user/login', values)
	content = opera.get(link)
	link = re.search("<h1><a href='(.+)'>", content).group(1)
	return opera.get(link, log=False, stream=True)	# return connection
