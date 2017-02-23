'''
Created on 2013-11-28

@author: dongmingchang
'''
import os
import traceback
import Global
import shutil
import codecs
import re
import zipfile
import time
import hashlib

from framework import (
     Decorators)

from xml.etree import ElementTree

@Decorators.Step
def createFolder(errorHandler, path):
    try:
        if not os.path.exists(path): os.makedirs(path)
    except Exception:

        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

@Decorators.Step
def deleteFolder(errorHandler, path):
    try:
        if os.path.exists(path): shutil.rmtree(path)
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

@Decorators.Step    
def createFile(errorHandler, fileName, content):
    try:
        if os.path.exists(fileName) : os.remove(fileName)
        
        
        (path, name) = os.path.split(fileName)
        if path != '' and not os.path.exists(path): os.makedirs(path)
        
        fout = codecs.open(fileName,'w',encoding='utf8')
        fout.write(content)
        fout.close()
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

@Decorators.Step
def deleteFile(errorHandler, fileName):
    try:
        if os.path.exists(fileName) : 
            os.remove(fileName)
           
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True

@Decorators.Step
def copyFile(errorHandler, scrFile, desFile):
    
    try:
        shutil.copy(scrFile, desFile)
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True

@Decorators.Step
def checkFolderWithFiles(errorHandler, folder, fileFlag = False):
    try:
        filesStr = ""
        for root, dirs, files in os.walk(folder): # Walk directory tree
            if files != None or len(files) > 0 :
                filesStr = filesStr+'\n'.join(files)
        if filesStr != "" and not fileFlag:
            raise Exception("The folder \"%s\" is not empty and includes \n%s"%(folder,filesStr))
        elif filesStr == "" and fileFlag:
            raise Exception("The folder \"%s\" is empty"%(folder))
                
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True

@Decorators.Step
def checkFileExist(errorHandler, filePath, isExist=False):
    try:
        if isExist :
            if not os.path.exists(filePath):
                raise Exception("The file \"%s\" does not exist!"%(filePath))
        else:
            if os.path.exists(filePath):
                raise Exception("The file \"%s\" exists!"%(filePath))
            
            
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True

@Decorators.Step
def checkFileIsEmpty(errorHandler, filePath, isEmpty=False):
    try:
        
        if not os.path.exists(filePath):
            raise Exception("The file \"%s\" does not exist!"%(filePath))
        
        if isEmpty and os.path.getsize(filePath) > 0:
            raise Exception("The file \"%s\" is not empty!"%(filePath))
        elif not isEmpty and os.path.getsize(filePath) == 0:
            raise Exception("The file \"%s\" is empty!"%(filePath))
            
            
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True

@Decorators.Step
def appendFileContent(errorHandler, fileName, content, encodeType='utf8'):
    fout = None
    try:
        fout = codecs.open(fileName,'a',encoding=encodeType)
        fout.write(content)
        
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if fout != None:
            fout.close()
        
    return True

@Decorators.Step
def replaceFileContent(errorHandler, fileName, srcStr, desStr, encodeType='utf8'):
    
    fsrc = None
    fdes = None
    
    try:
        
        fsrc = codecs.open(fileName,'r',encoding=encodeType)
        content = fsrc.readlines()
        
        contentStr = "".join(content)
        
        contentStr = contentStr.replace(srcStr, desStr)
        fdes = codecs.open(fileName,'w',encoding=encodeType)
        fdes.write(contentStr)
        
        
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if fsrc != None:
            fsrc.close()
        if fdes != None:
            fdes.close()
        
    return True

@Decorators.Step
def checkFileContent(errorHandler, fileName, matchedStr, flag=False):
    
    fsrc  = None
    try:
        matchedFlag = False
        fsrc = codecs.open(fileName,'r')
        for aline in fsrc.readlines():
            aline = aline.strip('\n')
            if matchedStr == aline:
                matchedFlag = True
                break
            
        if flag != matchedFlag:
            if flag : raise Exception("The string %s is not in %s"%(matchedStr, fileName))
            else: raise Exception("The string %s is in %s"%(matchedStr, fileName))
               
       
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    finally:
        if fsrc != None:
            fsrc.close()
        
    return True

@Decorators.Step
def compareFileContent(errorHandler, srcFile, targetFile, matchedFlag = True):
    
    fsrc = None
    ftarget = None
    
    try:
        fsrc = codecs.open(srcFile,'rb')
        srcContent = fsrc.read()
        
        
        ftarget = codecs.open(targetFile,'rb')
        targetContent = ftarget.read()
        
        
        matchResult = (srcContent == targetContent)
        if matchResult != matchedFlag:
            raise Exception("The result of source file %s compare with target file %s is %s"%(srcFile, targetFile, str(matchResult)))
        
        
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if fsrc != None:
            fsrc.close()
        if ftarget != None:   
            ftarget.close()
    return True

def getComponentText(errorHandler, confFile, tagName):
    
    tree = ElementTree.parse(confFile)
    root = tree.getroot()
    
    resNode = root.find("resources")
    stringsNode = resNode.find("strings")
    descNode = stringsNode.find(tagName)
    localeNode = descNode.find(Global.PROGRAM_LOCALE)
    
    if localeNode != None:
        localeReg = re.search('\[\/\.\]([^\[]*)', localeNode.text)
        if localeReg != None:
                localeStr =  localeReg.group(1)
                return localeStr
            
    return None

def UnzipAFile(errorHandler, zipFile, fileInZip, localFolder):
    
    file = None
    try:
        zfile = zipfile.ZipFile(zipFile,'r')
        
        if fileInZip in zfile.namelist():
            data = zfile.read(fileInZip)
            file = open(localFolder+"//"+fileInZip, 'w+b')
            file.write(data)
            
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    finally:
        if file != None:
            file.close()
        
    return True

def getMaxIdFileName(errorHandler, folder, extName):
    try:
        retPath = ''
        maxId = 0
        for root, dirs, files in os.walk(folder): # Walk directory tree
            for f in files:
                fileNameReg = re.search('(\d+).'+extName, f)
                if fileNameReg != None and int(fileNameReg.group(1)) > maxId: 
                    maxId = int(fileNameReg.group(1)) 
        retPath = folder+"\\"+ str(maxId+1)+"."+ extName 
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return retPath

@Decorators.Step
def waitFileExist(errorHandler, filePath, timeout, isExist=False):
    try:
        for i in range(0,timeout):
            if os.path.exists(filePath) == isExist:
                break
            time.sleep(1)
            
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True

@Decorators.Step
def renameFile(errorHandler, srcName, newName):
    try:
        if os.path.exists(srcName):
            os.rename(srcName, newName)
    except Exception:
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
    return True

def getMd5Hash(fileName):
    
    myhash = hashlib.md5()
    fobj = open(fileName, 'rb')
    while True:
        b = fobj.read(8096)
        if not b :
            break
        myhash.update(b)
    fobj.close()

    return myhash.hexdigest().lower()