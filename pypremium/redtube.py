#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login=None, passwd=None):
	'''Returns direct file url'''
	opera = requests.session(headers=headers)
	content = opera.get(link).content
	link = re.search('<source src="(.+)" type="video/mp4">', content).group(1)
	return opera.get(link).url
