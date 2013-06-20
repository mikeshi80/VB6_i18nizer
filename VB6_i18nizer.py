#!/usr/bin/env python
# -*- encoding: utf8 -*-

import os.path
import sys
import codecs

from StringTableGenerator import StringTableGenerator
from LineProcessor import LineProcessor
from SourceScanner import SourceScanner
from SourceWriter import SourceWriter

def writeRCs(stg, topdir):
    fj = codecs.open(os.path.join(topdir, 'StringTable_JP.RC'), 'w', 'utf-16')
    fj.write(stg.generate('jp'))
    fj.close()

    fc = codecs.open(os.path.join(topdir, 'StringTable_CN.RC'), 'w', 'utf-16')
    fc.write(stg.generate('cn'))
    fc.close()

    f = open(os.path.join(topdir, 'StringTable.RC'), 'w')
    f.write('#include "StringTable_JP.RC"\n#include "StringTable_CN.RC"\n')
    f.close()


def visitor(options, dirname, names):
    scanner = options[0]
    filters = options[1]
    mynames = filter(lambda n : os.path.splitext(n)[1].lower() in filters, names)

    for name in mynames:
        fname = os.path.join(dirname, name)
        if not os.path.isdir(fname):
            writer = SourceWriter(fname)
            scanner.scan(fname, writer)
            writer.write()


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
    os.path.walk(topdir, visitor, options)

    writeRCs(stg, topdir)

if __name__ == '__main__':
    main()
