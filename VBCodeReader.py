#!/usr/bin/env python
# -*- encoding: utf8 -*-

import codecs
import os.path
import re
import logging

encoding = 'cp932'

BEFORE_ATTR = 1
IN_ATTR = 2
AFTER_ATTR = 3


PCTRL = re.compile(r'\s*Begin VB\.(\w+) (\w+)\s*') # the pattern for VB Control definition line in frm file.
PPROP = re.compile(r'\s*(\w+)\s*=\s*("[^"]+"|\d+)(?:\'.*)?') # the pattern for VB Control Properties definition line
PBPROP = re.compile(r'\s*BeginProperty\s+(\w+)\s*')

def procCtrl(line, control):
    pass

def procProp(line, control, propname, controls, ctrlStack):
    if (len(propname) > 0):
        mo = PPROP.match(line)
        if mo == None:
            if line.strip() == u'EndProperty':
                propname = u''
        else:
            #logging.warning(u'control[%s][%s] = %s', propname, mo.group(1), mo.group(2))
            control[propname][mo.group(1)] = mo.group(2)
    else:
        if line.strip() == 'End':
            controls.append(control)
            if len(ctrlStack) > 0:
                control = ctrlStack.pop()
            else:
                control = None
        else:
            mo = PPROP.match(line) # match control property 'Caption = "Form1"'
            if mo != None:
                control[mo.group(1)] = mo.group(2)
            else:
                mo = PBPROP.match(line) # match control cascade property 'BeginProperty Font'
                if mo != None:
                    propname = mo.group(1)
                    control[propname] = {}

    return control, propname


def procFrm(line, pos, control, propname, controls, ctrlStack):
    '''
    The special function to process frm file, generate the controllers info
    The controllers info is for adding corresponding actions in Form_Load subroute
    '''

    if pos == BEFORE_ATTR:
        mo = PCTRL.match(line) # match control definition begin "Begin VB.TYPE NAME"
        if mo == None: # not matched
            if control != None:
                control, propname = procProp(line, control, propname, controls, ctrlStack)
        else:
            if control != None:
                ctrlStack.append(control) # save the out level control

            control = {'Type': mo.group(1), 'Name': mo.group(2)}
    return line, pos, control, propname

def readline(fname):
    '''
    read the line from the fname

    fname is the file name to read

    return value is a tuple

    (line, pos, controls)

    line: The current line
    pos: before, in or after attribute
    controls: if controls is not None, this line is just summary output

    '''
    try:
        rf = codecs.open(fname, 'r', encoding)
    except:
        logging.error('the file %s cannot be open', fname)
        raise StopIteration('file can not open')

    pos = BEFORE_ATTR
    
    filetype = os.path.splitext(fname).lower()

    control = None
    controls = [] # it is the result for summary output
    ctrlStack = [] # it is the stack for controls
    propname = u''

    for line in f:
        if pos == BEFORE_ATTR and line.startswith('Attribute '):
            pos = IN_ATTR
        elif pos == IN_ATTR and not line.startswith('Attribute '):
            pos = AFTER_ATTR
        
        if filetype == '.frm':
            line, pos, control = procFrm(line, pos, control, propname, controls, ctrlStack)

        yield line, pos, None

    f.close()
    yield None, None, controls


