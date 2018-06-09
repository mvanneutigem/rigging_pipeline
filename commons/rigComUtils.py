#rig commons utils module
#created 9-6-2018

from maya import cmds

def createRigGuide(name, side = 'C'):
    guideName = cmds.spaceLocator(n='%s_%s_Guide'%(side, name))[0]
    cmds.setAttr('%s.displayLocalAxis'%guideName,1)
    return guideName