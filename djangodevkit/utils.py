# -*- coding: utf-8 -*-
import os
import sys
import glob
import pkg_resources

extra_eggs = []
for d in [p for p in sys.path if '/python' in p]:
    if os.path.isdir(d) and d not in pkg_resources.working_set.entries:
        pkg_resources.working_set.add_entry(d)
for p in sys.path:
    if p.endswith('.egg') and p not in pkg_resources.working_set.entries:
        pkg_resources.working_set.add_entry(p)


def get_settings(mod_name=None, apps=(), middlewares=(), **kw):
    os.environ['DEVELOPMENT'] = '1'
    settings = os.environ.get('DJANGO_SETTINGS_MODULE')
    if settings in (None, 'settings', 'settings.py'):
        settings = ['settings.py']
        settings.extend(glob.glob(os.path.join('*', 'settings.py')))
        for filename in settings:
            if os.path.isfile(filename):
                dirname = os.path.dirname(os.path.abspath(filename))
                if os.path.isfile(os.path.join(dirname, '__init__.py')):
                    # Django 1.4+
                    dirname, proj = os.path.split(dirname)
                    sys.path.insert(0, dirname)
                    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % proj
                else:
                    # Django 1.3
                    sys.path.insert(0, dirname)
                    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
                break
    mod_name = mod_name or os.environ.get('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        settings = __import__(mod_name, globals(), locals(), [''])
    except ImportError:
        sys.path.append(os.getcwd())
        settings = __import__(mod_name, globals(), locals(), [''])
    settings.DEBUG = True
    settings.TEMPLATE_DEBUG = True
    settings.DEBUG_PROPAGATE_EXCEPTIONS = True
    settings.INSTALLED_APPS += tuple(apps)
    settings.MIDDLEWARE_CLASSES = \
        tuple(middlewares) + tuple(settings.MIDDLEWARE_CLASSES)
    settings.INTERNAL_IPS = ('127.0.0.1',)
    for k, v in kw.items():
        setattr(settings, k.upper(), v)
    return settings


def get_config_file():
    configs = [arg for arg in sys.argv if arg.endswith('.ini')]
    sys.argv = [arg for arg in sys.argv if not arg.endswith('.ini')]
    if configs:
        config = os.path.abspath(configs[0])
    else:
        if os.path.isfile('django-dev.ini'):
            config = 'django-dev.ini'
        else:
            config = os.path.join(os.path.dirname(__file__), 'django-dev.ini')
        config = os.path.abspath(config)
    return config


def get_version():
    from django import VERSION
    return VERSION[0:2]
