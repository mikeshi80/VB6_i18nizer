#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import StringTableInfo
import StringTableGenerator

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

if __name__ == '__main__':
    unittest.main()
