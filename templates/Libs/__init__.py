from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword, LibraryComponent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webcolors import *
import time
import os
from .keywords import *

__version__ = '1.0.0'

class MyCustomizedLibrary(SeleniumLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        SeleniumLibrary.__init__(self, 30)
        self.add_library_components([BrowserKeywords(self), ElementKeywords(self), MyCustomizedLibraryKeywords(self)])
