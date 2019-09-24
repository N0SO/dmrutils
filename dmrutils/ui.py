#!/usr/bin/python
"""
gui_dmrutils.py - GUI "front end" for DMR utilities
Update History:

* Wed Aug 29 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First iteration
* Thu Aug 29 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 - Fuctional enough for first use! Converts to 
- AnyTone 868/878 and Connect Systems CS-800D

"""
import sys
python_version = sys.version_info[0]
if (python_version == 2):
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog   import askopenfilename
    from tkFileDialog   import askdirectory
    from tkFileDialog   import asksaveasfilename
else:
    from tkinter import *
    from tkinter.messagebox import showinfo
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import askdirectory
    from tkinter.filedialog import asksaveasfilename

from datetime import datetime
from user2anytone import User2Anytone
from user2cs800d import User2CS800D

import os.path

VERSION = '1.0.1'
FILELIST = './'
RADIOIDURL = 'https://www.radioid.net/static/user.csv'

class guiDMRUtils(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, start=True):
        if (start):
            self.appMain()        

    def __version__(self):
        return VERSION

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
        self.filemenu.add_command(\
                    label="Browse for ID List File...", 
                    command=self.BrowseFile)
        self.filemenu.add_command(\
                    label="Fetch Latest ID List...", 
                    command=self.FetchFile)
        self.filemenu.add_separator()
        self.filemenu.add_command( \
                    label="Convert to AnyTone...", 
                    command=self.AnyTonecsv, 
                    state="disabled")
        self.filemenu.add_command( \
                    label="Convert to CS800D...", 
                    command=self.CS800Dcsv, 
                    state="disabled")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", 
                                  command=self.client_exit)

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
            self.filemenu.entryconfigure("Convert to AnyTone...", state="normal")
            self.filemenu.entryconfigure("Convert to CS800D...", state="normal")


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
        print ('About...')
        pythonversion = sys.version.splitlines()
        infotext = \
        'DMRCONTACTS - Version ' + VERSION + '\n' + \
        'Utilities to help manage DMR Contact Lists in CSV format.\n' \
        + 'Python ' + pythonversion[0]
        showinfo('DMRCONTACTS', infotext)



    def displayanytone(self):
        showinfo('AnyTone AT-868/878UV Support', \
                 'Convert user.csv file to the format required\n'+ \
                 'by the AnyTone AT-868UV and AT-878UV.')

        
    def fillLogTextfromData(self, Data, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        for line in Data:
            textWindow.insert(END, line.strip()+'\n')

    def fillLogTextfromFile(self, filename, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           self.fillLogTextfromData(retText, textWindow, clearWin)
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText

    def FetchFile(self, URL=RADIOIDURL):
       """
       Fetch latest user.csv file from URL
       """
       print('Fetching latest user.csv file from %s'%(URL))
       app = User2Anytone()
       IDData = app.fetchIDList(URL)
       #print('Fetched data = \n%s'%(self.usercsvData))         
       if (IDData):
           print ('IDData type is %s'%(type(IDData)))
           self.userfilename = 'user.csv'
           datestg = datetime.now().strftime('%Y%m%d-%H%M%S')
           newfilename = 'user-' + datestg  +'.csv'
           self.LogText.delete(1.0, END)
           print('Writing data to text window...')
           fileData = ''
           loops = 0
           for line in IDData:
               #linestg = ''
               first = True
               for nextstg in line:
                   if (first):        
                       linestg = nextstg
                       first=False
                   else:
                       linestg += ',' + nextstg
                   #linestg += nextstg
               #print ('Inserting...')
               #self.LogText.insert(END, linestg+'\n')
               fileData+=linestg+'\n'
               #print('...done inserting!')
               loops += 1
           self.LogText.insert(END, fileData)
           print('Done!\nWriting data to file...%d loops completed.'%(loops))
    
           filename = asksaveasfilename(initialdir = "./",
                      title = "Save user.csv file...",
                      initialfile = newfilename,
                      filetypes = [("csv files","*.csv"),
                                   ("text files","*.txt"),
                                   ("all files","*.*")])
           name = open(filename, 'w')
           name.writelines(fileData)
           name.close()
           print('Done!')
           self.usercsvData=None
           self.usercsvData = app.readFile(filename)
           self.filemenu.entryconfigure("Convert to AnyTone...", state="normal")
           self.filemenu.entryconfigure("Convert to CS800D...", state="normal")
       pass
        
    def appMain(self):
        # parameters that you want to send through the Frame class. 
        self.master = Tk()

        Frame.__init__(self, self.master)   

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        self.usercsvData = None

        self.userfilename = None

        self.master.mainloop()
        
if __name__ == '__main__':

      #creation of an instance
      app = guiDMRUtils()
