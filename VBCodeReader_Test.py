#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
from VBCodeReader import *

class VBCodeReader_Test(unittest.TestCase):

    def test_procProp_1(self):
        line = u'      BeginProperty Font '
        control = {u'Name':u'Label1', u'Type':u'Label'}
        controls = []
        ctrlStack = []
        propname = u''
        retCtrl, propname = procProp(line, control, propname, controls, ctrlStack)
        self.assertEqual(control[u'Name'], u'Label1')
        self.assertEqual(propname, u'Font')
        self.assertEqual(control[propname], {})

        line = u'         Name            =   "ＭＳ Ｐゴシック"'
        retCtrl, propname = procProp(line, control, propname, controls, ctrlStack)
        self.assertEqual(control[u'Name'], u'Label1')
        self.assertEqual(propname, u'Font')
        self.assertEqual(control[propname], {u'Name':u'"ＭＳ Ｐゴシック"'})
        
    
    def test_procFrm_1(self):

        line = u'VERSION 5.00'
        pos = BEFORE_ATTR
        control = None
        controls = []
        ctrlStack = []
        propname = u''

        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control, None)
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 0)

        line = u'Begin VB.Form Form1 '
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 0)

        line = u'   Caption         =   "Form1"'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 0)

        line = u'   Begin VB.Frame Frame1 '
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Frame1')
        self.assertEqual(control['Type'], u'Frame')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 1)

        line = u'      Width           =   3015'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Frame1')
        self.assertEqual(control['Type'], u'Frame')
        self.assertEqual(control['Width'], u'3015')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 1)

        line = u'      Begin VB.Label Label1 '
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Label1')
        self.assertEqual(control['Type'], u'Label')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 2)
        

        line = u'         TabIndex        =   3'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Label1')
        self.assertEqual(control['Type'], u'Label')
        self.assertEqual(control['TabIndex'], u'3')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 2)

        line = u'      End'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Frame1')
        self.assertEqual(control['Type'], u'Frame')
        self.assertEqual(len(controls), 1)
        self.assertEqual(len(ctrlStack), 1)

        line = u'   End'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(len(controls), 2)
        self.assertEqual(len(ctrlStack), 0)

        line = u'   Begin VB.Label Label2 '
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Label2')
        self.assertEqual(control['Type'], u'Label')
        self.assertEqual(len(controls), 2)
        self.assertEqual(len(ctrlStack), 1)

        line = u'   End'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'BeginProperty Font '
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(control['Font'], {})
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'         Name            =   "ＭＳ Ｐゴシック"'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(control['Font'], {u'Name': u'"ＭＳ Ｐゴシック"'})
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'      EndProperty'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(control['Font'], {u'Name': u'"ＭＳ Ｐゴシック"'})
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'End'
        retLine, retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retLine, line)
        self.assertEqual(retPos, pos)
        self.assertEqual(control, None)
        self.assertEqual(len(controls), 4)
        self.assertEqual(len(ctrlStack), 0)

if __name__ == '__main__':
    unittest.main()
