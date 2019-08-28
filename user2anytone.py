#!/bin/python
from dmrutils import *
import argparse

"""
AT8x8U - Child class of DMRUtils
Converts RADIOID.NET user.csv file to format required
by the Anytone 868/878 Handheld radios.
"""


class Usr2Anytone(DMRUtils):
    """
    Base class includes Anytone 868/878 support
    """
    pass

"""
Aurgument Parser Class
This may need to be modified for each individual type.
"""
class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version = DMRUTILS_VERS)
        parser.add_argument("-i", "--inputpath", default=None,
            help="Specifies the path to the DMR ID file in .csv format.")
        return parser.parse_args()



"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   args = get_args()
   testapp = User2Anytone(args.args.inputpath.strip())
   
    
