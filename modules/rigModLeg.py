#rig leg module
#created 9-6-2018
from modules import rigModBase
from commons import rigComUtils
reload(rigComUtils)
reload(rigModBase)

from maya import cmds

class quadLegIKFK(rigModBase.baseModule):

    def __init__(self, side = 'C'):
        ''' setup
        '''
        super(quadLegIKFK, self).__init__(side)

        self.names = ['Hip', 'Knee', 'Ankle', 'FootBall']
        self.chains = ['Ik', 'Fk', 'Blend']
        
    def create(self):
        ''' create guides
        '''
        for name in self.names:
            self.guides[name] = rigComUtils.createRigGuide(name, self.side)

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
        
        for i in range(len(self.controls['Fk'])-1):
            cmds.parent(
                self.controls['Fk'][self.names[i+1]], 
                self.controls['Fk'][self.names[i]]
            )

        fkGrp = cmds.group(
            self.joints['Fk'].values(),
            self.controls['Fk'].values(),
            n='%s_Fk_Grp'%self.side
        )

        #create IK setup
        for i in range(len(self.joints['Ik'])-1):
            cmds.parent(
                self.joints['Ik'][self.names[i+1]], 
                self.joints['Ik'][self.names[i]]
            )
        
        kneeHandle = cmds.ikHandle(
            n = '%s_Knee_ikHandle'%self.side,
            startJoint = self.joints['Ik'][self.names[0]],
            endEffector  = self.joints['Ik'][self.names[2]],
            solver = "ikRPsolver"
        )
        ankleHandle = cmds.ikHandle(
            n = '%s_Ankle_ikHandle'%self.side,
            startJoint = self.joints['Ik'][self.names[1]],
            endEffector  = self.joints['Ik'][self.names[3]],
            solver = "ikRPsolver" 
        )
        footBallHandle = cmds.ikHandle(
            n = '%s_FootBall_ikHandle'%self.side,
            startJoint = self.joints['Ik'][self.names[2]],
            endEffector  = self.joints['Ik'][self.names[3]],
            solver = "ikSCsolver"
        )
        cmds.poleVectorConstraint( 
            self.controls['Ik'][self.names[1]], 
            kneeHandle[0] 
        )
        cmds.poleVectorConstraint( 
            self.controls['Ik'][self.names[2]], 
            ankleHandle[0] 
        )

        cmds.parentConstraint(
            self.controls['Ik'][self.names[3]], 
            kneeHandle[0], mo=True
        )
        cmds.parentConstraint(
            self.controls['Ik'][self.names[3]], 
            ankleHandle[0], mo=True
        )
        cmds.parentConstraint(
            self.controls['Ik'][self.names[3]], 
            footBallHandle[0], mo=True
        )
        
        ikGrp = cmds.group(
            kneeHandle,
            ankleHandle,
            footBallHandle,
            self.joints['Ik'][self.names[0]],
            self.controls['Ik'].values(),
            n='%s_Ik_Grp'%self.side
        )

        #instance ikfk attr
        ikfkAttr = cmds.createNode(
            'locator', 
            n='%s_Leg_Global_Attr'%self.side
        )
        parentNode = cmds.listRelatives(ikfkAttr, p=True)
        cmds.addAttr(
            ikfkAttr, 
            longName = 'ikFkSwitch', 
            attributeType='enum', 
            enumName='IK:FK'
        )
        cmds.setAttr('%s.ikFkSwitch'%ikfkAttr, cb=True)
        for control in self.controls['Ik'].values():
            cmds.parent(ikfkAttr, control, add=True, shape=True)
        for control in self.controls['Fk'].values():
            cmds.parent(ikfkAttr, control, add=True, shape=True)
        
        cmds.rename(parentNode, '%s_Leg_Global_AttrHolder'%self.side)
        
        #create Blend setup
        

    def getBottom(self):
        ''' return bottom controller of this module
        '''
        #TO DO: use different hook for top and bottom.
        return self.joints['Blend']['FootBall']

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.joints['Blend']['Hip']