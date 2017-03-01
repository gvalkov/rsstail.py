Rsstail
=======

*Rsstail* is a command-line syndication feed monitor with behaviour
similar to ``tail -f``. *Rsstail* (Python/feedparser_) is inspired by
rsstail_ (C/libmrss_), but provides more customizable output
formatting and additional features.

Usage
-----

::

  $ rsstail --help
  Usage: rsstail [options] <url> [<url> ...]

  General Options:
    -v --verbose            increase verbosity
    -V --version            show version and exit
    -h --help               show this help message and exit
    -x --help-format        show formatting help and exit

  Feed Options:
    -i --interval <arg>     poll every <arg> seconds
    -e --iterations <arg>   poll <arg> times and quit
    -n --initial <arg>      initially show <arg> items
    -w --newer <arg>        show items newer than <arg>
    -b --bytes <arg>        show only <arg> description/comment bytes
    -r --reverse            show in reverse order
    -s --striphtml          strip html tags
    -o --nofail             do not exit on error
    -q --unique             skip duplicate items

  Format Options:
    -t --timestamp          show local timestamp
    -T --utc-timestamp      show utc timestamp
    -l --title              show title
    -u --url                show url
    -d --desc               show description
    -p --pubdate            show publication date
    -U --updated            show last update date
    -a --author             show author
    -c --comments           show comments
    -g --no-heading         do not show headings
    -m --time-format <arg>  date/time format
    -f --format <arg>       output format (overrides other format options)

  Examples:
    rsstail --timestamp --pubdate --title --author <url1> <url2> <url3>
    rsstail --reverse --title <url> <username:password@url>
    rsstail --interval 60|60s|5m|1h --newer "2011/12/20 23:50:12" <url>
    rsstail --format '%(timestamp)-30s %(title)s %(author)s\n' <url>
    rsstail --format '{timestamp:<30} {title} {author}\n' <url>


::

  $ rsstail --help-format
  Format specifiers must have one the following forms:
    %(placeholder)[flags]s
    {placeholder:flags}

  Examples:
    --format '%(timestamp)s %(pubdate)-30s %(author)s\n'
    --format '%(title)s was written by %(author)s on %(pubdate)s\n'
    --format '{timestamp:<20} {pubdate:^30} {author:>30}\n'

  Time format takes standard 'sprftime' specifiers:
    --time-format '%Y/%m/%d %H:%M:%S'
    --time-format 'Day of the year: %j Month: %b'

  Useful flags in this context are:
    %(placeholder)-10s - left align and pad
    %(placeholder)10s  - right align and pad
    {placeholder:<10}  - left align and pad
    {placeholder:>10}  - right align and pad
    {placeholder:^10}  - center align and pad

  Available placeholders:
    author
    comments
    created
    desc
    expired
    id
    link
    pubdate
    timestamp
    title
    updated
    utc-timestamp


Please note that ``{placeholder:flags}`` style placeholders are
available only with Python **>= 2.7**.

Installing
----------

The latest stable version of rsstail can be installed from pypi_:

.. code-block:: bash

    $ pip install rsstail

Or simply put the standalone rsstail script in your ``$PATH`` and make
it executable::

    https://github.com/gvalkov/rsstail.py/releases/download/v0.5.0/rsstail.pyz.zip

Colorizing output
-----------------

*Rsstail's'* output can be piped to one of the many console
colorizers. Consider using one of the following tools: clide_,
multitail_, ccze_, colorize_, colorex_ or colout_.

Example with clide_::

    $ rsstail <options> \
    | clide -e '/(Title|Pubdate|Author|Link|Description):/g,fg=yellow,bold' \
            -e '/^.*FAILURE.*$/,fg=red,bold \


Example with multitail_::

    # add to /etc/multitail.conf
    colorscheme:rsstail.py:console syndication feed monitor
    cs_re:red,,bold:^.*FAILURE.*$
    cs_re:cyan:(:|/)
    cs_re:yellow:^.......... ..:..:..
    cs_re:green:(Title|Author|Link|Pubdate):

    $ multitail -cS "rsstail.py" -l "rsstail <options>"

These two examples are barely touching the surface of what clide_ and
multitail_ can do. Refer to the documentation of these excellent
projects for more information.


Shell completion
----------------

*Rsstail* comes with shell completion scripts for bash and zsh.

    - **bash:** copy rsstail.sh_ to ``/etc/bash_completion.d/``.
    - **zsh:**  copy rsstail.zsh_ anywhere in ``$fpath``.

If you are installing system-wide, the setup script will attempt to
place these files in the right place.


Similar projects
----------------

    - rsstail_
    - feedstail_
    - theyoke_
    - wag_


License
-------

*Rsstail* is released under the terms of the `Revised BSD License`_.

.. _rsstail:    http://www.vanheusden.com/rsstail/
.. _feedstail:  http://pypi.python.org/pypi/feedstail/
.. _theyoke:    http://github.com/mackers/theyoke/
.. _wag:        http://github.com/knobe/wag/
.. _ccze:       http://bonehunter.rulez.org/CCZE.html
.. _clide:      http://suso.suso.org/xulu/Clide
.. _colorize:   http://colorize.raszi.hu/
.. _colorex:    http://pypi.python.org/pypi/colorex/
.. _colout:     http://nojhan.github.io/colout/
.. _multitail:  http://www.vanheusden.com/multitail/
.. _feedparser: http://code.google.com/p/feedparser/
.. _libmrss:    http://www.autistici.org/bakunin/libmrss/doc/
.. _`Revised BSD License`: https://raw.github.com/gvalkov/rsstail.py/master/LICENSE

.. _rsstail.sh:  https://raw.github.com/gvalkov/rsstail.py/master/etc/rsstail.sh
.. _rsstail.zsh: https://raw.github.com/gvalkov/rsstail.py/master/etc/_rsstail
.. _pypi:        https://pypi.python.org/pypi/rsstail
