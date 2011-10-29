#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re
from urllib import unquote

def geturl(link, hash, login=None, passwd=None):
	opera = browser()
	fileid = re.match('^http://[w\.]{,4}megaporn.com/video/\?v=(.+)$', link).group(1)
	content = opera.get('http://www.megaporn.com/video/xml/player_login.php?u='+hash+'&v='+fileid)
	link = unquote(re.search('downloadurl="(.+)"', content).group(1))
	return opera.get(link, log=False, stream=True)	# return connection
