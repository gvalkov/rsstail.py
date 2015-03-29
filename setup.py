#!/usr/bin/env python
# encoding: utf-8

from os import getuid
from setuptools import setup
from os.path import isdir
from rsstail import __version__


classifiers = [
    'Environment :: Console',
    'Topic :: Utilities',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: BSD License',
    'Development Status :: 5 - Production/Stable',
]

entry_points = {
    'console_scripts': ['rsstail = rsstail.main:main']
}

kw = {
    'name':             'rsstail',
    'version':          __version__,
    'description':      'A command-line syndication feed monitor mimicking tail -f',
    'long_description': open('README.rst').read(),
    'author':           'Georgi Valkov',
    'author_email':     'georgi.t.valkov@gmail.com',
    'license':          'Revised BSD License',
    'keywords':         'rss tail feed feedparser',
    'url':              'https://github.com/gvalkov/rsstail.py',
    'classifiers':      classifiers,
    'packages':         ['rsstail'],
    'install_requires': ['feedparser>=5.1.3'],
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
