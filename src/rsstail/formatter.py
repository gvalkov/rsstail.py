#!/usr/bin/env python

import re
from datetime import datetime


def safe_attrgetter(item, default=""):
    """operator.attrgetter with a default value."""

    def inner(obj):
        for name in item.split("."):
            obj = getattr(obj, name, default)
        return obj

    return inner


placeholders = {
    "id": safe_attrgetter("id"),
    "title": safe_attrgetter("title"),
    "link": safe_attrgetter("link"),
    "desc": safe_attrgetter("description"),
    "pubdate": safe_attrgetter("date_parsed"),
    "updated": safe_attrgetter("updated_parsed"),
    "created": None,
    "expired": None,
    "author": safe_attrgetter("author"),
    "comments": None,
    "timestamp": None,
    "utc-timestamp": None,
}


class Formatter:
    """I interpolate a format string with feedparser values."""

    PH_NEW = 0x1  # {:} placeholders
    PH_OLD = 0x2  # %()s placeholders

    def __init__(self, fmt, time_fmt, striphtml=False):
        self.fmt = str(fmt)
        self.time_fmt = time_fmt

        self.striphtml = striphtml
        if striphtml:
            from re import compile

            self.re_striphtml = compile(r"<[^>]*?>")

        self.placeholder_style = self.plcstyle()

    def plcstyle(self):
        """Check if we're dealing with {} or %()s placeholders."""

        cn = len(re.findall(r"{[^}]*}", self.fmt)), self.PH_NEW
        co = len(re.findall(r"%\([^\(]*\)[^ ]*s", self.fmt)), self.PH_OLD

        # Whichever style has the more occurrences, wins.
        s = max((cn, co))[1]

        return s

    def __call__(self, entry):
        return self.format(entry)

    def format(self, entry):
        rendered = {
            "timestamp": self.format_dt(datetime.now()),
            "utc-timestamp": self.format_dt(datetime.utcnow()),
        }

        for placeholder, callback in placeholders.items():
            if not callback:
                continue
            rendered[placeholder] = callback(entry)

        for i in ("pubdate", "updated"):
            if i in rendered and rendered[i]:
                rendered[i] = self.format_tt(rendered[i])

        if self.striphtml:
            rendered["desc"] = self.re_striphtml.sub("", rendered["desc"])

        if self.placeholder_style == self.PH_NEW:
            return self.fmt.format(**rendered)
        else:
            return self.fmt % rendered

    def format_dt(self, dt):
        return dt.strftime(self.time_fmt)

    def format_tt(self, tt):
        dt = datetime(*tt[:6])
        return self.format_dt(dt)
