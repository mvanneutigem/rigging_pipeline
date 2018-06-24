#leopard build module
#created 9-6-2018

import build
from modules import rigModLeg

reload(build)
reload(rigModLeg)

class buildRigSteps(build.buildRigSteps):

    def __init__(self, asset_name='leopard'):
        super(buildRigSteps, self).__init__(asset_name)

    def create(self):
        self.modules['rightLeg'] = rigModLeg.quadLegIKFK('R')
        self.modules['leftLeg'] = rigModLeg.quadLegIKFK('L')

        super(buildRigSteps, self).create()