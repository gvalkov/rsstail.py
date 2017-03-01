#!/bin/sh
set -xeu

# Bundles feedparser and rsstail into a stand-alone, executable zip file.
# Usage: pyzgen.sh [<destination.pyz>]

# This script can be replaced with zipapp once a feedparser that supports
# Python 2 and 3 from the same codebase is released.

DESTFILE="${1:-./rsstail.pyz}"
DESTFILE=$(readlink -f "$DESTFILE")
PYZEXCLUDE="\*__pycache__ \*.pyo \*.pyc feedparser-\*"
FEEDPARSER_URL="https://pypi.python.org/packages/source/f/feedparser/feedparser-5.2.1.tar.gz"

#-----------------------------------------------------------------------------
BUILDDIR=$(mktemp -d)
trap "rm -rf $BUILDDIR" EXIT

#-----------------------------------------------------------------------------
curl "$FEEDPARSER_URL" | tar -xz -C "$BUILDDIR"
cp -r ./rsstail "$BUILDDIR"
cp "$BUILDDIR"/feedparser-*/feedparser/feedparser.py "$BUILDDIR/rsstail/feedparser2.py"
cp "$BUILDDIR"/feedparser-*/feedparser/feedparser.py "$BUILDDIR/rsstail/feedparser3.py"
python -m lib2to3 --write "$BUILDDIR/rsstail/feedparser3.py"

#-----------------------------------------------------------------------------
cat > "$BUILDDIR/__main__.py" <<EOF
#!/usr/bin/env python
# -*- coding: utf-8; -*-

import sys
if sys.version_info < (3,0):
    import rsstail.feedparser2
    sys.modules['feedparser'] = rsstail.feedparser2
else:
    import rsstail.feedparser3
    sys.modules['feedparser'] = rsstail.feedparser3

from rsstail.main import main
if __name__ == '__main__':
    main()
EOF


#-----------------------------------------------------------------------------
[ -e "$DESTFILE" ] && rm -f "$DESTFILE"
(cd "$BUILDDIR" && eval zip -9 -r "$DESTFILE" . -x "$PYZEXCLUDE" )
sed -i '1i#!/usr/bin/env python' "$DESTFILE"
chmod +x "$DESTFILE"
