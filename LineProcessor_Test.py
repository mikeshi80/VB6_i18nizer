#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import LineProcessor

class LineProcessor_Test(unittest.TestCase):
    def setUp(self):
        self.__processor = LineProcessor.LineProcessor()

    def test_removeComments(self):

        self.assertEqual(self.__processor.removeComments('"this"'), '"this"')
        self.assertEqual(self.__processor.removeComments('\''), '')
        self.assertEqual(self.__processor.removeComments('\' this is the comments'), '')
        self.assertEqual(self.__processor.removeComments('this is "a test"'), 'this is "a test"')
        self.assertEqual(self.__processor.removeComments('this is "a \'test"'), 'this is "a \'test"')
        self.assertEqual(self.__processor.removeComments('"this \'is a" test, \' come on, "test it \'comments", \'yes ppg'), '"this \'is a" test, ')
        self.assertEqual(self.__processor.removeComments('this is \'test\'"Hello world"'), 'this is ')
        self.assertEqual(self.__processor.removeComments(u'this is "テスト"'), u'this is "テスト"')
        self.assertEqual(self.__processor.removeComments(u'this is\' "テスト"'), u'this is')
        self.assertEqual(self.__processor.removeComments('this is "the" test'), 'this is "the" test')

    def test_process_1(self):
        infos = self.__processor.process(u'a = "Hello, " & "世界" & "人たち"')
        self.assertEqual(len(infos), 2)
        self.assertEqual(infos[0].string, u'世界')
        self.assertEqual(infos[0].begin, 16)
        self.assertEqual(infos[0].end, 20)
        self.assertEqual(infos[1].string,  u'人たち')
        self.assertEqual(infos[1].begin, 23)
        self.assertEqual(infos[1].end, 28)

    def test_process_2(self):
        infos = self.__processor.process(u'a = "Hello, " & "世界" & "人たち" & SomeElse')
        self.assertEqual(len(infos), 2)
        self.assertEqual(infos[0].string, u'世界')
        self.assertEqual(infos[0].begin, 16)
        self.assertEqual(infos[0].end, 20)
        self.assertEqual(infos[1].string,  u'人たち')
        self.assertEqual(infos[1].begin, 23)
        self.assertEqual(infos[1].end, 28)

    def test_process_3(self):
        infos = self.__processor.process(u'a="hello, world" & "no japanese word"')
        self.assertEqual(len(infos), 0)

    def test_process_4(self):
        infos = self.__processor.process(u'a=b &c')
        self.assertEqual(len(infos), 0)


if __name__ == '__main__':
    unittest.main()

