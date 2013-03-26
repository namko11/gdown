# -*- coding: utf-8 -*-
import requests

from ..config import headers


def upload(login, passwd, filename):
    '''Returns uploaded file url'''
    #file_size = os.path.getsize(filename)  # get file size
    opera = requests.session(headers=headers)


    host = opera.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = opera.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    opera.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return opera.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': login, 'password': passwd}).content[:-1]  # start upload
