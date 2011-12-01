#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime


def safe_attrgetter(item, default=''):
    ''' operator.attrgetter with a default value '''
    def inner(obj):
        for name in item.split('.'):
            obj = getattr(obj, name, default)
        return obj

    return inner


placeholders = {
    'timestamp'  : None,
    'id'         : safe_attrgetter('id'),
    'title'      : safe_attrgetter('title'),
    'link'       : safe_attrgetter('link'),
    'desc'       : safe_attrgetter('description'),
    'pubdate'    : safe_attrgetter('date_parsed'),
    'updated'    : None,
    'created'    : None,
    'expired'    : None,
    'author'     : safe_attrgetter('author'),
    'comments'   : None,
    }


class Formatter(object):
    ''' I interpolate a format string with feed parser entry values '''

    def __init__(self, fmt, time_fmt, striphtml=False):
        self.fmt = fmt
        self.time_fmt = time_fmt

        self.striphtml = striphtml
        if striphtml:
            from re import compile
            self.re_striphtml = compile(r'<[^>]*?>')

    def __call__(self, entry):
        return self.format(entry)

    def format(self, entry):
        rendered = {
            'timestamp' : self.format_dt(datetime.now()),
        }

        for ph, cb in placeholders.iteritems():
            if not cb: continue
            rendered[ph] = cb(entry)

        if 'pubdate' in rendered:
            dt = datetime(*rendered['pubdate'][:6])
            rendered['pubdate'] = self.format_dt(dt)

        if self.striphtml:
            rendered['desc'] = self.re_striphtml.sub('', rendered['desc'])

        return self.fmt % rendered

    def format_dt(self, dt):
        return dt.strftime(self.time_fmt)
