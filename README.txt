Meta package for Django developers.

Contain:

- `django-debug-toolbar`_

- `django-extensions`_

- `django-webtest`_

This package also add some console scripts:

- **django-manage**: work like ``./manage.py`` but add ``django-extensions`` to installed apps on the fly.

- **django-shell**: work like ``./manage.py shell`` but use the ``django-extensions`` ``shell_plus``

- **django-test**: work like ``./manage.py test``.

- **django-serve**: wrap the django application in a WebError middleware and serve
  it. You can also use ``-t`` to add the ``django-debug-toolbar`` to
  ``INSTALLED_APPS`` on the fly.


.. _django-debug-toolbar: http://github.com/robhudson/django-debug-toolbar
.. _django-extensions: http://code.google.com/p/django-command-extensions/
.. _django-webtest: http://pypi.python.org/pypi/django-webtest
