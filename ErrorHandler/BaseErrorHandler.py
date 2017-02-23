'''
Created on 2013-11-28

@author: dongmingchang
'''
import Global
import framework.Util as Util
import traceback

class BaseErrorHandler(object):
    '''
    classdocs
    '''

   
    def __init__(self):
        '''
        Constructor
        '''
    
    def handler(self, params):
        
        try:
            Util.taskScreenshot(Global.mCaseManager.getLogPath()+"\\failed.bmp")
        except Exception:
            print("\n"+traceback.format_exc())
            print("\nCannot task screenshot")
        
        if params[Global.ERROR_CALLSTACK] != None :
            stackStr = ""
            for line in params[Global.ERROR_CALLSTACK].format_stack():
                stackStr = stackStr+line.strip()
            Global.mCaseManager.setTraceStack(stackStr)
            print("\n"+stackStr)
        
        if params[Global.ERROR_MESSAGE] != None :
            Global.mCaseManager.setErrorMessage(params[Global.ERROR_MESSAGE])
            
            try:
                print("\n"+params[Global.ERROR_MESSAGE])
            except Exception:
                print("\nFail to print error message")
        
        if Global.ADD_FLAG.find('wait') != -1:
            input("Wait for click ...")
        
    
class FailException(Exception):
    '''
    classdocs
    '''
    pass