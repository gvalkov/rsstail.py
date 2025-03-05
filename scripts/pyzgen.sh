#!/bin/sh

# Bundles feedparser and rsstail into a stand-alone, executable zip file.
# Usage: pyzgen.sh [<destination.pyz>]

set -xeu

DESTFILE="${1:-./rsstail.pyz}"
DESTFILE=$(readlink -f "$DESTFILE")

BUILDDIR=$(mktemp -d)
trap "rm -rf $BUILDDIR" EXIT

python3 -m pip install . --no-compile -t "$BUILDDIR"
cp -r src/rsstail "$BUILDDIR"
rm -rf "$BUILDDIR/bin" "$BUILDDIR"/*.dist-info "$BUILDDIR"/**/__pycache__

python3 -m zipapp "$BUILDDIR" -p "/usr/bin/env python3" -o "$DESTFILE" -m rsstail.__main__:main
chmod +x "$DESTFILE"
unzip -l "$DESTFILE"