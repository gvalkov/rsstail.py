# Rsstail

<p>
    <a href="https://pypi.python.org/pypi/rsstail"><img alt="pypi version" src="https://img.shields.io/pypi/v/rsstail.svg"></a>
    <a href="https://github.com/gvalkov/rsstail.py/blob/main/LICENSE.txt"><img alt="License" src="https://img.shields.io/pypi/l/rsstail"></a>
</p>


*Rsstail* is a command-line syndication feed monitor with behaviour
similar to `tail -f`. *Rsstail* (Python/[feedparser]) is inspired by
[rsstail] (C/[libmrss]), but provides more customizable output
formatting and additional features.

## Usage

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

## Installing

The latest stable version of rsstail can be installed from [pypi][]:

``` bash
$ pip install rsstail
```

Or simply put the standalone rsstail script in your `$PATH` and make it
executable:

    sudo curl -L -o /usr/local/bin/rsstail https://github.com/gvalkov/rsstail.py/releases/download/v0.6.0/rsstail.pyz
    sudo chmod 0755 /usr/local/bin/rsstail

## Colorizing output

*Rsstail\'s\'* output can be piped to one of the many console
colorizers. Consider using one of the following tools: [clide],
[multitail], [ccze], [colorize], [colorex] or [colout].

Example with [clide][]:

    $ rsstail <options> \
    | clide -e '/(Title|Pubdate|Author|Link|Description):/g,fg=yellow,bold' \
            -e '/^.*FAILURE.*$/,fg=red,bold \

Example with [multitail][]:

    # add to /etc/multitail.conf
    colorscheme:rsstail.py:console syndication feed monitor
    cs_re:red,,bold:^.*FAILURE.*$
    cs_re:cyan:(:|/)
    cs_re:yellow:^.......... ..:..:..
    cs_re:green:(Title|Author|Link|Pubdate):

    $ multitail -cS "rsstail.py" -l "rsstail <options>"

These two examples are barely touching the surface of what [clide] and
[multitail] can do. Refer to the documentation of these excellent
projects for more information.

## Shell completion

*Rsstail* comes with shell completion scripts for bash and zsh.

 - **bash:** copy [rsstail.sh] to `/etc/bash_completion.d/`.
 - **zsh:** copy [rsstail.zsh] anywhere in `$fpath`.

If you are installing system-wide, the setup script will attempt to
place these files in the right place.

## Similar projects

 - [rsstail]
 - [feedstail]
 - [theyoke]
 - [wag]

## License

*Rsstail* is released under the terms of the [Revised BSD License].

  [feedparser]: https://github.com/kurtmckee/feedparser
  [rsstail]: http://www.vanheusden.com/rsstail/
  [libmrss]: http://www.autistici.org/bakunin/libmrss/doc/
  [pypi]: https://pypi.org/project/rsstail/
  [clide]: http://suso.suso.org/xulu/Clide
  [multitail]: http://www.vanheusden.com/multitail/
  [ccze]: http://bonehunter.rulez.org/CCZE.html
  [colorize]: http://colorize.raszi.hu/
  [colorex]: https://pypi.org/project/colorex/
  [colout]: http://nojhan.github.io/colout/
  [rsstail.sh]: https://raw.github.com/gvalkov/rsstail.py/main/etc/rsstail.sh
  [rsstail.zsh]: https://raw.github.com/gvalkov/rsstail.py/main/etc/_rsstail
  [feedstail]: https://pypi.org/project/feedstail/
  [theyoke]: http://github.com/mackers/theyoke/
  [wag]: https://github.com/tylerharper/wag
  [Revised BSD License]: https://raw.github.com/gvalkov/rsstail.py/main/LICENSE.txt
