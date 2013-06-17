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

