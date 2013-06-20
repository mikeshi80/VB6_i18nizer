#!/usr/bin/env python
# -*- encoding: utf8 -*-

import codecs
import os.path
from FormProcessor import FormProcessor

class SourceScanner(object):
    '''
    Scan the VB source code to gather
    the useful information
    '''
    def __init__(self, stg, processor, encoding = 'cp932'):
        '''
        class contructor

        arguments:
        stg -- StringTableGenerator
        processor -- LineProcessor
        encoding -- The encoding of target files
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
        '''
        process the string line to get the
        processed line, which Japanese strings
        have been replaced by LoadResString
        function

        arguments:
        line -- the input line
        writer -- SourceWriter

        return:
        the processed line
        '''

        infos = self.processor.process(line)
        if len(infos) > 0:
            index = []
            for info in infos:
                index.append(self.stringTableGenerator.putInfo(info))
            line = writer.replace(line, infos, index)
        return line


    def scan(self, fname, writer):
        '''
        scan the file

        open the file named fname, and scan, process
        the contents

        arguments:
        fname -- the name of target file
        writer -- SourceWriter
        '''
        isForm = os.path.splitext(fname)[1].lower() == '.frm'

        if isForm:
            formProc = FormProcessor()

        f = codecs.open(fname, 'r', self.encoding)

        for line in f:
            line = self.processLine(line, writer)
            writer.addLine(line)

            if isForm:
                formProc.process(line)

        if isForm:
            formProc.generateControllerInfo()
            writer.addFormInfo(formProc.formLoad)
        f.close()

