#!/usr/bin/env python
# encoding: utf-8

from os import getuid
from setuptools import setup
from os.path import isdir


classifiers = [
    'Environment :: Console',
    'Topic :: Utilities',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: BSD License',
    'Development Status :: 5 - Production/Stable',
]

entry_points = {
    'console_scripts': ['rsstail = rsstail.main:main']
}

install_requires = [
    'feedparser >= 5.2.1'
]

extras_require = {
    'test': [
        'tox >= 2.6.0',
        'pytest >= 3.0.3',
        'scripttest >= 1.3',
        'pytest-cov >= 2.3.1',
    ],
    'devel': [
        'sphinx >= 1.4.6',
        'alabaster >= 0.7.3',
        'bumpversion >= 0.5.3',
        'check-manifest >= 0.35',
        'readme-renderer >= 16.0',
        'flake8',
        'pep8-naming',
    ]
}

kw = {
    'name':             'rsstail',
    'version':          '0.5.1',
    'description':      'A command-line syndication feed monitor mimicking tail -f',
    'long_description': open('README.rst').read(),
    'author':           'Georgi Valkov',
    'author_email':     'georgi.t.valkov@gmail.com',
    'license':          'Revised BSD License',
    'keywords':         'rss tail feed feedparser',
    'url':              'https://github.com/gvalkov/rsstail.py',
    'classifiers':      classifiers,
    'packages':         ['rsstail'],
    'install_requires': install_requires,
    'extras_require':   extras_require,
    'entry_points':     entry_points,
    'data_files':       [],
    'zip_safe':         True,
}

trydirs_bash = [
    '/etc/bash_completion.d',
    '/usr/local/etc/bash_completion.d',
]

trydirs_zsh = [
    '/etc/bash_completion.d'
    # Debian
    '/usr/share/zsh/functions/Completion/Unix/',
    # CentOS/RHEL
    '/usr/share/zsh/site-functions',
    # FreeBSD
    '/usr/local/share/zsh/site-functions/',
]

# Try to install bash and zsh completions (emphasis on the *try*).
if getuid() == 0:
    dirs = [i for i in trydirs_bash if isdir(i)]
    for path in dirs:
        kw['data_files'].append((path, ['etc/rsstail.sh']))

    dirs = [i for i in trydirs_zsh if isdir(i)]
    for path in dirs:
        kw['data_files'].append((path, ['etc/_rsstail']))


if __name__ == '__main__':
    setup(**kw)
