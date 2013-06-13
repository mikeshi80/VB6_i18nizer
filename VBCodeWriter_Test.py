#!/usr/bin/env python
# -*- encoding: utf8 -*-
import unittest

from VBCodeWriter import *
from VBCodeReader import *
import filecmp
import os

class VBCodeWriter_Test(unittest.TestCase):

    def test_writeSource_1(self):

        fname = 'test/vbtest/vbtest_with_load/Form1.frm'
        jps = []
        start = 1001

        lines, form_load, jps, index = analyze(fname, jps, start)
        writeSource(fname, lines, form_load, True)

        result = 'test/vbtest/results/vbtest_with_load/Form1.frm'
        generated = 'test/vbtest/vbtest_with_load/fortest_Form1.frm'
        
        try:
            self.assertTrue(filecmp.cmp(result, generated))
        except:
            raise
        finally:
            os.remove(generated)

    def test_writeSource_2(self):

        fname = 'test/vbtest/vbtest_with_load/Module1.bas'
        jps = []
        start = 1001

        lines, form_load, jps, index = analyze(fname, jps, start)
        writeSource(fname, lines, form_load, True)

        result = 'test/vbtest/results/vbtest_with_load/Module1.bas'
        generated = 'test/vbtest/vbtest_with_load/fortest_Module1.bas'

        try:
            self.assertTrue(filecmp.cmp(result, generated))
        except:
            raise
        finally:
            os.remove(generated)

    def test_writeSource_3(self):

        fname = 'test/vbtest/vbtest_with_load/People.cls'
        jps = []
        start = 1001

        lines, form_load, jps, index = analyze(fname, jps, start)
        writeSource(fname, lines, form_load, True)

        result = 'test/vbtest/results/vbtest_with_load/People.cls'
        generated = 'test/vbtest/vbtest_with_load/fortest_People.cls'

        try:
            self.assertTrue(filecmp.cmp(result, generated))
        except:
            raise
        finally:
            os.remove(generated)

    def test_writeSource_4(self):

        fname = 'test/vbtest/vbtest_without_load/Form1.frm'
        jps = []
        start = 1001

        lines, form_load, jps, index = analyze(fname, jps, start)
        writeSource(fname, lines, form_load, True)

        result = 'test/vbtest/results/vbtest_without_load/Form1.frm'
        generated = 'test/vbtest/vbtest_without_load/fortest_Form1.frm'
        
        try:
            self.assertTrue(filecmp.cmp(result, generated))
        except:
            raise
        finally:
            os.remove(generated)


if __name__ == '__main__':
    unittest.main()
