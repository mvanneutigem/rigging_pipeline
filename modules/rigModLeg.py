#rig leg module
#created 9-6-2018
from modules import rigModLimb
# reload(rigModLimb)

from maya import cmds

class quadLegIKFK(rigModLimb.limbIKFK):

    def __init__(self, side = 'C'):
        ''' setup
        '''
        super(quadLegIKFK, self).__init__(side)
        
        self.moduleName = 'Leg'
        self.names = ['Hip', 'Knee', 'Ankle', 'FootBall']
        self.chains = ['Ik', 'Fk', 'Blend']
    
    def _setupIkGrp(self):
        '''Set up Ik Grp
        '''
        for i in range(len(self.joints['Ik'])-1):
            cmds.parent(
                self.joints['Ik'][self.names[i+1]], 
                self.joints['Ik'][self.names[i]]
            )
        
        kneeHandle = cmds.ikHandle(
            n = '{0}_Knee_ikHandle'.format(self.side),
            startJoint = self.joints['Ik'][self.names[0]],
            endEffector  = self.joints['Ik'][self.names[2]],
            solver = "ikRPsolver"
        )[0]
        ankleHandle = cmds.ikHandle(
            n = '{0}_Ankle_ikHandle'.format(self.side),
            startJoint = self.joints['Ik'][self.names[1]],
            endEffector  = self.joints['Ik'][self.names[3]],
            solver = "ikRPsolver" 
        )[0]
        footBallHandle = cmds.ikHandle(
            n = '{0}_FootBall_ikHandle'.format(self.side),
            startJoint = self.joints['Ik'][self.names[2]],
            endEffector  = self.joints['Ik'][self.names[3]],
            solver = "ikSCsolver"
        )[0]
        cmds.poleVectorConstraint( 
            self.controls['Ik'][self.names[1]], 
            kneeHandle
        )
        cmds.poleVectorConstraint( 
            self.controls['Ik'][self.names[2]], 
            ankleHandle
        )

        cmds.parentConstraint(
            self.controls['Ik'][self.names[3]], 
            kneeHandle, mo=True
        )
        cmds.parentConstraint(
            self.controls['Ik'][self.names[3]], 
            ankleHandle, mo=True
        )
        cmds.parentConstraint(
            self.controls['Ik'][self.names[3]], 
            footBallHandle, mo=True
        )
        
        return cmds.group(
            footBallHandle,
            ankleHandle,
            kneeHandle,
            self.joints['Ik']['Hip'],
            self.controls['Ik'].values(),
            n='{0}_Ik_Grp'.format(self.side)
        )
    