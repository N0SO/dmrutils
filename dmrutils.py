#!/bin/python
from sys import stdin, stdout
import csv
import os
import argparse
#import httplib
import http.client
import traceback
from datetime import datetime

"""
DMRUtils - A collection of methods good for manipulating 
           and processing a DMR ID files.
             
           This base / parent class accepts the user.csv file
           downloaded from https://radioid.net/database/dumps#!
           and converts the file to the format required to
           import into the Anytone 868 and 878 handhelds.
"""
DMRUTILS_VERS = '1.0.7'
RADIOTYPE = 'AnyTone'
ANYTONE878fieldnames = ['No.','Radio ID', \
                        'Callsign', 'Name', \
                        'City', 'State', \
                        'Country', 'Remarks', \
                        'Call Type', 'Call Alert']


class DMRUtils():

    def __init__(self, filename = None):
        self.VERSION = DMRUTILS_VERS
        self.RADIOTYPE = RADIOTYPE
        self.FIELDNAMES = ANYTONE878fieldnames
        if (filename):
            self.dmrMain(filename)
        pass

    def __version__(self):
        return self.VERSION
        
        
    def readFile(self, filename):
        """ 
            Read csv file specified in filename. The first
            row of the .csv file (usually the column headers)
            will be used as field names. The .csv file will
            be read in it's entirety and returned as a list
            of python dictionary items containing key/value 
            pairs. The column header rows become the key
            portion of each pair.
        """
        ret_data =[]
        with open(filename, 'rb') as csv_file:
            csv_data = csv.DictReader(csv_file)
            for item in csv_data:
               ret_data.append(item)
        return ret_data

    def writeFile(self, data, filename):
        with open(filename, 'wb') as new_file:
            csv_writer = csv.DictWriter(new_file,
                                        self.FIELDNAMES)
            csv_writer.writeheader()
            for line in data:
                csv_writer.writerow(line)

    def autowriteFile(self, new_data, filename):
        filestuff = os.path.splitext(filename)
        datestg = datetime.now().strftime('%Y%m%d-%H%M%S')
        newfilepath = filestuff[0] + '-' + self.RADIOTYPE + \
                                           '-' + datestg  + \
                                           '.csv'
        self.writeFile(new_data, newfilepath)
        return newfilepath
                
    def findTag(self, data, key, value):
        retval = None
        for data_item in data:
            if( data_item.get(key == value) ):
                retval = data_item
        return retval
	
    def fetchIDList(self, urlbase, urlpath):
        retdata = None
        try:
            conn = httplib.HTTPSConnection(urlbase)
            conn.request("GET", urlpath)
            r1 = conn.getresponse()
            print("get status: %d -- %s"%(r1.status, r1.reason))
            print("reading data...")
            retdata = r1.read()
            conn.close()
            print("... done!")
        except:
            tb = traceback.format_exc()
            print("Error fetching %s%s"%(urlbase, urlpath))
            print("traceback:\n%s"%(tb))
        return retdata
 


    def processData(self, source_data):
        target_data = []
        linecount = 1
        for line in source_data:
            newline = dict({'No.': linecount, \
                       'Radio ID':line['RADIO_ID'], \
                       'Callsign':line['CALLSIGN'], \
                       'Name':line['FIRST_NAME']+' ' + \
                                    line['LAST_NAME'], \
                       'City': line['CITY'], \
                       'State': line['STATE'], \
                       'Country': line['COUNTRY'], \
                       'Remarks': line['REMARKS'], \
                       'Call Type': 'Private Call', \
                       'Call Alert': 'None'})
            target_data.append(newline)
            linecount += 1
        return target_data    
        
    def dmrMain(self, filename):
        data = self.readFile(filename)
 
        new_data = self.processData(data)

        resultfile = self.autowriteFile(new_data, filename)
                                        
                                        
          

"""
Aurgument Parser Class
This may need to be modified for each individual type.
"""
class get_args():
    def __init__(self):
        self.args = self.getargs()

    def __get_app_version__(self):
        TEMP = DMRUtils()
        return TEMP.__version__()
            
    def getargs(self):
        version = self.__get_app_version__()
        parser = argparse.ArgumentParser(
            description = 'Convert RADIOID.NET user.csv file to ' + \
                          'Anytone AT-8x8 UV Format.',
            epilog = 'This class is normally inherited by another '+ \
                     'for a specific radio or family of radios.')
        parser.add_argument('-v', '--version', action='version', version = version)
        parser.add_argument("-i", "--inputpath", default=None,
            help="Specifies the path to the DMR ID file in .csv format.")
        return parser.parse_args()


"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   args = get_args()
   app = DMRUtils(args.args.inputpath.strip())
