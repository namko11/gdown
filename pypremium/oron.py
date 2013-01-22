#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import re
from config import *

def geturl(link, login, passwd):
	'''Returns direct file url
	IP validator is present'''
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

def upload(login, passwd, filename, proxy=None):
	'''Returns uploaded file url'''
	if proxy:	proxy = {'http':proxy, 'https':proxy}
	opera = requests.session(headers=headers)
	values = { 'login':login, 'password':passwd, 'op':'login', 'redirect':'', 'rand':'' }	# redirect is not working?
	opera.post('http://oron.com/login', values, proxies=proxy)
	content = opera.get('http://oron.com/', proxies=proxy).content
	srv_id = re.search('name="srv_id" value="([0-9]+)"', content).group(1)
	sess_id = re.search('name="sess_id" value="(.+)"', content).group(1)
	srv_tmp_url = re.search('name="srv_tmp_url" value="(http://.+.oron.com)"', content).group(1)
	content = opera.post('%s/upload/%s' %(srv_tmp_url, srv_id), {'upload_type':'file', 'srv_id':srv_id, 'sess_id':sess_id, 'srv_tmp_url':srv_tmp_url, 'link_rcpt':'', 'link_pass':'', 'tos':'1', 'submit_btn':' Upload! '}, files={'file_1':open(filename, 'rb')}, proxies=proxy).content	# upload
	file_id = re.search("name='fn' value='(.+?)'", content).group(1)
	return 'http://oron.com/%s' %(file_id)
	
def status(login, passwd):
	'''Returns account premium status:
	-999	unknown error
	-2		invalid password
	-1		account temporary blocked
	0		free account
	>0		premium date end timestamp'''
	opera = requests.session(headers=headers)
	values = { 'login':login, 'password':passwd, 'op':'login', 'redirect':'', 'rand':'' }	# redirect is not working?
	content = opera.post('http://oron.com/login', values).content
	if 'Incorrect Login or Password' in content:
		return -2
	elif 'Enter correct captcha' in content:
		print 'captcha'
		captcha
		return -999
	return time.mktime(datetime.datetime.strptime(re.search('<td>([0-9]+ [a-zA-Z]+ [0-9]+)</td>', content).group(1), '%d %B %Y').timetuple())
	