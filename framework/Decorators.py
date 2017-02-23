'''
Created on 2014-1-7

@author: dongmingchang
'''
import Global

def Step(func):
    
    def StepExecute(*args, **kwargs):
        if Global.MANUAL :
            input("\n>> %s%s%s ..."%(func.__name__, str(args), str(kwargs)))
        if Global.ADD_FLAG.find("debug") > -1:
            print("\n>> %s%s%s ..."%(func.__name__, str(args), str(kwargs)))
        return func(*args, **kwargs)
    
    return StepExecute


    