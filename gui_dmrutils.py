#!/usr/bin/python
"""
gui_dmrutils.py - GUI "front end" for DMR utilities

          V0.0.1 - 2019-08-28
          First interation
          
          V0.1.0 - 2019-08-29
          Fuctional enough for first use! Converts to 
          AnyTone 868/878 and Connect Systems CS-800D
          
"""
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from tkFileDialog   import asksaveasfilename
from datetime import datetime
from user2anytone import User2Anytone
from user2cs800d import User2CS800D

import os.path
import argparse

VERSION = '1.0.0'
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
        print( "Exiting..." )
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
        self.filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Browse for ID List File...", command=self.BrowseFile)
        self.filemenu.add_command(label="Fetch Latest ID List...", command=self.FetchFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Convert to AnyTone...", command=self.AnyTonecsv)
        self.filemenu.add_command(label="Convert to CS800D...", command=self.CS800Dcsv)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.client_exit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label='AnyTone AT-8x8UV Support',
                             command=self.displayanytone)
        helpmenu.add_command(label="About...", command=self.About)

        #mainloop()

    def BrowseFile(self):
        print ("Browse for previously downloaded user.csv file!")
        fileName = askopenfilename(title = "Select user.csv:",
                                      filetypes=[("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        if os.path.isfile(fileName):
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
            print (resultfile)
        else:
            print ('Fetch or browse or a user.csv file first!')
            showinfo('File conversion error!', \
                     'Fetch or browse or a user.csv file first!')
        
    def CS800Dcsv(self):
        print ('Convert to Connect Systems CS-800D format...')
        if (self.userfilename):
            dmrapp=User2CS800D()
            new_data = dmrapp.processData(self.usercsvData)
            resultfile = dmrapp.autowriteFile(new_data,
                                          self.userfilename)
            self.LogText.delete(1.0, END)
            self.fillLogTextfromFile(resultfile, self.LogText)
            showinfo('Connect Systems CS800D Conversion Complete', \
                 'After adding your Talk Groups with a text ' + \
                 'editor or spreadsheet program, ' + \
                 'Import this file into your CPS:\n'+ \
                  resultfile)
            print (resultfile)
        else:
            print ('Fetch or browse or a user.csv file first!')
            showinfo('File conversion error!', \
                     'Fetch or browse or a user.csv file first!')
       

    def About(self):
        showinfo('GUI_DMRUTILS', 'GUI_DMRUTILS - Version ' + VERSION + '\n' + \
              'Utilities to help manage DMR Contact Lists in CSV format.')

    def displayanytone(self):
        showinfo('AnyTone AT-868/878UV Support', \
                 'Convert user.csv file to the format required\n'+ \
                 'by the AnyTone AT-868UV and AT-878UV.')

        
    def fillLogTextfromFile(self, filename, textWindow):
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           for line in retText:
              textWindow.insert(END, line.strip()+'\n')
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText

    def FetchFile(self, URL=None, pathname=None):
       """
       Fetch latest user.csv file from RADIO ID.NET
       """
       print('Fetching latest user.csv file from %s'%(RADIOIDURL))
       app = User2Anytone()
       self.usercsvData = app.fetchIDList('www.radioid.net',
                                     '/static/user.csv')         
       if (self.usercsvData):
           self.userfilename = 'user.csv'
           datestg = datetime.now().strftime('%Y%m%d-%H%M%S')
           newfilename = 'user-' + datestg  +'.csv'
           self.LogText.delete(1.0, END)
           for line in self.usercsvData:
               self.LogText.insert(END, line)
           
           filename = asksaveasfilename(initialdir = "./",
	                  title = "Save user.csv file...",
			  initialfile = newfilename,
			  filetypes = [("csv files","*.csv"),
			               ("text files","*.txt"),
			               ("all files","*.*")])
           name = open(filename, 'wb')
           name.write(self.usercsvData)
           name.close()
           self.userfilename = os.path.dirname(filename) + \
	                        '/user.csv'
           self.usercsvData = None
           self.usercsvData = app.readFile(filename) 
           print (self.usercsvData)
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
   
        
