#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	# get token
	content = opera.get('http://chomikuj.pl').content
	token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', content).group(1)
	# login
	content = opera.post('http://chomikuj.pl/action/Login/TopBarLogin', {'__RequestVerificationToken':token, 'ReturnUrl':link, 'Login':login, 'Password':passwd, 'rememberLogin':'true', 'topBar_LoginBtn':'Zaloguj'}).content
	# get download url
	fileId = re.search('name="FileId" value="([0-9]+)"', content).group(1)
	token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', content).group(1)
	content = opera.post('http://chomikuj.pl/action/License/Download', {'fileId':fileId, '__RequestVerificationToken':token}).content
	return re.search('"redirectUrl":"(.*?)"', content).group(1)
