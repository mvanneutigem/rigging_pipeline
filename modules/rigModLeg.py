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
        ''' build joints/ctls
        '''
        #create joints
        for chain in self.chains:
            self.joints[chain] = {}
            for name in self.names:
                joint = cmds.joint('%s_%s_%s_Jnt'%(self.side, name, chain))
                cmds.delete(cmds.parentConstraint(joint, self.guides[name]))
                self.joints[chain][name] = blend

        #create IK setup


        #create FK setup


    def getBottom(self):
        ''' return bottom controller of this module
        '''
        return self.controls['footBall']

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.controls['hip']