#!/usr/bin/env python
# -*- encoding: utf8 -*-

import unittest
import codecs
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

        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control, None)
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 0)

        line = u'Begin VB.Form Form1 '
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 0)

        line = u'   Caption         =   "Form1"'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 0)

        line = u'   Begin VB.Frame Frame1 '
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Frame1')
        self.assertEqual(control['Type'], u'Frame')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 1)

        line = u'      Width           =   3015'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Frame1')
        self.assertEqual(control['Type'], u'Frame')
        self.assertEqual(control['Width'], u'3015')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 1)

        line = u'      Begin VB.Label Label1 '
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Label1')
        self.assertEqual(control['Type'], u'Label')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 2)
        

        line = u'         TabIndex        =   3'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Label1')
        self.assertEqual(control['Type'], u'Label')
        self.assertEqual(control['TabIndex'], u'3')
        self.assertEqual(len(controls), 0)
        self.assertEqual(len(ctrlStack), 2)

        line = u'      End'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Frame1')
        self.assertEqual(control['Type'], u'Frame')
        self.assertEqual(len(controls), 1)
        self.assertEqual(len(ctrlStack), 1)

        line = u'   End'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(len(controls), 2)
        self.assertEqual(len(ctrlStack), 0)

        line = u'   Begin VB.Label Label2 '
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Label2')
        self.assertEqual(control['Type'], u'Label')
        self.assertEqual(len(controls), 2)
        self.assertEqual(len(ctrlStack), 1)

        line = u'   End'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'BeginProperty Font '
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(control['Font'], {})
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'         Name            =   "ＭＳ Ｐゴシック"'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(control['Font'], {u'Name': u'"ＭＳ Ｐゴシック"'})
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'      EndProperty'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control['Name'], u'Form1')
        self.assertEqual(control['Type'], u'Form')
        self.assertEqual(control['Caption'], u'"Form1"')
        self.assertEqual(control['Font'], {u'Name': u'"ＭＳ Ｐゴシック"'})
        self.assertEqual(len(controls), 3)
        self.assertEqual(len(ctrlStack), 0)

        line = u'End'
        retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(retPos, pos)
        self.assertEqual(control, None)
        self.assertEqual(len(controls), 4)
        self.assertEqual(len(ctrlStack), 0)

    def test_procFrm_2(self):
        testdata = codecs.open('test/vbtest/test01.TXT', 'r', 'cp932')
        pos = BEFORE_ATTR
        control = None
        controls = []
        ctrlStack = []
        propname = u''

        for line in testdata:
            retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 

        self.assertEqual(control, None)
        self.assertEqual(propname, u'')
        self.assertEqual(retPos, BEFORE_ATTR)
        self.assertEqual(len(controls), 5)
        self.assertEqual(ctrlStack, [])

        self.assertEqual(controls[0]['Name'], u'Label1')
        self.assertEqual(controls[0]['Caption'], u'"ラベル３"')
        self.assertEqual(controls[0]['Index'], u'1')

        testdata.close()


    def test_genJpsByCtrls_1(self):
        pos = BEFORE_ATTR
        control = None
        controls = []
        ctrlStack = []
        propname = u''
        testdata = codecs.open('test/vbtest/test01.TXT', 'r', 'cp932')

        for line in testdata:
            retPos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack) 
        testdata.close()

        jps = []
        start = 1001
        
        lines, index = genJpsByCtrls(jps, controls, start)

        self.assertEqual(index, 1005)
        self.assertEqual(lines[0], u'    Label1(1).Caption = LoadResString(1001)')
        self.assertEqual(jps[0]['string'], u'"ラベル３"')
        self.assertEqual(lines[1], u'    Frame1.Caption = LoadResString(1002)')
        self.assertEqual(jps[1]['string'], u'"フレーム１"')
        self.assertEqual(lines[2], u'    Label2.Caption = LoadResString(1003)')
        self.assertEqual(jps[2]['string'], u'"ラベル２"')
        self.assertEqual(lines[3], u'    Label1(0).Caption = LoadResString(1004)')
        self.assertEqual(jps[3]['string'], u'"ラベル１"')

    def test_analyze(self):
        fname = 'test/vbtest/vbtest_with_load/Form1.frm'
        jps = []
        start = 1001

        lines, form_load, jps, index = analyze(fname, jps, start)

        self.assertEqual(len(jps), 7)
        



if __name__ == '__main__':
    unittest.main()
