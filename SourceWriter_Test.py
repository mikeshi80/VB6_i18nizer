#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from SourceWriter import SourceWriter
from LineProcessor import LineProcessor
import logging

class SourceWriter_Test(unittest.TestCase):
    def setUp(self):
        self.__writer = SourceWriter('c:/test.txt')
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

    def test_addFormInfo(self):
        self.__writer._SourceWriter__lines = [
                u'A = 1\r\n', u'B = 2\r\n', u'Private Sub Form_Load()\r\n',
                u'C = 1\r\n', u'End Sub\r\n']
        form_load = ['abc = 1', 'cde = 2']
        self.__writer.addFormInfo(form_load)
        #logging.warning(self.__writer._SourceWriter__lines)
        self.assertEqual(len(self.__writer._SourceWriter__lines), 6)
        self.assertEqual(self.__writer._SourceWriter__lines[3], u'abc = 1\r\ncde = 2')


if __name__ == '__main__':
    unittest.main()

