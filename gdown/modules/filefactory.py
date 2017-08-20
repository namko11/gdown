# -*- coding: utf-8 -*-

"""
gdown.modules.filefactory
~~~~~~~~~~~~~~~~~~~

This module contains handlers for filefactory.

"""

import re
from datetime import datetime
from dateutil import parser
from time import sleep

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    r = browser()
    r.post('http://www.filefactory.com/member/signin.php', {'loginEmail': username, 'loginPassword': passwd, 'Submit': 'Sign In'})  # login to get ff_membership cookie
    # host = r.get('http://www.filefactory.com/servers.php?single=1').text  # get best server to upload
    host = 'http://upload.filefactory.com/upload.php'  # always returning the same url (?)
    viewhash = re.search('<viewhash>(.+)</viewhash>', r.get('http://www.filefactory.com/upload/upload_flash_begin.php?files=1').text).group(1)  # get viewhash
    r.post('%s/upload_flash.php?viewhash=%s' % (host, viewhash), {'Filename': filename, 'Upload': 'Submit Query'}, files={'file': open(filename, 'rb')}).text  # upload
    return 'http://www.filefactory.com/file/%s/n/%s' % (viewhash, filename)


def accInfo(username, passwd, date_birth=True, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    content = r.post('https://www.filefactory.com/member/signin.php', data={'loginEmail': username, 'loginPassword': passwd, 'Submit': 'Sign In'}).text
    open('gdown.log', 'w').write(content)
    # r.cookies['locale'] = 'en_US.utf8'
    # content = r.get('https://www.filefactory.com', params={'language': 'en_US.utf8'}).text
    # open('gdownl.log', 'w').write(content)

    if 'What is your date of birth?' in content:
        if not date_birth:
            raise ModuleError('Birth date not set.')
        print('date birth',)  # DEBUG
        content = r.post('https://www.filefactory.com/member/setdob.php', {'newDobMonth': '1', 'newDobDay': '1', 'newDobYear': '1970', 'Submit': 'Continue'}).text
        open('gdown.log', 'w').write(content)

    if 'Please Update your Password' in content:
        if not date_birth:
            raise ModuleError('Password has to be updated.')
        print('password resetting',)  # DEBUG
        content = r.post('https://www.filefactory.com/member/setpwd.php', {'dobMonth': '1', 'dobDay': '1', 'dobYear': '1970', 'newPassword': passwd, 'Submit': 'Continue'}).text
        open('gdown.log', 'w').write(content)
        if 'Your Date of Birth was incorrect.' in content:
            print('wrong date birth',)  # DEBUG
            acc_info['status'] = 'free'
            return acc_info
        elif 'You have been signed out of your account due to a change being made to one of your core account settings.  Please sign in again.' in content or 'Your password has been changed successfully' in content:
            print('relogging after password reset',)  # DEBUG
            sleep(5)
            return accInfo(username, passwd)

    if 'Review Acceptable Use Policy' in content:  # new policy
        print('new policy')
        content = r.post('https://www.filefactory.com/member/settos.php', data={'agree': '1', 'Submit': 'I understand'}).text()


    if 'Account Pending Deletion' in content or 'The Email Address submitted was invalid' in content or 'The email address or password you have entered is incorrect.' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Too Many Failed Sign In Attempts' in content:
        # raise ModuleError('ip banned')
        # print('ip banned')  # DEBUG
        sleep(30)
        return accInfo(username=username, passwd=passwd, proxy=proxy)

    content = r.get('https://www.filefactory.com/account/').text

    if '<strong>Free Member</strong>' in content or '<strong>Kostenloses Mitglied</strong>' in content or '<strong>Membro Gratuito</strong>' in content:
        acc_info['status'] = 'free'
        return acc_info
    elif any(i in content for i in ('The account you are trying to use has been deleted.', 'This account has been automatically suspended due to account sharing.', 'The account you have tried to sign into is pending deletion.')):
        acc_info['status'] = 'blocked'
        return acc_info
    elif any(i in content for i in ('The email or password you have entered is incorrect', 'The email or password wre invalid.  Please try again.', 'The Email Address submitted was invalid', 'The email address or password you have entered is incorrect.')):
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'title="Premium valid until:' in content:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(re.search('title="Premium valid until: <strong>(.+?)</strong>">', content).group(1))
        return acc_info
    elif "Congratulations! You're a FileFactory Lifetime member. We value your loyalty and support." in content or '<strong>Lifetime</strong>' in content:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = datetime.max
        return acc_info
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
