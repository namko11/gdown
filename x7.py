#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'id':login, 'pw':passwd }
	opera.post('http://x7.to/james/login', values, referer='x7.to')
	return opera.get(link).url
