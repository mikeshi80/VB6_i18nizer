#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import StringTableInfo

class StringTableInfo_Test(unittest.TestCase):
    def test_NewStringTableInfo(self):
        sti = StringTableInfo.StringTableInfo('hello', 5, 10, 'yeah hello world')
        self.assertEqual(sti.string, 'hello')
        self.assertEqual(sti.begin, 5)
        self.assertEqual(sti.end, 10)
        self.assertEqual(sti.line, 'yeah hello world')

if __name__ == '__main__':
    unittest.main()
