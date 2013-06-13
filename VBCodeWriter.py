#!/usr/bin/env python
# -*- encoding: utf8 -*-
import codecs
import os.path
import logging


def writeSource(fname, lines, form_load, forTest = False):

    ns = os.path.split(fname)
    wf = codecs.open(os.path.join(ns[0], ('fortest_' if forTest else '') + ns[1]), 'w', 'cp932')
    #logging.warning('file name is %s', wf.name)


    if len(form_load) == 0:
        wf.writelines(lines)
    else:
        hasForm_Load = False
        for line in lines:
            wf.write(line)
            if line.startswith(u'Private Sub Form_Load()'):
                wf.writelines('\r\n'.join(form_load))
                hasForm_Load = True

        if not hasForm_Load:
            wf.write('\r\nPrivate Sub Form_Load()\r\n')
            wf.writelines('\r\n'.join(form_load))
            wf.write('\r\nEnd Sub\r\n')

    wf.close()



