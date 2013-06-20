#!/usr/bin/env python
# -*- encoding: utf8 -*-

import re
from StringTableInfo import StringTableInfo
from JPChecker import hasJP
from BaseProcessor import BaseProcessor

class LineProcessor(BaseProcessor):
    '''
    class for processing line
    there are 2 functions:
    remove the comments
    extract the quoted string from the line
    '''
    quoted_patt = re.compile(r'("[^"]*")')

    
    def process(self, line):
        line = self.removeComments(line)
        infos = []
        for i in LineProcessor.quoted_patt.finditer(line):
            info = StringTableInfo(i.group(1)[1:-1], i.start(), i.end(), line[:-2] if line.endswith('\r\n') else line)
            if hasJP(info.string):
                infos.append(info)

        return infos 


