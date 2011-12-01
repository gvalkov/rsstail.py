#!/usr/bin/env python
# encoding: utf-8

import os, sys
import signal
import logging
import textwrap
import feedparser

from sys import stdout, stderr
from time import strptime, sleep

from rsstail.formatter import placeholders
from rsstail.formatter import Formatter


logfmt = '%(message)s' #'%(levelname)-6s: %(message)s'
logging.basicConfig(format=logfmt)
log = logging.getLogger('')


def parseopt(args=None):
    import optparse as opt

    o = opt.make_option

    gen_opts = (
        o('-v', '--verbose',    action='count',       help='increase verbosity'                ) ,
        o('-V', '--version',    action='store_true',  help='print version and exit'            ) ,
        o('-h', '--help',       action='store_true',  help='show this help message and exit'   ) ,
        o('-x', '--help-format',action='store_true',  help='show formatting help and exit'     ) ,
    )

    feed_opts = (
        o('-i', '--interval',   action='store',       help='poll every <arg> seconds',   type='int', default=300) ,
        o('-e', '--iterations', action='store',       help='poll <arg> times and quit',  type='int', default=0) ,
        o('-n', '--initial',    action='store',       help='initially show <arg> items', type='int',     ) ,
        o('-w', '--newer',      action='store',       help='show items newer than <arg>',               ) ,
        o('-b', '--bytes',      action='store',       help='show only <arg> description/comment bytes', type='int' ) ,
        o('-r', '--reverse',    action='store_true',  help='print in reverse order',                    ) ,
        o('-s', '--striphtml',  action='store_true',  help='strip html tags',                           ) ,
        o('-o', '--nofail',     action='store_true',  help='do not exit on error',                      ) ,
    )

    fmt_opts = (
        o('-t', '--timestamp',  action='store_true',  help='show timestamp',        ) ,
        o('-l', '--title',      action='store_true',  help='show title',            ) ,
        o('-u', '--url',        action='store_true',  help='show url',              ) ,
        o('-d', '--desc',       action='store_true',  help='show description',      ) ,
        o('-p', '--pubdate',    action='store_true',  help='show publication date', ) ,
        o('-a', '--author',     action='store_true',  help='show author',           ) ,
        o('-c', '--comments',   action='store_true',  help='show comments',         ) ,
        o('-g', '--no-heading', action='store',       help='do not show headings',  ) ,
        o('-m', '--time-format',action='store',       help='date/time format',      ) ,
        o('-f', '--format',     action='store',       help='output format (overrides other format options)', ) ,
    )


    epilog = '''
    Examples:
      %(prog)s --timestamp --pubdate --title --author <url1> <url2> <url3>
      %(prog)s --reverse --title <url> <username:password@url>
      %(prog)s --format '%%(timestamp)-30s %%(title)s %%(author)s\\n' <url>
      %(prog)s --newer "2011/12/20 23:50:12" <url>

    ''' % {'prog' : os.path.basename(sys.argv[0])}

    format_help = '''\
    Format specifiers have the following form:
        %%(placeholder)[flags]s

    Examples:
        --format '%%(timestamp) %%(pubdate)-30s %%(author)s\\n'
        --format '%%(title)s was written by %%(author)s on %%(pubdate)s\\n'

    Time format takes standard 'sprftime' specifiers:
        --time-format '%%Y/%%m/%%d %%H:%%M:%%S'
        --time-format 'Day of the year: %%j Month: %%b'

    Useful flags in this context are:
        %%(placeholder)-10s -  left align placeholder and pad to 10 characters
        %%(placeholder)10s  - right align placeholder and pad to 10 characters

    Available placeholders: \n%s
    ''' % os.linesep.join(
            sorted(
                map(lambda x: 8*' ' + x, placeholders),
                cmp=lambda x,y: len(x) - len(y))
            )

    description = None


    def _format_option_strings(option):
        ''' ('-f', '--format')  ->  -f --format arg'''

        opts = []

        if option._short_opts: opts.append(option._short_opts[0])
        if option._long_opts:  opts.append(option._long_opts[0])
        if len(opts) > 1: opts.insert(1, ' ')

        if option.takes_value(): opts.append(' <arg>')

        return ''.join(opts)

    def _format_heading(heading):
        if heading == 'Options': return ''
        return heading + ':\n'

    # A more compact option formatter
    fmt = opt.IndentedHelpFormatter(max_help_position=40, indent_increment=1)
    fmt.format_option_strings = _format_option_strings
    fmt.format_heading = _format_heading
    fmt.format_epilog = lambda x: x if x else ""

    kw = {
        'usage'       : '%prog [options] <url> [<url> ...]',
        'formatter'   : fmt,
        'epilog'      : textwrap.dedent(epilog),
        'description' : description,
        'add_help_option' : False,
    }

    p = opt.OptionParser(**kw)
    p.print_help_format = lambda: stdout.write(textwrap.dedent(format_help))

    gen_group  = opt.OptionGroup(p, 'General Options')
    feed_group = opt.OptionGroup(p, 'Feed Options')
    fmt_group  = opt.OptionGroup(p, 'Format Options')

    gen_group.add_options(gen_opts)
    feed_group.add_options(feed_opts)
    fmt_group.add_options(fmt_opts)

    p.add_option_group(gen_group)
    p.add_option_group(feed_group)
    p.add_option_group(fmt_group)

    if not args: o, a = p.parse_args()
    else:        o, a = p.parse_args(args)

    return p, o, a


def error(msg, flunk=False):
    log.error(msg)
    if not flunk: sys.exit(1)


def parse_date(dt_str):
    formats = ( '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d %H:%M',
                '%Y/%m/%d', )

    def _try_parse(f):
        try:
            return strptime(dt_str, f)
        except ValueError:
            return None

    res = map(_try_parse, formats)
    if not any(res):
        raise ValueError('date "%s" could not be parsed' % dt_str)

    return [i for i in res if i][0]


def setup_formatter(o):
    fmt = []
    wh = not o.no_heading

    if o.timestamp:
        fmt.append('%(timestamp)s  ')

    if o.pubdate:
        fmt.append('Pubdate: %(pubdate)s  ' if wh else '%(pubdate)s  ' )

    if o.title:
        fmt.append('Title: %(title)-50s' if wh else '%(title)-50s' )

    if o.author:
        fmt.append('Author: %(author)s  ' if wh else '%(author)s  ' )

    if o.url:
        fmt.append('Link: %(link)s\n' if wh else '%(link)s\n' )

    if o.desc:
        fmt.append('Description: %(desc)s\n' if wh else '%(desc)s\n' )

    if o.comments:
        fmt.append('Comments: %(comments)s\n' if wh else '%(comments)s\n' )

    time_fmt = '%Y/%m/%d %H:%M:%S' if not o.time_format else o.time_format

    if not fmt:
        # default formatter
        formatter = Formatter('Title: %(title)s', time_fmt, o.striphtml)
    else:
        #if not fmt[-1].endswith('\n'): fmt.append('\n')
        formatter = Formatter(''.join(fmt), time_fmt)

    log.debug('using format %s' % repr(formatter.fmt))
    log.debug('using time format %s' % repr(formatter.time_fmt))
    return formatter


def sigint_handler(num=None, frame=None):
    print >>stderr, '...quitting'
    sys.exit(0)


def tick(feeds, options, formatter):
    o = options

    for url, el in feeds.iteritems():
        etag, last_modified = el

        log.debug('parsing %s ...' % url)
        feed = feedparser.parse(url, etag=etag, modified=last_modified)

        if feed.bozo == 1:
            msg = 'feed error \'%s\':\n%s' % (url, feed.bozo_exception)
            error(msg, o.nofail)

        if o.initial:
            entries = feed.entries[:o.initial]
        else:
            entries = feed.entries

        if options.newer:
            p = lambda entry: entry.date_parsed > options.newer
            entries = filter(p, entries)

        if o.reverse:
            entries = reversed(entries)

        for entry in entries:
            out = formatter(entry)
            stdout.write(out)
            stdout.flush()
            stdout.write(os.linesep)

        # update modified and etag values
        etag = getattr(feed, 'etag', None)
        last_modified = getattr(feed.feed, 'modified_parsed', None)

        feeds[url] = (etag, last_modified)


def main():
    p, o, args = parseopt()

    if o.help or len(sys.argv) == 1:
        p.print_help() ; sys.exit(0)

    if o.help_format:
        p.print_help_format() ; sys.exit(0)

    if o.version:
        from rsstail.version import version_verbose
        print version_verbose()
        sys.exit(0)

    if o.verbose:
        log.setLevel(logging.DEBUG)

    if o.newer:
        try: o.newer = parse_date(o.newer)
        except ValueError as e: error(e)
        log.debug('showing entries newer than \'%s\'' % o.newer)
    else:
        o.newer = None

    signal.signal(signal.SIGINT, sigint_handler)

    formatter = setup_formatter(o)

    # { url1 : (None, None) ... }
    feeds = dict.fromkeys(args, (None, None))

    # global iteration count
    iteration = 1

    while True:
        try:
            tick(feeds, o, formatter)

            if o.iterations and iteration >= o.iterations:
                log.debug('maximum number of iterations (%d) reached' % o.iterations)
                sigint_handler()

            iteration += 1 # limited only by available memory in >=2.5

            log.debug('sleeping for %d seconds' % o.interval)
            sleep(o.interval)
        except Exception:
            if not o.nofail:
                log.exception('')
                sys.exit(1)


if __name__ == '__main__':
    main()
