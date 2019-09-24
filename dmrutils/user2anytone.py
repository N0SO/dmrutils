#!/usr/bin/env python
from dmrutils import DMRUtils

ANYTONE_VERS='1.0.0'

"""
User2Anytone - Child class of DMRUtils
Converts RADIOID.NET user.csv file to format required
by the Anytone 868/878 Handheld radios.
"""
class User2Anytone(DMRUtils):
    def __init__(self, filename = None):
        DMRUtils.__init__(self)
        self.VERSION = ANYTONE_VERS
        if (filename):
            self.dmrMain(filename)
        pass

"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   app = User2Anytone()
   print('Version: %s'%(app.__version__()))
   
