#!/usr/bin/env python
# -*- encoding: utf8 -*-
import unittest
from BaseProcessor import BaseProcessor

class BaseProcessor_Test(unittest.TestCase):
    def setUp(self):
        self.__processor = BaseProcessor()

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

if __name__ == '__main__':
    unittest.main()
