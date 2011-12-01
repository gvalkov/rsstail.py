#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
from rsstail.version import version
from os.path import dirname, join as pjoin

here = dirname(__file__)

requires = ('feedparser>=4.1',)
tests_require = ('attest', 'scripttest')

classifiers = (
    'Environment :: Console',
    'Topic :: Utilities',
    'Development Status :: 4 - Beta',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.5',
    'License :: OSI Approved :: BSD License',
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

    'install_requires'     : requires,
    'tests_require'        : tests_require,
    'test_loader'          : 'attest:auto_reporter.test_loader',
    'test_suite'           : 'tests.all',

    'zip_safe'             : True,
}


setup(**kw)
