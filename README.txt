
Meta package for Django developers. In fact you should use `twod.wsgi`_ so you don't need all this messy stuff.

Installation::

  $ easy_install -U DjangoDevKit

Contain (as dependencies):

- `django-debug-toolbar`_

- `django-extensions`_

- `django-webtest`_

This package also install some console scripts:

- **django-admin**: work like ``./django-admin.py``.

- **django-manage**: work like ``./manage.py`` but add `django-extensions` to ``INSTALLED_APPS`` on the fly.

- **django-shell**: work like ``./manage.py shell`` but use the `django-extensions` ``shell_plus``

- **django-test**: work like ``./manage.py test``. Also set
  ``DEBUG_PROPAGATE_EXCEPTIONS`` to ``True`` so `WebTest` show the full traceback
  in tests output.

- **django-serve**: wrap the Django application in a `WebError`_ middleware and
  serve it. It's also serve `/media/` directories found in installed apps. You
  can also use ``-t`` to add the `django-debug-toolbar` to ``INSTALLED_APPS``
  and ``MIDDLEWARE_CLASSES`` on the fly. You can also use **request** and
  **post** to test a single request::

    $ django-serve request /path arg1=foo

    $ django-serve post /path arg1=foo

    $ django-serve help [request|post]

.. _django-debug-toolbar: http://github.com/robhudson/django-debug-toolbar
.. _django-extensions: http://code.google.com/p/django-command-extensions/
.. _django-webtest: http://pypi.python.org/pypi/django-webtest
.. _weberror: http://bitbucket.org/bbangert/weberror
.. _twod.wsgi: http://packages.python.org/twod.wsgi/
