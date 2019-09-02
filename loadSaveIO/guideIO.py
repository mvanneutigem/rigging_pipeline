#guide IO module
#created 9-6-2018
import logging
import os
import re

from maya import cmds

LOGGER = logging.getLogger(__name__)

def loadGuides(asset_name):
    '''load guide trnasforms from file if exists
    
    Args:
        asset_name (str): name of the asset to load the guides for.
    '''
    fileLoc = __file__
    basePath = fileLoc.split('loadSaveIO')[0]
    
    files = []
    folder = os.path.join(basePath, asset_name, 'rigdata')
    for file in os.listdir(folder):
        if file.startswith("guides"):
            files.append(os.path.join(folder, file))
    
    def extract_number(f):
        s = re.findall("\d+$",f)
        return (int(s[0]) if s else -1,f)
    
    fullPath = (max(files,key=extract_number))
    guides = cmds.ls('*_Guide')

    try:
        with open(fullPath, 'r') as file: 
            lines = file.readlines()
            for line in lines:
                guide, pos, rot = line.strip('\n').split(';')
                try:
                    rot = rot.replace(',', '').replace('[', '').replace(']', '')
                    x,y,z = rot.split()
                    cmds.xform(guide, 
                                ws = True, 
                                ro = (float(x),float(y),float(z)))
                    pos = pos.replace(',', '').replace('[', '').replace(']', '')
                    x,y,z = pos.split()
                    cmds.xform(guide, 
                                ws = True,
                                t = (float(x),float(y),float(z)))
                except:
                    LOGGER.warn('# WARNING {0} was not found'.format(guide))
    except:
        LOGGER.warn( '# No guides save file found in {0}'.format(fullPath))

def saveGuides(asset_name):
    '''save guide transforms to file
    
    Args:
        asset_name (str): name of the asset to save the guides for.
    '''
    fileLoc = __file__
    basePath = fileLoc.split('loadSaveIO')[0]
    fullPath = os.path.join(basePath, asset_name, 'rigdata', 'guides.txt')
    i = 0
    while os.path.exists(fullPath):
        fullPath = os.path.join(
            basePath, 
            asset_name, 
            'rigdata', 
            'guidesV{0}.txt'.format(i)
        )
        i += 1

    guides = cmds.ls('*_Guide')

    if not os.path.exists(os.path.join(basePath, asset_name, 'rigdata')):
        os.makedirs(os.path.join(basePath, asset_name, 'rigdata'))

    with open(fullPath, 'w') as file: 
        for guide in guides:
            rot = cmds.xform(guide, 
                            q = True, 
                            ws = True, 
                            ro = True)
            pos = cmds.xform(guide, 
                             q = True,
                             ws = True,
                             t = True)
            file.write('{0};{1};{2}\n'.format(guide, pos, rot))
