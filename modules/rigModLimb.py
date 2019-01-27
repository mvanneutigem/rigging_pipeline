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
                joint = cmds.joint(n = '%s_%s_%s_Jnt'%(self.side, name, chain))
                cmds.delete(cmds.parentConstraint(self.guides[name], joint))
                cmds.makeIdentity(joint, apply=True)
                self.joints[chain][name] = joint
                cmds.select(cl=True)
                if chain is not 'Blend':
                    #TO DO: control class
                    control = cmds.circle(nr=(1,0,0), 
                                          c=(0, 0, 0), 
                                          r=3, n='%s_%s_%s_Ctl'%(self.side, name, chain))
                    cmds.delete(cmds.parentConstraint(self.guides[name], control))
                    cmds.makeIdentity(control, apply=True)
                    self.controls[chain][name] = control[0]

                #create FK setup
                if chain == 'Fk':
                    cmds.parentConstraint(control, joint)
        
        fkGrp = cmds.group(
            self.joints['Fk'].values(),
            self.controls['Fk'].values(),
            n='%s_Fk_Grp'%self.side
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
            n='%s_Top_Grp'%self.side
            )
        
        cmds.group(
            self.topGrp,
            n='%s_%s_Module'%(self.side,self.moduleName)
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
            'locator', 
            n='%s_%s_Global_Attr'%(self.side,self.moduleName)
        )
        parentNode = cmds.listRelatives(ikfkAttr, p=True)
        cmds.addAttr(
            ikfkAttr, 
            longName = 'ikFkSwitch', 
            attributeType='enum', 
            enumName='IK:FK'
        )
        cmds.setAttr('%s.ikFkSwitch'%ikfkAttr, cb=True)
        cmds.setAttr('%s.visibility'%ikfkAttr, 0)
        for control in self.controls['Ik'].values():
            cmds.parent(ikfkAttr, control, add=True, shape=True)
        for control in self.controls['Fk'].values():
            cmds.parent(ikfkAttr, control, add=True, shape=True)
        
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
            cmds.setAttr('%s.ikFkSwitch'%ikfkAttr, 0)
            cmds.setAttr('%s.visibility'%self.controls['Ik'][name],1)
            cmds.setAttr('%s.visibility'%self.controls['Fk'][name],0)
            cmds.setDrivenKeyframe(
                '%s.visibility'%self.controls['Ik'][name],
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
            cmds.setDrivenKeyframe(
                '%s.visibility'%self.controls['Fk'][name],
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
        
            cmds.setDrivenKeyframe(
                '%s.%s_%s_Ik_JntW0'%(constraint, self.side, name),
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
            cmds.setDrivenKeyframe(
                '%s.%s_%s_Fk_JntW1'%(constraint, self.side, name),
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
            
            # joint follow
            cmds.setAttr('%s.ikFkSwitch'%ikfkAttr, 1)
            cmds.setAttr('%s.%s_%s_Ik_JntW0'%(constraint, self.side, name), 0)
            cmds.setAttr('%s.%s_%s_Fk_JntW1'%(constraint, self.side, name), 1)
            cmds.setDrivenKeyframe(
                '%s.%s_%s_Ik_JntW0'%(constraint, self.side, name),
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
            cmds.setDrivenKeyframe(
                '%s.%s_%s_Fk_JntW1'%(constraint, self.side, name),
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
            # controller visibility.
            cmds.setAttr('%s.visibility'%self.controls['Ik'][name],0)
            cmds.setAttr('%s.visibility'%self.controls['Fk'][name],1)
            cmds.setDrivenKeyframe(
                '%s.visibility'%self.controls['Ik'][name],
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
            cmds.setDrivenKeyframe(
                '%s.visibility'%self.controls['Fk'][name],
                cd='%s.ikFkSwitch'%ikfkAttr,
            )
        
        attrHolder = cmds.rename(parentNode, '%s_%s_Global_AttrHolder'%(self.side, self.moduleName))
        
        return cmds.group(
            self.joints['Blend'].values(),
            attrHolder,
            n='%s_Blend_Grp'%self.side
        )