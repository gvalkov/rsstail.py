#!/usr/bin/env python
# encoding: utf-8

from attest import Tests
from test_script import script
from test_formatter import formatter

tests = (
    script,
    formatter,
)

all = Tests(tests)

if __name__ == '__main__':
    all.main()
