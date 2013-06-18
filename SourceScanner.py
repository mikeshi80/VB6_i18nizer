#!/usr/bin/env python
# -*- encoding: utf8 -*-

import codecs

class SourceScanner(object):
    def __init__(self, stg, processor, encoding = 'cp932'):
        '''
        stg StringTableGenerator
        '''
        self.__stg = stg
        self.__processor = processor
        self.__encoding = encoding
    
    @property
    def stringTableGenerator(self):
        return self.__stg

    @property
    def encoding(self):
        return self.__encoding

    @property
    def processor(self):
        return self.__processor

    def processLine(self, line, writer):
        infos = self.processor.process(line)
        if len(infos) > 0:
            index = []
            for info in infos:
                index.append(self.stringTableGenerator.putInfo(info))
            line = writer.replace(line, infos, index)
        return line


    def scan(self, fname, writer):
        f = codecs.open(fname, 'r', self.encoding)

        for line in f:
            line = self.processLine(line, writer)
            writer.addLine(line)

        f.close()

