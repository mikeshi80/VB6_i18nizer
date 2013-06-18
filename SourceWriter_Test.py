#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from SourceWriter import SourceWriter
from LineProcessor import LineProcessor

class SourceWriter_Test(unittest.TestCase):
    def setUp(self):
        self.__writer = SourceWriter()
        self.__processor = LineProcessor()

    def test_replace_1(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        infos = self.__processor.process(teststr)
        index = (1001, 1002)
        retline = self.__writer.replace(teststr, infos, index)
        self.assertEqual(retline, u'a = "Hello, " & LoadResString(1001) & LoadResString(1002)')

    def test_replace_2(self):
        teststr = u'a = "Hello, " & "World" & " People"'
        infos = self.__processor.process(teststr)
        index = ()
        retline = self.__writer.replace(teststr, infos, index)
        self.assertEqual(retline, teststr)

if __name__ == '__main__':
    unittest.main()

