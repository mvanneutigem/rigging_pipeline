#rig commons utils module
#created 9-6-2018

from maya import cmds

def createRigGuide(name, side = 'C'):
    guideName = cmds.spaceLocator(n='{0}_{1}_Guide'.format(side, name))[0]
    cmds.setAttr('{0}.displayLocalAxis'.format(guideName),1)
    return guideName