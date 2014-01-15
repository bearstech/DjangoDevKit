# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
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
    app = loadapp('config:%s' % config)  # NOQA
    from django.core import management
    management.setup_environ = lambda *args: os.getcwd
    loadapp('config:%s' % config)
    from django.conf import settings as sets  # NOQA
    args = args or sys.argv[1:]

    if not args:
        return sys.exit(management.execute_manager(settings))

    cmd = args[0]
    config = ConfigParser()
    config.read(os.path.expanduser('~/.djangodevkitrc'))
    try:
        alias = config.get('aliases', cmd)
    except:
        cmds = [args]
    else:
        sargs = ' '.join(args[1:])
        cmds = [a.replace('[]', sargs) for a in alias.split('\n') if a.strip()]
        cmds = [a.split() for a in cmds]
    for cmd in cmds:
        sys.argv[1:] = cmd
        management.execute_manager(settings)


def manage_migrate():
    manage('syncdb', '--noinput')
    from django.conf import settings
    if 'south' in settings.INSTALLED_APPS:
        manage('migrate', '--noinput')


def manage_test():
    manage('test')


def manage_shell():
    manage('shell_plus')


def admin():
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        del os.environ['DJANGO_SETTINGS_MODULE']
    from django.core.management import execute_from_command_line
    execute_from_command_line()
