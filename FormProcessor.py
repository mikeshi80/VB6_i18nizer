#!/usr/bin/env python
# -*- encoding: utf8 -*-

import re
from StringTableInfo import StringTableInfo
from JPChecker import hasJP
from BaseProcessor import BaseProcessor

class FormProcessor(BaseProcessor):
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

    def __init__(self, stg):
        '''
        class contructor
        
        arguments:
        stg -- StringTableGenerator
        '''
        self.__ctrls = []
        self.__ctrl = None
        self.__ctrlStack = []
        self.__pos = FormProcessor.BEFORE_ATTR
        self.__propname = ''
        self.__form_load = []
        self.__stg = stg

    @property
    def formLoad(self):
        return self.__form_load;

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

        return:
        the current position in the frm file
        '''

        line = self.removeComments(line)
        if self.__pos == FormProcessor.BEFORE_ATTR and line.startswith('Attribute '):
            self.__pos = FormProcessor.IN_ATTR
        elif self.__pos == FormProcessor.IN_ATTR and not line.startswith('Attribute '):
            self.__pos = FormProcessor.AFTER_ATTR

        if self.__pos == FormProcessor.BEFORE_ATTR:
            mo = FormProcessor.PCTRL.match(line) # match control definition begin "Begin VB.TYPE NAME"
            if mo == None: # not matched
                if self.__ctrl != None:
                    self.procProp(line)
            else:
                if self.__ctrl != None:
                    self.__ctrlStack.append(self.__ctrl) # save the out level control

                self.__ctrl = {'Type': mo.group(1), 'Name': mo.group(2)}
        return self.__pos

    
    def generateControllerInfo(self):
        '''
        analyze the controls info to generate the Japanese strings
        return:
        lines: the generated initialization code for form load
        start: the start index for next process
        '''
        lines = []
        for ctrl in self.__ctrls:

            lines.append('    %s%s.Font.Name = LoadResString(%d)' % (ctrl['Name'],
                    #if there is 'Index' property, then it is a member of controller array
                    '('+ctrl['Index'] + ')' if u'Index' in ctrl else '', self.__stg.index))
            info = StringTableInfo(u'ＭＳ ゴシック', None, None, '%s%s.Font.Name' % (ctrl['Name'],
                '('+ctrl['Index'] + ')' if u'Index' in ctrl else ''))

            self.__stg.putInfo(info)

            lines.append('    %s%s.Font.Charset = LoadResString(%d)' % (ctrl['Name'],
                    #if there is 'Index' property, then it is a member of controller array
                    '('+ctrl['Index'] + ')' if u'Index' in ctrl else '', self.__stg.index))
            info = StringTableInfo('128', None, None, '%s%s.Font.Charset: 128 for JP, 134 for CN' % (ctrl['Name'],
                '('+ctrl['Index'] + ')' if u'Index' in ctrl else ''))
            self.__stg.putInfo(info)


            for prop in ctrl:
                # 'Name' and 'Type' are not real control's properties
                # 'Font' need to be processed specially
                if prop in ('Name', 'Type', u'Font'): 
                    continue

                if type(ctrl[prop]) == dict:
                    for propname in ctrl[prop]:
                        if hasJP(ctrl[prop][propname]):
                            info = StringTableInfo(ctrl[prop][propname][1:-1], None, None, u'%s.%s.%s = "%s"'
                                % (ctrl['Name'], prop, propname, ctrl[prop][propname][1:-1]))
                            line = u'    %s%s.%s.%s = LoadResString(%d)' % (ctrl['Name'],
                                    #if there is 'Index' property, then it is a member of controller array
                                    '('+ctrl['Index'] + ')' if u'Index' in ctrl else '',
                                    prop, propname, self.__stg.index)
                            self.__stg.putInfo(info)
                            lines.append(line)

                elif hasJP(ctrl[prop]):
                    info = StringTableInfo(ctrl[prop][1:-1], None, None, u'%s%s.%s = %s'
                            % (ctrl['Name'], '('+ctrl['Index'] + ')' if u'Index' in ctrl else '',
                            prop, ctrl[prop][1:-1]) )
                    line = u'    %s%s.%s = LoadResString(%d)' % (ctrl['Name'],
                            #if there is 'Index' property, then it is a member of controller array
                            '('+ctrl['Index'] + ')' if u'Index' in ctrl else '',
                            prop, self.__stg.index)
                    self.__stg.putInfo(info)
                    lines.append(line)

            lines.append('\r\n')

        self.__form_load = lines

