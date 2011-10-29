#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def mediafire_geturl(link, premium_key, login=None, passwd=None):
	fileid = re.match('http://[w\.]{,4}mediafire.com/\?(.+)', link).group(1)
	opera = browser()
	values = { 'premium_key':premium_key, 'files':fileid }
	content = opera.get('http://www.mediafire.com/basicapi/premiumapi.php', values)
	link = re.search('<url>(.+)</url>', content).group(1)
	return opera.get(link, log=False, stream=True)
