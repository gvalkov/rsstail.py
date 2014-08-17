#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os, sys, copy
import signal
import logging
import textwrap
import feedparser
import optparse as opt

from sys import stdout, stderr
from time import strptime, sleep
from datetime import datetime as dt

from rsstail.formatter import placeholders
from rsstail.formatter import Formatter, hasformat


logfmt = '! %(message)s' # '%(levelname)-6s %(message)s'
logging.basicConfig(format=logfmt)
log = logging.getLogger('')


def parseopt(args=None):
    o = RsstailOption

    gen_opts = (
        o('-v', '--verbose',     action='count',      help='increase verbosity'),
        o('-V', '--version',     action='store_true', help='show version and exit'),
        o('-h', '--help',        action='store_true', help='show this help message and exit'),
        o('-x', '--help-format', action='store_true', help='show formatting help and exit'),
    )

    feed_opts = (
        o('-i', '--interval',   action='store',      help='poll every <arg> seconds',   type='timespec', default='300'),
        o('-e', '--iterations', action='store',      help='poll <arg> times and quit',  type='int', default=0),
        o('-n', '--initial',    action='store',      help='initially show <arg> items', type='int'),
        o('-w', '--newer',      action='store',      help='show items newer than <arg>'),
        o('-b', '--bytes',      action='store',      help='show only <arg> description/comment bytes', type='int'),
        o('-r', '--reverse',    action='store_true', help='show in reverse order'),
        o('-s', '--striphtml',  action='store_true', help='strip html tags'),
        o('-o', '--nofail',     action='store_true', help='do not exit on error'),
    )

    fmt_opts = (
        o('-t', '--timestamp',  action='store_true', help='show timestamp'),
        o('-l', '--title',      action='store_true', help='show title'),
        o('-u', '--url',        action='store_true', help='show url'),
        o('-d', '--desc',       action='store_true', help='show description'),
        o('-p', '--pubdate',    action='store_true', help='show publication date'),
        o('-U', '--updated',    action='store_true', help='show last update date'),
        o('-a', '--author',     action='store_true', help='show author'),
        o('-c', '--comments',   action='store_true', help='show comments'),
        o('-g', '--no-heading', action='store_true', help='do not show headings'),
        o('-m', '--time-format',action='store',      help='date/time format'),
        o('-f', '--format',     action='store',      help='output format (overrides other format options)'),
    )

    epilog = r'''
    Examples:
      %(prog)s --timestamp --pubdate --title --author <url1> <url2> <url3>
      %(prog)s --reverse --title <url> <username:password@url>
      %(prog)s --interval 60|60s|5m|1h --newer "2011/12/20 23:50:12" <url>
      %(prog)s --format '%%(timestamp)-30s %%(title)s %%(author)s\n' <url>
      %(prog)s --format '{timestamp:<30} {title} {author}\n' <url>
    ''' % {'prog': os.path.basename(sys.argv[0])}

    if not hasformat:
        epilog = epilog.splitlines()[:-3]
        epilog.append(os.linesep)
        epilog = os.linesep.join(epilog)

    # readability is better than de-duplication in this case, imho
    if hasformat:
        format_help = '''\
        Format specifiers must have one the following forms:
          %(placeholder)[flags]s
          {placeholder:flags}

        Examples:
          --format '%(timestamp)s %(pubdate)-30s %(author)s\\n'
          --format '%(title)s was written by %(author)s on %(pubdate)s\\n'
          --format '{timestamp:<20} {pubdate:^30} {author:>30}\\n'

        Time format takes standard 'sprftime' specifiers:
          --time-format '%Y/%m/%d %H:%M:%S'
          --time-format 'Day of the year: %j Month: %b'

        Useful flags in this context are:
          %(placeholder)-10s - left align and pad
          %(placeholder)10s  - right align and pad
          {placeholder:<10}  - left align and pad
          {placeholder:>10}  - right align and pad
          {placeholder:^10}  - center align and pad
        '''

    else:
        format_help = '''\
        Format specifiers have the following form:
          %(placeholder)[flags]s

        Examples:
          --format '%(timestamp)s %(pubdate)-30s %(author)s\\n'
          --format '%(title)s was written by %(author)s on %(pubdate)s\\n'

        Time format takes standard 'sprftime' specifiers:
          --time-format '%Y/%m/%d %H:%M:%S'
          --time-format 'Day of the year: %j Month: %b'

        Useful flags in this context are:
          %(placeholder)-10s - left align and pad
          %(placeholder)10s  - right align and pad
        '''

    res = [textwrap.dedent(format_help), 'Available placeholders:']
    res += sorted(map(lambda x: 2*' ' + x, placeholders))
    format_help =  os.linesep.join(res)

    description = None

    def _format_option_strings(option):
        ''' >>> _format_option_strings(('-f', '--format'))
            -f --format arg'''

        opts = []

        if option._short_opts:
            opts.append(option._short_opts[0])
        if option._long_opts:
            opts.append(option._long_opts[0])
        if len(opts) > 1:
            opts.insert(1, ' ')
        if option.takes_value():
            opts.append(' <arg>')

        return ''.join(opts)

    def _format_heading(heading):
        return '' if heading == 'Options' else heading + ':\n'

    # A more compact option formatter
    fmt = opt.IndentedHelpFormatter(max_help_position=40, indent_increment=1)
    fmt.format_option_strings = _format_option_strings
    fmt.format_heading = _format_heading
    fmt.format_epilog = lambda x: x if x else ''

    kw = {
        'usage': '%prog [options] <url> [<url> ...]',
        'epilog': textwrap.dedent(epilog),
        'formatter': fmt,
        'description': description,
        'add_help_option': False,
    }

    p = opt.OptionParser(**kw)
    p.print_help_format = lambda: print(format_help)

    gen_group  = opt.OptionGroup(p, 'General Options')
    feed_group = opt.OptionGroup(p, 'Feed Options')
    fmt_group  = opt.OptionGroup(p, 'Format Options')

    gen_group.add_options(gen_opts)
    feed_group.add_options(feed_opts)
    fmt_group.add_options(fmt_opts)

    p.add_option_group(gen_group)
    p.add_option_group(feed_group)
    p.add_option_group(fmt_group)

    if not args:
        o, a = p.parse_args()
    else:
        o, a = p.parse_args(args)

    return p, o, a


def check_timespec(option, o, value):
    '''Parse and validate 'timespec' options:
       >>> check_timespec(1)    -> 1
       >>> check_timespec('5m') -> 300
       >>> check_timespec('1h') -> 3600'''

    try:
        return int(value)
    except ValueError:
        multiply = {'s': 1, 'm': 60, 'h': 3600}
        suffix = value[-1]

        msg = 'option %s: invalid timespec value %s - hint: 60, 60s, 1m, 1h'
        if suffix in multiply:
            try:
                v = int(value[:-1])
                return v * multiply[suffix]
            except ValueError:
                raise opt.OptionValueError(msg % (option, value))

        raise opt.OptionValueError(msg % (option, value))


class RsstailOption(opt.Option):
    TYPES = opt.Option.TYPES + ('timespec',)
    TYPE_CHECKER = copy.copy(opt.Option.TYPE_CHECKER)
    TYPE_CHECKER['timespec'] = check_timespec


def error(msg, flunk=False, *args):
    log.error(msg, *args)
    if not flunk: sys.exit(1)


def sigint_handler(num=None, frame=None):
    print('... quitting\n', file=stderr)
    sys.exit(0)


def parse_date(dt_str):
    formats = ('%Y/%m/%d %H:%M:%S',
               '%Y/%m/%d %H:%M',
               '%Y/%m/%d',)

    def _try_parse(f):
        try:
            return strptime(dt_str, f)
        except ValueError:
            return None

    res = [_try_parse(i) for i in formats]
    if not any(res):
        raise ValueError('date "%s" could not be parsed' % dt_str)

    return [i for i in res if i][0]


def date_fmt(date):
    if date:
        d = dt(*date[:6]).strftime('%Y/%m/%d %H:%M:%S')
        return d


def get_last_mtime(entries):
    try:
        last = max(entries, key=lambda e: e.updated_parsed)
        return last.updated_parsed
    except (ValueError, AttributeError):
        return None


def setup_formatter(o):
    fmt = []
    wh = not o.no_heading

    if o.timestamp:
        fmt.append('%(timestamp)s')

    if o.pubdate:
        fmt.append('Pubdate: %(pubdate)s' if wh else '%(pubdate)s')

    if o.updated:
        fmt.append('Updated: %(updated)s' if wh else '%(updated)s')

    if o.title:
        fmt.append('Title: %(title)-50s' if wh else '%(title)-50s')

    if o.author:
        fmt.append('Author: %(author)s' if wh else '%(author)s')

    if o.url:
        fmt.append('Link: %(link)s' if wh else '%(link)s')

    if o.desc:
        fmt.append('\nDescription: %(desc)s\n' if wh else '\n%(desc)s\n')

    if o.comments:
        fmt.append('Comments: %(comments)s' if wh else '%(comments)s')

    time_fmt = '%Y/%m/%d %H:%M:%S' if not o.time_format else o.time_format

    if o.format:
        fmt = o.format
    elif not fmt:
        # default formatter
        fmt = 'Title: %(title)s'
    else:
        fmt = '  '.join(fmt)

    formatter = Formatter(fmt, time_fmt, o.striphtml)

    log.debug('using format: %r', formatter.fmt)
    log.debug('using time format: %r', formatter.time_fmt)
    return formatter


def tick(feeds, options, formatter, iteration):
    o = options

    for url, el in feeds.items():
        etag, last_mtime, last_update = el

        log.debug('parsing: %r', url)
        log.debug('etag:  %s', etag)
        log.debug('mtime: %s', date_fmt(last_mtime))

        feed = feedparser.parse(url, etag=etag, modified=last_mtime)

        if feed.bozo == 1:
            safeexc = (feedparser.CharacterEncodingOverride,)
            if not isinstance(feed.bozo_exception, safeexc):
                msg = 'feed error %r:\n%s'
                error(msg, o.nofail, url, feed.bozo_exception)

        if iteration == 1 and isinstance(o.initial, int):
            entries = feed.entries[:o.initial]
        else:
            entries = feed.entries

        if options.newer:
            log.debug('showing entries older than %s', date_fmt(last_update))
            p = lambda entry: entry.date_parsed > options.newer
            entries = list(filter(p, entries))

        if last_update:
            log.debug('showing entries older than %s', date_fmt(last_update))
            p = lambda entry: entry.updated_parsed > last_update
            entries = list(filter(p, entries))

        new_last_update = get_last_mtime(entries)
        if not new_last_update and not entries:
            new_last_update = last_update

        if o.reverse:
            entries = reversed(entries)

        for entry in entries:
            out = formatter(entry)
            print(out.rstrip(' '), file=sys.stdout)
        sys.stdout.flush()

        # needed for fetching/showing only new entries on next run
        etag = getattr(feed, 'etag', None)
        last_mtime = getattr(feed.feed, 'modified_parsed', None)

        feeds[url] = (etag, last_mtime, new_last_update)


def main():
    p, o, args = parseopt()

    if o.help or len(sys.argv) == 1:
        p.print_help(); sys.exit(0)

    if o.help_format:
        p.print_help_format(); sys.exit(0)

    if o.version:
        from rsstail import __version__
        print('rsstail version %s' % __version__)
        sys.exit(0)

    if len(args) == 0:
        p.print_help(); sys.exit(0)

    if o.verbose:
        log.setLevel(logging.DEBUG)

    if o.newer:
        try: o.newer = parse_date(o.newer)
        except ValueError as e: error(e)
        log.debug('showing entries newer than %s', o.newer)
    else:
        o.newer = None

    signal.signal(signal.SIGINT, sigint_handler)

    formatter = setup_formatter(o)

    # { url1 : (None,  # etag
    #           None,  # last modified (time tuple)
    #           None)} # last update time (time tuple)
    feeds = dict.fromkeys(args, (None, None, None))

    # global iteration count
    iteration = 1

    # handle stdout encoding on Python 2.x
    if sys.version_info.major == 2 and not sys.stdout.isatty():
        import locale, codecs
        encoding = locale.getpreferredencoding()
        sys.stdout = codecs.getwriter(encoding)(sys.stdout)
        # todo: does this break PYTHONENCODING?

    while True:
        try:
            tick(feeds, o, formatter, iteration)

            if isinstance(o.iterations, int) and iteration >= o.iterations:
                log.debug('maximum number of iterations reached: %d', o.iterations)
                sigint_handler()

            iteration += 1  # limited only by available memory in >= 2.5

            log.debug('sleeping for %d seconds', o.interval)
            sleep(o.interval)
        except Exception:
            if not o.nofail:
                log.exception('')
                sys.exit(1)


if __name__ == '__main__':
    main()
