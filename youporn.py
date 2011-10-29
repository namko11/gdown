#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def youporn_geturl(link, login=None, passwd=None):
	opera = browser()
	videoid = re.match('$http://[w\.]{,4}youporn.com/watch/(.+?)/.+^', link).group(1)
	link = 'http://download.youporn.com/download/'+videoid+'?xml=1'
	content = opera.get(link)
	link = re.search('<location>(.+)</location>', content).group(1)
	return opera.get(link, log=False, stream=True)
