#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import filecmp
import os
from SourceScanner import SourceScanner
from SourceWriter import SourceWriter
from StringTableGenerator import StringTableGenerator
from LineProcessor import LineProcessor

class SourceScanner_Test(unittest.TestCase):
    def setUp(self):
        self.__stg = StringTableGenerator(1001)
        self.__processor = LineProcessor()
        self.__scanner = SourceScanner(self.__stg, self.__processor)

    def test_processLine(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        writer = SourceWriter('c:/test.txt')
        retline = self.__scanner.processLine(teststr, writer)
        self.assertEqual(retline, u'a = "Hello, " & LoadResString(1001) & LoadResString(1002)')

    def test_scan_1(self):
        fname = 'test/vbtest/vbtest_with_load/Form1.frm'
        writer = SourceWriter(fname)
        self.__scanner.scan(fname, writer)
        writer.write(True)
        try:
            result = 'test/vbtest/results/vbtest_with_load/Form1.frm'
            self.assertTrue(filecmp.cmp(result, fname+ '.test'))
        except:
            raise
        finally:
           os.remove(fname+'.test')

    def test_scan_2(self):
        fname = 'test/vbtest/vbtest_without_load/Form1.frm'
        writer = SourceWriter(fname)
        self.__scanner.scan(fname, writer)
        writer.write(True)
        try:
            result = 'test/vbtest/results/vbtest_without_load/Form1.frm'
            self.assertTrue(filecmp.cmp(result, fname+ '.test'))
        except:
            raise
        finally:
           os.remove(fname+'.test')
        



if __name__ == '__main__':
    unittest.main()
