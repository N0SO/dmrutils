#!/usr/bin/env python
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
Main program - run stand-alone if not included as part of
a larger application.
"""
if __name__ == '__main__':
   app = User2CS800D()
   print('VERSION: %s'%(app.__version__()))
    
