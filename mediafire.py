#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import re
from config import *

def geturl(link, premium_key, login=None, passwd=None):
	fileid = re.match('http://[w\.]{,4}mediafire.com/\?(.+)', link).group(1)
	opera = requests.session(headers=headers)
	values = { 'premium_key':premium_key, 'files':fileid }
	content = opera.post('http://www.mediafire.com/basicapi/premiumapi.php', values).content
	link = re.search('<url>(.+)</url>', content).group(1)
	return opera.get(link).url
