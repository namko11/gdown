#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re
from urllib import unquote
from urlparse import parse_qs

def geturl(link, login=None, passwd=None):
	opera = browser()
	content = opera.get(link)
	content = unquote(re.search('url_encoded_fmt_stream_map=(.+?)&', content).group(1)).split()
	links = []
	for i in content:	links.append(parse_qs(i))
	return opera.get(links[0]['url'][0], log=False, stream=True)
