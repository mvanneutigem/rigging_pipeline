#rig leg module
#created 9-6-2018
from modules import rigModBase
from commons import rigComUtils
reload(rigComUtils)
# reload(rigModBase)

class spineIK(rigModBase.baseModule):

    def __init__(self, side = 'C', nrElements = 10):
        ''' setup
        '''
        super(spineIK, self).__init__(side)
        
        self.moduleName = 'Spine'
        self.chains = ['Ik']
        self.nrElements = nrElements
        
    def create(self):
        ''' create guides
        '''
        for i in range(self.nrElements):
            name = '%s%s'%(self.moduleName, i)
            self.guides[name] = rigComUtils.createRigGuide(name, self.side)

    def build(self):
        ''' build joints/ctls
        '''
        #create joints and controls
        for chain in self.chains:
            self.joints[chain] = {}
            for i in range(0, self.nrElements):
                joint = cmds.joint(n = '%s_%s%s_%s_Jnt'%(self.side, self.moduleName, i, chain))
                cmds.delete(cmds.parentConstraint(self.guides[name], joint))
                self.joints[chain][name] = joint

        #create IK Spline setup
        ikGrp = self._setupIkGrp()

    def _setupIkGrp(self):
        '''Set up Ik Grp
        '''
        return None
    
    def getBottom(self):
        ''' return bottom controller of this module
        '''
        return self.controls[-1]

    def getTop(self):
        ''' return top controller of this module
        '''
        return self.controls[0]