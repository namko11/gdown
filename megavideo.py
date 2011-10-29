#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def megavideo_geturl(link, hash, login=None, passwd=None):
	opera = browser()
	fileid = re.match('^http://[w\.]{,4}megavideo.com/\?v=(.+)$', link).group(1)
	content = opera.get('http://www.megavideo.com/xml/player_login.php?u='+hash+'&v='+fileid)
	link = unquote(re.search('downloadurl="(.+)"', content).group(1))
	return opera.get(link, log=False, stream=True)	# return connection
