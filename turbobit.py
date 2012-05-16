#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	opera = requests.session(headers=headers)
	values = { 'user[login]':login, 'user[pass]':passwd, 'user[memory]':'1', 'user[submit]':'Zaloguj się' }
	opera.post('http://turbobit.net/user/login', values)
	content = opera.get(link).content
	link = re.search("<h1><a href='(.+)'>", content).group(1)
	return opera.get(link).url	# return connection

def upload(login, passwd, filename):
	#file_size = os.path.getsize(filename)	# get file size
	opera = requests.session(headers=headers)
	values = { 'user[login]':login, 'user[pass]':passwd, 'user[memory']:'1', 'user[submit]':'Zaloguj się' }
	opera.post('http://turbobit.net/user/login', values).content				# login
	content = opera.get('http://turbobit.net/').content
	content = re.search('urlSite=(http://s[0-9]+.turbobit.ru/uploadfile)&userId=(.+)&', content)
	host = content.group(1)
	user_id = content.group(2)
	content = opera.post(host, {'Filename':filename, 'user_id':user_id, 'stype':'null', 'apptype':'fd1', 'id':'null', 'Upload':'Submit Query'}, files={'Filedata':open(filename, 'rb')}).content	# upload
	file_id = re.search('{"result":true,"id":"(.+)","message":"Everything is ok"}', content).group(1)
	return 'http://turbobit.net/%s.html' %(file_id)
	
def status(login, passwd):
	opera = requests.session(headers=headers)
	values = { 'user[login]':login, 'user[pass]':passwd, 'user[memory']:'1', 'user[submit]':'Zaloguj się' }
	content = opera.post('http://turbobit.net/user/login', values).content				# login
	