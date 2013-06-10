#!/usr/bin/env python
# -*- encoding: utf8 -*-

import re

from JPChecker import hasJP

Patt = re.compile(r'("[^"]*")')
def extract(line):
    '''
    extract the quoted Japanese string

    Examples:
    extract(u'a = "Hello, " & "世界" & "人たち"')

    return:
    (
        {string:"世界", start: 16, end: 20},
        <string:"人たち", start: 23, end: 28}
    )
    '''
    retVal = []
    for i in Patt.finditer(line):
        item = {}
        item['string'] = i.group(1)[1:-1]
        item['start'] = i.start()
        item['end'] = i.end()
        if hasJP(item['string']):
            retVal.append(item)

    return retVal

def replace(line, jps, start):
    '''
    Replace the Japanese string with LoadResString method
    jps is the result returned by extract
    start is the number for StringTable
    '''
    retVal = u''
    last = 0
    index = start
    for jp in jps:
        retVal = retVal + line[last:jp['start']] + 'LoadResString(' + str(index) + ')'
        index = index + 1
        last = jp['end']

    if last == 0:
        retVal = line
    else:
        retVal = retVal + line[last:]

    return retVal, jps, start, index
        
        
