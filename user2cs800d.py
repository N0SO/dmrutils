#!/bin/python
import argparse
from datetime import datetime
import os

from dmrutils import DMRUtils



"""
User2CS800D - Child class of DMRUtils
Converts RADIOID.NET user.csv file to format required
by the Connect Systems CS-800D.
"""

CS800D_VERS = '1.0.1'
RADIOTYPE = 'CS800D'
CS800Dfieldnames = ['No','Call Alias', \
                         'Call Type', \
			             'Call ID', \
                         'Receive Tone']

class User2CS800D(DMRUtils):
    def __init__(self, filename = None):
        self.VERSION = CS800D_VERS
        self.RADIOTYPE = RADIOTYPE
        self.FIELDNAMES = CS800Dfieldnames
        if (filename):
            self.dmrMain(filename)
        pass


    def processData(self, source_data):
        """
	    Overloads and replaces the same
	    named method in Parent class
	    DMRUtils
	    """
        target_data = []
        linecount = 1
        for line in source_data:
            newline = dict({'No': linecount, \
                       'Call ID':line['RADIO_ID'], \
                       'Call Alias':line['CALLSIGN'] +',' + \
                                    line['FIRST_NAME']+' ' + \
                                    line['LAST_NAME'], \
                       'Call Type': 'Private Call', \
                       'Receive Tone': 'No'})
            target_data.append(newline)
            linecount += 1
        return target_data
    
"""
Aurgument Parser Class
This may need to be modified for each individual type.
"""
class get_args():
    def __init__(self):
        self.args = self.getargs()

    def __get_app_version__(self):
        TEMP = User2CS800D()
        return TEMP.__version__()
            
    def getargs(self):
        version = self.__get_app_version__()
        parser = argparse.ArgumentParser(
            description = 'Convert RADIOID.NET user.csv ' + \
                          'file to Connect Systems CS-800D ' + \
                          'Format.',
            epilog = 'The CS-800D includes TALK GROUPS in ' + \
                     'this contact list. \nPlease add the ' + \
                     'TALK GROUP list to this file manually ' + \
                     'before inporting to your CPS.')
        parser.add_argument('-v', '--version', action='version',
                                               version = version)
        parser.add_argument("-i", "--inputpath", default=None,
            help='Specifies the path to the DMR ID ' + \
                 'file in .csv format.')
        return parser.parse_args()

        
    
"""
Main program - run stand-alone if not included as part of
a larger application.
"""
if __name__ == '__main__':
   args = get_args()
   app = User2CS800D(args.args.inputpath.strip())
    
