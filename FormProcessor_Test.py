#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from FormProcessor import FormProcessor

class FormProcessor_Test(unittest.TestCase):
    def setUp(self):
        self.__processor = FormProcessor()

    def test_procProp(self):
        line = u'      BeginProperty Font '
        self.__processor._FormProcessor__ctrl = {u'Name':u'Label1', u'Type':u'Label'}
        self.__processor.procProp(line)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Label1')
        self.assertEqual(self.__processor._FormProcessor__propname, u'Font')
        self.assertEqual(self.__processor._FormProcessor__ctrl[self.__processor._FormProcessor__propname], {})

        line = u'         Name            =   "ＭＳ Ｐゴシック"'
        self.__processor.procProp(line)
        self.assertEqual(self.__processor._FormProcessor__ctrl[u'Name'], u'Label1')
        self.assertEqual(self.__processor._FormProcessor__propname, u'Font')
        self.assertEqual(self.__processor._FormProcessor__ctrl[self.__processor._FormProcessor__propname], {u'Name':u'"ＭＳ Ｐゴシック"'})

    def test_process(self):
        line = u'VERSION 5.00'
        self.__processor._FormProcessor__pos = FormProcessor.BEFORE_ATTR

        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl, None)
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)

        line = u'Begin VB.Form Form1 '
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)

        line = u'   Caption         =   "Form1"'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Caption'], u'"Form1"')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)

        line = u'   Begin VB.Frame Frame1 '
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Frame1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Frame')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 1)

        line = u'      Width           =   3015'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Frame1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Frame')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Width'], u'3015')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 1)

        line = u'      Begin VB.Label Label1 '
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Label1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Label')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 2)


        line = u'         TabIndex        =   3'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Label1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Label')
        self.assertEqual(self.__processor._FormProcessor__ctrl['TabIndex'], u'3')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 0)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 2)

        line = u'      End'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Frame1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Frame')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 1)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 1)

        line = u'   End'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Caption'], u'"Form1"')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 2)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)


        line = u'   Begin VB.Label Label2 '
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Label2')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Label')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 2)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 1)


        line = u'   End'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Caption'], u'"Form1"')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 3)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)


        line = u'BeginProperty Font '
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Caption'], u'"Form1"')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Font'], {})
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 3)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)


        line = u'         Name            =   "ＭＳ Ｐゴシック"'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Caption'], u'"Form1"')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Font'], {u'Name': u'"ＭＳ Ｐゴシック"'})
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 3)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)


        line = u'      EndProperty'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl['Name'], u'Form1')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Type'], u'Form')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Caption'], u'"Form1"')
        self.assertEqual(self.__processor._FormProcessor__ctrl['Font'], {u'Name': u'"ＭＳ Ｐゴシック"'})
        self.assertEqual(self.__processor._FormProcessor__propname, u'')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 3)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)


        line = u'End'
        self.__processor.process(line)

        self.assertEqual(self.__processor._FormProcessor__pos, FormProcessor.BEFORE_ATTR)
        self.assertEqual(self.__processor._FormProcessor__ctrl, None)
        self.assertEqual(self.__processor._FormProcessor__propname, u'')
        self.assertEqual(len(self.__processor._FormProcessor__ctrls), 4)
        self.assertEqual(len(self.__processor._FormProcessor__ctrlStack), 0)

        
if __name__ == '__main__':
    unittest.main()
