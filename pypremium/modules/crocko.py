#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
import os
from ..config import *

def getApikey(login, passwd):
	opera = requests.session(headers=headers)
	content = re.search('<content type="text">(.+)</content>', opera.post('http://api.crocko.com/apikeys', {'login':login, 'password':passwd}).content).group(1)
	if content == 'Invalid login or password':
		return False
	else:
		return content

def status(login, passwd):
	'''Returns account premium status:
	-999	unknown error
	-2		invalid password
	-1		account temporary blocked
	0		free account
	>0		premium date end timestamp'''
	# get apikey
	apikey = getApikey(login, passwd)
	if not apikey:	return -2		# invalid login or password (?)
	opera = requests.session(headers=headers)
	content = opera.get('http://api.crocko.com/account', headers={'Authorization':apikey}).content
	premium_end = re.search('<ed:premium_end>(.*?)</ed:premium_end>', content).group(1)
	if not premium_end:	return 0	# free
	else:	return premium_end		# premium

def upload(login, passwd, filename):
	'''Returns uploaded file url'''
	# get apikey
	apikey = getApikey(login, passwd)
	opera = requests.session(headers=headers)
	content = opera.post('http://api.crocko.com/files', headers={'Authorization':apikey}, files={'file':open(filename, 'rb')}).content	# upload
	return re.search('<link title="download_link" href="(.+)"', content).group(1)
	