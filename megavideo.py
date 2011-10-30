#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from urllib import unquote
from config import *

def geturl(link, hash, login=None, passwd=None):
	opera = requests.session(headers=headers)
	fileid = re.match('^http://[w\.]{,4}megavideo.com/\?v=(.+)$', link).group(1)
	content = opera.get('http://www.megavideo.com/xml/player_login.php?u=%s&v=%s' %(hash, fileid)).content
	link = unquote(re.search('downloadurl="(.+)"', content).group(1))
	return opera.get(link).url	# return connection
