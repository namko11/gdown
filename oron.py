#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'login':login, 'password':passwd, 'op':'login', 'redirect':'', 'rand':'' }	# redirect is not working?
	opera.post('http://oron.com/login', values)
	content = opera.get(link).content
	op = re.search('name="op" value="(.+)"', content).group(1)
	id = re.search('name="id" value="(.+)"', content).group(1)
	rand = re.search('name="rand" value="(.+)"', content).group(1)
	referer = ''
	method_free = ''
	method_premium = '1'
	down_direct = '1'
	values = { 'op':op, 'id':id, 'rand':rand, 'referer':referer, 'method_free':method_free, 'method_premium':method_premium, 'down_direct':down_direct }
	content = opera.post(link, values).content
	link = re.search('<a href="(.+)" class="atitle">Download File</a>', content).group(1)
	return opera.get(link).url	# return connection
