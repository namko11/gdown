#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login, passwd):
	opera = browser()
	values = { 'id':login, 'pw':passwd }
	opera.get('http://x7.to/james/login', values, referer='x7.to')
	return opera.get(link, log=False, stream=True)
