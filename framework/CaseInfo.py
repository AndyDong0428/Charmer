'''
Created on 2013-11-28

@author: dongmingchang
'''

ID = 'id'
DESCRP = 'description'
PRI = 'priority'
PROLOG = 'prolog'
EPILOG = 'epilog'
RESULT = 'result'
HERROR = 'errorHandler'
TIMEOUT = 'timeout'
DURATION = 'duration'
TYPE = 'type'
START = 'start_time'
END = 'end_time'
ERROR = 'error_messsage'
PERF = 'performance_report'
LOGPATH = 'log_path'
TOLERATE = 'tolerate'
PLATFORM = 'platform'

#
DEFAULT = 0x0000
SMOKE = 0x0001
STRESS = 0x0002
PERF = 0x0004
MANUAL = 0x0008

BUG = 0xFFFF

# Test result type
RESULT_PASS = 1
RESULT_FAIL = 0
RESULT_SKIP = 2
RESULT_TIMEOUT = 3
RESULT_ERROR = 4

def resultToString(resultId):
    if resultId == RESULT_PASS :
        return("pass")
    elif resultId == RESULT_FAIL :
        return("fail")
    elif resultId == RESULT_SKIP :
        return("notExecuted")
    elif resultId == RESULT_TIMEOUT :
        return("timeout")
    elif resultId == RESULT_ERROR :
        return("error")
    
def typeToString(typeValue):
    
    typeStr = ""
    if typeValue & SMOKE :
        typeStr = typeStr+"Smoke;"
        
    if typeValue & STRESS :
        typeStr = typeStr+"Stress;"
        
    if typeValue & PERF :
        typeStr = typeStr+"Performance;"
        
    if typeValue & MANUAL :
        typeStr = typeStr+"Manual;"
        
    if typeValue == DEFAULT :
        typeStr = typeStr+"Default;"
        
    return typeStr