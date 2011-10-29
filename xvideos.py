#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re
from urllib import unquote

def geturl(link, login=None, passwd=None):
	opera = browser()
	content = opera.get(link)
	link = unquote(re.search('flv_url=(.+)&amp;', content).group(1))
	return opera.get(link, log=False, stream=True)
