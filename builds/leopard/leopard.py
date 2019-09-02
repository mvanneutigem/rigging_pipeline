#leopard build module
#created 9-6-2018

import build
from modules import rigModLeg, rigModArm, rigModSpine

reload(build)
reload(rigModLeg)
reload(rigModArm)

class buildRigSteps(build.buildRigSteps):

    def __init__(self, asset_name='leopard'):
        super(buildRigSteps, self).__init__(asset_name)

    def create(self):
        self.modules['rightLeg'] = rigModLeg.quadLegIKFK('R')
        self.modules['leftLeg'] = rigModLeg.quadLegIKFK('L')

        self.modules['rightArm'] = rigModArm.armIKFK('R')
        self.modules['leftArm'] = rigModArm.armIKFK('L')
        
        self.modules['spine'] = rigModSpine.spineIK(nrElements=19)
        
        super(buildRigSteps, self).create()