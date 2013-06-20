#!/usr/bin/env python
# -*- encoding: utf8 -*-

import os.path
import sys
from StringTableGenerator import StringTableGenerator
from LineProcessor import LineProcessor
from SourceScanner import SourceScanner
from SourceWriter import SourceWriter

def visitor(options, dirname, names):
    scanner = options[0]
    filters = options[1]
    mynames = filter(lambda n : os.path.splitext(n)[1].lower() in filters, names)

    for name in mynames:
        fname = os.path.join(dirname, name)
        if not os.path.isdir(fname):
            writer = SourceWriter(fname)
            scanner.scan(fname, writer)
            writer.write(fname, True)


def main():
    start = 1001
    stg = StringTableGenerator(start)
    lineproc = LineProcessor()
    scanner = SourceScanner(stg, lineproc)

    topdir = sys.argv[1]

    filters = ('.frm', '.bas', '.cls')
    if len(sys.argv) > 2:
        filters = sys.argv[2:]
    options = (scanner, filters)

