'''
Created on 2013-12-5

@author: dongmingchang
'''
import Global
import traceback
import win32process
import time
import win32api, win32pdhutil, win32con, win32event, locale, codecs, os, subprocess

from framework import (
     Decorators)

@Decorators.Step
def createProcess(errorHandler, exePath, args, currentDir = None):
   
    hProc = None
    try:
       
        hProc = win32process.CreateProcess(exePath, args, \
                                   None , None , 0 ,win32process.CREATE_NEW_CONSOLE , None , currentDir , \
                                   win32process.STARTUPINFO())
        
        
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return hProc

@Decorators.Step
def createProcessAndWait(errorHandler, exePath, args, currentDir = None, checkedWord = None):
   
    hProc = None
    try:
    
        hProc = win32process.CreateProcess(exePath, args, \
                                   None , None , 0 ,win32process.CREATE_NEW_CONSOLE , None , currentDir , \
                                   win32process.STARTUPINFO())
        
        win32event.WaitForSingleObject(hProc[0], -1)
        time.sleep(0.5)
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return hProc

@Decorators.Step
def terminateProcess(errorHandler, hProc, waitTime=5):
    
    try:
        if hProc != None and len(hProc) > 1:
            win32process.TerminateProcess(hProc[0], 1)
            win32event.WaitForSingleObject(hProc[0], waitTime)
            time.sleep(1)
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

@Decorators.Step
def killProcByName(errorHandler, procname):
   
    try:
       
        for i in range(0,5):
            outStr = ''
            p = subprocess.Popen("tasklist | find \"%s\""%procname ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
            
            encoding = locale.getdefaultlocale()[1]
            for line in p.stdout :
                outStr = outStr+"\n"+line.decode(encoding)
            
            if outStr != '':
                p = subprocess.Popen("taskkill /f /im \"%s\""%procname ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
            else:
                break
            time.sleep(1)
                
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

def checkProcessTerminate(errorHandler, procname, timeout=10):
    try:
        exitFlag = False
        if len(procname) > 25:
            procname = procname[0:25]
        
        for i in range(0, timeout) :
            outStr = ''
            p = subprocess.Popen("tasklist | find \"%s\""%procname ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
            
            encoding = locale.getdefaultlocale()[1]
            for line in p.stdout :
                outStr = outStr+"\n"+line.decode(encoding)
            if outStr == '':
                exitFlag = True
                break;        
            time.sleep(1)
          
        if not exitFlag :        
            raise Exception("The process %s still exits: %s"%(procname,outStr))
            
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True


def checkProcessExist(errorHandler, procname, timeout=10):

    retryTime = 5
    retryCount = 0
    while True:
        retryCount = retryCount + 1
        try:
            existFlag = False
            for i in range(0, timeout) :
                outStr = ''
                p = subprocess.Popen("tasklist | find \"%s\""%procname ,stdin = subprocess.PIPE, \
                         stdout = subprocess.PIPE, \
                         stderr = subprocess.PIPE, \
                         shell=True)
                
                encoding = locale.getdefaultlocale()[1]
                for line in p.stdout :
                    outStr = outStr+"\n"+line.decode(encoding)
                if outStr != '':
                    existFlag = True
                    break;        
                time.sleep(1)
                
            if not existFlag :        
                raise Exception("The process %s doesn't exist"%(procname))
            break
                
        except Exception:
            if retryCount < retryTime:
                pass
            else:
                errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
                errorHandler.handler(errorInfo);
                break
        
    return True
