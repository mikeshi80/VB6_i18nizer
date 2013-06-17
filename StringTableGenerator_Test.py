#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import StringTableInfo
import StringTableGenerator

class StringTableGenerator_Test(unittest.TestCase):
    def setUp(self):
        self.generator = StringTableGenerator.StringTableGenerator(1001)

    def testNewStringTableGenerator(self):
        self.assertEqual(self.generator.index, 1001)
        sti = StringTableInfo.StringTableInfo('hello', 5, 'yeah hello world')
        index = self.generator.putInfo(sti)
        self.assertEqual(index, 1001)
        self.assertEqual(self.generator.index, 1002)
        self.assertEqual(self.generator.getInfo(1001), sti)
        with self.assertRaises(IndexError):
            self.generator.getInfo(1002)


if __name__ == '__main__':
    unittest.main()
