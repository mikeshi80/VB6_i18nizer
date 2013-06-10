#!/usr/bin/env python
# -*- encoding: utf8 -*-
import re

Patt = re.compile(u'("[^"]*")')


def remove(line):
    u'''
    remove the comments


    >>> remove('"this"')
    '"this"'
    >>> remove('\\'')
    ''
    >>> remove('\\' this is the comments')
    ''
    >>> remove('this is "a test"')
    'this is "a test"'
    >>> remove('this is "a \\'test"')
    'this is "a \\'test"'
    >>> remove('this is a test')
    'this is a test'
    >>> remove('"this \\'is a" test, \\' come on, "test it \\'comments", \\'yes ppg')
    '"this \\'is a" test, '
    >>> remove('this is \\'test\\'"Hello world"')
    'this is '
    >>> remove(u'this is "テスト"')
    u'this is "\\u30c6\\u30b9\\u30c8"'
    >>> remove(u'this is\\' "テスト"')
    u'this is'
    >>> remove('this is "the" test')
    'this is "the" test'
    '''

    r = Patt.finditer(line)
    
    last = 0 # Last position
    retVal = ""

    for i in r:
        if i.start() > last: # if there are charactors between two quoted stirngs
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

if __name__ == '__main__':
    import doctest
    doctest.testmod()

