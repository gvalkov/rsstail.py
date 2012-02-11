#!/usr/bin/env python
# encoding: utf-8

from os import getuid
from setuptools import setup
from rsstail.version import version
from os.path import dirname, isdir, join as pjoin

here = dirname(__file__)

requires = ('feedparser>=4.1',)
tests_require = ('attest', 'scripttest')

classifiers = (
    'Environment :: Console',
    'Topic :: Utilities',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.5',
    'License :: OSI Approved :: BSD License',
    #'Development Status :: 1 - Planning',
    #'Development Status :: 2 - Pre-Alpha',
    #'Development Status :: 3 - Alpha',
    'Development Status :: 4 - Beta',
    #'Development Status :: 5 - Production/Stable',
    #'Development Status :: 6 - Mature',
    #'Development Status :: 7 - Inactive',
)

kw = {
    'name'                 : 'rsstail',
    'version'              : version(),

    'description'          : 'A command-line syndication feed monitor mimicking tail -f',
    'long_description'     : open(pjoin(here, 'README.rst')).read(),

    'author'               : 'Georgi Valkov',
    'author_email'         : 'georgi.t.valkov@gmail.com',

    'license'              : 'New BSD License',

    'keywords'             : 'rss tail feed feedparser',
    'classifiers'          : classifiers,

    'url'                  : 'https://github.com/gvalkov/rsstail.py',

    'packages'             : ('rsstail',),
    'entry_points'         : {
        'console_scripts'  : ['rsstail = rsstail.main:main']
    },

    'data_files'           : [],

    'install_requires'     : requires,
    'tests_require'        : tests_require,
    'test_loader'          : 'attest:auto_reporter.test_loader',
    'test_suite'           : 'tests.all',

    'zip_safe'             : True,
}

# try to install bash and zsh completions (emphasis on the *try*)
if getuid() == 0:
    if isdir('/etc/bash_completion.d'):
        t = ('/etc/bash_completion.d/', ['etc/rsstail.sh'])
        kw['data_files'].append(t)

    # this is only valid for most debians
    if isdir('/usr/share/zsh/functions/Completion/Unix/'):
        t = ('/usr/share/zsh/functions/Completion/Unix/', ['etc/_rsstail'])
        kw['data_files'].append(t)

setup(**kw)
