# -*- coding: utf-8 -*-
import os
import glob
import posixpath
import urllib
from webob import static


class StaticFiles(object):

    def __init__(self):
        from django.contrib.staticfiles import finders
        self.finders = finders

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
        absolute_path = self.finders.find(normalized_path)
        if not absolute_path:
            print 'Static file %s does not exist' % path
            start_response('404 NotFound', [])
            return ['']
        else:
            return static.FileApp(absolute_path)(environ, start_response)


class MediaMap(list):
    """An app to iterate over installed apps and bound the media directory to a
    DirectoryApp"""
    def __init__(self, settings):
        map = {}
        if getattr(settings, 'MEDIA_URL', '').startswith('/'):
            for app_name in settings.INSTALLED_APPS:
                if app_name == 'django.contrib.admin':
                    continue
                mod = __import__(app_name, globals(), locals(), [''])
                dirname = os.path.dirname(os.path.abspath(mod.__file__))
                medias = glob.glob(os.path.join(dirname, 'media*', '*'))
                for media in medias:
                    dummy, name = os.path.split(media)
                    if not dirname.startswith('.'):
                        map[settings.MEDIA_URL + name] = \
                            static.DirectoryApp(media)
            map[settings.MEDIA_URL] = static.DirectoryApp(settings.MEDIA_ROOT)

        # staticfiles
        has_statics = False
        if hasattr(settings, "STATIC_URL"):
            if settings.STATIC_URL.startswith('/'):
                try:
                    map[settings.STATIC_URL] = StaticFiles()
                except ImportError:
                    pass
                else:
                    has_statics = True

        # admin medias
        if not has_statics and hasattr(settings, "ADMIN_MEDIA_PREFIX"):
            if settings.ADMIN_MEDIA_PREFIX.startswith('/'):
                import django.contrib.admin
                dirname = os.path.dirname(os.path.abspath(
                    django.contrib.admin.__file__))
                map[settings.ADMIN_MEDIA_PREFIX] = static.DirectoryApp(
                    os.path.join(dirname, 'media'))

        for l, k in sorted([(len(k), k) for k in map], reverse=True):
            self.append((k, map[k]))

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        for k, v in self:
            if path.startswith(k):
                environ = environ.copy()
                environ['PATH_INFO'] = path[len(k):]
                return v(environ, start_response)
