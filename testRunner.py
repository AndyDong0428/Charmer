'''
Created on 2013-11-22

@author: dongmingchang
'''

from optparse import OptionParser

import sys
import Global

from datetime import * 
import time
import os
import shutil

from framework import (
                       Runner, DumpInfo, XmlParser
                       )

if __name__ == '__main__':
   
    # Variable declare
    Options = None
    
    parser = OptionParser()
    parser.add_option("-d", "--id", dest="case",
                      help="Assign case ID to execute", metavar="[Case ID]")
    parser.add_option("-f", "--file", dest="file",
                      help="Assign case list file", metavar="[file name]")
    parser.add_option("-c", "--clean", action="store_false", dest="clean",
                      help="Enable clean flag")
    parser.add_option("-m", "--manual", action="store_false", dest="manual",
                      help="manual execute")
    parser.add_option("-p", "--plan", dest="plan", 
                      help="Execute cases by plan", metavar="[plan name]")
    parser.add_option("-a", "--add", dest="addition", 
                      help="Addition flag", metavar="[addition flag]")
    
    if len(sys.argv) > 1 :
         (Options, args) = parser.parse_args()
    
    runner = Runner.Runner()
    
    Global.mStartTime = time.time()
    
    if os.path.exists(Global.OUT_LOG): 
        shutil.rmtree(Global.OUT_LOG)
    os.makedirs(Global.OUT_LOG)
    
    
    if Options != None :
        if Options.clean != None :
            Global.CLEAN = True
        if Options.manual != None :
            Global.MANUAL = True
        if Options.addition != None :
            Global.ADD_FLAG = Options.addition
        
        if Options.case != None :
            
            fullCaseId = Global.CASE_FOLDER+"."+Options.case
            Global.mExecuteType = 'all'
            Global.TEST_PLAN = fullCaseId
            runner.executeCase(fullCaseId)
            
        elif Options.plan != None :
            
            if not os.path.exists(Options.plan):
                print("Error! The plan %s doesn't exist."%Options.plan)
                parser.print_help()
                exit()
            xmlCases = XmlParser.cXmlParser()
            xmlCases.readXml(Options.plan)
            Global.mExecuteType = 'all'
            runner.executeByPlan(xmlCases)
            
        else:
            runner.executeAll()
    else :
        runner.executeAll()
    
    Global.mEndTime = time.time()
    
    summaryLog = DumpInfo.cDumpInfo()
    summaryLog.dumpResult(DumpInfo.DUMP_SCREEN|DumpInfo.DUMP_HTML)


