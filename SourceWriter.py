#!/usr/bin/env python
# -*- encoding: utf8 -*-

class SourceWriter(object):
    '''
    The writer to write the processed source code
    '''
    def __init__(self):
        self.__lines = []

    def replace(self, line, infos, index):
        '''
        replace the line's japanese strings with
        LoadResString function

        arguments:
        line -- the target line
        infos -- the StringTableInfo array
        index -- the index array

        return:
        the processed line, now the Japanese strings
        are replaced with LoadResString function.
        '''
        if len(infos) == 0:
            return line

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

    def addLine(self, line):
        '''
        store the processed line for generating the source code

        arguments:
        line -- the processed line
        '''
        self.__lines.append(line)

