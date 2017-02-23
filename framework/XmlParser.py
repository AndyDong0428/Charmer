'''
Created on 2013-11-22

@author: dongmingchang
'''
from xml.etree import ElementTree
import framework.Util as Util
import Global

class cXmlParser(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.mPlan = {}
    
    def readXml(self, xmlFile):
        
        tree = ElementTree.parse(xmlFile)
        root = tree.getroot()
        
        self.mPlan['name'] = root.attrib['name']
        
        self.mPlan['groups'] = []
        for group in root:
            groupData = {}
            groupData['precondition'] = group.attrib['precondition']
            groupData['postcondition'] = group.attrib['postcondition']
            
            caseList = {}
            for case in group:
                (moduleName, caseId) = Util.getModuleAndAPI(case.text)
                moduleName = Global.CASE_FOLDER + "." +moduleName
                
                if moduleName not in caseList: caseList[moduleName] = []
                
                caseList[moduleName].append(caseId)
                
            groupData['cases'] = caseList
            self.mPlan['groups'].append(groupData)
            
    def getPlanName(self):
        return self.mPlan['name']
    
    def getGroupCount(self):
        return len(self.mPlan['groups'])
    
    def getGroupCondition(self, index):
        return self.mPlan['groups'][index]['precondition'], self.mPlan['groups'][index]['postcondition']
    
    def getCaseList(self, index):
        return self.mPlan['groups'][index]['cases']
        
        

        