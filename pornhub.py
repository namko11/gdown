#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browser import browser
import datetime
import time
import re

def pornhub_geturl(link, login=None, passwd=None):
	opera = browser()
	content = opera.get(link)
	link = unquote(re.search('to.addVariable\("video_url","(.+)"\);', content).group(1))
	return opera.get(link, log=False, stream=True)
