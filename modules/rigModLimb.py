#rig leg module
#created 9-6-2018
from modules import rigModBase
# reload(rigModBase)

from maya import cmds

class limbIKFK(rigModBase.baseModule):
    '''Base ikfk limb module.'''
    def __init__(self, side = 'C'):
        ''' setup
        '''
        super(limbIKFK, self).__init__(side)
        self.moduleName = 'limb'
        self.names = []
        self.chains = []

    def build(self):
        ''' build joints/ctls setup
        '''
        #create joints and controls
        for chain in self.chains:
            self.joints[chain] = {}
            self.controls[chain] = {}
            for name in self.names:
                cmds.select(cl=True)
                joint = cmds.joint(n = '{0}_{1}_{2}_Jnt'.format(self.side, name, chain))
                cmds.delete(cmds.parentConstraint(self.guides[name], joint))
                cmds.makeIdentity(joint, apply=True)
                self.joints[chain][name] = joint
                cmds.select(cl=True)
                if chain is not 'Blend':
                    #TO DO: control class
                    control = cmds.circle(nr=(1,0,0), 
                                          c=(0, 0, 0), 
                                          r=3, n='{0}_{1}_{2}_Ctl'.format(self.side, name, chain))
                    cmds.delete(cmds.parentConstraint(self.guides[name], control))
                    cmds.makeIdentity(control, apply=True)
                    self.controls[chain][name] = control[0]

                #create FK setup
                if chain == 'Fk':
                    cmds.parentConstraint(control, joint)
        
        fkGrp = cmds.group(
            self.joints['Fk'].values(),
            self.controls['Fk'].values(),
            n='{0}_Fk_Grp'.format(self.side)
        )
        for i in range(len(self.controls['Fk'])-1):
            cmds.parent(
                self.controls['Fk'][self.names[i+1]], 
                self.controls['Fk'][self.names[i]]
            )

        ikGrp = self._setupIkGrp()
        blendGrp = self._setupBlendGrp()
        
        self.topGrp = cmds.group(
            blendGrp,
            ikGrp,
            fkGrp,
            n='{0}_Top_Grp'.format(self.side)
            )
        
        cmds.group(
            self.topGrp,
            n='{0}_{1}_Module'.format(self.side,self.moduleName)
            )
    
    def getBottom(self):
        ''' return bottom controller of this module
        '''
        return self.joints['Blend'][self.names[-1]]

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.topGrp

    def _setupIkGrp(self):
        '''Set up Ik Grp, needs to be implemented.
        '''
        return None
    
    def _setupBlendGrp(self):
        '''Set up Blend Grp
        '''
        #instance ikfk attr
        ikfkAttr = cmds.createNode(
            'transform', 
            n='{0}_{1}_Global_Attr'.format(self.side,self.moduleName)
        )

        parentNode = cmds.listRelatives(ikfkAttr, p=True)
        cmds.addAttr(
            ikfkAttr, 
            longName = 'ikFkSwitch', 
            attributeType='enum', 
            enumName='IK:FK'
        )
        cmds.setAttr('{0}.ikFkSwitch'.format(ikfkAttr), cb=True)
        
        #create Blend setup
        for name in self.names:
            cmds.parentConstraint(
                self.joints['Ik'][name], 
                self.joints['Blend'][name],
                w=1
            )
            constraint = cmds.parentConstraint(
                self.joints['Fk'][name], 
                self.joints['Blend'][name],
                w=0
            )[0]
            cmds.setAttr('{0}.ikFkSwitch'.format(ikfkAttr), 0)
            cmds.setAttr('{0}.visibility'.format(self.controls['Ik'][name]),1)
            cmds.setAttr('{0}.visibility'.format(self.controls['Fk'][name]),0)
            cmds.setDrivenKeyframe(
                '{0}.visibility'.format(self.controls['Ik'][name]),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
            cmds.setDrivenKeyframe(
                '{0}.visibility'.format(self.controls['Fk'][name]),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
        
            cmds.setDrivenKeyframe(
                '{0}.{1}_{2}_Ik_JntW0'.format(constraint, self.side, name),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
            cmds.setDrivenKeyframe(
                '{0}.{1}_{2}_Fk_JntW1'.format(constraint, self.side, name),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
            
            # joint follow
            cmds.setAttr('{0}.ikFkSwitch'.format(ikfkAttr), 1)
            cmds.setAttr('{0}.{1}_{2}_Ik_JntW0'.format(constraint, self.side, name), 0)
            cmds.setAttr('{0}.{1}_{2}_Fk_JntW1'.format(constraint, self.side, name), 1)
            cmds.setDrivenKeyframe(
                '{0}.{1}_{2}_Ik_JntW0'.format(constraint, self.side, name),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
            cmds.setDrivenKeyframe(
                '{0}.{1}_{2}_Fk_JntW1'.format(constraint, self.side, name),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
            # controller visibility.
            cmds.setAttr('{0}.visibility'%self.controls['Ik'][name],0)
            cmds.setAttr('{0}.visibility'%self.controls['Fk'][name],1)
            cmds.setDrivenKeyframe(
                '{0}.visibility'.format(self.controls['Ik'][name]),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
            cmds.setDrivenKeyframe(
                '{0}.visibility'.format(self.controls['Fk'][name]),
                cd='{0}.ikFkSwitch'.format(ikfkAttr),
            )
        
        for control in self.controls['Ik'].values():
            for axis in 'XYZ':
                cmds.setAttr('{0}.scale{1}'.format(control, axis), keyable=False, channelBox=False, lock=True)
        for control in self.controls['Fk'].values():
            for axis in 'XYZ':
                cmds.setAttr('{0}.scale{1}'.format(control, axis), keyable=False, channelBox=False, lock=True)
                cmds.setAttr('{0}.translate{1}'.format(control, axis), keyable=False, channelBox=False, lock=True)
        
        attrHolder = cmds.rename(parentNode, '{0}_{0}_Global_AttrHolder'.format(self.side, self.moduleName))
        
        return cmds.group(
            self.joints['Blend'].values(),
            attrHolder,
            n='{0}_Blend_Grp'.format(self.side)
        )