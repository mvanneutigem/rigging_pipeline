#rig leg module
#created 9-6-2018
from modules import rigModBase
from commons import rigComUtils
reload(rigComUtils)
reload(rigModBase)

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
            for name in self.names:
                joint = cmds.joint('%s_%s_%s_Jnt'%(self.side, name, chain))
                cmds.delete(cmds.parentConstraint(joint, self.guides[name]))
                self.joints[chain][name] = joint

                control = cmds.circle(nr=(1,0,0), c=(0, 0, 0), r=1.5, n='%s_%s_%s_Ctl' %(self.side, name, chain))
                cmds.delete(cmds.parentConstraint(control, self.guides[name]))
                self.controls[chain][name] = control

                #create FK setup
                if chain == 'Fk':
                    cmds.parentConstraint(joint, control)

        #create IK setup
        kneeHandle = cmds.ikHandle(startJoint = self.joints['Ik']['Hip'],
                      endJoint = self.joints['Ik']['Ankle'],
                      solver = "ikRPsolver")
        ankleHandle = cmds.ikHandle(startJoint = self.joints['Ik']['Knee'],
                      endJoint = self.joints['Ik']['FootBall'],
                      solver = "ikRPsolver")
        footBallHandle = cmds.ikHandle(startJoint = self.joints['Ik']['Ankle'],
                      endJoint = self.joints['Ik']['FootBall'],
                      solver = "ikSCsolver ")
        cmds.poleVectorConstraint( self.controls['Ik']['Knee'], kneeHandle )
        cmds.poleVectorConstraint( self.controls['Ik']['Ankle'], ankleHandle )

        cmds.parentConstraint(kneeHandle, self.controls['Ik']['FootBall'])
        cmds.parentConstraint(ankleHandle, self.controls['Ik']['FootBall'])
        cmds.parentConstraint(footBallHandle, self.controls['Ik']['FootBall'])

        hipGrp = cmds.group(self.joints['Ik']['Hip'], n=self.joints['Ik']['Hip'].replace('_Jnt','_Grp'))
        cmds.parentConstraint(hipGrp, self.controls['Ik']['Hip'])

        #create Blend setup


    def getBottom(self):
        ''' return bottom controller of this module
        '''
        #can also be used for pickwalking
        return self.controls['footBall']

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.controls['hip']