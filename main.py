#!/usr/bin/env python
# -*- encoding: utf8 -*-

import sys
import os.path
import logging
import codecs

from VBCodeReader import analyze


def visitor(options, dirname, names):
    mynames = filter(lambda n : os.path.splitext(n)[1].lower() in options[1], names)
    
    jps = options[0]
    start = options[1]
    for name in mynames:
        fname = os.path.join(dirname, name)
        if not os.path.isdir(fname):
            data[fname] = analyze(fname, jps, start)


'''
Usage:
    python main.py topdir .ext1 [.ext2] ...
'''
if __name__ == "__main__":
    logging.basicConfig(filename='analyze.log')

    topdir = sys.argv[1]

    filters = ('*.frm', '*.bas', '*.cls')
    if len(sys.argv) > 2:
        filters = sys.argv[2:]

    jps = {} # jps is the Japanese StringTable container
    start = 1001

    os.path.walk(topdir, visitor, (jps, start, filters))



