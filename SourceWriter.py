#!/usr/bin/env python
# -*- encoding: utf8 -*-

import codecs

class SourceWriter(object):
    '''
    The writer to write the processed source code
    '''
    def __init__(self, fname, encoding='cp932'):
        self.__lines = []
        self.__fname = fname
        self.__encoding = encoding

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        self.__encoding = value

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

    def addFormInfo(self, form_load):
        '''
        merge the form load source code
        '''
        if len(form_load) > 0:
            form_load_line = -1
            i = 0
            for line in self.__lines:
                i += 1
                if line.startswith(u'Private Sub Form_Load()'):
                    form_load_line = i
                    break

            if form_load_line == -1:
                self.__lines += [u'\r\nPrivate Sub Form_Load()\r\n', u'\r\n'.join(form_load), u'\r\nEnd Sub\r\n']
            else:
                self.__lines.insert(form_load_line, u'\r\n'.join(form_load))

    def write(self, test=False):
        f = codecs.open(self.__fname + ('.test' if test else ''), 'w', self.encoding)
        f.writelines(self.__lines)
        f.close()

