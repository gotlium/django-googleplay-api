Django-GooglePlay-API
=====================

.. image:: https://api.travis-ci.org/gotlium/django-googleplay-api.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/gotlium/django-googleplay-api


With this package, you can configure device id and proxy params,
for google play api. Also you can change google account, and link device
with new or existing account.
This reusable app give you capabilities to search, download and etc.


Installation:
-------------
1. Package:

.. code-block:: bash

    $ git clone https://github.com/gotlium/django-googleplay-api.git

    $ cd django-googleplay-api && sudo python setup.py install

**OR**

.. code-block:: bash

    $  sudo pip install django-googleplay-api

2. Add the ``djgpa`` and ``preferences`` applications to ``INSTALLED_APPS``
   in your settings file (usually ``settings.py``)
3. Sync database (``./manage.py syncdb``)


Usage example:
--------------
1. Setup Google Account, DeviceID, Proxy settings on admin panel
2. Try to use it from shell (``./manage.py shell``):

>>> from djgpa.api import GooglePlay
>>>
>>> api = GooglePlay().auth()
>>> # Search apps
>>> for row in api.search('google'):
...     print row.title
>>> # App details
>>> details = api.details('com.android.chrome')
>>> print details.docV2.title, details.docV2.creator
>>> # Download app
>>> api.download('com.google.android.apps.docs', '~/Download/chrome.apk')
