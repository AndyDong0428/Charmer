'''
Created on 2013-12-13

@author: dongmingchang
'''

import pythoncom
import wmi
import codecs

import time
import threading
import os

class PerformanceThread(threading.Thread):
    
    
    def __init__(self, processMap, outFolder):
        threading.Thread.__init__(self)
        self.mProcessMap = processMap
        self.mOutFolder = outFolder
        
        self.mStop = False
        self.mMemStat = {}
    
    def stopMonitor(self):
        self.mStop = True
        
    
    def setPerformanceStatistics(self, memStat):
        self.mMemStat = memStat
    
    def getCategoryList(self):
        
        def MemoryFunc(process):
            return float(int(process.WorkingSet) /1024/1024)
        
        def IOCountFunc(process):
            return int(process.IOReadOperationsPersec)
        
        def IOBytesFunc(process):
            return float(int(process.IOReadBytesPersec)/1024/1024)
        
        categoryList = []
        categoryList.append(PerfCategory('Memory Usage (MB)', MemoryFunc))
        categoryList.append(PerfCategory('Read I/O Count (Persec)', IOCountFunc))
        categoryList.append(PerfCategory('Read I/O (MB/Sec)', IOBytesFunc))
        
        return  categoryList
    
    def run(self):
        
        if self.mProcessMap == None and len(self.mProcessMap.keys()) > 0:
            return
        pythoncom.CoInitialize()
        
        comp = wmi.WMI()
        
        targetList = self.mProcessMap.keys()
        
        fhMap = {}
        
        while not self.mStop:
            for aTarget in targetList :
                for process in comp.Win32_PerfRawData_PerfProc_Process(Name = aTarget):
                    
                    procTag = "%d-%s"%(process.IDProcess, aTarget)
                    fileName = "%s%s%s.html"%(self.mOutFolder, os.sep, procTag)
                    
                    fout = None
                    if not procTag in fhMap :
                        fhMap[procTag] = codecs.open(fileName,'a',encoding='utf8')
                        self.mMemStat[procTag] = ProcessPerf()
                        self.mMemStat[procTag].mCategoryList = self.getCategoryList()
                        self.mMemStat[procTag].mPid = process.IDProcess
                        self.mMemStat[procTag].mProcessName = aTarget
                        self.printHtmlHeader(fhMap[procTag], self.mMemStat[procTag].mCategoryList)
                    
                    fout = fhMap[procTag] 
                    fout.write("\t\t\t\t<TR>\n\t\t\t\t<TD class=\"pass\">%d</TD>\n"%time.time())
                    for aPerfCategory in self.mMemStat[procTag].mCategoryList :
                        
                       
                        perfValue = aPerfCategory.callQueryFunc(process)
                        fout.write("\t\t\t\t<TD class=\"pass\">%f</TD>\n"%perfValue)
                        
                        aPerfCategory.mTotalValue += perfValue
                        
                        if perfValue > aPerfCategory.mMaxValue:
                            aPerfCategory.mMaxValue = perfValue
                        
                    fout.write("\t\t\t\t</TR>\n")
                    
                    self.mMemStat[procTag].mTotalCount += 1
                    
                    
                
            time.sleep(0.2)
                
        for fileKey in fhMap.keys() :
            
            self.printHtmlEnd(fhMap[fileKey])
            fhMap[fileKey].close()
            for aPerfCategory in self.mMemStat[fileKey].mCategoryList :
                aPerfCategory.mAveValue = aPerfCategory.mTotalValue / self.mMemStat[fileKey].mTotalCount

            
    def printHtmlHeader(self, hFile, catgoryList):
        
        if hFile == None : return
         
        hFile.write("<html>\n\t<STYLE type=\"text/css\">\n\t\t@import \"charmer_result.css\";\n\t</STYLE>\n")
        
        hFile.write("<body>\n\t<DIV id=\"testsummary\">\n\t\t<TABLE width=\"90%\" frame=\"none\">\n\t\t\t<TR>\n\t\t\t\t<TH>Time</TH>\n")
        
        for aCategory in catgoryList:
            hFile.write("\t\t\t\t<TH>%s</TH>\n"%aCategory.mName)
        hFile.write("\t\t\t</TR>\n\t\t\t<TR>\n\t\t\t\t<div id=\"summaryinfo\">")


    def printHtmlEnd(self, hFile):
        
        if hFile == None: return
        
        hFile.write("\t\t\t</div>\n\t\t</TABLE>\n\t</DIV>\n</body>\n</html>\n")


class PerfCategory():
    
    def __init__(self, name, func):
        self.mName = name
        self.queryFun = func
        
        self.mMaxValue = 0
        self.mTotalValue = 0
        self.mAveValue = 0
    

    def callQueryFunc(self, *arg):
        return self.queryFun(*arg)

        
        
class ProcessPerf():
    
    def __init__(self):
        self.mPid = 0
        self.mProcessName = ''
        
        self.mCategoryList = []
        self.mTotalCount = 0
    
    
 