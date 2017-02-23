'''
Created on 2013-12-4

@author: dongmingchang
'''
import os
import platform
import locale
import socket
import wmi
import codecs
import shutil
import Global
import framework.CaseInfo as CaseInfo
import framework.FileUtil as FileUtil
import framework.Util as Util
import framework.PerfMonitor as PerfMonitor
from datetime import *

DUMP_SCREEN = 0x01
DUMP_HTML = 0x02
    

class cDumpInfo(object):
    '''
    classdocs
    '''
    
    PLAT = 'platform'
    LOCALES = 'locales'
    NETNAME = 'netname'
    NETIP = 'netip'
    PART = 'partition'
    APP_VER = 'app_version'
    
    def __init__(self):
        '''
        Constructor
        '''
    

    def dumpResult(self, dumpType):
        
        if dumpType & DUMP_SCREEN :
            print('-'*50)
            print("Pass:\t\t%d" %Global.mTestResult[CaseInfo.RESULT_PASS])
            print("Failed:\t\t%d" %Global.mTestResult[CaseInfo.RESULT_FAIL])
            print("NotExecuted:\t%d"%Global.mTestResult[CaseInfo.RESULT_SKIP])
            print("Timeout:\t%d\n"%Global.mTestResult[CaseInfo.RESULT_TIMEOUT])
            print("... in %d s" %(Global.mEndTime-Global.mStartTime))
        
        if dumpType & DUMP_HTML :
            
            shutil.copy(Global.REPORT_FOLDER+os.sep+"charmer_result.css", Global.OUT_LOG+os.sep+"charmer_result.css")
            shutil.copy(Global.REPORT_FOLDER+os.sep+"charmer_result.xsl", Global.OUT_LOG+os.sep+"charmer_result.xsl")
            shutil.copy(Global.REPORT_FOLDER+os.sep+"logo.png", Global.OUT_LOG+os.sep+"logo.png")
            shutil.copy(Global.REPORT_FOLDER+os.sep+"newrule-green.png", Global.OUT_LOG+os.sep+"newrule-green.png")
            
            print("Dump platform information ... ", end="")
           
            systemInfo = {}
            
            systemInfo[self.APP_VER] =  "1.0"
            
            systemInfo[self.PLAT] =  platform.platform()
            
            systemInfo[self.LOCALES] = locale.getdefaultlocale()[1]
            
            systemInfo[self.NETNAME] = socket.getfqdn(socket.gethostname())
            try:
                systemInfo[self.NETIP] = socket.gethostbyname(systemInfo[self.NETNAME])
            except Exception:
                systemInfo[self.NETIP] = "Disconnect"
            
            print("Done")
            
            print("Dump disk information ... ", end="")
           
            services = wmi.WMI(privileges=["security"], find_classes=False)
    
            drive_letters = {}
            
           
            for physical_disk in services.Win32_DiskDrive():
                for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                       
                        size_s = "%.1f" % (int(logical_disk.Size)/1024/1024)
                        freesize_s = "%.1f" % (int(logical_disk.FreeSpace)/1024/1024)
                        
                        usesize_f = "%.1f" % ((int(logical_disk.Size)/1024/1024)-(int(logical_disk.FreeSpace)/1024/1024))
                        usesize_s = str(usesize_f)
                        
                        drive_letters[logical_disk.DeviceID] = size_s+"        "+usesize_s+"        "+freesize_s
            
            letterStr = ""
            for letter in sorted(drive_letters.keys()) :
                letterStr = letterStr+letter+"          "+drive_letters[letter]+";"
                                             
            partContent = "Filesystem   Size(MB)      Used(MB)       Free(MB);"+ \
                letterStr
            
            systemInfo[self.PART] = partContent
            print("Done")
            
            self.dumpHtml(Global.RESULT_HTML, systemInfo)
            
        
    def dumpHtml(self, fileName, systemInfo):
        
        fout = codecs.open(fileName,'w',encoding='utf8')
        fout.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'+"\n")
        fout.write('<?xml-stylesheet type="text/xsl"  href="charmer_result.xsl"?>'+"\n")
        fout.write("<TestResult endtime=\"%s\" starttime=\"%s\" testPlan=\"%s\" version=\"%s\">\n"% \
                   (datetime.fromtimestamp(Global.mEndTime), datetime.fromtimestamp(Global.mStartTime),Global.TEST_PLAN, Global.VERSION))
        fout.write("<DeviceInfo>\n")
        fout.write("<BuildInfo build_model=\"Charmer\" deviceID=\"%s\" buildVersion=\"%s\" locales=\"%s;\" network=\"%s\" partitions=\"%s\"/>\n"% \
                   (systemInfo[self.PLAT], systemInfo[self.APP_VER], systemInfo[self.LOCALES], systemInfo[self.NETIP], systemInfo[self.PART]))
        fout.write("<FeatureInfo>\n")
        #fout.write("<FeatureInfo>\n")
        for feature in Global.mFeatureList.keys() :
            fout.write("<Feature available=\"%s\" name=\"%s\" type=\"sdk\"/>\n"%(Global.mFeatureList[feature],feature))
        
        fout.write("</FeatureInfo>\n")
        fout.write("</DeviceInfo>\n")
        fout.write("<HostInfo name=\"%s\">\n"%systemInfo[self.NETNAME])
        fout.write("<Charmer version=\"%s\">\n"%Global.VERSION)
        
        fout.write("<IntValue name=\"testStatusTimeoutMs\" value=\"%d\"/>\n"%Global.CASE_TIMEOUT)
        
        perfStr = "ProcessName\tBoundary(MB);"
        for monitorObj in Global.MONITOR_PROC.keys() :
            perfStr = perfStr+monitorObj+"\t"+str(Global.MONITOR_PROC[monitorObj])+";"
        
        fout.write("<IntValue name=\"testMonitorPerf\" value=\"%s\"/>\n"%perfStr)
        fout.write("</Charmer>\n")
        fout.write("</HostInfo>\n")
        
        fout.write("<Summary failed=\"%d\" notExecuted=\"%d\" pass=\"%d\" timeout=\"%d\"/>\n"% \
                   (Global.mTestResult[CaseInfo.RESULT_FAIL], Global.mTestResult[CaseInfo.RESULT_SKIP], \
                    Global.mTestResult[CaseInfo.RESULT_PASS], Global.mTestResult[CaseInfo.RESULT_TIMEOUT]))
       
        procPerf = {}
        procCaseName = {}
        
        for moduleName in Global.mCaseManager.getCaseMap().keys() :
            fout.write("<TestPackage name=\"%s\">\n"%moduleName)
            fout.write("<TestSuite>\n")
            
            for caseInfo in Global.mCaseManager.getCaseMap()[moduleName] :
                
                if CaseInfo.START not in caseInfo :
                    continue
                
                if CaseInfo.PERF in caseInfo :
                    
                    perfResultMap = caseInfo[CaseInfo.PERF]
                    for pidName in perfResultMap.keys() :
                        processPerfObj = perfResultMap[pidName]
                        
                        if  not processPerfObj.mProcessName in procPerf :
                            procPerf[processPerfObj.mProcessName] = PerfMonitor.ProcessPerf()
                            procPerf[processPerfObj.mProcessName].mCategoryList = processPerfObj.mCategoryList
                            procCaseName[processPerfObj.mProcessName] = []
                            
                            for aCategory in processPerfObj.mCategoryList:
                                procCaseName[processPerfObj.mProcessName].append(moduleName+"."+caseInfo[CaseInfo.ID])
                                
                            
                        elif procPerf[processPerfObj.mProcessName] != None:
                            
                            count = 0
                            for aPerfObj in processPerfObj.mCategoryList:
                                if procPerf[processPerfObj.mProcessName].mCategoryList[count].mMaxValue < aPerfObj.mMaxValue :
                                    procPerf[processPerfObj.mProcessName].mCategoryList[count] = aPerfObj
                                    procCaseName[processPerfObj.mProcessName][count] = moduleName+"."+caseInfo[CaseInfo.ID]
                                count += 1
                            '''
                            if  not processPerfObj.mProcessName in procPerf :
                                procPerf[processPerfObj.mProcessName] = processPerfObj
                                procPackage[processPerfObj.mProcessName] = moduleName+"."+caseInfo[CaseInfo.ID]
                            
                            elif procPerf[processPerfObj.mProcessName].mMaxMemory < processPerfObj.mMaxMemory :
                                procPerf[processPerfObj.mProcessName] = processPerfObj
                                procPackage[processPerfObj.mProcessName] = moduleName+"."+caseInfo[CaseInfo.ID]
                            '''
                    
                    
                startTime = ""
                endTime = ""
                if CaseInfo.END in caseInfo :
                    endTime = datetime.fromtimestamp(caseInfo[CaseInfo.END])
                if CaseInfo.START in caseInfo :
                    startTime = datetime.fromtimestamp(caseInfo[CaseInfo.START])
                
                logPath = Util.convertToPath(moduleName)
                logPath = logPath +os.sep+caseInfo[CaseInfo.ID]+os.sep+"detailResult.xml"
                
                if caseInfo[CaseInfo.RESULT] == CaseInfo.RESULT_FAIL :
                    
                    message = ''
                    if CaseInfo.ERROR in caseInfo:
                        message = FileUtil.replaceXmlRemainedKey(caseInfo[CaseInfo.ERROR])
                   
                    
                    fout.write("<Test endtime=\"%s\" name=\"%s\" result=\"%s\" starttime=\"%s\" logPath=\"%s\" message=\"%s\"/>\n"% \
                               (endTime, caseInfo[CaseInfo.ID]+": "+FileUtil.replaceXmlRemainedKey(caseInfo[CaseInfo.DESCRP]), CaseInfo.resultToString(caseInfo[CaseInfo.RESULT]), startTime, logPath, message))
                else:        
                    fout.write("<Test endtime=\"%s\" name=\"%s\" result=\"%s\" starttime=\"%s\" logPath=\"%s\"/>\n"% \
                               (endTime, caseInfo[CaseInfo.ID]+": "+FileUtil.replaceXmlRemainedKey(caseInfo[CaseInfo.DESCRP]), CaseInfo.resultToString(caseInfo[CaseInfo.RESULT]), startTime, logPath))
            
            fout.write("</TestSuite>\n")
            fout.write("</TestPackage>\n")
        
        if len(procPerf.keys()) > 0  :
            fout.write("<Performance>\n")
            for procName in procPerf.keys():
                fout.write("\t<Proc name=\"%s\">"%procName)
                count = 0;
                for aCategory in procPerf[procName].mCategoryList:
                    fout.write("\t\t<Category maximum=\"%f (%s)\" average=\"%f\"/>\n"%(aCategory.mMaxValue, procCaseName[procName][count], aCategory.mAveValue))
                    count += 1
                fout.write("\t</Proc>")
            
            fout.write(" <Category>\n") 
            for aCategory in procPerf[procName].mCategoryList:
                fout.write("\t<Descrip name=\"%s\"/>\n"%aCategory.mName)
            fout.write(" </Category>\n") 
                
            fout.write("</Performance>\n")
        
        fout.write("</TestResult>\n")
        fout.close()
        
def dumpCaseAsHtml(caseInfo, folderName):
    
    fileName = folderName+"\\detailResult.xml" 
    
    fout = codecs.open(fileName,'w',encoding='utf8')
    fout.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'+"\n")
    fout.write('<?xml-stylesheet type="text/xsl"  href="detail_result.xsl"?>'+"\n")
    fout.write("<TestResult>\n")
    fout.write("<CaseInfo>\n")
    
    startTime = ""
    endTime = ""
    errorMessage = ""
    traceStr = ""
    errorHandler = Global.DEFAULT_ERROR_HANDLER
    type = "Default"
    
    if CaseInfo.END in caseInfo and caseInfo[CaseInfo.END] != None:
        endTime = datetime.fromtimestamp(caseInfo[CaseInfo.END])
    if CaseInfo.START in caseInfo and caseInfo[CaseInfo.START] != None:
        startTime = datetime.fromtimestamp(caseInfo[CaseInfo.START])
    if CaseInfo.ERROR in caseInfo and caseInfo[CaseInfo.ERROR] != None:
        errorMessage = FileUtil.replaceXmlRemainedKey(caseInfo[CaseInfo.ERROR])
    if Global.mCaseManager.getTraceStack() != None :
        traceStr = FileUtil.replaceXmlRemainedKey(Global.mCaseManager.getTraceStack())
    
    if CaseInfo.HERROR in caseInfo and caseInfo[CaseInfo.HERROR]!= None :
        errorHandler = caseInfo[CaseInfo.HERROR]
    
    if CaseInfo.TYPE in caseInfo and caseInfo[CaseInfo.TYPE]!= None :
        type = caseInfo[CaseInfo.TYPE]
    
    
    fout.write("<CaseID name=\"%s\"/>\n"%(caseInfo[CaseInfo.ID]))
    fout.write("<Description name=\"%s\"/>\n"%(caseInfo[CaseInfo.DESCRP]))
    fout.write("<Result name=\"%s\"/>\n"%(CaseInfo.resultToString(caseInfo[CaseInfo.RESULT])))
    fout.write("<Duration name=\"%d ms\"/>\n"%(caseInfo[CaseInfo.DURATION]))
    fout.write("<Timeout name=\"%s\"/>\n"%(caseInfo[CaseInfo.TIMEOUT]))
    fout.write("<Type name=\"%s\"/>\n"%(CaseInfo.typeToString(type)))
    fout.write("<ErrorHandler name=\"%s\"/>\n"%(FileUtil.replaceXmlRemainedKey(str(errorHandler.__class__))))
    fout.write("<StartTime name=\"%s\"/>\n"%(startTime))
    fout.write("<EndTime name=\"%s\"/>\n"%(endTime))
    fout.write("<ErrorMessage name=\"%s\"/>\n"%(errorMessage))
    fout.write("<TraceStack name=\"%s\"/>\n"%(traceStr))
    
    if caseInfo[CaseInfo.PERF] != None and len(caseInfo[CaseInfo.PERF].keys()) > 0 :
        fout.write("<Performance>\n")
        
        perfObj = None
        for procKey in caseInfo[CaseInfo.PERF].keys() :
            perfObj = caseInfo[CaseInfo.PERF][procKey]
            fout.write("  <Proc name=\"%s\" pid=\"%d\" detail=\"%s\">\n"% \
                       (perfObj.mProcessName, perfObj.mPid, "."+os.sep+procKey+".html"))
            for aCategory in perfObj.mCategoryList :
                fout.write("\t<Category maximum=\"%f\" average=\"%f\"/>\n"%(aCategory.mMaxValue, aCategory.mAveValue))
                
            fout.write("  </Proc>\n")
        fout.write("<Category>\n")
        for categoryObj in perfObj.mCategoryList:
            fout.write("\t<Descrip name=\"%s\"/>\n"%categoryObj.mName)
        fout.write("</Category>\n")
        fout.write("</Performance>\n")
    
    fout.write("</CaseInfo>\n")
    fout.write("</TestResult>\n")
    fout.close()
    
    shutil.copy(Global.REPORT_FOLDER+os.sep+"charmer_result.css", folderName+os.sep+"charmer_result.css")
    shutil.copy(Global.REPORT_FOLDER+os.sep+"detail_result.xsl", folderName+os.sep+"detail_result.xsl")
    shutil.copy(Global.REPORT_FOLDER+os.sep+"logo.png", folderName+os.sep+"logo.png")
    shutil.copy(Global.REPORT_FOLDER+os.sep+"newrule-green.png", folderName+os.sep+"newrule-green.png")
    
            
        
        