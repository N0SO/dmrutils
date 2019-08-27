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

CS800D_VERS = '0.0.3'
CS800Dfieldnames = ['No','Call Alias', \
                         'Call Type', \
			             'Call ID', \
                         'Receive Tone']

class User2CS800D(DMRUtils):

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
        
    def dmrMain(self, filename):
        """
	Overloads and replaces the same
	named method in Parent class
	DMRUtils
	"""
        filestuff = os.path.splitext(filename)
        datestg = datetime.now().strftime('%Y%m%d-%H%M%S')
        data = self.readFile(filename)
 
        new_data = self.processData(data)
          
        self.writeFile(new_data, \
                       filestuff[0] + '-CS800D-' + \
                          datestg \
                          + '.csv', \
                       CS800Dfieldnames)

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
        parser.add_argument('-v', '--version', action='version', version = CS800D_VERS)
        parser.add_argument("-i", "--inputpath", default=None,
            help="Specifies the path to the DMR ID file in .csv format.")
        return parser.parse_args()
    
"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   args = get_args()
   testapp = CS800D(args.args.inputpath.strip())
    
