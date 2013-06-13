#!/usr/bin/env python
# -*- encoding: utf8 -*-

import codecs
import os.path
import re
import logging

from JPStringExtractor import *

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
    '''
    The function for processing VB frm file's property section like following sample:

         BeginProperty Font 
            Name            =   "ＭＳ ゴシック"
            Size            =   9
            Charset         =   128
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
        
    line:       the input line
    control:    the current control
    propname:   the current property name
    controls:   the generated controls
    ctrlStack:  the stack for control
    '''

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
    return pos, control, propname

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
    
    filetype = os.path.splitext(fname)[1].lower()

    control = None
    controls = [] # it is the result for summary output
    ctrlStack = [] # it is the stack for controls
    propname = u''

    for line in rf:
        if pos == BEFORE_ATTR and line.startswith('Attribute '):
            pos = IN_ATTR
        elif pos == IN_ATTR and not line.startswith('Attribute '):
            pos = AFTER_ATTR
        
        if filetype == '.frm':
            pos, control, propname = procFrm(line, pos, control, propname, controls, ctrlStack)

        yield line, pos, None

    rf.close()
    yield None, None, controls

def genJpsByCtrls(jps, controls, start):
    '''
    analyze the controls info to generate the Japanese strings
    return:
    lines: the generated initialization code for form load
    start: the start index for next process
    '''
    lines = []
    for ctrl in controls:
        for prop in ctrl:
            # 'Name' and 'Type' are not real control's properties
            # 'Font' need to be processed specially
            if prop in ('Name', 'Type', u'Font'): 
                continue

            if type(ctrl[prop]) == dict:
                for propname in ctrl[prop]:
                    if hasJP(ctrl[prop][propname]):
                        jp = {'index': start, 'string': ctrl[prop][propname],
                                'hint': u'control name: {%s}, property name: {%s.%s}, value: {%s}'
                                % (ctrl['Name'], prop, propname, ctrl[prop][propname])}
                        line = u'    %s%s.%s.%s = LoadResString(%d)\r\n' % (ctrl['Name'],
                                #if there is 'Index' property, then it is a member of controller array
                                '('+ctrl['Index'] + ')' if u'Index' in ctrl else '',
                                prop, propname, ctrl[prop][propname])
                        jps.append(jp)
                        lines.append(line)
                        start = start + 1

            elif hasJP(ctrl[prop]):
                jp = {'index': start, 'string': ctrl[prop],
                        'hint': u'control name: {%s}, property name: {%s}, value: {%s}'
                        % (ctrl['Name'], prop, ctrl[prop])}
                line = u'    %s%s.%s = LoadResString(%d)\r\n' % (ctrl['Name'],
                        #if there is 'Index' property, then it is a member of controller array
                        '('+ctrl['Index'] + ')' if u'Index' in ctrl else '',
                        prop, start)
                jps.append(jp)
                lines.append(line)
                start = start + 1

    return lines, start

def analyze(fname, jps, start):
    '''
    analyze the lines of file (fname)
    
    return
    lines: replaced lines and jps container which contains Japanese for generating StringTable
    form_load: the source code in the form load subroutine for updating the controllers' properties.
    jps: the Japanese strings information.
    start: the RC index for the next source file.
    '''
    lines = []
    form_load = [] # the initialization code for update controllers' properties in the form load subroutine
    retVal = {'lines': lines}
    for line, pos, controls in readline(fname):
        if controls != None:
             form_load, start = genJpsByCtrls(jps, controls, start)
             #logging.warning('at last the start is %d', start)
        else:
            if pos != AFTER_ATTR:
                lines.append(line)
            else:
                newjps = extract(line)
                retLine, start = replace(line, newjps, start)
                jps = jps + newjps
                #logging.warning('in vb code start is %d', start)
                lines.append(retLine)
    return lines, form_load, jps, start

