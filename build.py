#build module
#created 9-6-2018

from maya import cmds

class buildRigSteps(object):
    '''
    make sure to call this class create and build methods at 
    the end when overriding them in your child class.
    '''
    def __init__(self):
        '''
        '''
        cmds.file(new=True, force=True)
        self.modules = {}

    def create(self):
        ''' register modules here.
        '''
        for mod in self.modules.itervalues():
            mod.create()

    def postcreate(self):
        ''' load guide positions
        '''
        pass

    def build(self):
        ''' build modules
        '''
        for mod in self.modules.itervalues():
            mod.build()

    def postbuild(self):
        ''' postbuild modules
        '''
        for mod in self.modules.itervalues():
            mod.postbuild()

    def connect(self):
        ''' connect modules here
        '''
        for mod in self.modules.itervalues():
            mod.connect()
        pass

    def postconnect(self):
        ''' load constraints/skinning/others.
        '''
        pass

    def run(self):
        ''' run all necessary methods to build rig
        '''
        self.create()
        error()
        self.postcreate()

        self.build()
        self.postbuild()

        self.connect()
        self.postconnect()