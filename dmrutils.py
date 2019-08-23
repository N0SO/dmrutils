#!/bin/python
from sys import stdin, stdout
import csv
import pprint

"""
DMRUtils - A collection of methods good for manipulating 
             and processing a DMR ID files.
"""
DMRUTILS_VERS = '0.0.1'


class DMRUtils():

    def __init__(self):
        pass

    def __version__(self):
        return DMRUTILS_VERS
        
        
    def readFile(self, filename):
        """ 
            Open variable-based csv, iterate over the 
            rows and map values to a list of dictionaries 
            containing key/value pairs
        """
        ret_data =[]
        with open(filename, 'rb') as csv_file:
            csv_data = csv.DictReader(csv_file)
            for item in csv_data:
               ret_data.append(item)
        return ret_data

    def writeFile(self, data, filename):
    
        fieldnames = ['No.','Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country', 'Remarks', 'Call Type', 'Call Alert']
        
        with open(filename, 'w') as new_file:
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for line in data:
                csv_writer.writerow(line)

    def processData(self, source_data):
        target_data = []
        linecount = 1
        for line in source_data:
            
            newline = dict({'No.': linecount, \
                       'Radio ID':line['RADIO_ID'], \
                       'Callsign':line['CALLSIGN'], \
                       'Name':line['FIRST_NAME']+' '+line['LAST_NAME'], \
                       'City': line['CITY'], \
                       'State': line['STATE'], \
                       'Country': line['COUNTRY'], \
                       'Remarks': line['REMARKS'], \
                       'Call Type': 'Private Call', \
                       'Call Alert': 'None'})
            target_data.append(newline)
            linecount += 1
        return target_data    


"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   testapp = DMRUtils()
   print testapp.__version__()
   data = testapp.readFile('testfiles/user.csv')
   new_data = testapp.processData(data)
   for data_item in new_data:
       if(data_item.get('Callsign','N0SO') == 'N0SO'):
           pprint.pprint(data_item['Radio ID'])
   
   testapp.writeFile(new_data,'testfiles/testoutput.csv')
   
