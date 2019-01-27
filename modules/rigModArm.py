#rig leg module
#created 9-6-2018
from modules import rigModLimb
# reload(rigModLimb)

from maya import cmds

class armIKFK(rigModLimb.limbIKFK):

    def __init__(self, side = 'C'):
        ''' setup
        '''
        super(armIKFK, self).__init__(side)
        
        self.moduleName = 'Arm'
        self.names = ['Shoulder', 'Elbow', 'Wrist']
        self.chains = ['Ik', 'Fk', 'Blend']
    
    def _setupIkGrp(self):
        '''Set up Ik Grp
        '''
        for i in range(len(self.joints['Ik'])-1):
            cmds.parent(
                self.joints['Ik'][self.names[i+1]], 
                self.joints['Ik'][self.names[i]]
            )
        
        elbowHandle = cmds.ikHandle(
            n = '%s_%s_ikHandle'%(self.side,self.names[1]),
            startJoint = self.joints['Ik'][self.names[0]],
            endEffector  = self.joints['Ik'][self.names[2]],
            solver = "ikRPsolver"
        )[0]
        cmds.poleVectorConstraint( 
            self.controls['Ik'][self.names[1]], 
            elbowHandle
        )

        cmds.parentConstraint(
            self.controls['Ik'][self.names[2]], 
            elbowHandle, mo=True
        )
        
        return cmds.group(
            elbowHandle,
            self.joints['Ik'][self.names[0]],
            self.controls['Ik'].values(),
            n='%s_Ik_Grp'%self.side
        )
    