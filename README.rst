DjangoDevKit
=============

Meta package for Django developers.

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

- **django-migrate**: work like ``./manage.py syncdb --nointput && ./manage.py migrate --noinput`` Run migrate only if south is installed.

- **django-test**: work like ``./manage.py test``. Also set
  ``DEBUG_PROPAGATE_EXCEPTIONS`` to ``True`` so `WebTest` show the full traceback
  in tests output.

- **django-serve**: wrap the Django application in a `backlash`_ middleware and
  serve it. It's also serve `/media/` directories found in installed apps. You
  can also use ``-t`` to add the `django-debug-toolbar` to ``INSTALLED_APPS``
  and ``MIDDLEWARE_CLASSES`` on the fly. You can also use **request** and
  **post** to test a single request::

    $ django-serve request /path

You can also use some aliases. Create a ``~/.djangodevkitrc`` like this::

    [aliases]
    m =
        syncdb --noinput
        migrate --noinput
    si =
        schemamigration --initial []
    sm =
        schemamigration --auto []

``[]`` is replace with command line arguments. This mean that::

    $ django-manage sm myapp

is equal to::

    $ ./manage.py schemamigration --auto myapp

Notices that aliases are not listed in ``django-manage``'s help

.. _django-debug-toolbar: http://github.com/robhudson/django-debug-toolbar
.. _django-extensions: http://code.google.com/p/django-command-extensions/
.. _django-webtest: http://pypi.python.org/pypi/django-webtest
.. _backlash: https://pypi.python.org/pypi/backlash/
