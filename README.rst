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

    >>> from gdown import uploaded
    >>> uploaded.accInfo('login', 'password')
    {
        'email': 'sample@email.com',
        'id': 542,
        'status': 'premium',
        'expire_date': datetime.datetime(2014, 5, 28, 11, 16, 33),
        'transfer': None,
        'points': None
    }
    >>> uploaded.accInfo('login', 'password')['expire_date']
    datetime.datetime(2014, 5, 28, 11, 16, 33)
    >>> uploaded.upload('README.rst', 'login', 'password')
    'http://uploaded.net/file/b66fx0q9'
    >>> uploaded.getUrl('http://uploaded.net/file/b66fx0q9', 'login', 'password')
    'http://am4-r1f9-stor06.uploaded.net/dl/d1010186-518b-4b3a-8f90-140b58ad75a0'
    ...


CLI examples
------------
.. code-block:: bash

    >>> gdown status uploaded -u login -p password
    Premium expire on: 2014-05-28 11:16:33
    # TODO: accInfo
    >>> gdown up uploaded README.rst -u login -p password
    http://uploaded.net/file/b66fx0q9
    >>> gdown dl http://uploaded.net/file/b66fx0q9 -u login -p password
    done.
    # TODO: more verbose download (show progress etc.)
    ...


Modules status
--------------

Hosting sites
^^^^^^^^^^^^^^
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

Torrent sites
^^^^^^^^^^^^^^
+-------------+-----------------+-----------+-----------+-----------+-----------+
|   Module    |     Website     |  accInfo  |  getUrl   |  upload   |  rateGood |
+=============+=================+===========+===========+===========+===========+
|kickass      |kickass.to       |✔          |✖          |✖          |✔          |
+-------------+-----------------+-----------+-----------+-----------+-----------+


Various sites
^^^^^^^^^^^^^^
+-------------+-----------------+-----------+-----------+
|   Module    |     Website     |  accInfo  |  comment  |
+=============+=================+===========+===========+
|wp           |wp.pl            |✔          |-          |
+-------------+-----------------+-----------+-----------+
|onet         |onet.pl          |✔          |-          |
+-------------+-----------------+-----------+-----------+
|interia      |interia.pl       |✔          |-          |
+-------------+-----------------+-----------+-----------+
|rlslog       |rlslog.net       |-          |✔          |
+-------------+-----------------+-----------+-----------+

License
-------

GNU GPLv3
