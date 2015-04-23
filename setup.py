from setuptools import setup, find_packages
import os

version = '1.0.6'


def read(*names):
    values = dict()
    for name in names:
        if os.path.isfile(name):
            value = open(name).read()
        else:
            value = ''
        values[name] = value
    return values

long_description = """
%(README.rst)s

News
====

%(CHANGES.txt)s

""" % read('README.rst', 'CHANGES.txt')

install_requires = [
    'WebOb',
    'backlash',
    'WebTest',
    'IPython',
    'waitress',
    'django-webtest',
    'django-extensions',
    'django-debug-toolbar',
]


setup(name='DjangoDevKit',
      version=version,
      description="DjangoDevKit package",
      long_description=long_description,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='django',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='https://github.com/bearstech/DjangoDevKit',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'docs', 'tests']),
      namespace_packages=['djangodevkit'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      django-serve = djangodevkit.serve:main
      django-manage = djangodevkit.scripts:manage
      django-migrate = djangodevkit.scripts:manage_migrate
      django-shell = djangodevkit.scripts:manage_shell
      django-admin = djangodevkit.scripts:admin
      [paste.app_factory]
      main = djangodevkit.serve:make_app
      """,
      )
