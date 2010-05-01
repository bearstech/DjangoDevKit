# -*- coding: utf-8 -*-
import os
import sys
import utils
import traceback
import paste.script.command
from optparse import OptionParser
from webob import Request, Response
from paste.httpserver import serve
from weberror.evalexception import EvalException
import django.core.handlers.wsgi


def make_app(global_conf, **local_conf):

    conf = local_conf.copy()
    conf.update(global_conf)

    if 'request' in sys.argv or 'post' in sys.argv:
        conf['no_error'] = True

    apps = middlewares =()
    if conf.get('toolbar', False):
        apps = ('debug_toolbar',)
        middlewares = ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    mod_name = conf.get('settings', os.environ.get('DJANGO_SETTINGS_MODULE', 'settings'))
    os.environ['DJANGO_SETTINGS_MODULE'] = mod_name

    settings = utils.get_settings(apps=apps, middlewares=middlewares)


    django_app = django.core.handlers.wsgi.WSGIHandler()
    def app(environ, start_response):
        if 'request' in sys.argv or 'post' in sys.argv:
            req = Request(environ)
            try:
                resp = req.get_response(django_app)
            except Exception, e:
                resp = Response(content_type='text/plain')
                traceback.print_exc(file=resp.body_file)
            return resp(environ, start_response)
        return django_app(environ, start_response)

    if 'no_error' in conf:
        return app
    else:
        return EvalException(app, debug=True)

def main(*args, **kwargs):
    args = sys.argv

    config = os.path.join(os.path.dirname(__file__), 'django-dev.ini')

    if 'help' in args:
        pass
    elif 'request' in args:
        sys.argv[2:2] = [config]
    elif 'post' in args:
        sys.argv[2:2] = [config]
    elif 'serve' not in args:
        parser = OptionParser()
        parser.add_option("-t", "--debug-toolbar", dest="toolbar",
                          action="store_true", default=False)
        parser.add_option("-i", "--non-interactive", dest="interactive",
                          action="store_true", default=False)
        options, args = parser.parse_args()
        if options.toolbar:
            print 'Including django-debug-toolbar'
            sys.argv.append('toolbar=true')
        if options.interactive:
            sys.argv.append('no_error=true')
        else:
            print 'Including WebError middleware'
        sys.argv = [a for a in sys.argv if a not in ('-t', '-i')]
        sys.argv[1:1] = ['serve', '--reload', config]
    paste.script.command.run()

