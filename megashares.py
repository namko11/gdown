#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.browser import browser
import datetime
import time
import re

def geturl(link, login, passwd):
	fileid = re.match('http://d01.megashares.com/dl/(.+)/.+', link).group(1)
	link = 'http://d01.megashares.com/index.php?d01='+fileid
	opera = browser()
	values = { 'mymslogin_name':login, 'mymspassword':passwd, 'httpref':link, 'myms_login':'Login' }
	content = opera.get('http://d01.megashares.com/myms_login.php', values)
	link = re.search('show_download_button_1">\n	<a href="(.+)">', content).group(1)
	return opera.get(link, log=False, stream=True)
