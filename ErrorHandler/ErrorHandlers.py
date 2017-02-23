'''
Created on 2013-11-28

@author: dongmingchang
'''
import ErrorHandler.BaseErrorHandler as BaseErrorHandler
import Global

class DefaultErrorHandler(BaseErrorHandler.BaseErrorHandler):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def handler(self, params):
        super(DefaultErrorHandler, self).handler(params)
        raise BaseErrorHandler.FailException(params[Global.ERROR_MESSAGE])

class AdditionErrorHandler(BaseErrorHandler.BaseErrorHandler):
    
    mAdditionFunc = None
    mAdditionParams = None
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def registerAdditionFunc(self, funcObj, *params):
        self.mAdditionFunc = funcObj
        self.mAdditionParams = params
    
    def handler(self, params):
        
        super(AdditionErrorHandler, self).handler(params)
        if self.mAdditionFunc != None :
            self.mAdditionFunc(*(self.mAdditionParams))
        
        raise BaseErrorHandler.FailException(params[Global.ERROR_MESSAGE])
       
class IgnoreErrorHandler(BaseErrorHandler.BaseErrorHandler):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def handler(self, params): 
        pass
    
class NotifyErrorHandler(BaseErrorHandler.BaseErrorHandler):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def handler(self, params): 
        raise BaseErrorHandler.FailException('')