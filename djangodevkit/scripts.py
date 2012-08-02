# -*- coding: utf-8 -*-
from paste.deploy import loadapp
from djangodevkit import utils
import sys
import os

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

os.environ['DJANGO_MODE'] = 'local'


def manage(*args):
    settings = utils.get_settings(apps=('django_extensions',))
    del settings.DEBUG
    config = utils.get_config_file()
    app = loadapp('config:%s' % config) # NOQA
    from django.core import management
    management.setup_environ = lambda *args: os.getcwd
    loadapp('config:%s' % config)
    from django.conf import settings as sets # NOQA
    sys.argv[1:1] = args
    management.execute_manager(settings)


def manage_test():
    manage('test')


def manage_shell():
    manage('shell_plus')


def admin():
    from django.core.management import execute_from_command_line
    execute_from_command_line()
