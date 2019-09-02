#rig leg module
#created 9-6-2018
from modules import rigModBase
from commons import rigComUtils
# reload(rigComUtils)
# reload(rigModBase)

from maya import cmds

class spineIK(rigModBase.baseModule):

    def __init__(
            self, 
            side = 'C', 
            nrElements = 10,
            nrControls = 5
        ):
        ''' setup
        '''
        super(spineIK, self).__init__(side)
        
        self.moduleName = 'Spine'
        self.chains = ['Ik']
        self.nrElements = nrElements
        self.nrControls = nrControls
        
    def create(self):
        ''' create guides
        '''
        for i in range(self.nrElements):
            name = '{0}{1}'.format(self.moduleName, i)
            self.guides[name] = rigComUtils.createRigGuide(name, self.side)

    def build(self):
        ''' build joints/ctls
        '''
        #create joints and controls
        for chain in self.chains:
            self.joints[chain] = {}
            self.controls[chain] = {}
            for i in range(0, self.nrElements):
                joint = cmds.joint(n = '{0}_{1}{2}_{3}_Jnt'.format(self.side, self.moduleName, i, chain))
                name = '{0}{1}'.format(self.moduleName, i)
                cmds.delete(cmds.parentConstraint(self.guides[name], joint))
                self.joints[chain][name] = joint
                control = cmds.circle(
                    nr=(1,0,0), 
                    c=(0, 0, 0), 
                    r=3, n='{0}_{1}_{2}_Ctl'.format(self.side, name, chain)
                )
                cmds.delete(cmds.parentConstraint(self.guides[name], control))
                cmds.makeIdentity(control, apply=True)
                self.controls[chain][name] = control[0]

        #create IK Spline setup
        ikGrp = self._setupIkGrp()

    def _setupIkGrp(self):
        '''Set up Ik Grp
        '''
        for i in range(len(self.joints['Ik'])-1):
            cmds.parent(
                self.joints['Ik']['{0}{1}'.format(self.moduleName, i+1)], 
                self.joints['Ik']['{0}{1}'.format(self.moduleName, i)]
            )
        start_joint = '{0}0'.format(self.moduleName)
        end_joint = '{0}{1}'.format(self.moduleName, len(self.joints['Ik'])-1)
        splineHandle = cmds.ikHandle(
            n = '{0}_Spine_ikHandle'.format(self.side),
            startJoint = self.joints['Ik'][start_joint],
            endEffector  = self.joints['Ik'][end_joint],
            solver = "ikSplineSolver",
            numSpans = self.nrControls
        )
        print splineHandle
        error()
        return None
    
    def getBottom(self):
        ''' return bottom controller of this module
        '''
        return self.controls[-1]

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.controls[0]