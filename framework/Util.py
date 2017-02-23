'''
Created on 2013-11-28

@author: dongmingchang
'''

import os
import imp
import platform

import win32gui
import win32ui
import win32con
import time

import framework.FileUtil as FileUtil
import framework.BaseCases as BaseCases
import threading

class cExecution(threading.Thread):
    
    def __init__(self, obj, *args, **keyArgs):
        threading.Thread.__init__(self)
        self.mFuncObj=obj
        self.mArgs = args
        self.mKeyArgs = keyArgs
        
    def run(self):
        self.mFuncObj(*self.mArgs, **self.mKeyArgs)
        

        
def load_from_file(filepath):
    classInst = None
    py_mod = None

    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
    
    expected_class =  mod_name
    
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)
       
    #Remove to parse .pyc files
    #elif file_ext.lower() == '.pyc':
    #    py_mod = imp.load_compiled(mod_name, filepath)
    
    if hasattr(py_mod, expected_class):
        
        testClass = getattr(py_mod, expected_class)
        classInst = testClass()
        
        
    return classInst
    
def load_from_folder(folder):
    
    classInst = {}
    
    fileList = FileUtil.traverseFolder(folder)
    for aFile in fileList:
        inst = load_from_file(aFile)
        if inst != None and isinstance(inst, BaseCases.Cases):
            
            classInst[convertToPackageName(aFile)] = inst
    return classInst

def getModuleAndAPI(funcName):
    
    temps = funcName.split('.')
    if len(temps) > 1:
        api = temps[len(temps)-1]
        module = '.'.join(temps[:len(temps)-1])
    else:
        module = funcName
        api = None
    return (module, api)

def convertToPackageName(filePath):
    
    filePath = filePath.replace(os.sep, '.')
    filePath = filePath.replace(".py", '')
    
    count = 0
    for char in filePath:
        if char != '.' :
            break
        count+=1;
          
    filePath = filePath[count:len(filePath)]
 
    return filePath

def convertToPath(package):
    
    filePath = package.replace('.', os.sep)
   
    return filePath

def is64Platform():
    archArray = platform.architecture()
    if archArray[0] == '64bit':
        return True
    return False

def taskScreenshot(imagePath):
    hwnd=win32gui.GetDesktopWindow()
    l,t,r,b=win32gui.GetWindowRect(hwnd)
    h=b-t
    w=r-l
    hDC = win32gui.GetWindowDC(hwnd)
    myDC=win32ui.CreateDCFromHandle(hDC)
    newDC=myDC.CreateCompatibleDC()
    
    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)
    
    newDC.SelectObject(myBitMap)
    
    newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
    myBitMap.Paint(newDC)
    myBitMap.SaveBitmapFile(newDC, imagePath)
    newDC.DeleteDC()
    win32gui.DeleteObject(myBitMap.GetHandle())
        
    