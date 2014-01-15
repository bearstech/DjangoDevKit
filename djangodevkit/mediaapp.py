# -*- coding: utf-8 -*-
import os
import glob
from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser
from paste.fileapp import FileApp
import posixpath
import urllib


class StaticFiles(object):

    def __init__(self, settings):
        from django.contrib.staticfiles import finders
        self.finders = finders
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
        absolute_path = self.finders.find(normalized_path)
        if not absolute_path:
            print 'Static file %s does not exist' % path
            start_response('404 NotFound', [])
            return ['']
        else:
            return FileApp(absolute_path)(environ, start_response)


class MediaMap(URLMap):
    """An app to iterate over installed apps and bound the media directory to a
    StaticURLParser"""
    def __init__(self, settings):
        URLMap.__init__(self)
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
                        map[settings.MEDIA_URL + name] = StaticURLParser(media)
            map[settings.MEDIA_URL] = StaticURLParser(settings.MEDIA_ROOT)

        # staticfiles
        has_statics = False
        if hasattr(settings, "STATIC_URL"):
            if settings.STATIC_URL.startswith('/'):
                try:
                    map[settings.STATIC_URL] = StaticFiles(settings)
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
                map[settings.ADMIN_MEDIA_PREFIX] = StaticURLParser(
                    os.path.join(dirname, 'media'))
        for k in sorted(map, reverse=True):
            v = map[k]
            self[k] = v
