'''
Created on 2014-2-15

@author: dongmingchang
'''

from framework import (
    BaseCases, RegisterCase, CaseInfo, Util
    )


from ErrorHandler import ( ErrorHandlers)

import Global
import time

import os
import sys
sys.path.append("."+os.sep+"SDK")
import FileFunc
import SystemFunc
import ProcessFunc
import time

class DemoTest(BaseCases.Cases):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    def prolog(self, errorHandler):
        
        pass
        
    def epilog(self, errorHandler):
        pass
        
    def setUp(self, errorHandler):
        pass
        
    @RegisterCase.register("Demo failed case", tolerate=2)
    def S01001001(self, errorHandler):
        raise Exception('Exception in S01001001!') 
        

    @RegisterCase.register("Demo success case", tolerate=2)
    def S01001002(self, errorHandler):
        
        time.sleep(5);