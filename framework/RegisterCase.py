'''
Created on 2013-12-2

@author: dongmingchang
'''

import Global
import framework.CaseInfo as CaseInfo
import framework.Util as Util
import inspect

class register(object):
    '''
    classdocs
    '''
    mCase = {}

    def __init__(self, descp=None, priority=0, prolog=None, epilog=None, errorHandler=None, timeout=Global.CASE_TIMEOUT, caseType=0, tolerate=1, platform='all'):
        '''
        Constructor
        '''
        self.mCase = {CaseInfo.DESCRP:descp, \
                CaseInfo.PRI:priority, \
                CaseInfo.PROLOG:prolog, \
                CaseInfo.EPILOG:epilog,\
                CaseInfo.HERROR:errorHandler,\
                CaseInfo.TIMEOUT:timeout,\
                CaseInfo.TYPE:caseType, \
                CaseInfo.RESULT:CaseInfo.RESULT_SKIP, \
                CaseInfo.DURATION:0, \
                CaseInfo.TOLERATE:tolerate, \
                CaseInfo.PLATFORM:platform}
        
        
    
    def __call__(self, f):
        
        self.mCase[CaseInfo.ID] = f.__name__
     
      
        Global.mCaseManager.addCase(Util.convertToPackageName(inspect.getmodule(f).__file__), self.mCase)
        return f
        
