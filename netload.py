#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'txtuser':login, 'txtpass':passwd, 'txtcheck':'login', 'txtlogin':'' }
	opera.post('http://netload.in/index.php', values)
	return opera.get(link).url	# return connection
