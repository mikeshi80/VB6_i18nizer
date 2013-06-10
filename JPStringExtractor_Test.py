#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from JPStringExtractor import extract, replace

class JPStringExtractor_Test(unittest.TestCase):

    def test_extract_1(self):
        r = extract(u'a = "Hello, " & "世界" & "人たち"')
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['string'], u'世界')
        self.assertEqual(r[0]['start'], 16)
        self.assertEqual(r[0]['end'], 20)
        self.assertEqual(r[1]['string'], u'人たち')
        self.assertEqual(r[1]['start'], 23)
        self.assertEqual(r[1]['end'], 28)

    def test_extract_2(self):
        r = extract(u'a = "Hello, " & "世界" & "人たち" & SomeElse')
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['string'], u'世界')
        self.assertEqual(r[0]['start'], 16)
        self.assertEqual(r[0]['end'], 20)
        self.assertEqual(r[1]['string'], u'人たち')
        self.assertEqual(r[1]['start'], 23)
        self.assertEqual(r[1]['end'], 28)

    def test_extract_3(self):
        r = extract(u'a="hello, world" & "no japanese word"')
        self.assertEqual(len(r), 0)

    def test_replace_1(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        r = extract(teststr)
        retline, rjp, start, index = replace(teststr, r, 1001)
        self.assertEqual(rjp, r)
        self.assertEqual(retline, u'a = "Hello, " & LoadResString(1001) & LoadResString(1002)')
        self.assertEqual(start, 1001)
        self.assertEqual(index, 1003)


if __name__ == '__main__':
    unittest.main()

