#!/usr/bin/env python
# encoding: utf-8

from os import getuid
from setuptools import setup, Command
from os.path import dirname, isdir, join as pjoin
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
    #'Development Status :: 6 - Mature',
    #'Development Status :: 7 - Inactive',
]

kw = {
    'name'                 : 'rsstail',
    'version'              : __version__,
    'description'          : 'A command-line syndication feed monitor mimicking tail -f',
    'long_description'     : open('README.rst').read(),
    'author'               : 'Georgi Valkov',
    'author_email'         : 'georgi.t.valkov@gmail.com',
    'license'              : 'Revised BSD License',
    'keywords'             : 'rss tail feed feedparser',
    'classifiers'          : classifiers,
    'url'                  : 'https://github.com/gvalkov/rsstail.py',
    'packages'             : ('rsstail',),
    'entry_points'         : {'console_scripts': ['rsstail = rsstail.main:main']},
    'data_files'           : [],
    'install_requires'     : ['feedparser>=5.1.3'],
    'tests_require'        : ['pytest', 'scripttest'],
    'cmdclass'             : {},
    'zip_safe'             : True,
}


# setup.py test -> py.test tests
class PyTest(Command):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self):   pass
    def run(self):
        from subprocess import call
        errno = call(('py.test', 'tests'))
        raise SystemExit(errno)

kw['cmdclass']['test'] = PyTest

# try to install bash and zsh completions (emphasis on the *try*)
if getuid() == 0:
    if isdir('/etc/bash_completion.d'):
        t = ('/etc/bash_completion.d/', ['etc/rsstail.sh'])
        kw['data_files'].append(t)

    # this is only valid for fedora and most debians
    dirs = ['/usr/share/zsh/functions/Completion/Unix/',
            '/usr/share/zsh/site-functions']

    for dir in dirs:
        if isdir(dir):
            t = (dir, ['etc/_rsstail'])
            kw['data_files'].append(t)
            continue

if __name__ == '__main__':
    setup(**kw)
