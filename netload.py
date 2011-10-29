#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def netload_geturl(link, login, passwd):
	opera = browser()
	values = { 'txtuser':login, 'txtpass':passwd, 'txtcheck':'login', 'txtlogin':'' }
	opera.get('http://netload.in/index.php', values)
	return opera.get(link, log=False, stream=True)	# return connection
