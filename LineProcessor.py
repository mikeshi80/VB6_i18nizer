#!/usr/bin/env python
# -*- encoding: utf8 -*-

import re
from StringTableInfo import StringTableInfo
from JPChecker import hasJP

class LineProcessor(object):
    comments_patt = re.compile(u'("[^"]*")')
    quoted_patt = re.compile(r'("[^"]*")')

    def removeComments(self, line):
        r = LineProcessor.comments_patt.finditer(line)
        
        last = 0 # Last position
        retVal = ""

        for i in r:
            if i.start() > last: # if there are charactors between two quoted strings
                seg = line[last:i.start()]
                cp = seg.find("'") # if there is comment mark in non quoted string
                if cp != -1:
                    return retVal + seg[0:cp]
                else:
                    last = i.end()
                    retVal = line[:last]
            else:
                last = i.end()
                retVal = line[:last]

        if last == 0: # no quoted string at all
            cp = line.find("'")
            if cp != -1:
                return line[0:cp]
            else:
                return line
        else:
            return retVal + line[last:]
    
    def process(self, line):
        infos = []
        for i in LineProcessor.quoted_patt.finditer(line):
            info = StringTableInfo(i.group(1)[1:-1], i.start(), i.end(), line[:-2] if line.endswith('\r\n') else line)
            if hasJP(info.string):
                infos.append(info)

        return infos 


