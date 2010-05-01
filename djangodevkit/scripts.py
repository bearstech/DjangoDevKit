# -*- coding: utf-8 -*-
import utils
import sys
import os

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

os.environ['DJANGO_MODE'] = 'local'


def manage(*args):
    settings = utils.get_settings(apps=('django_extensions',))
    from django.core.management import execute_manager
    sys.argv[1:1] = args
    execute_manager(settings)

def manage_test():
    manage('test')

def manage_shell():
    manage('shell_plus')

def admin():
    from django.core.management import execute_from_command_line
    execute_from_command_line()
