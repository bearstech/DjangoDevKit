# -*- coding: utf-8 -*-

TRAVIS_CONF = '''
language: python
python: 3.5

sudo: false

install:
  - pip install tox
script:
  - tox
env:
'''

if __name__ == '__main__':
    import subprocess
    p = subprocess.check_output(
        'tox -l', encoding='utf8', shell=True)
    with open('.travis.yml', 'w') as fd:
        fd.write(TRAVIS_CONF)
        for env in p.split('\n'):
            env = env.strip()
            if env and env not in ('travis',):
                fd.write('  - TOXENV={}\n'.format(env))
