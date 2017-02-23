'''
Created on 2013-11-28

@author: dongmingchang
'''
import os

def traverseFolder(folder):
    infos = []
    for root, dirs, files in os.walk(folder): # Walk directory tree
        for f in files:
            infos.append(root+os.sep+f)
    return infos

def replaceXmlRemainedKey(srcStr):
    srcStr = srcStr.replace("&","&amp;")
    srcStr = srcStr.replace(">","&gt;")
    srcStr = srcStr.replace("<","&lt;")
    srcStr = srcStr.replace("'","&apos;")
    srcStr = srcStr.replace("\"","&quot;")
    
    return srcStr