#guide IO module
#created 9-6-2018

import os
from maya import cmds

def loadGuides(asset_name):
    '''load guide trnasforms from file if exists
    '''
    fileLoc = __file__
    basePath = fileLoc.split('loadSaveIO')[0]
    fullPath = os.path.join(basePath, asset_name, 'rigdata', 'guides.txt')

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
                    print '# WARNING %s was not found'%guide
    except:
        print 'no guides save file found in %s'%fullPath

def saveGuides(asset_name):
    '''save guide transforms to file
    '''

    fileLoc = __file__
    basePath = fileLoc.split('loadSaveIO')[0]
    fullPath = os.path.join(basePath, asset_name, 'rigdata', 'guides.txt')

    guides = cmds.ls('*_Guide')
    print fullPath
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
            file.write('%s;%s;%s\n'%(guide, pos, rot))
