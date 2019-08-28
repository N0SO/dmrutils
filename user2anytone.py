#!/bin/python
from dmrutils import DMRUtils
import argparse
ANYTONE_VERS='1.0.0'

"""
User2Anytone - Child class of DMRUtils
Converts RADIOID.NET user.csv file to format required
by the Anytone 868/878 Handheld radios.
"""
class User2Anytone(DMRUtils):
    def __init__(self, filename = None):
        self.VERSION = ANYTONE_VERS
        if (filename):
            self.dmrMain(filename)
        pass
"""
Aurgument Parser Class
This may need to be modified for each individual type.
"""
class get_args():
    def __init__(self):
        self.args = self.getargs()

    def __get_app_version__(self):
        TEMP = User2Anytone()
        return TEMP.__version__()
            
    def getargs(self):
        version = self.__get_app_version__()
        parser = argparse.ArgumentParser(
            description = 'Convert RADIOID.NET user.csv file to ' + \
                          'Anytone AT-8x8 UV Format.',
            epilog = 'Output file will be in the same ' + \
                     'location as the source with ' + \
                     '-AnyTone-YYYYMMDD-HHMMSS embedded ' + \
                     'in the file name.')
        parser.add_argument('-v', '--version', action='version',
                                               version = version)
        parser.add_argument("-i", "--inputpath", default=None,
            help='Specifies the path to the DMR ID ' + \
                 'file in .csv format.')
        return parser.parse_args()


"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   args = get_args()
   app = User2Anytone(args.args.inputpath.strip())
   
