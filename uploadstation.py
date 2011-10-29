#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login, passwd):
	opera = browser()
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login'}
	opera.get('http://www.uploadstation.com/login.php', values)
	return opera.get(link, log=False, stream=True)	# return connection	
