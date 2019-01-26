#file IO module
#created 9-6-2018

import os
from maya import cmds

def loadModel(asset_name):
    '''load guide trnasforms from file if exists
    '''

    fileLoc = __file__
    basePath = fileLoc.split('\loadSaveIO')[0]
    fullPath = os.path.join(basePath, asset_name, 'modeldata', '%s.ma'%asset_name)
    
    try:
        cmds.file(fullPath, i=True)
    except:
        print 'no model file found in %s'%fullPath
