'''
Created on 2013-12-23

@author: dongmingchang
'''
import winreg
import Global
import traceback
import time

from framework import (
     Decorators)


def splitKeyName(key):
    keyarray = key.split('\\')
    return  keyarray[0], '\\'.join(keyarray[1:])

def splitLastKey(key):
    keyarray = key.split('\\')
    return  '\\'.join(keyarray[0:len(keyarray)-1]), keyarray[len(keyarray)-1]

def getKeyHandle(ketStr):
    
    if ketStr == 'HKEY_LOCAL_MACHINE' or ketStr == 'HKLM' :
        return winreg.HKEY_LOCAL_MACHINE
    elif ketStr == 'HKEY_CLASSES_ROOT' or ketStr == 'HKCR' :
        return winreg.HKEY_CLASSES_ROOT
    elif ketStr == 'HKEY_CURRENT_CONFIG' or ketStr == 'HKCC' :
        return winreg.HKEY_CURRENT_CONFIG
    elif ketStr == 'HKEY_CURRENT_USER' or ketStr == 'HKCU' :
        return winreg.HKEY_CURRENT_USER
    elif ketStr == 'HKEY_DYN_DATA' or ketStr == 'HKDD' :
        return  winreg.HKEY_DYN_DATA
    elif ketStr == 'HKEY_PERFORMANCE_DATA' or ketStr == 'HKPD' :
        return winreg.HKEY_PERFORMANCE_DATA
    elif ketStr == 'HKEY_USERS' or ketStr == 'HKU' :
        return winreg.HKEY_USERS
    else:
        return None
    
def getValueType(regType):
    
    if regType == 'REG_BINARY' :
        return winreg.REG_BINARY
    elif regType == 'REG_DWORD' :
        return winreg.REG_DWORD
    elif regType == 'REG_DWORD_LITTLE_ENDIAN' :
        return winreg.REG_DWORD_LITTLE_ENDIAN 
    elif regType == 'REG_DWORD_BIG_ENDIAN' :
        return winreg.REG_DWORD_BIG_ENDIAN 
    elif regType == 'REG_EXPAND_SZ' :
        return winreg.REG_EXPAND_SZ
    elif regType == 'REG_LINK' :
        return winreg.REG_LINK
    elif regType == 'REG_MULTI_SZ' :
        return winreg.REG_MULTI_SZ
    elif regType == 'REG_NONE' :
        return winreg.REG_NONE
    elif regType == 'REG_RESOURCE_LIST' :
        return winreg.REG_RESOURCE_LIST
    elif regType == 'REG_SZ' :
        return winreg.REG_SZ
    else:
        return 0
 

@Decorators.Step
def createRegKeyValue(errorHandler, key, name=None, regType=None, value=None):
    
    hKey = None
    try:
        mainKey, subKey = splitKeyName(key)
        
        try:
            hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_ALL_ACCESS)
        except:
            hKey = winreg.CreateKeyEx(getKeyHandle(mainKey), subKey)
        
        if name!= None and regType != None and value != None :
            winreg.SetValueEx(hKey, name, 0, getValueType(regType), value)   
        
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)
        
    return True

@Decorators.Step
def deleteRegKey(errorHandler, key):
    hKey = None
    try:
        mainKey, subKey = splitKeyName(key)
        
        preKey , lastKey = splitLastKey(subKey)
        hKey = winreg.OpenKey(getKeyHandle(mainKey), preKey, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(hKey, lastKey)   
        
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)
        
    return True

@Decorators.Step
def deleteRegValue(errorHandler, key, name):
    hKey = None
    try:
        mainKey, subKey = splitKeyName(key)
        
        hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_ALL_ACCESS)
        
        winreg.DeleteValue(hKey, name)   
        
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)
        
    return True

@Decorators.Step
def checkRegValueExist(errorHandler, key, name, existFlag):
    hKey = None
    try:
        mainKey, subKey = splitKeyName(key)
        
        retArray = None
        hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_ALL_ACCESS)
        try:
            retArray = winreg.QueryValueEx(hKey, name)
        except:
            pass
        
        if existFlag and  retArray == None:
            raise Exception("The %s\\%s doesn't exist"%(key, name))
        elif not existFlag and retArray != None:
            raise Exception("The %s\\%s exist"%(key, name))
              
        return True
    
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        return False
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)
            
@Decorators.Step
def checkRegKeyExist(errorHandler, key, existFlag):
    hKey = None
    try:
        actualFlag = False
        mainKey, subKey = splitKeyName(key)
        try:
            hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_ALL_ACCESS)
            actualFlag = True
        except:
            actualFlag = False
        
        if existFlag and  not actualFlag:
            raise Exception("The %s doesn't exist"%(key))
        elif not existFlag and actualFlag:
            raise Exception("The %s exist"%(key))
              
        return True
    
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        return False
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)
        
    

@Decorators.Step
def getRegValue(errorHandler, key, name):
    hKey = None
    try:
        mainKey, subKey = splitKeyName(key)
        
        retArray = None
        hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_ALL_ACCESS)
        try:
            retArray = winreg.QueryValueEx(hKey, name)
            return retArray[0]
        except:
            pass
        
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)
        
    return None

def WaitForRegValueExist(errorHandler, key, name, timeout, existFlag):
    hKey = None
    try:
        mainKey, subKey = splitKeyName(key)
        try:
            hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_QUERY_VALUE)
        except Exception:
            time.sleep(1)
            hKey = winreg.OpenKey(getKeyHandle(mainKey), subKey, 0, winreg.KEY_QUERY_VALUE)
       
        for i in range(0,timeout):
            
            try:
                value, type = winreg.QueryValueEx(hKey, name)
                if existFlag : break
            except:
                if not existFlag : break
                
            
            time.sleep(1)
        
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if hKey != None :
            winreg.CloseKey(hKey)