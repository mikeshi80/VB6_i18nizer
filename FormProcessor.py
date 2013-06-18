#!/usr/bin/env python
# -*- encoding: utf8 -*-

import re

class FormProcessor(object):
    '''
    the processor for processing the controllers information
    in the frm files
    '''

    PCTRL = re.compile(r'\s*Begin VB\.(\w+) (\w+)\s*') # the pattern for VB Control definition line in frm file.
    PPROP = re.compile(r'\s*(\w+)\s*=\s*("[^"]+"|\d+)(?:\'.*)?') # the pattern for VB Control Properties definition line
    PBPROP = re.compile(r'\s*BeginProperty\s+(\w+)\s*')

    BEFORE_ATTR = 1
    IN_ATTR = 2
    AFTER_ATTR = 3

    def __init__(self):
        self.__ctrls = []
        self.__ctrl = None
        self.__ctrlStack = []
        self.__pos = FormProcessor.BEFORE_ATTR
        self.__propname = ''

    def procProp(self, line):
        '''
        process the cascaded property informatin, which begins
        with 'BeginProperty'

        arguments:
        line -- the target line
        '''
        if (len(self.__propname) > 0):
            mo = FormProcessor.PPROP.match(line)
            if mo == None:
                if line.strip() == u'EndProperty':
                    self.__propname = u''
            else:
                #logging.warning(u'control[%s][%s] = %s', propname, mo.group(1), mo.group(2))
                self.__ctrl[self.__propname][mo.group(1)] = mo.group(2)
        else:
            if line.strip() == 'End':
                self.__ctrls.append(self.__ctrl)
                if len(self.__ctrlStack) > 0:
                    self.__ctrl = self.__ctrlStack.pop()
                else:
                    self.__ctrl = None
            else:
                mo = FormProcessor.PPROP.match(line) # match control property 'Caption = "Form1"'
                if mo != None:
                    self.__ctrl[mo.group(1)] = mo.group(2)
                else:
                    mo = FormProcessor.PBPROP.match(line) # match control cascade property 'BeginProperty Font'
                    if mo != None:
                        self.__propname = mo.group(1)
                        self.__ctrl[self.__propname] = {}


    def process(self, line):
        '''
        process the frm files, and gather the controllers informations

        arguments:
        line -- the target line
        '''
        if self.__pos == FormProcessor.BEFORE_ATTR:
            mo = FormProcessor.PCTRL.match(line) # match control definition begin "Begin VB.TYPE NAME"
            if mo == None: # not matched
                if self.__ctrl != None:
                    self.procProp(line)
            else:
                if self.__ctrl != None:
                    self.__ctrlStack.append(self.__ctrl) # save the out level control

                self.__ctrl = {'Type': mo.group(1), 'Name': mo.group(2)}

