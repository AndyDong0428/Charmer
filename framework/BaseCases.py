'''
Created on 2013-11-28

@author: dongmingchang
'''
import Global

SETUP_FUNC= "setUp"
TEARDOWN_FUNC = "tearDown"
PROLOG_FUNC= "prolog"
EPILOG_FUNC = "epilog"

class Cases(object):
    '''
    classdocs
    '''
    
    mErrorHandler = None
    

    def __init__(self):
        '''
        Constructor
        '''
        self.mErrorHandler = Global.DEFAULT_ERROR_HANDLER
        
    def setErrorHandler(self, errorHandler):
        self.mErrorHandler = errorHandler
    
    def getErrorHandler(self):
        return self.mErrorHandler
    
    #Execute before executing a case    
    def setUp(self, errorHandler):
        pass
    
    #Execute after executing a case
    def tearDown(self, errorHandler):
        pass
    
    #Execute before executing all cases in case class
    def prolog(self, errorHandler):
        pass
    
    #Execute after executing all cases in case class
    def epilog(self, errorHandler):
        pass