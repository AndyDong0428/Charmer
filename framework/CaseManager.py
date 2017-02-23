'''
Created on 2013-12-2

@author: dongmingchang
'''

import framework.Util as Util
import framework.CaseInfo as CaseInfo

class cCaseManager(object):
    '''
    classdocs
    '''
    
    mCaseMap = {}
    mResultCount = {}
    mWorkingCase = None
    mPerfResult = {}
    mTraceStack = None

    def __init__(self):
        '''
        Constructor
        '''
    def setWorkingCase(self, caseInfo):
        self.mWorkingCase = caseInfo
        
    def getWorkingCase(self):
        return self.mWorkingCase
    
    def setErrorMessage(self, message):
        if self.mWorkingCase == None :
            return
        self.mWorkingCase[CaseInfo.ERROR] = message
        
    def setTraceStack(self, traceStack):
        self.mTraceStack= traceStack
        
    def getTraceStack(self):
        
        return self.mTraceStack
        
    def getLogPath(self):
        if self.mWorkingCase == None :
            return None
        return self.mWorkingCase[CaseInfo.LOGPATH]
    
    def addCase(self, moduleName, case):
        
        caseList = []
        if moduleName not in self.mCaseMap :
            caseList.append(case)
            self.mCaseMap[moduleName] = caseList
        else:
            caseList = self.mCaseMap[moduleName];
            count = 0
            for existedCase in caseList :
                if existedCase[CaseInfo.PRI] < case[CaseInfo.PRI] :
                    break
                elif existedCase[CaseInfo.ID] == case[CaseInfo.ID] :
                    return
                count += 1
            caseList.insert(count, case)
                
   
    def getCaseMap(self):
        
        return self.mCaseMap;
    
   
            
         
        