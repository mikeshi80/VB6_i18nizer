#!/usr/bin/env python
# -*- encoding: utf8 -*-
import re

class BaseProcessor(object):

    comments_patt = re.compile(u'("[^"]*")')
    def removeComments(self, line):
        r = BaseProcessor.comments_patt.finditer(line)
        
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
