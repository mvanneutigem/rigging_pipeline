#rig base module
#created 9-6-2018

from maya import cmds

class baseModule(object):

    def __init__(self, side = 'C', parent = None):
        ''' setup
        '''
        self.guides = {}
        self.controls = {}
        self.joints = {}
        self.side = side
        self.parent = parent
        
    def create(self):
        ''' create guides
        '''
        pass

    def build(self):
        ''' build joints/ctls
        '''
        pass

    def postbuild(self):
        ''' remove modules
        '''
        for guide in self.guides.itervalues():
            cmds.delete(guide)

    def getBottom(self):
        ''' return bottom controller of this module
        '''
        return None

    def getTop(self):
        ''' return top controller of this module
        '''
        return None

    def connect(self):
        '''connect to other module
        '''
        if self.parent:
            cmds.parentConstraint(self.getTop(), self.parent.getBottom())