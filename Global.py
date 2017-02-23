import ErrorHandler.ErrorHandlers as ErrorHandlers
import framework.CaseManager as CaseManager
import framework.CaseInfo as CaseInfo
import framework.Util as Util
import os, winreg, codecs, re


def getProgramLocale():
    
    localeStr = ''
    config = TARGET_FOLDER+"\\config.ini"
    try:
        fConfig = codecs.open(config,'r',encoding='utf16')
        
        for aline in fConfig.readlines():
            aline = aline.rstrip('\n')
            aline = aline.rstrip('\r')
            localeReg = re.search('language=(.+)', aline)
            if localeReg != None:
                localeStr =  localeReg.group(1)
            
        fConfig.close()
    except:
        pass
        
    return localeStr

VERSION = "1.0.0"

CLEAN = False
MANUAL = False


# Environment variables
CURRENT_DIR = os.getcwd()
SAMPLE_FOLDER = CURRENT_DIR+"\\Samples"
CASE_FOLDER = "Cases"
REPORT_FOLDER = "Report"
CASE_TIMEOUT = 10000
OUT_LOG = "."+os.sep+"logs"
RESULT_HTML = OUT_LOG+os.sep+"testResult.xml"
TEST_PLAN = "Default"
ADD_FLAG = ''
READY_TIME = 3

DEFAULT_TARGET_FOLDER = '.'
#updateProgramVar()

#####################



MONITOR_PROC = { 'python':300}

mExecuteType = ''
mCaseManager = CaseManager.cCaseManager()
mTestResult = {CaseInfo.RESULT_PASS:0, CaseInfo.RESULT_FAIL:0, CaseInfo.RESULT_SKIP:0, CaseInfo.RESULT_TIMEOUT:0}
mStartTime = 0
mEndTime = 0
mFeatureList = {"BasicFunc":"True"}

# Error Handler
ERROR_CALLSTACK = "stack"
ERROR_MESSAGE = "message"
DEFAULT_ERROR_HANDLER = ErrorHandlers.DefaultErrorHandler()
IGNORE_ERROR_HANDLER = ErrorHandlers.IgnoreErrorHandler()
NOTIFY_ERROR_HANDLER = ErrorHandlers.NotifyErrorHandler()



