#rig leg module
#created 9-6-2018
from modules import rigModBase
from commons import rigComUtils
reload(rigComUtils)
reload(rigModBase)

class quadLegIKFK(rigModBase.baseModule):

    def __init__(self, side = 'C', nrElements = 10):
        ''' setup
        '''
        super(quadLegIKFK, self).__init__(side)

        self.chains = ['Ik', 'Fk', 'Blend']
        self.nrElements = nrElements
        
    def create(self):
        ''' create guides
        '''
        for name in self.names:
            self.guides[name] = rigComUtils.createRigGuide(name, self.side)

    def build(self):
        ''' build joints/ctls
        '''
        #create joints and controls
        for chain in self.chains:
            self.joints[chain] = {}
            for i in range(0, self.nrElements):
                joint = cmds.joint(n = '%s_Spine%s_%s_Jnt'%(self.side, i, chain))
                cmds.delete(cmds.parentConstraint(self.guides[name], joint))
                self.joints[chain][name] = joint

        #create IK Spline setup

        #create FK setup


    def getBottom(self):
        ''' return bottom controller of this module
        '''
        return self.controls['footBall']

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.controls['hip']