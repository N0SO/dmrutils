#!/usr/bin/python
"""
gui_dmrutils.py - GUI "front end" for DMR utilities

          V0.0.1 - 2019-08-28
          First interation
          
"""
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from user2anytone import User2Anytone
from user2cs800d import User2CS800D

import os.path
import argparse

VERSION = '0.0.2'
FILELIST = './'
RADIOIDURL = 'https://radioid.net/static/user.csv'

class guiDMRUtils(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        self.usercsvData = None

        self.userfilename = None

    #Creation of init_window
    def client_exit(self):
        print "Exiting..."
        exit()

    def init_window(self):
        root = self.master
        S = Scrollbar(root)
        self.LogText = Text(root, height=10, width=120)
        S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=S.set)

        root.title("DMR Contact List Utilities")
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Browse for ID List File...", command=self.BrowseFile)
        filemenu.add_command(label="Fetch Latest ID List...", command=self.FetchFile)
        filemenu.add_separator()
        filemenu.add_command(label="Convert to AnyTone...", command=self.AnyTonecsv)
        filemenu.add_command(label="Convert to CS800D...", command=self.CS800Dcsv)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.client_exit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label='AnyTone AT-8x8UV Support',
                             command=self.displayanytone)
        helpmenu.add_command(label="About...", command=self.About)

        #mainloop()

    def BrowseFile(self):
        print "Browse for previously downloaded user.csv file!"
        fileName = askopenfilename(title = "Select user.csv:",
                                      filetypes=[("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(fileName))
        dmrapp = User2Anytone()
        self.usercsvData = dmrapp.readFile(fileName)
        self.fillLogTextfromFile(fileName, self.LogText)
        self.userfilename = fileName

    def AnyTonecsv(self):
        print ('Convert to AnyTone AT-8x8UV format...')
        if (self.userfilename):
            dmrapp=User2Anytone()
            new_data = dmrapp.processData(self.usercsvData)
            resultfile = dmrapp.autowriteFile(new_data,
                                          self.userfilename)
            self.LogText.delete(1.0, END)
            self.fillLogTextfromFile(resultfile, self.LogText)
            showinfo('AnyTone AT-868/878UV Conversion Complete', \
                 'Import this file into your AnyTone CPS:\n'+ \
                  resultfile)
            print resultfile
        else:
            print ('Fetch or browse or a user.csv file first!')
            showinfo('File conversion error!', \
                     'Fetch or browse or a user.csv file first!')
        
    def CS800Dcsv(self):
        print ('Convert to Connect Systems CS-800D format...')

    def About(self):
        showinfo('GUI_DMRUTILS', 'GUI_DMRUTILS - Version ' + VERSION + '\n' + \
              'Utilities to help manage DMR Contact Lists in CSV format.')

    def displayanytone(self):
        showinfo('AnyTone AT-868/878UV Support', \
                 'Convert user.csv file to the format required\n'+ \
                 'by the AnyTone AT-868UV and AT-878UV.')

    def SumOneXOnes(self):
        logpathName = askdirectory()
        print('Directory name selected: %s'%logpathName)
        sumApp = MOQPCategory()
        sumData = sumApp.exportcsvflist(logpathName)
        sumLines = sumData.split('\n')
        for line in sumLines:
           self.LogText.insert(END, line.strip()+'\n')
        sumfile = logpathName + "logsummaryreport.txt"
        with open(sumfile,'w') as f:
           f.write(sumData)
        showinfo('CSV summary File created and saved', 'Saved as file:\n%s'%sumfile)

    def SumDir(self):
        logpathName = askdirectory()
        print('Directory name selected: %s'%logpathName)
        sumApp = MOQPCategory()
        sumData = sumApp.exportcsvflist(logpathName)
        sumLines = sumData.split('\n')
        for line in sumLines:
           self.LogText.insert(END, line.strip()+'\n')
        sumfile = logpathName + "logsummaryreport.txt"
        with open(sumfile,'w') as f:
           f.write(sumData)
        showinfo('CSV summary File created and saved', 'Saved as file:\n%s'%sumfile)
        
        
        

    def SumFile(self):
        logfileName = askopenfilename(title = "Select input log file:",
                                      filetypes=[("LOG files","*.log"),
                                                 ("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(logfileName))
        
        logdata = self.fillLogTextfromFile(logfileName, self.LogText)
        
        sumApp = MOQPCategory()
        sumData = sumApp.exportcsvfile(logfileName)
        sumLines = sumData.split('\n')
        for line in sumLines:
           self.LogText.insert(END, line.strip()+'\n')
        sumfile = logfileName + ".txt"
        with open(sumfile,'w') as f:
           f.write(sumData)
        showinfo('CSV summary File created and saved', 'Saved as file:\n%s'%sumfile)
        
        
        
    def fillLogTextfromFile(self, filename, textWindow):
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           for line in retText:
              textWindow.insert(END, line.strip()+'\n')
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText

    def OpenFile(self):
        csvfilename = askopenfilename(title = "Select input ID file:",
                                      filetypes=[("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        print('File name selected: %s'%(csvfilename))
        if os.path.isfile(csvfilename):
            csvtext = self.fillLogTextfromFile(csvfilename, self.LogText)
            app = csv2CAB()
            cabtext = r""
            cabtext = app.processcsvData(csvtext)
            #print csvtext
            for line in cabtext:
               self.LogText.insert(END, line.strip()+'\n')
            cabfile = csvfilename + ".log"
            with open(cabfile,'w') as f:
                f.write(cabtext)
            showinfo('CAB File created and saved', 'Saved as CAB file:\n'+cabfile)
            
    def FetchFile(self, URL=None, pathname=None):
       """
       Fetch latest user.csv file from RADIO ID.NET
       """
       print('Fetching latest user.csv file from %s'%(RADIOIDURL))
       pass
        
    def appMain(self, pathname):
       #import moqpcategory
       mqpcat = MOQPCategory()
       
       if (os.path.isfile(pathname)):
          mqpcat.exportcsvfile(pathname.strip())
       else:
          mqpcat.exportcsvflist(pathname.strip())
        
if __name__ == '__main__':
      root = Tk()

      root.geometry("900x300")

      #creation of an instance
      app = guiDMRUtils(root)

      #mainloop 
      root.mainloop()     
   
        