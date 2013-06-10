#!/usr/bin/env python
# -*- encoding: utf8 -*-

import logging
import re

CJK = [
        [0x3000, 0x303f],    # Japanese-style punctuation
        [0x3040, 0x309F],    # Hiragana
        [0x30A0, 0x30FF],    # Katakana
        [0x31F0, 0x31FF],    # Katakana Extension
        [0xFF00, 0xFFEF],    # Half width charactors
        [0x4E00, 0x9FC3]     # Han # Lo [20932] CJK UNIFIED IDEOGRAPH-4E00, CJK UNIFIED IDEOGRAPH-9FC3
    ] 

def build_re():
    L = []
    for i in CJK:
        f, t = i
        try: 
            f = unichr(f)
            t = unichr(t)
            L.append('%s-%s' % (f, t))
        except: 
            pass # A narrow python build, so can't use chars > 65535 without surrogate pairs!


    RES = '[%s]' % ''.join(L)
    # logging.warning('RE: %s', RES.encode('utf-8'))
    return re.compile(RES, re.UNICODE)

RE = build_re()

def hasJP(line):
    u'''
    Check whether there is Japanese charactors in the line

    >>> hasJP('This is a good test')
    False
    >>> hasJP(u'い')
    True
    >>> hasJP(u'This is a いい test')
    True
    >>> hasJP(u'This is a 素晴しい test')
    True
    >>> hasJP(u'This is a 中文 test') #because CJK codecs are shared in UNICODE database, so even Chinese can be recognized.
    True
    >>> hasJP(u'This is a 爱 test') # This word only exists in Simplified Chinese Database, but also recognizable.
    True
    >>> hasJP(u'목란') # This is Korean charactors, not included.
    False
    '''

    return RE.search(line) != None

#logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":

    import doctest
    doctest.testmod()


