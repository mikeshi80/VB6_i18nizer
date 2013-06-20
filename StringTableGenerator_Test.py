#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import StringTableInfo
import StringTableGenerator
import logging
from LineProcessor import LineProcessor

class StringTableGenerator_Test(unittest.TestCase):
    def setUp(self):
        self.generator = StringTableGenerator.StringTableGenerator(1001)

    def test_NewStringTableGenerator(self):
        self.assertEqual(self.generator.index, 1001)
        sti = StringTableInfo.StringTableInfo('hello', 5, 10, 'yeah hello world')
        index = self.generator.putInfo(sti)
        self.assertEqual(index, 1001)
        self.assertEqual(self.generator.index, 1002)
        self.assertEqual(self.generator.getInfo(1001), sti)
        with self.assertRaises(IndexError):
            self.generator.getInfo(1002)

    def test_genHint(self):
        sti = StringTableInfo.StringTableInfo('hello', 5, 10, 'yeah hello world')
        self.assertEqual(self.generator.genHint(sti), 'yeah <target>hello</target> world')

    def test_generate(self):
        proc = LineProcessor()

        teststr = u'a = "Hello, " & "世界" & "人たち"'
        infos = proc.process(teststr)
        #logging.warning(infos)
        for info in infos:
            self.generator.putInfo(info)

        st = self.generator.generate('jp')
        self.assertEqual(st, u'''STRINGTABLE\r
LANGUAGE 0x11, 0x01\r
BEGIN\r
    1001            "世界" //a = "Hello, " & <target>"世界"</target> & "人たち"\r
    1002            "人たち" //a = "Hello, " & "世界" & <target>"人たち"</target>\r
END\r
''')


if __name__ == '__main__':
    unittest.main()
