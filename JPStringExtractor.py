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
        item['hint'] = line[:item['start']] + '<target>' + line[item['start']:item['end']] + '</target>' + line[item['end']:]
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

def export(jps, start, lines):
    '''
    export jps info to lines
    '''
    for jp in jps:
        lines.append(' ' * 4 + str(start) + ' ' * 12 + '"' + jp['string'] + ('" //' + jp['hint'] if 'hint' in jp else '') )
        start = start + 1

def genStringTable(lines, lang):
    '''
    generate the string table file
    only three languages supported
    'en_US', 'zh_CN', 'jp_JP'
    '''
    langs = {
            'en_us': ('0x09', '0x01'),
            'zh_cn': ('0x04', '0x02'),
            'jp_jp': ('0x11', '0x01'),
            'en': ('0x09', '0x01'),
            'zh': ('0x04', '0x02'),
            'jp': ('0x11', '0x01'),
            'us': ('0x09', '0x01'),
            'cn': ('0x04', '0x02')
            }
    if not lang.lower() in langs:
        raise ValueError('lang only supports en_us, zh_cn, jp_jp, en, us, zh, cn, jp')

    prim, sub = langs[lang.lower()]

    return u'''STRINGTABLE
LANGUAGE %s, %s
BEGIN
%s
END''' % (prim, sub, u'\n'.join(lines))

