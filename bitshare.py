#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'user':login, 'password':passwd, 'rememberlogin':'1', 'submit':'Login' }
	opera.post('http://bitshare.com/login.html', values)
	return opera.get(link).url
