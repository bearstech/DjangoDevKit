.. impress::
  :func: spiral

==============
DjangoDevKit
==============

.. slide::
   :class: first center

Gael Pasgrimaud

`@gawel_ <http://twitter.com/gawel_>`_

Why ?
======

- I use buildout. ``manage.py`` dont work with buildout

- I always use same development tools

How ?
=====

- meta package. requires DjDt, Dj-extensions, IPython

- extra binaries scripts. django-manage, django-serve, django-shell

- pre-load ``settings.py`` and update it on the fly

Usage
=====

Install it::

    $ pip install DjangoDevKit

Use it::

    $ django-manage

Debug server
============

Wrap django application with WebError and serve it with Paste::

    $ django-serve

Same with django toolbar activated::

    $ django-serve -t

Aliases
=======

You can put some aliases in your ~/.djangodevkitrc:

.. literalinclude:: djangodevkitrc.ini
   :language: ini

.. impress::
   :func: default

That's it!
==========

.. step::
   :data-scale: 4
   :data-x: -1000
   :data-y: -750
   :data-z: 700
   :data-rotate-x: 50

For more information check:

`pypi.python.org/DjangoDevKit <http://pypi.python.org/DjangoDevKit>`_

`github.com/bearstech/DjangoDevKit <http://github.com/bearstech/DjangoDevKit/>`_

Powered by `github.com/gawel/impress <http://github.com/gawel/impress>`_



