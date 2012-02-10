#!/usr/bin/env python
# encoding: utf-8

from attest import Tests
from rsstail.formatter import Formatter

formatter = Tests()


@formatter.test
def placeholder_style_detect():
    f = Formatter('{asdf} {zxcv} {qwerty}', None)
    assert f.placeholder_style == f.PH_NEW

    f = Formatter('%(asdf)s %(zxcv)s %(qwerty)-20s', None)
    assert f.placeholder_style == f.PH_OLD

    f = Formatter('{asdf} %(zxcv)s %(qwerty)s', None)
    assert f.placeholder_style == f.PH_OLD

    f = Formatter('{asdf} {zxcv} %(qwerty)s', None)
    assert f.placeholder_style == f.PH_NEW

    f = Formatter('{asdf} {zxcv} %(qwerty)s %(azerty)s', None)
    assert f.placeholder_style == f.PH_OLD


if __name__ == '__main__':
    formatter.main()
