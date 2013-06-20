#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from SourceScanner import SourceScanner
from SourceWriter import SourceWriter
from StringTableGenerator import StringTableGenerator
from LineProcessor import LineProcessor

class SourceScanner_Test(unittest.TestCase):
    def setUp(self):
        self.__stg = StringTableGenerator(1001)
        self.__processor = LineProcessor()
        self.__scanner = SourceScanner(self.__stg, self.__processor)
        self.__writer = SourceWriter('c:/test.txt')

    def test_processLine(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        retline = self.__scanner.processLine(teststr, self.__writer)
        self.assertEqual(retline, u'a = "Hello, " & LoadResString(1001) & LoadResString(1002)')


if __name__ == '__main__':
    unittest.main()
