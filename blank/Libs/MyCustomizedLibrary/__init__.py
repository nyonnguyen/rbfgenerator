from SeleniumLibrary import SeleniumLibrary
from .keywords import *
from .extendedkeywords import *

__version__ = '1.0.0'

class MyCustomizedLibrary(SeleniumLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        SeleniumLibrary.__init__(self, 30)
        self.add_library_components([Module1(self), Module2(self), OtherModules(self)])
