#!/usr/bin/env python
from sys import stdin, stdout
import csv
import os, sys
import traceback
from datetime import datetime
python_version = sys.version_info[0]
if (python_version == 2):
    #import httplib
    import requests
else:
    #import http.client as httplib
    import requests

"""
DMRUtils - A collection of methods good for manipulating 
           and processing a DMR ID files.
             
           This base / parent class accepts the user.csv file
           downloaded from https://radioid.net/database/dumps#!
           and converts the file to the format required to
           import into the Anytone 868 and 878 handhelds.
Update History:
* Wed Sep 08 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.8 - First interation
- Fixed a crash that occcured when converting the USR.CSV file
- from radioid.net - the source no longer contains a REMARKS
- field. 
- Improved error handling for failure to download the USR.CSV
- file. The error message will be trapped and displayed in the
- main window.
"""
DMRUTILS_VERS = '1.0.8'
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
        with open(filename, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            for item in csv_data:
               ret_data.append(item)
        return ret_data

    def writeFile(self, data, filename):
        with open(filename, 'w') as new_file:
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
	
    def fetchIDList(self, url):
        retdata = []
        rawdata = None
        try:
            print("reading data from %s..."%(url))
            r1 = requests.get(url) 
            r1.encoding = 'utf-8'
            print ("URL read status: %d"%(r1.status_code))
            rawdata = r1.text
            #print('rawdata = \n%s'%(rawdata))
            print("... done!")
        except:
            tb = traceback.format_exc()
            #Load error message instead of data
            rawdata = 'Error fetching %s\n\nError traceback:\n%s'%(url,tb)
            print(rawdata)
        linestg = rawdata.splitlines()
        print ('Creating retdata...')
        for line in linestg:
            nextline = []
            lineparts = line.split(',')
            for nextpart in lineparts:
                nextline.append(nextpart)
            retdata.append(nextline)
            #print (retdata)
        print('...done!')
        return retdata
 
    def processData(self, source_data):
        target_data = []
        linecount = 1
        for line in source_data:
            #print(line)
            newline = dict({'No.': linecount, \
                       'Radio ID':line['RADIO_ID'], \
                       'Callsign':line['CALLSIGN'], \
                       'Name':line['FIRST_NAME']+' ' + \
                                    line['LAST_NAME'], \
                       'City': line['CITY'], \
                       'State': line['STATE'], \
                       'Country': line['COUNTRY'], \
                       #'Remarks': line['REMARKS'], \
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
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   app = DMRUtils()
   print ('VERSION: %s'%(app.__version__()))

