from setuptools import setup, find_packages
import sys, os

version = '0.1'

def read(*names):
    values = dict()
    for name in names:
        filename = name+'.txt'
        if os.path.isfile(filename):
            value = open(name+'.txt').read()
        else:
            value = ''
        values[name] = value
    return values

long_description="""
%(README)s

See http://www.gawel.org/docs/DjangoDevKit/ for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(name='DjangoDevKit',
      version=version,
      description="DjangoDevKit package",
      long_description=long_description,
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Operating System :: POSIX',
      ],
      keywords='',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='http://www.gawel.org/docs/DjangoDevKit/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'docs', 'tests']),
      namespace_packages=['djangodevkit'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'PasteScript',
          'WebOb',
          'WebError',
          'WebTest',
          'IPython',
          'django-webtest',
          'django-extensions',
          'django-debug-toolbar',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      django-serve = djangodevkit.serve:main
      django-manage = djangodevkit.scripts:manage
      django-shell = djangodevkit.scripts:manage_shell
      django-test = djangodevkit.scripts:manage_test
      django-admin = djangodevkit.scripts:admin
      [paste.app_factory]
      main = djangodevkit.serve:make_app
      """,
      )
