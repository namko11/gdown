#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def bitshare_geturl(link, login, passwd):
	opera = browser()
	values = { 'user':login, 'password':passwd, 'rememberlogin':'1', 'submit':'Login' }
	opera.get('http://bitshare.com/login.html', values)
	return opera.get(link, log=False, stream=True)
