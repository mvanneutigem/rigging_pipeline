#guide IO module
#created 9-6-2018

import os
from maya import cmds

def loadGuides(asset_name):
    '''load guide trnasforms from file if exists
    '''

def saveGuides(asset_name):
    '''save guide transforms to file
    '''

    fileLoc = __file__
    basePath = fileLoc.split('io')[0]
    fullPath = os.path.join(basePath, asset_name, 'rigdata', 'guides')

    guides = cmds.ls('*_Guide')

    with open(fullPath, 'w') as file: 
        file.write()