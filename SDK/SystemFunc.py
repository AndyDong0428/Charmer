'''
Created on 2013-11-28

@author: dongmingchang
'''

import traceback
import Global
import subprocess
import locale
import re
import platform
import pythoncom
import win32com.client
import os
import win32process
import win32event
import SDK.FileFunc as FileFunc
import codecs
import time
import sys

from framework import (
     Decorators)

def isXPPlatform():
    version =  platform.platform()
    verReg = re.search('Windows-(\w+)-', version)
    if verReg != None :
        if verReg.group(1) == 'XP'  or verReg.group(1) == '2003Server':
            return True
    return False

@Decorators.Step
def createScheduler(errorHandler, name, exePath):
    
    #SCHTASKS /Create /SC DAILY /TN gaming /TR c:\freecell /ST 12:00 /ET 14:00
    
    try:
        
        version =  platform.platform()
        rootFolder = None
        
        command = "SCHTASKS /Create /SC DAILY /TN \""+name+"\" /TR "+exePath+" /ST 12:00 /ET 14:00 /F"
        
        verReg = re.search('Windows-(\w+)-', version)
        if verReg != None :
            if verReg.group(1) == 'XP'  or verReg.group(1) == '2003Server':
                command = "SCHTASKS /Create /SC DAILY /TN \""+name+"\" /TR "+exePath+" /RU SYSTEM"
        
     
         
        p = subprocess.Popen(command ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
    
        
        encoding = locale.getdefaultlocale()[1]
       	'''
        for line in p.stdout :
            columns = line.decode(encoding)
            print(columns)
        '''
        
    except Exception:
         
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

@Decorators.Step
def deleteScheduler(errorHandler, name):
    
    try:
        command = "SCHTASKS /Delete /TN \""+name +"\" /F"
       
        p = subprocess.Popen(command ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
        
        '''
        encoding = locale.getdefaultlocale()[1]
        
        for line in p.stderr :
            columns = line.decode(encoding).split()
            if columns:
                print(columns[-1])
        '''
                
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return True

@Decorators.Step
def checkSchedulerStart(errorHandler, name, isExisted):
    
    errorFile = "error.log"
    listFile = "schList.log"

    
    try:
        
        XPMode = False
        version =  platform.platform()
        verReg = re.search('Windows-(\w+)-', version)
        if verReg != None :
            if verReg.group(1) == 'XP' or verReg.group(1) == '2003Server':
                XPMode = True
            
        
        if XPMode :
            filePath = os.getenv('windir')+os.sep+"Tasks"+os.sep+name+".job"
            FileFunc.checkFileExist(errorHandler, filePath, isExisted)
        
        else:
        
            command = "cmd.exe /c chcp 437 | SCHTASKS /QUERY /TN "+"\""+name+"\" 2>"+errorFile+" 1>"+listFile
            
            exePath = "C:\Windows\System32\cmd.exe"
            handle = win32process.CreateProcess(exePath, command, \
                                       None , None , 0 ,win32process.CREATE_NEW_CONSOLE , None , None , \
                                       win32process.STARTUPINFO())
       
           
            win32event.WaitForSingleObject(handle[0], -1)
            time.sleep(1)
            
            if isExisted and os.path.getsize(errorFile) > 0:
                raise Exception("The job \"%s\" does not exist"%(name))
            elif not isExisted and os.path.getsize(errorFile) == 0 :
                disableFlag = False
                
                if os.path.exists(listFile) :
                    fList = codecs.open(listFile,'r',encoding='utf8')
                    
                    for aLine in fList.readlines():
                        if aLine.find("Disabled") > -1:
                            disableFlag = True
                            break
                    
                    fList.close()
                
                if not disableFlag:
                    raise Exception("The job \"%s\" exists"%(name))
            
           
            #os.remove(errorFile)
            #os.remove(listFile)
                
    except Exception:
        
        if os.path.exists(errorFile) : os.remove(errorFile)
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return True


@Decorators.Step
def createService(errorHandler, srcName, exePath):
    
    
    try:
        command = "sc create \""+srcName+"\" binpath= \""+exePath+"\" type= share start= auto"
        p = subprocess.Popen(command ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
        

        encoding = locale.getdefaultlocale()[1]
        
        for line in p.stdout :
            outStr = line.decode(encoding)
						
            failedCodeReg = re.search('(\d+):', outStr)
            if failedCodeReg != None and failedCodeReg.group(1) != "1073" :
                raise Exception(outStr)
                    
                
    except Exception:
         
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return True

@Decorators.Step
def deleteService(errorHandler, srvName):
    
    try:
        command = "sc delete \""+srvName+"\""
        p = subprocess.Popen(command ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
        

        encoding = locale.getdefaultlocale()[1]
        
        for line in p.stdout :
            outStr = line.decode(encoding)

            failedCodeReg = re.search('(\d+):', outStr)
            if failedCodeReg != None and failedCodeReg.group(1) != "1060" :
                raise Exception(outStr)
                    
                
    except Exception:
       
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return True

@Decorators.Step
def checkServiceExist(errorHandler, srvName, isExisted):
    
    try:
        command = "sc query \""+srvName+"\""
        p = subprocess.Popen(command ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
        

        encoding = locale.getdefaultlocale()[1]
        
        errorMatch = False
        for line in p.stdout :
            outStr = line.decode(encoding)
            
            failedCodeReg = re.search('(\d+):', outStr)
            if failedCodeReg != None and \
                failedCodeReg.group(1) == "1060" :
                errorMatch = True
        
        if not isExisted and not errorMatch:
            raise Exception("The service \"%s\" exists"%srvName)
        elif isExisted and errorMatch:
            raise Exception("The service \"%s\" does not exist"%srvName)
                
    except Exception:
       
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return True

@Decorators.Step
def checkServiceStartMode(errorHandler, srvName, statusStr):
    
    try:
        pythoncom.CoInitialize() 
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_Service")
        for objItem in colItems :
            
            if objItem.Name == srvName :
                if objItem.StartMode != statusStr :
                    raise Exception("The status of service \"%s\" is %s, not %s"%(srvName,objItem.StartMode,statusStr))
                break
            
    except Exception:
       
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return True

@Decorators.Step
def createShortcut(errorHandler, exePath, linkPath, linkName, descrp=""):
    try:
        localeStr = locale.getdefaultlocale()[1]
        if linkPath.find(os.getenv('USERPROFILE')+"\\Desktop\\") > -1:
            if localeStr == 'cp950' and isXPPlatform():
                linkPath = linkPath.replace('Desktop', '桌面')
                
        pythoncom.CoInitialize() 
        ws = win32com.client.Dispatch("wscript.shell")
        scut = ws.CreateShortcut(linkPath+os.sep+linkName+'.lnk')
        scut.TargetPath = exePath
        scut.Description = descrp
        scut.WindowStyle = 4
        scut.Save()
        
        FileFunc.checkFileExist(errorHandler, linkPath+"\\"+linkName+".lnk", True)
            
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    
    return linkPath

@Decorators.Step    
def getWindodwsVersion(errorHandler):
    try:
        version =  platform.platform()
        verReg = re.search('Windows-(\w+)-', version)
        if verReg != None and verReg.group(1) != None:
            return verReg.group(1)
        	
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return ''

@Decorators.Step
def executeCommand(errorHandler, command, errJudge=None, waitFlag=True):
    try:
        
        p = subprocess.Popen(command ,stdin = subprocess.PIPE, \
                     stdout = subprocess.PIPE, \
                     stderr = subprocess.PIPE, \
                     shell=True)
        
       
        encoding = locale.getdefaultlocale()[1]
        outStr = ''
        if waitFlag:    
            for line in p.stdout :
                outStr = outStr+line.decode(encoding)
        
        
        if errJudge != None:
            errReg = re.search(errJudge, outStr)
            if errReg != None :
                raise Exception("%s match error string %s"%(outStr, errJudge))
            
    except Exception:
         
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True
    
def getStartupPath(errorHandler):
    
    rootFolder = ''
    try:
    
        version =  platform.platform()
        verReg = re.search('Windows-(\w+)-', version)
        if verReg != None :
            if verReg.group(1) == 'XP' or verReg.group(1) == '2003Server':
                localeStr = locale.getdefaultlocale()[1]
                if localeStr == 'cp950':
                    rootFolder = os.getenv('USERPROFILE')+"\\「開始」功能表\\程式集\\啟動\\"
                else:
                    rootFolder = os.getenv('USERPROFILE')+"\\Start Menu\\Programs\\Startup\\"
                    
            else:
                rootFolder = os.getenv('USERPROFILE')+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"  
            
    except Exception:
         
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return rootFolder

def getPythonPath():
    for pyPath in sys.path:
        if os.path.exists(pyPath+"\\python.exe"):
            return pyPath+"\\python.exe"
    return None
    
    
