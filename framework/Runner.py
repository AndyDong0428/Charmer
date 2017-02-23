'''
Created on 2013-11-27

@author: dongmingchang
'''
import os
import framework.Util as Util
import Global

import sys
sys.path.append("."+os.sep+"framework")
import CaseInfo
import BaseCases
import DumpInfo
import PerfMonitor

import ErrorHandler.BaseErrorHandler as BaseErrorHandler
import time
import threading
import traceback


class Runner(object):
    '''
    classdocs
    '''
    #mTestResult = {CaseInfo.RESULT_PASS:0, CaseInfo.RESULT_FAIL:0, CaseInfo.RESULT_SKIP:0, CaseInfo.RESULT_TIMEOUT:0}
    mModuleObjs = None
    

    def __init__(self):
        '''
        Constructor
        '''
        self.mModuleObjs = Util.load_from_folder("."+os.sep+Global.CASE_FOLDER)
    
    def isExecute(self, caseInfo):
        
        if caseInfo[CaseInfo.PLATFORM] != 'all':
            if (Util.is64Platform() and caseInfo[CaseInfo.PLATFORM] != '64') or \
                (not Util.is64Platform() and caseInfo[CaseInfo.PLATFORM] != '32'):
                return False
        
        if Global.mExecuteType == 'all':
            return True
        if caseInfo[CaseInfo.TYPE] & CaseInfo.STRESS :
            if Global.mExecuteType.find("stress") == -1: return False
        return True
              
    def executeAll(self, caseId = None):
        
        for moduleName in sorted(Global.mCaseManager.getCaseMap().keys()) :
            self.executeCase(moduleName)
    
    def executeByPlan(self, planXml):
        
        
        for i in range(0, planXml.getGroupCount()):
            #TODO: execute precondition
           
            precondStr = planXml.getGroupCondition(i)[0]
            postcondStr = planXml.getGroupCondition(i)[1]
            if precondStr != 'None':
                (moduleName, funcName) = Util.getModuleAndAPI(precondStr)
                if Global.CASE_FOLDER+"."+moduleName not in self.mModuleObjs:
                    print("[Error] Cannot find module %s under %s"%(moduleName, Global.CASE_FOLDER))
                    return
                precondFunc = getattr(self.mModuleObjs[Global.CASE_FOLDER+"."+moduleName], funcName)
                precondFunc(Global.DEFAULT_ERROR_HANDLER)
            for moduleName in sorted(planXml.getCaseList(i).keys()):
                #print(moduleName+" : ")
                #print(planXml.getCaseList(i)[moduleName])
                self.executeCase(moduleName, planXml.getCaseList(i)[moduleName])
        
            if postcondStr != 'None':
                (moduleName, funcName) = Util.getModuleAndAPI(postcondStr)
                if Global.CASE_FOLDER+"."+moduleName not in self.mModuleObjs:
                    print("[Error] Cannot find module %s under %s"%(moduleName, Global.CASE_FOLDER))
                    return
                postcondFunc = getattr(self.mModuleObjs[Global.CASE_FOLDER+"."+moduleName], funcName)
                postcondFunc(Global.IGNORE_ERROR_HANDLER)
    
                
    def executeCase(self, moduleName, caseIds=None):
        
        #if moduleName in self.mModuleObjs :
        if moduleName not in self.mModuleObjs:
            (moduleName, caseIds) = Util.getModuleAndAPI(moduleName)
            if moduleName not in self.mModuleObjs or moduleName not in Global.mCaseManager.getCaseMap():
                return False
        
        print("---[%s]----------------------------"%moduleName)
        
        errorHandler = None
        envFailedFlag = False
        
        # Set default error handler
        getErrorHandlerFunc = getattr(self.mModuleObjs[moduleName], "getErrorHandler")
        if getErrorHandlerFunc != None :
            errorHandler = getErrorHandlerFunc()
            if errorHandler == None :
                errorHandler = Global.DEFAULT_ERROR_HANDLER
        
        prologFunc = getattr(self.mModuleObjs[moduleName], BaseCases.PROLOG_FUNC)
        if prologFunc != None :
            try:
                prologFunc(errorHandler)
            except Exception:
                print(traceback.format_exc())
                envFailedFlag = True
              
        for caseInfo in Global.mCaseManager.getCaseMap()[moduleName] :
            
            if not self.isExecute(caseInfo):
                continue
            
            elif caseIds != None:
                if not isinstance(caseIds , list) :
                    if caseInfo[CaseInfo.ID].find(caseIds) == -1:
                        continue
                else:
                    if None in caseIds:
                        pass 
                    elif caseInfo[CaseInfo.ID] not in caseIds :
                        continue
            elif envFailedFlag:
                self.updateCaseInfo(caseInfo, result=CaseInfo.RESULT_FAIL)
                continue
            
            Global.mCaseManager.setWorkingCase(caseInfo)
            
            logPath = Global.OUT_LOG+os.sep+Util.convertToPath(moduleName)+os.sep+caseInfo[CaseInfo.ID]
            caseInfo[CaseInfo.LOGPATH] = logPath
            if not os.path.exists(logPath) :
                os.makedirs(logPath)
            
            
            if caseInfo[CaseInfo.HERROR] != None :
                errorHandler =  caseInfo[CaseInfo.HERROR]
            
            caseFunc = getattr(self.mModuleObjs[moduleName], caseInfo[CaseInfo.ID])
            setupFunc = getattr(self.mModuleObjs[moduleName], BaseCases.SETUP_FUNC)
            tearDownFunc = getattr(self.mModuleObjs[moduleName], BaseCases.TEARDOWN_FUNC)
            
            descrp = ""
            timeout = Global.CASE_TIMEOUT
            if CaseInfo.TIMEOUT in caseInfo :
                timeout = caseInfo[CaseInfo.TIMEOUT]
            
            
            if caseInfo[CaseInfo.DESCRP] != None:
                descrp = caseInfo[CaseInfo.DESCRP]
            print(caseInfo[CaseInfo.ID]+" : "+descrp, end="")
            
            caseInfo[CaseInfo.START] = time.time()
            
            
            
            perfMonitor = PerfMonitor.PerformanceThread(Global.MONITOR_PROC, logPath)
            
            memoryStat = {}
            perfMonitor.setPerformanceStatistics(memoryStat)
            perfMonitor.start()
            
            finalResult = CaseInfo.RESULT_SKIP
            # Launch executionThread to execute case, and tolerate failed count
            for failedCount in range(0,caseInfo[CaseInfo.TOLERATE]):
                
                if setupFunc != None :
                    try:
                        setupFunc(errorHandler)
                    except:
                        print(traceback.format_exc())
                        self.updateCaseInfo(caseInfo, result=CaseInfo.RESULT_FAIL)
                        break
                
                caseThread = ExecutionThread(caseFunc)
                caseThread.setErrorHandler(errorHandler)
                
                
                
                if not caseInfo[CaseInfo.TYPE] & CaseInfo.MANUAL:
                    caseThread.start()
                    caseThread.join(timeout)
                    if caseThread.isAlive() :
                        caseThread._stop()
                    finalResult = caseThread.getResult()
                
                if tearDownFunc != None :
                    try:
                        tearDownFunc(errorHandler)
                    except:
                        print(traceback.format_exc())
                        
                
                if finalResult != CaseInfo.RESULT_FAIL:
                    break
            
            time.sleep(2)
                
            perfMonitor.stopMonitor()
            perfMonitor.join(timeout)
            caseInfo[CaseInfo.PERF] = memoryStat
            
            perfResult = self.checkProcessBoundary(caseInfo[CaseInfo.PERF])
            print("\n"+perfResult)
            if perfResult != '' :
                finalResult = CaseInfo.RESULT_FAIL
                if CaseInfo.ERROR not in caseInfo or caseInfo[CaseInfo.ERROR] == None :
                    caseInfo[CaseInfo.ERROR] = ''
                caseInfo[CaseInfo.ERROR] = caseInfo[CaseInfo.ERROR]+perfResult
            
           
            self.updateCaseInfo(caseInfo, result=finalResult)
            
            DumpInfo.dumpCaseAsHtml(caseInfo, logPath)

        epilogFunc = getattr(self.mModuleObjs[moduleName], BaseCases.EPILOG_FUNC)
        if epilogFunc != None :
            try:
                epilogFunc(errorHandler)
            except:
                print(traceback.format_exc())
    
    def updateCaseInfo(self, caseObj, result=CaseInfo.RESULT_SKIP ):
        
        caseObj[CaseInfo.END] = time.time()
        if CaseInfo.START in caseObj:
            caseObj[CaseInfo.DURATION] = int(round(caseObj[CaseInfo.END] * 1000)) - int(round(caseObj[CaseInfo.START] * 1000))
        else:
            caseObj[CaseInfo.DURATION] = 0
        caseObj[CaseInfo.RESULT] = result
        Global.mTestResult[result] += 1
        print(" => %s"%CaseInfo.resultToString(result))
           
    
            
    def checkProcessBoundary(self, perfStat):
        
        failedMessage = ''
        for aStat in perfStat.keys() :
            procName = perfStat[aStat].mProcessName
            if procName in Global.MONITOR_PROC and Global.MONITOR_PROC[procName] < perfStat[aStat].mCategoryList[0].mMaxValue:
                failedMessage = failedMessage+"[ERROR] The working set %f of process \"%s\" overs the boundary %d.\n"%(perfStat[aStat].mCategoryList[0].mMaxValue,procName,Global.MONITOR_PROC[procName])
            
        return failedMessage

            
class ExecutionThread(threading.Thread):
    
    mFuncObj = None
    mResult = CaseInfo.RESULT_TIMEOUT
    mErrorHandler = None
    
    def __init__(self,obj):
        threading.Thread.__init__(self)
        self.mFuncObj=obj
    
    def setErrorHandler(self, errorHandler):
        self.mErrorHandler = errorHandler
             
    def run(self):
        try:
            self.mFuncObj(self.mErrorHandler)
            self.mResult = CaseInfo.RESULT_PASS
           
        except BaseErrorHandler.FailException:
            self.mResult = CaseInfo.RESULT_FAIL
        except Exception:
            Global.mCaseManager.setErrorMessage(traceback.format_exc())
            print("\n"+traceback.format_exc())
            self.mResult = CaseInfo.RESULT_FAIL
    
    def getResult(self):
        return self.mResult
    
    
    