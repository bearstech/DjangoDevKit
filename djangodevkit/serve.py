# -*- coding: utf-8 -*-
import os
import sys
import traceback
import paste.script.command
from djangodevkit import utils
from djangodevkit.mediaapp import MediaMap
from optparse import OptionParser
from webob import Request, Response
from paste.cascade import Cascade
from weberror.evalexception import EvalException


def make_app(global_conf, **local_conf):

    conf = local_conf.copy()
    conf.update(global_conf)

    if 'request' in sys.argv or 'post' in sys.argv:
        conf['no_error'] = True

    apps = middlewares = ()
    if conf.get('toolbar', False):
        apps = ('debug_toolbar',)
        middlewares = ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    mod_name = conf.get('settings',
                        os.environ.get('DJANGO_SETTINGS_MODULE', 'settings'))
    os.environ['DJANGO_SETTINGS_MODULE'] = mod_name
    if 'django_settings_module' not in global_conf:
        global_conf['django_settings_module'] = mod_name
    if 'debug' not in global_conf:
        global_conf['debug'] = 'true'

    settings = utils.get_settings(apps=apps, middlewares=middlewares)

    import django.core.handlers.wsgi
    django_app = django.core.handlers.wsgi.WSGIHandler()

    def app(environ, start_response):
        if 'request' in sys.argv or 'post' in sys.argv:
            req = Request(environ)
            try:
                resp = req.get_response(django_app)
            except Exception:
                resp = Response(content_type='text/plain')
                traceback.print_exc(file=resp.body_file)
            return resp(environ, start_response)
        return django_app(environ, start_response)

    if 'no_error' not in conf:
        app = EvalException(app, debug=True)
    if 'no_media' not in conf:
        app = Cascade([app, MediaMap(settings)])
    return app


def main(*args, **kwargs):
    args = sys.argv

    if 'help' in args:
        pass
    elif 'request' in args:
        config = utils.get_config_file()
        sys.argv[2:2] = [config]
    elif 'post' in args:
        config = utils.get_config_file()
        sys.argv[2:2] = [config]
    elif 'serve' not in args:
        config = utils.get_config_file()
        parser = OptionParser()
        parser.add_option("-t", "--debug-toolbar", dest="toolbar",
                          action="store_true", default=False)
        parser.add_option("-i", "--non-interactive", dest="interactive",
                          action="store_true", default=False)
        parser.add_option("-m", "--no-media", dest="no_media",
                          action="store_true", default=False)
        options, args = parser.parse_args()

        if options.toolbar:
            print 'Including django-debug-toolbar'
            sys.argv.append('toolbar=true')

        if options.interactive:
            sys.argv.append('no_error=true')
        else:
            print 'Including WebError middleware'

        if options.no_media:
            print 'Do not serve media files'
            sys.argv.append('no_media=true')

        sys.argv = [a for a in sys.argv if a not in ('-t', '-i', '-m')]
        sys.argv[1:1] = ['serve', '--reload', config]
    paste.script.command.run()
