#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, abspath, join as pjoin
from functools import partial
from scripttest import TestFileEnvironment


here = dirname(abspath(__file__))
env = TestFileEnvironment(pjoin(here, './test-output'))

feed1 = '%s/feeds/jenkins.rss' % here
cmd = 'rsstail'

run = partial(env.run, expect_stderr=True)


def test_run_no_args_no_opts():
    r = run(cmd)
    assert r.returncode == 0
    assert 'General Options:' in r.stdout


def test_run_initial():
    r = run(cmd + ' -e 1 --initial 3 %s' % feed1)
    assert len(r.stdout.splitlines()) == 3


def test_run_order():
    r = run(cmd + ' -e 1 --reverse --title %s' % feed1)

    exp = [
        'Title: pip_python2.6 #1002 (SUCCESS)',
        'Title: pip_python2.6 #1003 (SUCCESS)',
        'Title: pip_python2.6 #1004 (SUCCESS)',
        'Title: pip_python2.6 #1005 (SUCCESS)',
        'Title: pip_python2.6 #1006 (FAILURE)'
    ]

    res = [i.strip(' ') for i in r.stdout.splitlines()]
    assert res == exp

    r = run(cmd + ' -e 1 --title %s' % feed1)
    res = [i.strip(' ') for i in r.stdout.splitlines()]
    assert res == list(reversed(exp))


def test_run_headings():
    r = run(cmd + ' -e 1 --title --url --no-heading %s' % feed1)
    assert ('Title' not in r.stdout) and ('Link' not in r.stdout)


def test_run_newer():
    r = run(cmd + ' -e 1 --newer "2012/01/04 11:00:00" %s' % feed1)
    assert (len(r.stdout.splitlines())) == 1

    r = run(cmd + ' -e 1 --newer "2012/01/04 11:00" %s' % feed1)
    assert (len(r.stdout.splitlines())) == 1

    r = run(cmd + ' -e 1 --newer "2012/01/04" %s' % feed1)
    assert (len(r.stdout.splitlines())) == 2

    r = run(cmd + ' -e 1 --newer "2012/01/04 $#@!@#" %s' % feed1, expect_error=True)
    assert r.returncode == 1


def test_run_striphtml():
    # TODO: find test feed
    r = run(cmd + ' -e 1 --desc --striphtml  %s' % feed1)
