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
                self.joints[chain][name] = joint
                cmds.select(cl=True)
                control = cmds.circle(nr=(1,0,0), 
                                      c=(0, 0, 0), 
                                      r=1.5, n='%s_%s_%s_Ctl' %(self.side, name, chain))
                cmds.delete(cmds.parentConstraint(self.guides[name], control))
                self.controls[chain][name] = control

                #create FK setup
                if chain == 'Fk':
                    cmds.parentConstraint(control, joint)

        #create IK setup
        cmds.parent(self.joints['Ik']['Knee'], self.joints['Ik']['Hip'])
        cmds.parent(self.joints['Ik']['Ankle'], self.joints['Ik']['Knee'])
        cmds.parent(self.joints['Ik']['FootBall'], self.joints['Ik']['Ankle'])
        kneeHandle = cmds.ikHandle(startJoint = self.joints['Ik']['Hip'],
                      endEffector  = self.joints['Ik']['Ankle'],
                      solver = "ikRPsolver")
        ankleHandle = cmds.ikHandle(startJoint = self.joints['Ik']['Knee'],
                      endEffector  = self.joints['Ik']['FootBall'],
                      solver = "ikRPsolver" )
        footBallHandle = cmds.ikHandle(startJoint = self.joints['Ik']['Ankle'],
                      endEffector  = self.joints['Ik']['FootBall'],
                      solver = "ikSCsolver")
        cmds.poleVectorConstraint( self.controls['Ik']['Knee'], kneeHandle[0] )
        cmds.poleVectorConstraint( self.controls['Ik']['Ankle'], ankleHandle[0] )

        cmds.parentConstraint(self.controls['Ik']['FootBall'], kneeHandle[0], mo=True)
        cmds.parentConstraint(self.controls['Ik']['FootBall'], ankleHandle[0], mo=True)
        cmds.parentConstraint(self.controls['Ik']['FootBall'], footBallHandle[0], mo=True)

        hipGrp = cmds.group(self.joints['Ik']['Hip'], 
                            n=self.joints['Ik']['Hip'].replace('_Jnt','_Grp'))

        #create Blend setup


    def getBottom(self):
        ''' return bottom controller of this module
        '''
        #can also be used for pickwalking
        return self.joints['Blend']['FootBall']

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.joints['Blend']['Hip']