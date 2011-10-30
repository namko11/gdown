#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = {'loginUserName':login, 'loginUserPassword':passwd, 'loginFormSubmit':'Login'}
	opera.post('http://www.uploadstation.com/login.php', values)
	return opera.get(link).url	# return connection	
