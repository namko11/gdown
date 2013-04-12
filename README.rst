gdown
=====


.. image:: https://travis-ci.org/oczkers/gdown.png?branch=master
        :target: https://travis-ci.org/oczkers/gdown

gdown is a library for managing sharing websites (like netload.in and uploaded.net).
It is written entirely in Python.

Check gdown script for CLI interface.


Usage
-----

.. code-block:: pycon

    >>> from gdown import hotfile
    >>> hotfile.accInfo('login', 'password')
    {
        'email': 'sample@email.com',
        'id': 542,
        'status': 'premium',
        'expire_date': datetime.datetime(2014, 5, 28, 11, 16, 33),
        'transfer': None,
        'points': None
    }
    >>> hotfile.accInfo('login', 'password')['expire_date']
    datetime.datetime(2014, 5, 28, 11, 16, 33)
    >>> hotfile.upload('README.rst', 'login', 'password')
    'http://hotfile.com/dl/193968487/73da5c1/README.rst.html'
    >>> hotfile.getUrl('https://hotfile.com/dl/193966926/685bd36/chrome_frame_helper.dll.html', 'login', 'password')
    'http://s749.hotfile.com/get/f4ac4f6ae12e42973bca22b969c3b99915f9383b/51196253/1/4a70d63eb35925fa/b8fb34e/496034/chrome_frame_helper.dll'
    ...


CLI examples
------------
.. code-block:: bash

    >>> gdown status hotfile -u login -p password
    Premium expire on: 2014-05-28 11:16:33
    # TODO: accInfo
    >>> gdown up hotfile README.rst -u login -p password
    http://hotfile.com/dl/193968597/f3ca3eb/README.rst.html
    >>> gdown dl https://hotfile.com/dl/193966926/685bd36/chrome_frame_helper.dll.html -u login -p password
    done.
    # TODO: more verbose download (show progress etc.)
    ...


Modules status
--------------

+-------------+-----------------+-----------+-----------+-----------+
|   Module    |     Website     |  accInfo  |  getUrl   |  upload   |
+=============+=================+===========+===========+===========+
|bitshare     |bitshare.com     |✔          |✔          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|chomikuj     |chomikuj.pl      |✔          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|crocko       |crocko.com       |✔          |✖          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|depositfiles |depositfiles.com |✔          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|extabit      |extabit.com      |✔          |✖          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|filefactory  |filefactory.com  |✔          |✖          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|freakshare   |freakshare.com   |✔          |✖          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|hellshare    |hellshare.com    |✔          |✖          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|hotfile      |hotfile.com      |✔          |✔          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|imgur        |imgur.com        |✖          |✖          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|letitbit     |letitbit.net     |✔          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|mediafire    |mediafire.com    |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|megashares   |megashares.com   |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|netload      |netload.in       |✔          |✔          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|pornhub      |pornhub.com      |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|rapidgator   |rapidgator.com   |✔          |✖          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|rapidshare   |rapidshare.com   |✔          |✔          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|redtube      |redtube.com      |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|ryushare     |ryushare.com     |✔          |✖          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|shareonline  |share-online.biz |✖          |✖          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|turbobit     |turbobit.net     |✔          |✔          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|uploaded     |uploaded.net     |✔          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|uploadstation|uploadstation.com|✖          |✔          |✔          |
+-------------+-----------------+-----------+-----------+-----------+
|videobam     |videobam.com     |✖          |✖          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|xhamster     |xhamster.com     |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|xvideos      |xvideos.com      |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|youjizz      |youjizz.com      |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|youporn      |youporn.com      |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+
|youtube      |youtube.com      |✖          |✔          |✖          |
+-------------+-----------------+-----------+-----------+-----------+


License
-------

GNU GPLv3
