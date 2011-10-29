#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login=None, passwd=None):
	opera = browser()
	content = opera.get(link)
	link = re.search('<source src="(.+)" type="video/mp4">', content).group(1)
	return opera.get(link, log=False, stream=True)
