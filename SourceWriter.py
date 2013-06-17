#!/usr/bin/env python
# -*- encoding: utf8 -*-

class SourceWriter(object):
    def __init__(self):
        pass

    def replace(self, infos, index):
        if len(infos) == 0:
            return ''

        line = infos[0].string
        retVal = u''
        last = 0

        i = 0
        for info in infos:
            retVal = retVal + line[last:info.begin] + 'LoadResString(' + str(index[i]) + ')'
            i = i + 1
            last = info.end

        if last == 0:
            retVal = line
        else:
            retVal = retVal + line[last:]

        return retVal

