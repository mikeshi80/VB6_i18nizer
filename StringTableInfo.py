#!/usr/bin/env python
# -*- encoding: utf8 -*-

class StringTableInfo(object):
    def __init__(self, string, begin, end, line):
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

