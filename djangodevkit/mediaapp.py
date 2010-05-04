# -*- coding: utf-8 -*-
import os
import glob
from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser

class MediaMap(URLMap):
    """An app to iterate over installed apps and bound the media directory to a
    StaticURLParser"""
    def __init__(self, settings):
        URLMap.__init__(self)
        map = {}
        if settings.MEDIA_URL.startswith('/'):
            for app_name in settings.INSTALLED_APPS:
                if app_name == 'django.contrib.admin':
                    continue
                mod = __import__(app_name, globals(), locals(), [''])
                dirname = os.path.dirname(os.path.abspath(mod.__file__))
                medias = glob.glob(os.path.join(dirname, 'media*', '*'))
                for media in medias:
                    dummy, name = os.path.split(media)
                    if not dirname.startswith('.'):
                        map[settings.MEDIA_URL+name] = StaticURLParser(media)
            map[settings.MEDIA_URL] = StaticURLParser(settings.MEDIA_ROOT)

        # admin medias
        if settings.ADMIN_MEDIA_PREFIX.startswith('/'):
            import django.contrib.admin
            dirname = os.path.dirname(os.path.abspath(django.contrib.admin.__file__))
            map[settings.ADMIN_MEDIA_PREFIX] = StaticURLParser(os.path.join(dirname, 'media'))
        for k in sorted(map, reverse=True):
            v = map[k]
            print '%s -> %s' % (k, v.directory)
            self[k] = v

