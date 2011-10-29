#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login=None, passwd=None):
	opera = browser()
	content = opera.get(link)
	srv = re.search("'srv': '(.+)',", content).group(1)
	link = srv+'/flv2/'+re.search("'file': '(.+)',", content).group(1)
	return opera.get(link, log=False, stream=True)
