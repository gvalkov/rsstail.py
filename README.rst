Rsstail
=======

Rsstail is a command-line syndication feed monitor with behaviour similar to
'tail -f'. Rsstail (python/feedparser_) is inspired by rsstail_ (C/libmrss_), but
provides more customizable output formatting and additional features.


Usage
-----

::

    $ rsstail --help
    Usage: rsstail [options] <url> [<url> ...]

    General Options:
    -v --verbose            increase verbosity
    -V --version            print version and exit
    -h --help               show this help message and exit
    -x --help-format        show formatting help and exit

    Feed Options:
    -i --interval <arg>     poll every <arg> seconds
    -e --iterations <arg>   poll <arg> times and quit
    -n --initial <arg>      initially show <arg> items
    -w --newer <arg>        show items newer than <arg>
    -b --bytes <arg>        show only <arg> description/comment bytes
    -r --reverse            print in reverse order
    -s --striphtml          strip html tags
    -o --nofail             do not exit on error

    Format Options:
    -t --timestamp          show timestamp
    -l --title              show title
    -u --url                show url
    -d --desc               show description
    -p --pubdate            show publication date
    -a --author             show author
    -c --comments           show comments
    -g --no-heading <arg>   do not show headings
    -m --time-format <arg>  date/time format
    -f --format <arg>       output format (overrides other format options)

    Examples:
    rsstail --timestamp --pubdate --title --author <url1> <url2> <url3>
    rsstail --reverse --title <url> <username:password@url>
    rsstail --format '%(timestamp)-30s %(title)s %(author)s\n' <url>
    rsstail --newer "2011/12/20 23:50:12" <url>


::

    $ rsstail --help-format
    Format specifiers have the following form:
        %(placeholder)[flags]s

    Examples:
        --format '%(timestamp) %(pubdate)-30s %(author)s\n'
        --format '%(title)s was written by %(author)s on %(pubdate)s\n'

    Time format takes standard 'sprftime' specifiers:
        --time-format '%Y/%m/%d %H:%M:%S'
        --time-format 'Day of the year: %j Month: %b'

    Useful flags in this context are:
        %(placeholder)-10s -  left align placeholder and pad to 10 characters
        %(placeholder)10s  - right align placeholder and pad to 10 characters

    Available placeholders: 
        id
        link
        desc
        title
        author
        updated
        pubdate
        expired
        created
        comments
        timestamp
    


Installing
----------

The latest stable version of rsstail is available on pypi, while the
development version can be installed from github::

    $ pip install rsstail  # latest stable version
    $ pip install git+git://github.com/gvalkov/rsstail.git # latest development version

Alternatively, you can install it manually like any other python package:: 

    $ git clone git@github.com:gvalkov/rsstail.py.git
    $ cd rsstail.py
    $ git co $versiontag
    $ python setup.py install


Colorizing output
-----------------

Since the output of rsstail can be easily piped to another process for
processing, the preferred way of adding color is to use an utility like
clide_ or multitail_ (other potential tools are ccze_ and colorize_).

Example clide_ settings::

    $ rsstail ... \
    | clide -e '/(Title|Pubdate|Author|Link|Description):/g,fg=yellow,bold' \
            -e '/^.*FAILURE.*$/,fg=red,bold \
    

Example multitail_ settings::

    # add to /etc/multitail.conf
    colorscheme:rsstail.py:console syndication feed monitor
    cs_re:red,,bold:^.*FAILURE.*$
    cs_re:cyan:(:|/)
    cs_re:yellow:^.......... ..:..:..  
    cs_re:green:(Title|Author|Link|Pubdate):

    $ multitail -cS "rsstail.py" -l "rsstail ..."

These two examples are barely touching the surface of what clide_ and
multitail_ are capable of. Refer to the documentation of these excellent
projects for more information.
    

Memory/Cpu
----------

rsstail_ (C)::

    $ /usr/bin/time -v rsstail -u http://rss.slashdot.org/Slashdot/slashdot
    Percent of CPU this job got: 1%
    Maximum resident set size (kbytes): 2852

rsstail (python)::

    $ /usr/bin/time -v rsstail http://rss.slashdot.org/Slashdot/slashdot
    Percent of CPU this job got: 16%
    Maximum resident set size (kbytes): 12484

No surprises here - the C rsstail_ is more memory/cpu efficient than this one.
Use rsstail_ if memory/cpu efficiency is of concert to you.


Similar projects
----------------

    - rsstail_
    - feedstail_
    - theyoke_
    - wag_

License
-------

Rsstail is released under the terms of the `New BSD License`_.


.. _rsstail:    http://www.vanheusden.com/rsstail/
.. _feedstail:  http://pypi.python.org/pypi/feedstail/
.. _theyoke:    http://github.com/mackers/theyoke/
.. _wag:        http://github.com/knobe/wag/
.. _ccze:       http://bonehunter.rulez.org/CCZE.html
.. _clide:      http://suso.suso.org/xulu/Clide
.. _colorize:   http://colorize.raszi.hu/
.. _multitail:  http://www.vanheusden.com/multitail/
.. _feedparser: http://code.google.com/p/feedparser/
.. _libmrss:    http://www.autistici.org/bakunin/libmrss/doc/
.. _`New BSD License`: http://raw.github.com/gvalkov/rsstail.py/master/LICENSE
