# -*- coding: utf-8 -*-
from djangodevkit import utils
import sys
import os

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

os.environ['DJANGO_MODE'] = 'local'


def manage(*args):
    settings = utils.get_settings(
        apps=('django_extensions',),
        DEBUG_PROPAGATE_EXCEPTIONS=False)
    del settings.DEBUG
    from django.core import management
    if utils.get_version() < (1, 4):
        # django < 1.6
        def run(argv=None):
            return management.execute_manager(settings)
        management.setup_environ = lambda *args: os.getcwd
    else:
        def run(argv=None):
            return management.execute_from_command_line(argv=argv)
    if utils.get_version() < (1, 7):
        from django.conf import settings as sets  # NOQA
    args = args or sys.argv[1:]

    if not args:
        return sys.exit(run())

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
        run(argv=sys.argv)


def manage_migrate():
    if utils.get_version() >= (1, 7):
        manage('migrate', '--noinput')
    else:
        manage('syncdb', '--noinput')
        from django.conf import settings
        if 'south' in settings.INSTALLED_APPS:
            manage('migrate', '--noinput')


def manage_shell():
    manage('shell_plus')


def admin():
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        del os.environ['DJANGO_SETTINGS_MODULE']
    from django.core.management import execute_from_command_line
    execute_from_command_line()
