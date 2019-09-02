#file IO module
#created 9-6-2018
import logging
import os

from maya import cmds

LOGGER = logging.getLogger(__name__)

def loadModel(asset_name):
    '''load guide trnasforms from file if exists
    '''

    fileLoc = __file__
    basePath = fileLoc.split('\loadSaveIO')[0]
    fullPath = os.path.join(
        basePath, 
        asset_name, 
        'modeldata', 
        '{0}.ma'.format(asset_name)
    )
    
    try:
        cmds.file(fullPath, i=True)
    except:
        LOGGER.warn('no model file found in {0}'.format(fullPath))
