#!/usr/bin/env python
# -*- encoding: utf8 -*-

class StringTableGenerator(object):
    def __init__(self, start):
        self.__strtbl = {}
        self.__current = start

    @property
    def index(self):
        return self.__current

    def getInfo(self, index):
        if index in self.__strtbl:
            return self.__strtbl[index]
        else:
            raise IndexError()

    def putInfo(self, info):
        self.__strtbl[self.__current] = info
        retVal = self.__current
        self.__current = self.__current + 1
        return retVal

    def genHint(self, info, begin = '<target>', end = '</target>'):
        if len(info.line) > 0:
            return info.line[:info.begin] + begin + info.line[info.begin:info.end] + end + info.line[info.end:]
        else:
            return ''

    def generate(self, lang):
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

        lines = []
        for info in self.__strtbl:
            hint = self.genHint(info)
            comment = ' //' + hint if len(hint) > 0 else ''
            lines.append(' ' * 4 + str(info.index) + ' ' * 12 + '"' + info.string + '"' + comment )

        return u'''STRINGTABLE\r
    LANGUAGE %s, %s\r
    BEGIN\r
    %s\r
    END\r
    ''' % (prim, sub, u'\r\n'.join(lines))


