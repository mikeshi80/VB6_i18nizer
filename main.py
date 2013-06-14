#!/usr/bin/env python
# -*- encoding: utf8 -*-

import sys
import os.path
import logging
import codecs

from VBCodeReader import analyze
from VBCodeWriter import writeSource
from JPStringExtractor import export, genStringTable


def visitor(filters, dirname, names):
    mynames = filter(lambda n : os.path.splitext(n)[1].lower() in filters, names)

    #logging.warning('names is %s', names)
    
    global jps
    global start
    for name in mynames:
        fname = os.path.join(dirname, name)
        if not os.path.isdir(fname):
            #logging.warning('is processing {%s}', fname)
            lines, form_load, jps, start = analyze(fname, jps, start)
            writeSource(fname, lines, form_load)

def writeRCFiles(topdir, jps):
    stlines = []
    export(jps, stlines)

    f = codecs.open(os.path.join(topdir, 'StringTable_JP.RC'), 'w', 'utf-16')
    f.write(genStringTable(stlines, 'jp'))
    f.close()

    f = codecs.open(os.path.join(topdir, 'StringTable_CN.RC'), 'w', 'utf-16')
    f.write(genStringTable(stlines, 'zh_CN'))
    f.close()

    f = open(os.path.join(topdir, 'StringTable.RC'), 'w')
    f.write('#include "StringTable_JP.RC"\n#include "StringTable_CN.RC"\n')
    f.close()


'''
Usage:
    python main.py topdir [.ext1] [.ext2] ...
'''
if __name__ == "__main__":
    #logging.basicConfig(filename='analyze.log')

    topdir = sys.argv[1]

    filters = ('.frm', '.bas', '.cls')
    if len(sys.argv) > 2:
        filters = sys.argv[2:]

    global jps
    jps = [] # jps is the Japanese StringTable container
    global start
    start = 1001

    os.path.walk(topdir, visitor, filters)

    writeRCFiles(topdir, jps)

