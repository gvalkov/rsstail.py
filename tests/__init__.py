#!/usr/bin/env python
# encoding: utf-8

from attest import Tests
from test_script import script

tests = (
    script,
)

all = Tests(tests)

if __name__ == '__main__':
    all.main()
