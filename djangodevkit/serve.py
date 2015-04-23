# -*- coding: utf-8 -*-
import os
import sys
import webob
import backlash
import waitress
from djangodevkit import utils
from djangodevkit.mediaapp import MediaMap
from optparse import OptionParser


class Cascade(object):

    def __init__(self, app, medias):
        self.app = app
        self.medias = medias

    def log(self, req, resp):
        print('{0.method} {0.path_info} {1.status}'.format(req, resp))

    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        req.environ['wsgi.errors'] = sys.stderr
        resp = req.get_response(self.app)
        if resp.status_int != 404:
            self.log(req, resp)
            return resp(environ, start_response)
        if self.medias:
            media = self.medias(environ, start_response)
            if media is None:
                self.log(req, resp)
                return resp(environ, start_response)
            return media
        else:
            self.log(req, resp)
            return resp(environ, start_response)


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

    try:
        from django.core.wsgi import get_wsgi_application
    except ImportError:
        import django.core.handlers.wsgi
        app = django.core.handlers.wsgi.WSGIHandler()
    else:
        app = get_wsgi_application()

    if 'no_media' not in conf:
        app = Cascade(app, MediaMap(settings))
    else:
        app = Cascade(app, None)
    if 'no_error' not in conf:
        app = backlash.DebuggedApplication(app)
    return app


def main(*args, **kwargs):
    args = sys.argv
    config = None
    conf = {}

    config = utils.get_config_file()
    parser = OptionParser()
    parser.add_option("-t", "--debug-toolbar", dest="toolbar",
                      action="store_true", default=False)
    parser.add_option("-i", "--non-interactive", dest="interactive",
                      action="store_true", default=False)
    parser.add_option("-m", "--no-media", dest="no_media",
                      action="store_true", default=False)
    parser.add_option("--host", dest="host",
                      action="store", default="0.0.0.0")
    parser.add_option("-p", "--port", dest="port",
                      action="store", default="8000")
    parser.add_option("--threads", dest="threads",
                      action="store", default="2")
    options, args = parser.parse_args()

    if options.toolbar:
        conf['toolbar'] = True

    if options.interactive:
        conf['no_error'] = True

    if options.no_media:
        conf['no_media'] = True

    if config is None:
        config = utils.get_config_file()

    if 'request' in args:
        app = make_app({}, no_error=True)
        req = webob.Request.blank(args[1])
        try:
            resp = req.get_response(app)
        except:
            raise
        else:
            if resp.charset:
                body = resp.text
            else:
                body = resp.body
            if not isinstance(body, str):
                body = body.decode('utf8')
            print(body)
    else:
        config = utils.get_config_file()
        app = make_app(conf)
        from django.utils import autoreload
        autoreload.main(serve, (app,), {
            'expose_tracebacks': True,
            'host': options.host,
            'port': options.port,
            'threads': options.threads,
        })
        return


def serve(app, **kwargs):
    print('')
    waitress.serve(app, **kwargs)
