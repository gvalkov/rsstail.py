from os.path import dirname, abspath, join as pjoin


here = dirname(abspath(__file__))
feed1 = '%s/feeds/jenkins.rss' % here


def test_run_no_args_no_opts(rsstail):
    r = rsstail()
    assert r.returncode == 0
    assert b'General Options:' in r.stdout


def test_run_initial(rsstail):
    r = rsstail("-e", "1", "--initial", "3", feed1)
    assert len(r.stdout.splitlines()) == 3


def test_run_order(rsstail):
    r = rsstail('-e', '1', '--reverse', '--title', feed1)

    exp = [
        b'Title: pip_python2.6 #1002 (SUCCESS)',
        b'Title: pip_python2.6 #1003 (SUCCESS)',
        b'Title: pip_python2.6 #1004 (SUCCESS)',
        b'Title: pip_python2.6 #1005 (SUCCESS)',
        b'Title: pip_python2.6 #1006 (FAILURE)'
    ]

    res = [i.strip() for i in r.stdout.splitlines()]
    assert res == exp

    r = rsstail('-e', '1', '--title', feed1)
    res = [i.strip() for i in r.stdout.splitlines()]
    assert res == list(reversed(exp))


def test_run_headings(rsstail):
    r = rsstail('-e', '1', '--title', '--url', '--no-heading', feed1)
    assert (b'Title' not in r.stdout) and (b'Link' not in r.stdout)


def test_run_newer(rsstail):
    r = rsstail('-e', '1', '--newer', "2012/01/04 11:00:00", feed1)
    assert (len(r.stdout.splitlines())) == 1

    r = rsstail('-e', '1', '--newer', "2012/01/04 11:00", feed1)
    assert (len(r.stdout.splitlines())) == 1

    r = rsstail('-e', '1', '--newer', "2012/01/04", feed1)
    assert (len(r.stdout.splitlines())) == 2

    r = rsstail('-e', '1', '--newer', "2012/01/04 $#@!@#", feed1)
    assert r.returncode == 1


def test_run_striphtml(rsstail):
    # TODO: find test feed
    r = rsstail('-e', '1', '--desc', '--striphtml', feed1)
