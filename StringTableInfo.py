#!/usr/bin/env python
# -*- encoding: utf8 -*-

class StringTableInfo(object):
    '''
    the class to store the information for 
    generating StringTable
    '''
    def __init__(self, string, begin, end, line):
        '''
        the constructor of the class
        
        arguments:
        string -- the Japanese string which needs to be replaced
        begin -- the begin position of the string in the target line
        end -- the end position of the string in the target line
        line -- the target line
        '''
        self.__string = string
        self.__begin = begin
        self.__end = end
        self.__line = line

    @property
    def string(self):
        return self.__string

    @property
    def begin(self):
        return self.__begin

    @property
    def end(self):
        return self.__end

    @property
    def line(self):
        return self.__line

