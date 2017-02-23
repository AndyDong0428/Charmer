from SDK import (
    IEC, UIFunc
    )
from framework import (
     Decorators)
import win32gui, win32con, win32ui, time
import Global
import traceback

def PushButton(handle, label):
    print(win32gui.GetWindowText(handle))
    if win32gui.GetWindowText(handle).find(label) > 0:
        win32gui.SendMessage(handle, win32con.BM_CLICK, None, None)
        return True

@Decorators.Step
def navigateUrl(errorHandler, url):
    try:
        ie = IEC.IEController()                  # Create a new IE Window.
        ie.Navigate(url)    # Navigate to a website.
            
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True   
    
@Decorators.Step
def downloadFile(errorHandler, url):
    try:
        ie = IEC.IEController()                  # Create a new IE Window.
        ie.Navigate(url)    # Navigate to a website.
        time.sleep(3)
        wnd = win32gui.GetForegroundWindow()
        print(win32gui.GetClassName(wnd))
        if win32gui.GetClassName(wnd).find("#") ==  0:
            win32gui.EnumChildWindows(wnd, PushButton, "&S");
            time.sleep(1)
            wnd = win32gui.GetForegroundWindow()
            if len(wnd) > 0:
                UIFunc.setWindowForeground(wnd[0])
            
        if win32gui.GetClassName(wnd).find("#") ==  0:
            win32gui.EnumChildWindows(wnd, PushButton, "&S");
            if len(wnd) > 0:
                UIFunc.setWindowForeground(wnd[0]) 
            
    except Exception:
        
        errorInfo={Global.ERROR_CALLSTACK:traceback, Global.ERROR_MESSAGE:traceback.format_exc()}
        errorHandler.handler(errorInfo);
        
    return True