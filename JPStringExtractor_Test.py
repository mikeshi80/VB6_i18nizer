#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from JPStringExtractor import *

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

    def test_extract_4(self):
        r = extract(u'a=b & c')
        self.assertEqual(len(r), 0)

    def test_replace_1(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        r = extract(teststr)
        retline, index = replace(teststr, r, 1001)
        self.assertEqual(retline, u'a = "Hello, " & LoadResString(1001) & LoadResString(1002)')
        self.assertEqual(index, 1003)

    def test_replace_2(self):
        teststr = u'a = "Hello, " & "World" & " People"'
        r = extract(teststr)
        retline, index = replace(teststr, r, 1001)
        self.assertEqual(retline, teststr)
        self.assertEqual(index, 1001)

    def test_export_1(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        r = extract(teststr)
        start = 1001
        lines = []
        export(r, start, lines)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], u'    1001            "世界" //a = "Hello, " & <target>"世界"</target> & "人たち"')
        self.assertEqual(lines[1], u'    1002            "人たち" //a = "Hello, " & "世界" & <target>"人たち"</target>')

    def test_export_2(self):
        teststr = u'a = "Hello, " & "World" & " People"'
        r = extract(teststr)
        start = 1001
        lines = []
        export(r, start, lines)
        self.assertEqual(len(lines), 0)

    def test_genStringTable(self):
        teststr = u'a = "Hello, " & "世界" & "人たち"'
        r = extract(teststr)
        start = 1001
        lines = []
        export(r, start, lines)
        st = genStringTable(lines, 'jp')
        self.assertEqual(st, u'''STRINGTABLE
LANGUAGE 0x11, 0x01
BEGIN
    1001            "世界" //a = "Hello, " & <target>"世界"</target> & "人たち"
    1002            "人たち" //a = "Hello, " & "世界" & <target>"人たち"</target>
END''')
        with self.assertRaises(ValueError) as cm:
            genStringTable(lines, 'fr')
        self.assertEqual(str(cm.exception), 'lang only supports en_us, zh_cn, jp_jp, en, us, zh, cn, jp')

if __name__ == '__main__':
    unittest.main()

