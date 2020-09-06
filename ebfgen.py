#!/usr/bin/python3
########################################################################
#
#                       script: ebfgen
#                           by: Dan Purgert KE8PFU
#                    copyright: 2020
#                      version: 1.0.4
#                         date: Wed, 26 Aug 2020 17:30:21 -0400
#                      purpose: Generates a batch file for upload to
#                             : the FCC EBF system.
#
#                      license: GPL v2 (only)
#                   repository: https://github.com/dpurgert
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#  02110-1301 USA.
#
########################################################################
## pyEBFgen
#  @file
#  This module is to assist the user in generating the batch files
#  necessary for automated FCC filing using the Universal Licensing
#  System (ULS) Electronic Batch File (EBF).
#
#  2020-08-19 22:00 GMT -4 Well played WL1B, W5AD, and KN4EWI

import tkinter as tk
import configparser as cp
import pathlib
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import * 
from array import *

## Major Version number
maver = "1"

## Minor Version Number. Minor versions reset on Major version updates.
miver = "0" 

## Patch Number. Patch numbers reset on Major or Minor version updates.
ptver = "4"

## Array to hold Applicant objects, as new applicants are saved.
#  The array is flushed on saving of each session batchfile.
VAs=[]  

## Counter / pointer into the array's next position.
c=0

## List of States, Territories, etc.
#  Used to fill in VEC header information and applicant address
#  information.  
states=['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA'\
        ,'GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA'\
        ,'MI','MN','MO','MS','MT','NE','NV','NH','NJ','NM','NY','NC'\
        ,'ND','MP','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX'\
        ,'UM','UT','VT','VA','VI','WA','WV','WI','WY','-----','AE','AP'\
        ,'AA','-----','DX','(blank)']

## List of application purpose codes
#  "AU" = Administrative Update
#  "MD" = Modification (e.g. upgrading Tech. to General)
#  "NE" = New Applicant
#  "RM" = Renew and Modify (e.g. Tech. renewal AND upgrade to General)
#  "RO" = Renew Only
apppur=['AU','MD','NE','RM','RO']

## List of applicant license classes
#  "N" = Novice
#  "T" = Technician
#  "G" = General
#  "A" = Advanced (Deprecated by FCC)
#  "E" = Extra (replaced 'Advanced')
liccls=['N','T','G','A','E']

## List for answers about the felony question
#  Used to answer the Basic Qualification Question
felony=['null','Y','N']

## Y|N option list for relevant dropdowns
opts=['Y','N']

## Volunteer Examiner Code
VEC = None

## Session Date
sdt = None

## Session City
vecity = None

## Session State
vestate = None

## Number of Applicants Tested
appt = None

## Number of Applicants Passed
appp = None

## Number of Applicants Failed
appf = None

## Number of Elements Passed
elmp = None

## Number of Elements Failed
elmf = None

## Global record of the completed VEC header string
VE_str = ""
VEset = False

## Regional Identifier for filenaming purposes.
tloc = None

## Session counter for filenaming purposes.
tcnt = 1

## Keeps track of state selected for VEC header
vestidx = 0

## Global object for the "preview" frame.
VA_list = None

va_state=""

## Global applicant offsets to maybe keep it from crying?
vapl=0

## Enable Club applications in File Menu
clubfm = False 

## Enable Visibility features
vis = False 

## VA
#  
#  The "VA" class object maintains the details of an individual
#  applicant for a given testing session.  At the present time, pyebfgen
#  does not support editing of applicant data once saved.
class VA:
  def __init__(self,fn,call,ssn,entname,fname,mi,lname,nmsuf,attn\
    ,street,pobox,city,state,zipcd,phone,fax,email,appcd,opclass,sigok\
    ,physcert,reqexp,waivereq,att,updcall,trusteecall,apptyp,frn,dob\
    ,lnchg,psqcd,psq,psqa,felon):

    self.fn = fn
    self.call = call
    self.ssn = ssn
    self.entname = entname
    self.fname = fname
    self.mi = mi
    self.lname = lname
    self.nmsuf = nmsuf
    self.attn = attn
    self.street = street
    self.pobox = pobox
    self.city = city
    self.state = state
    self.zipcd = zipcd
    self.phone = phone
    self.fax = fax
    self.email = email
    self.appcd = appcd
    self.opclass = opclass
    self.sigok = sigok
    self.physcert = physcert
    self.reqexp = reqexp
    self.waivereq = waivereq
    self.att = att
    self.updcall = updcall
    self.trusteecall = trusteecall
    self.apptyp = apptyp
    self.frn = frn
    self.dob = dob
    self.lnchg = lnchg
    self.psqcd = psqcd
    self.psq = psq
    self.psqa = psqa
    self.felon = felon

## fileManager
#
#  This class provides some of the basic framework necessary for reading
#  input response files from the FCC.
class fileManager():
  ## convertFile
  #
  #  This function reads in an FCC Response file, and converts it into
  #  comma-separated format, which is saved to the filesystem in the
  #  same location as the response file was opened from. It is strongly
  #  recommended that you do not open responses from temporary
  #  directories. Additionally, the converted text is displayed in the
  #  main window's preview pane.
  def convertFile():
    inFN=askopenfilename (title="Select File",
      filetypes=(("EBF Response Files","*.rsp"),
      ("All Files","*.*")))

    if inFN is None:
      return

    inF = open(inFN, "r") 

    outFN = inFN[:-4] + ".csv"
    outF = open(outFN, "w")
    inDat=inF.readlines()
    newWin=tk.Tk()
    prevWin(newWin)
    for line in inDat:
      outln=line.replace("|",",")
      prevWin.rspUpdate(outln)  
      outF.writelines(outln)
    outF.close()

    showinfo(title="Convert complete", message="Saved as: " + outFN)
  
  ## writeFile
  #
  #  This function handles writing batch file for submission to the
  #  FCC's processing system.  In addition, it prepares the tool for a
  #  subesquent testing session.
  def writeFile():
      global VAs
      global VE_str
      global VEC
      global sdt
      global appt
      global appp
      global appf
      global elmp
      global elmf
      global tloc
      global tcnt
      global c
  
      # Format the date for use in the output filename
      fdt = sdt.get().replace("/","")[:4]
      # Set the default filename
      deffn = VEC.get()+fdt+tloc.get()+str(tcnt).zfill(2)
      
      # Open saveas dialog box
      F=asksaveasfile(initialfile=deffn+".dat", mode='w',
        defaultextension=".dat")
      if F is None:
        return
  
      # Write VE Header to file
      F.write (VE_str+"\r\n")
  
      # Loop over applicant data, and write to the file.
      for i in range(len(VAs)):
        F.write("VA|" + VAs[i].fn + "|" + VAs[i].call + "|" \
          + VAs[i].ssn + "|" + VAs[i].entname + "|" + VAs[i].fname \
          + "|" + VAs[i].mi + "|" + VAs[i].lname + "|" + VAs[i].nmsuf \
          + "|" + VAs[i].attn + "|" + VAs[i].street + "|" \
          + VAs[i].pobox + "|" + VAs[i].city + "|" + VAs[i].state \
          + "|" + VAs[i].zipcd + "|" + VAs[i].phone + "|" + VAs[i].fax \
          + "|" + VAs[i].email + "|" + VAs[i].appcd + "|" \
          + VAs[i].opclass + "|" + VAs[i].sigok + "|" \
          + VAs[i].physcert + "|" + VAs[i].reqexp + "|" \
          + VAs[i].waivereq + "|" + VAs[i].att + "|||" \
  #Extra pipes here for attachment file / fax ind ^^^
          + VAs[i].updcall + "|" + VAs[i].trusteecall + "|" \
          + VAs[i].apptyp + "|" +  VAs[i].frn + "|" + VAs[i].dob + "|" \
          + VAs[i].lnchg + "|" + VAs[i].psqcd + "|" + VAs[i].psq + "|" \
          + VAs[i].psqa + "|" + VAs[i].felon + "\r\n")
  
      # Everything written to filesystem.  Close filehandle
      F.close()
  
      # Prepare global variables for next session
      tcnt+=1
      appt.set("0")
      appp.set("0")
      appf.set("0")
      elmp.set("0")
      elmf.set("0")
  
      #clear VA array
      VAs.clear()
      #reset VA Counter
      c = 0
  
## mainWindow

#  This class represents the main navigation window for ebfgen.  Its
#  only real purpose is to provide navigation for the user.
class mainWindow(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    #VE Record fields
    global VEC
    global sdt
    global vecity
    global vestate
    global appt
    global appp
    global appf
    global elmp
    global elmf
    global tloc
    global tcnt
    global vestidx
    global vis
    global clubfm

    global VA_list
    global VAs
    global vapl

    VEC = StringVar()
    sdt = StringVar()
    vecity = StringVar()
    vestate = StringVar()
    appt = StringVar()
    appp = StringVar()
    appf = StringVar()
    elmp = StringVar()
    elmf = StringVar()
    tloc = StringVar()

    #there has to ba a better way than writing 'vec.cfg' twice
    cfg=pathlib.Path('./vec.cfg')

    if cfg.is_file():
      self.cp = cp.RawConfigParser()
      configFilePath = r'./vec.cfg'
      self.cp.read(configFilePath)
      #Read defaults in from config file
      vis=(self.cp.getboolean('VEC_CFG','visaid',fallback=False))
      VEC.set(self.cp.get('VEC_CFG','VEC'))
      vecity.set(self.cp.get('VEC_CFG','city'))
      vestate.set(self.cp.get('VEC_CFG','state'))
      # state reverse lookup dict.  Skip 57 and 61 because they're
      # separators
      strl={ 'AL': 0, 'AK': 1, 'AS': 2, 'AZ': 3, 'AR': 4, 'CA': 5, 
        'CO': 6, 'CT': 7, 'DE': 8, 'DC': 9, 'FL': 10, 'GA': 11, 
        'GU': 12, 'HI': 13, 'ID': 14, 'IL': 15, 'IN': 16, 'IA': 17, 
        'KS': 18, 'KY': 19, 'LA': 20, 'ME': 21, 'MD': 22, 'MA': 23, 
        'MI': 24, 'MN': 25, 'MO': 26, 'MS': 27, 'MT': 28, 'NE': 29, 
        'NV': 30, 'NH': 31, 'NJ': 32, 'NM': 33, 'NY': 34, 'NC': 35, 
        'ND': 36, 'MP': 37, 'OH': 38, 'OK': 39, 'OR': 40, 'PA': 41, 
        'PR': 42, 'RI': 43, 'SC': 44, 'SD': 45, 'TN': 46, 'TX': 47, 
        'UM': 48, 'UT': 49, 'VT': 50, 'VA': 51, 'VI': 52, 'WA': 53, 
        'WV': 54, 'WI': 55, 'WY': 56, 'AE': 58, 'AP': 59, 'AA': 60, 
        'DX': 62, '(blank)': 63}
      tloc.set(self.cp.get('VEC_CFG','regcd'))
      vestidx = strl[vestate.get()]
      #semi-secret option to enable club applications
      clubfm = self.cp.getboolean('VEC_CFG', 'club', fallback=False)
    


    cntr = tk.Frame(self)
    cntr.pack(side="top", fill="both", expand=True)

    cntr.grid_rowconfigure(0,weight=1)
    cntr.grid_columnconfigure(0,weight=1)
    self.frames={}

    for Frm in (clubApplicant, stdApplicant, updVEC):
      frame = Frm(cntr, self)
      self.frames[Frm] = frame
      frame.grid (row=0, column=0, sticky="nsew")

    self.show_frame(updVEC)

  def show_frame(self,cont):
    frame=self.frames[cont]
    frame.tkraise()

  #  Clears the preview frame.  May be deprecated since the preview is a
  #  new tkinter instance now.
  def clrFrame():
    global VA_list
    VA_list.delete('1.0', END)

  ## Quit
  def exitProgram(self):
    exit()

## Update VEC
#
#  Subwindow to update VE header row information for the session.
class updVEC(tk.Frame):
  def __init__ (self, parent, controller):
    tk.Frame.__init__(self, parent)
    global vestidx
    global vis
    global clubfm
    global VE_str
    global VEset
    global VA_list

    def UpdateStateIdx (event):
      global vestidx
      global tloc
      tloc = StringVar()
      vestidx = self.e_vestate.current()
      i=vestidx
      self.e_tloc.delete(0,END)
      if i==7 or i==23 or i==21 or i==31 or i==43 or i==50:
        tloc.set("A")
        self.e_tloc.insert(0,tloc.get())
      elif i==32 or i==34:
        tloc.set("B")
        self.e_tloc.insert(0,tloc.get())
      elif i==8 or i==9 or i==22 or i==41:
        tloc.set("C")
        self.e_tloc.insert(0,tloc.get())
      elif i==0 or i==10 or i==11 or i==19 or i==35 or i==44 \
        or i==46 or i==51:
        tloc.set("D")
        self.e_tloc.insert(0,tloc.get())
      elif i==4 or i==20 or i==27 or i==33 or i==39 or i==47:
        tloc.set("E")
        self.e_tloc.insert(0,tloc.get())
      elif i==5:
        tloc.set("F")
        self.e_tloc.insert(0,tloc.get())
      elif i==3 or i==14 or i==28 or i==30 or i==40 or i==49 \
        or i==53 or i==56:
        tloc.set("G")
        self.e_tloc.insert(0,tloc.get())
      elif i==24 or i==38 or i==54:
        tloc.set("H")
        self.e_tloc.insert(0,tloc.get())
      elif i==15 or i==16 or i==55:
        tloc.set("I")
        self.e_tloc.insert(0,tloc.get())
      elif i==6 or i==17 or i==18 or i==25 or i==26 or i==36 \
        or i==29 or i==45:
        tloc.set("J")
        self.e_tloc.insert(0,tloc.get())
      elif i==1:
        tloc.set("K")
        self.e_tloc.insert(0,tloc.get())
      elif i==42 or i==52:
        tloc.set("L")
        self.e_tloc.insert(0,tloc.get())
      elif i==2 or i==12 or i==13 or i==37:
        tloc.set("M")
        self.e_tloc.insert(0,tloc.get())
      elif i==60:
        tloc.set("N")
        self.e_tloc.insert(0,tloc.get())
      elif i==58:
        tloc.set("O")
        self.e_tloc.insert(0,tloc.get())
      elif i==59:
        tloc.set("P")
        self.e_tloc.insert(0,tloc.get())
      elif i==62:
        tloc.set("Q")
        self.e_tloc.insert(0,tloc.get())
      elif i==48:
        tloc.set("R")
        self.e_tloc.insert(0,tloc.get())
      elif i==63:
        tloc.set("S")
        self.e_tloc.insert(0,tloc.get())
      else:
        tloc.set("X")
        self.e_tloc.insert(0,tloc.get())

    def preview ():  
      if not VEset:
        showerror(title="VEC Error", message="VEC Data not saved.")
        return
      else:
        newWin=tk.Tk()
        prevWin(newWin)
        prevWin.rspUpdate(VE_str +"\n")
        for i in range(len(VAs)):
         outln=str(i)+": VA|" + VAs[i].fn + "|" + VAs[i].call + "|" \
          + VAs[i].ssn + "|" + VAs[i].entname + "|" + VAs[i].fname \
          + "|" + VAs[i].mi + "|" + VAs[i].lname + "|" + VAs[i].nmsuf \
          + "|" + VAs[i].attn + "|" + VAs[i].street + "|" \
          + VAs[i].pobox + "|" + VAs[i].city + "|" + VAs[i].state \
          + "|" + VAs[i].zipcd + "|" + VAs[i].phone + "|" + VAs[i].fax \
          + "|" + VAs[i].email + "|" + VAs[i].appcd + "|" \
          + VAs[i].opclass + "|" + VAs[i].sigok + "|" \
          + VAs[i].physcert + "|" + VAs[i].reqexp + "|" \
          + VAs[i].waivereq + "|" + VAs[i].att + "|||" \
          + VAs[i].updcall + "|" + VAs[i].trusteecall + "|" \
          + VAs[i].apptyp + "|" +  VAs[i].frn + "|" + VAs[i].dob + "|" \
          + VAs[i].lnchg + "|" + VAs[i].psqcd + "|" + VAs[i].psq + "|" \
          + VAs[i].psqa + "|" + VAs[i].felon + "\n"
         prevWin.rspUpdate(outln)

    vec_sec = tk.Label(self, text="")
    vec_sec.grid(row=0, column=2)
    l_VEC = tk.Label(self, text="VEC Code:")
    self.e_VEC = tk.Entry(self)
    self.e_VEC.insert(0,VEC.get())    
    l_sess = tk.Label(self, text="Session Date:")
    self.e_sess = tk.Entry(self)
    self.e_sess.insert(0,sdt.get())
    l_city = tk.Label(self, text="Exam City:")
    self.e_vecity = tk.Entry(self)
    self.e_vecity.insert(0,vecity.get())
    l_state = tk.Label(self, text="Exam State:")
    self.e_vestate = Combobox(self, values=states,
       textvariable=vestate)
    self.e_vestate.current(vestidx)
    self.e_vestate.bind("<<ComboboxSelected>>", UpdateStateIdx)
    l_appT = tk.Label(self, text="Applicants Tested:")
    self.e_appT = tk.Entry(self)
    self.e_appT.insert(0,appt.get())
    l_appP = tk.Label(self, text="Applicants Passed:")
    self.e_appP = tk.Entry(self)
    self.e_appP.insert(0,appp.get())
    l_appF = tk.Label(self, text="Applicants Failed:")
    self.e_appF = tk.Entry(self)
    self.e_appF.insert(0,appf.get())
    l_elmP = tk.Label(self, text="Elements Passed:")
    self.e_elmP = tk.Entry(self)
    self.e_elmP.insert(0,elmp.get())
    l_elmF = tk.Label(self, text="Elements Failed:")
    self.e_elmF = tk.Entry(self)
    self.e_elmF.insert(0,elmf.get())
    l_tloc = tk.Label(self, text="Regional Identifier:")
    self.e_tloc = tk.Entry(self)
    self.e_tloc.insert(0,tloc.get())
    l_tcnt = tk.Label(self, text="File Counter:")
    self.e_tcnt = tk.Entry(self)
    l_uappid = tk.Label(self, text="Applicant ID:")
    self.e_uappid = tk.Entry(self)
    self.e_tcnt.insert(0,tcnt)
    ve_save = tk.Button(self, text="Apply",
        command=self.sVE)

    l_VEC.grid(row=1, column=1)
    self.e_VEC.grid(row=1, column=2)
    l_sess.grid(row=2, column=1)
    self.e_sess.grid(row=2, column=2)
    l_city.grid(row=3, column=1)
    self.e_vecity.grid(row=3, column=2)
    l_state.grid(row=4, column=1)
    self.e_vestate.grid(row=4, column=2)
    l_appT.grid(row=1, column=4)
    self.e_appT.grid(row=1, column=5)
    l_appP.grid(row=2, column=4)
    self.e_appP.grid(row=2, column=5)
    l_appF.grid(row=3, column=4)
    self.e_appF.grid(row=3, column=5)
    l_elmP.grid(row=4, column=4)
    self.e_elmP.grid(row=4, column=5)
    l_elmF.grid(row=5, column=4)
    self.e_elmF.grid(row=5, column=5)
    l_tloc.grid(row=9, column=4)
    self.e_tloc.grid(row=9, column=5)
    l_tcnt.grid(row=8, column=1)
    self.e_tcnt.grid(row=8, column=2)
    ve_save.grid(row=9,column=1)

    b_prev= Button(self, text="Preview Batch File",
      command=preview)
    b_prev.grid(row=9,column=2)
    b_stdapp = Button(self, text="Add Applicant", 
      command=lambda:controller.show_frame(stdApplicant))
    b_stdapp.grid(row=13,column=2)
    l_uappid.grid(row=12,column=4)
    self.e_uappid.grid(row=13,column=4)
    b_stdapp = Button(self, text="Update Applicant", 
      command=self.prepUpd)
    b_stdapp.grid(row=13,column=5)
    if clubfm:
      b_clubapp = Button(self, text="Club Applicant", 
        command=lambda:controller.show_frame(clubApplicant))
      b_clubapp.grid(row=13, column=1)
    self.b_save = Button(self, text="Save Session", 
      command=self.prepWrite, background="Red") 
    self.b_save.grid(row=14, column=2)
    b_conv = Button(self, text="Convert .rsp File", 
      command=fileManager.convertFile)
    b_conv.grid(row=14, column=3)
    b_quit = Button(self, text="Quit", 
      command= self.exitProgram)
    b_quit.grid(row=15, column=2)

    if vis:
      self.b_save.config({"background":"Yellow", "foreground":"Black"})

  ## Prepare output
  def prepWrite(self):
    global vis
    global VEset
    VEset = False
    if vis:
      self.b_save.config({"background":"Yellow", "foreground":"Black"})
    else:
      self.b_save.config({"background":"Red"})
    fileManager.writeFile()

  def prepUpd(self):
    global vapl
    global VAs
    if self.e_uappid.get() == "":
      showerror(title="Update Error", message="Applicant ID Not Provided.")
      return
    else:
      vapl=int(self.e_uappid.get())
      if vapl > (len(VAs)-1):
        showerror(title="Update Error", 
          message="Invalid Applicant ID.")
        return
      else:
        newWin=tk.Tk()
        updApplicant(newWin)
    

  ## Quit
  def exitProgram(self):
    exit()

      
  ## Save VE
  #
  #  Saves VEC (Exam) data for the EBF header, and prints to the file
  #  preview.  Note - no matter how many entries are in the preview
  #  pane, only one (1) VE record will be in the output.
  def sVE(self):
    #VE Record fields
    global VEC
    global sdt
    global vecity
    global vestate
    global appt
    global appp
    global appf
    global elmp
    global elmf
    global tloc
    global vis
    global VEset
    global VE_str

    VEC.set(self.e_VEC.get().upper())
    sdt.set(self.e_sess.get())
    vecity.set(self.e_vecity.get())
    vestate.set(self.e_vestate.get())
    appt.set(self.e_appT.get())
    appp.set(self.e_appP.get())
    appf.set(self.e_appF.get())
    elmp.set(self.e_elmP.get())
    elmf.set(self.e_elmF.get())
    tloc.set(self.e_tloc.get())

    #allow setting the VEC state to a blank... 
    if vestate.get() == "(blank)":
      vestate.set("")


    VE_str="VE|" + VEC.get() + "|" + sdt.get() + "|" + vecity.get() + \
        "|" + vestate.get() + "|" + appt.get() + "|" + appp.get() + \
        "|" + appf.get() + "|" + elmp.get() + "|" + elmf.get()

    VEset = True

    if vis:
      self.b_save.config({"background":"Blue", "foreground":"White"})
    else:
      self.b_save.config({"background":"Green"})

    
## App_Windows Class
#
#  Class to handle the Applicant Information window.  TODO - figure out
#  how to make both the "standard" and "extended" forms extend this, so
#  we don't need any code duplication.
class appWindow(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    global vapl
    global VAs
    
    # set some local variables for holding onto dropdown selections
    va_state=""
    va_appcd=""
    va_opclass=""
    va_updcall=""
    va_felon=""
    
    self.l_vafn = tk.Label(self, text="Pending File Number")
    self.e_vafn = tk.Entry(self)
    self.l_call = tk.Label(self, text="Callsign, if licensed")
    self.e_call = tk.Entry(self)
    self.l_ssn = tk.Label(self, text="Social Security Number")
    self.e_ssn = tk.Entry(self)
    self.l_ent = tk.Label(self, text="Entity Name")
    self.e_ent = tk.Entry(self)
    self.l_fname = tk.Label(self, text="First Name")
    self.e_fname = tk.Entry(self)
    self.l_mi = tk.Label(self, text="Middle Initial")
    self.e_mi = tk.Entry(self)
    self.l_lname = tk.Label(self, text="Last Name")
    self.e_lname = tk.Entry(self)
    self.l_nmsuf = tk.Label(self, text="Suffix")
    self.e_nmsuf = tk.Entry(self)
    self.l_attn = tk.Label(self, text="Attention")
    self.e_attn = tk.Entry(self)
    self.l_street = tk.Label(self, text="Mailing Address")
    self.e_street = tk.Entry(self)
    self.l_pobox = tk.Label(self, text="P.O. Box")
    self.e_pobox = tk.Entry(self)
    self.l_city = tk.Label(self, text="City")
    self.e_city = tk.Entry(self)
    self.l_state = tk.Label(self, text="State / U.S. Territory")
    self.e_state = Combobox(self, values=states,
      textvariable=va_state)
    self.l_zipcd = tk.Label(self, text="Zip Code")
    self.e_zipcd = tk.Entry(self)
    self.l_phone = tk.Label(self, text="Phone Number")
    self.e_phone = tk.Entry(self)
    self.l_fax = tk.Label(self, text="Fax Number")
    self.e_fax = tk.Entry(self)
    self.l_email = tk.Label(self, text="E-Mail Address")
    self.e_email = tk.Entry(self)
    self.l_appcd = tk.Label(self, text="Application Purpose")
    self.e_appcd = Combobox(self, values=apppur,
      textvariable=va_appcd)
    self.l_opclass = tk.Label(self, text="Operator Class")
    self.e_opclass = Combobox(self, values=liccls,
      textvariable=va_opclass)
    self.l_sigok = tk.Label(self, text="Valid Signature")
    self.e_sigok = tk.Entry(self)
    self.l_physcert = tk.Label(self, text="Physician Certificate")
    self.e_physcert = tk.Entry(self)
    self.l_reqexp = tk.Label(self, text="Requested Expiration")
    self.e_reqexp = tk.Entry(self)
    self.l_waiverreq = tk.Label(self, text="Waiver Request")
    self.e_waiverreq = tk.Entry(self)
    self.l_att = tk.Label(self, text="Attachments")
    self.e_att = tk.Entry(self)
    self.l_updcall = tk.Label(self, 
      text="Change Callsign Systematically?")
    self.e_updcall = Combobox(self, values=opts, 
      textvariable=va_updcall)
    self.l_trusteecall = tk.Label(self, text="Trustee Callsign")
    self.e_trusteecall = tk.Entry(self)
    self.l_apptyp = tk.Label(self, text="Applicant Type")
    self.e_apptyp = tk.Entry(self)
    self.l_frn = tk.Label(self, 
      text="Federal Registration Number")
    self.e_frn = tk.Entry(self)
    self.l_dob = tk.Label(self, text="Date of Birth")
    self.e_dob = tk.Entry(self)
    self.l_lnchg = tk.Label(self, text="Licensee Name Change")
    self.e_lnchg = tk.Entry(self)
    self.l_psqcd = tk.Label(self, 
      text="Personal Security Question Code")
    self.e_psqcd = tk.Entry(self)
    self.l_psq = tk.Label(self, text="Custom PSQ")
    self.e_psq = tk.Entry(self)
    self.l_psqa = tk.Label(self, text="PSQ Answer")
    self.e_psqa = tk.Entry(self)
    self.l_felon = tk.Label(self, 
      text="Basic Qualification Question")
    self.e_felon = Combobox(self, values=felony,
      textvariable=va_felon)

    self.b_save = tk.Button(self, text="Save Applicant", 
      command=self.sVA)
    self.b_close = tk.Button(self, text="Close Window", 
      command=lambda:controller.show_frame(updVEC))
    
        
  ## Save VA
  #
  #  Save applicant information to the applicants array for this
  #  session.
  def sVA(self):
    # Most of these probably don't need to be set like this, but it
    # does make the array append a little cleaner
    va_fn = self.e_vafn.get()
    va_call = self.e_call.get().upper()
    # Remove dashes from the ssn, if included
    va_ssn = self.e_ssn.get().replace("-","")
    va_ent = self.e_ent.get()
    # First name is 20 char max
    va_fname = self.e_fname.get()[:20]
    # MI is one char, and must be caps
    va_mi = self.e_mi.get().upper()[:1]
    # Last name is 20 char max
    va_lname = self.e_lname.get()[:20]
    # Suffix is 3 char max
    va_nmsuf = self.e_nmsuf.get()[:3]
    va_attn = self.e_attn.get()
    # Street address is 60 char max
    va_street = self.e_street.get()[:60]
    # P.O. Box is 20 char max
    va_pobox = self.e_pobox.get()[:20]
    # City is 20 char
    va_city = self.e_city.get()[:20]
    va_state = self.e_state.get()
    # Remove dashes from zip code (if present)
    va_zipcd = self.e_zipcd.get().replace("-","")
    # Remove formatting from phone number (if present)
    va_phone = self.e_phone.get().replace("(","").\
      replace(")","").replace("-","")
    # Remove formatting from fax number (if present)
    va_fax = self.e_fax.get().replace("(","").\
      replace(")","").replace("-","")
    # Email is 50 char max
    va_email = self.e_email.get()[:50]
    va_appcd = self.e_appcd.get()
    va_opclass = self.e_opclass.get()
    va_sigok = self.e_sigok.get()
    va_physcert = self.e_physcert.get()
    va_reqexp = self.e_reqexp.get()
    va_waivereq = self.e_waiverreq.get()
    va_att = self.e_att.get()
    va_updcall = self.e_updcall.get()
    va_trusteecall = self.e_trusteecall.get()
    va_apptyp = self.e_apptyp.get()
    va_frn = self.e_frn.get()
    va_dob = self.e_dob.get()
    va_lnchg = self.e_lnchg.get()
    va_psqcd = self.e_psqcd.get()
    va_psq = self.e_psq.get()
    va_psqa = self.e_psqa.get()
    va_felon = self.e_felon.get()

    # Formatted (zero-padded) FRN
    frn = ""

    # FRN supercedes ssn 
    if va_frn:
      va_ssn = ""
      #If the FRN is <10 digits, zero pad it
      frn = va_frn.zfill(10)
    else:
      if len(va_ssn)!=9:
        showerror(title="SSN Error", message="SSN is not 9 digits.")
        return

    if va_felon == "null" or va_felon == "":
      va_felon = ""
      if va_appcd != "AU":
        showerror(title="Basic Qualification Question Error",
          message="'Basic Qualification Question' must be answered.")
        return

    if va_state == "-----" or va_state == "":
      showerror(title="State Error", 
        message="Please select a valid state.")
      return

    if va_opclass == "null" or va_opclass == "":
      showerror(title="Class Error",
        message="Please select a valid operator class.")
      return

    VAs.append(VA( va_fn, va_call, va_ssn, va_ent\
      , va_fname, va_mi, va_lname, va_nmsuf\
      , va_attn, va_street, va_pobox, va_city\
      , va_state, va_zipcd, va_phone, va_fax\
      , va_email, va_appcd, va_opclass, va_sigok\
      , va_physcert, va_reqexp, va_waivereq\
      , va_att, va_updcall, va_trusteecall\
      , va_apptyp, frn, va_dob, va_lnchg\
      , va_psqcd, va_psq, va_psqa, va_felon))
    
    # Reset the form for the next applicant.
    self.e_vafn.delete(0,'end')
    self.e_call.delete(0, 'end')
    self.e_ssn.delete(0, 'end')
    self.e_ent.delete(0, 'end')
    self.e_fname.delete(0, 'end')
    self.e_mi.delete(0, 'end')
    self.e_lname.delete(0, 'end')
    self.e_nmsuf.delete(0, 'end')
    self.e_attn.delete(0, 'end')
    self.e_street.delete(0, 'end')
    self.e_pobox.delete(0, 'end')
    self.e_city.delete(0, 'end')
    self.e_state.delete(0, 'end')
    self.e_zipcd.delete(0, 'end')
    self.e_phone.delete(0, 'end')
    self.e_fax.delete(0, 'end')
    self.e_email.delete(0, 'end')
    self.e_appcd.delete(0, 'end')
    self.e_opclass.delete(0, 'end')
    self.e_reqexp.delete(0, 'end')
    self.e_waiverreq.delete(0, 'end')
    self.e_updcall.delete(0, 'end')
    self.e_trusteecall.delete(0, 'end')
    self.e_frn.delete(0, 'end')
    self.e_dob.delete(0, 'end')
    self.e_lnchg.delete(0, 'end')
    self.e_psqcd.delete(0, 'end')
    self.e_psq.delete(0, 'end')
    self.e_psqa.delete(0, 'end')
    self.e_felon.delete(0, 'end')
   
## clubApplicant class
#
# Subclass / Child of appWindow class - prints out the labels and
# element frames for club application entries into the batch file.
# This can only be enabled by adding a "club" config file entry to
# enable the pane. Nearly all VECs SHOULD NOT be using this.
class clubApplicant(appWindow):
  def __init__ (self, parent, controller):
    appWindow.__init__(self, parent, controller)

    # Force some static values for attachments, signature, applicant
    # type, and physician certificate
    self.e_physcert.insert(0,"N")
    self.e_att.insert(0,"N")
    self.e_sigok.insert(0,"Y")
    self.e_apptyp.insert(0,"B")

    self.l_ent.grid(row=1, column=1)
    self.e_ent.grid(row=2, column=1)
    self.l_trusteecall.grid(row=1,column=2)
    self.e_trusteecall.grid(row=2,column=2)
 
    self.l_attn.grid(row=3, column=1)
    self.e_attn.grid(row=4, column=1)
  
    self.l_street.grid(row=3,column=2)
    self.e_street.grid(row=4,column=2)

    self.l_city.grid(row=5,column=1)
    self.e_city.grid(row=6,column=1)
    self.l_state.grid(row=5,column=2)
    self.e_state.grid(row=6,column=2)
    self.l_zipcd.grid(row=5,column=3)
    self.e_zipcd.grid(row=6,column=3)
    
    self.l_ssn.grid(row=8, column=1)
    self.e_ssn.grid(row=9,column=1)
    self.l_frn.grid(row=8,column=2)
    self.e_frn.grid(row=9,column=2)

    self.l_phone.grid(row=10,column=1)
    self.e_phone.grid(row=11,column=1)
    self.l_email.grid(row=10,column=2)
    self.e_email.grid(row=11,column=2)

    self.l_felon.grid(row=12,column=1)
    self.e_felon.grid(row=13,column=1)
    self.l_appcd.grid(row=12,column=2)
    self.e_appcd.grid(row=13,column=2)
    self.l_vafn.grid(row=12, column=3)
    self.e_vafn.grid(row=13, column=3)

    self.b_save.grid(row=14,column=1)
    self.b_close.grid(row=14,column=2)

    

    #set the widget tab-order properly.
    taborder=(self.e_ent, self.e_trusteecall,\
      self.e_attn, self.e_street, self.e_city, self.e_state,\
      self.e_zipcd, self.e_ssn, self.e_frn, self.e_phone,\
      self.e_email, self.e_felon, self.e_appcd, self.e_vafn)
    for wid in taborder:
      wid.lift()
    
    def change_dropdown(*args):
        print( va_updcall.get() )

## stdApplicant class
#
# Subclass / Child of appWindow class - prints out the labels and
# element frames for standard (individual) applicant entries into the
# batch file.
class stdApplicant(appWindow):
  def __init__ (self, parent, controller):
    appWindow.__init__(self, parent, controller)

    # Force some static values for attachments, signature, applicant
    # type, and physician certificate
    self.e_physcert.insert(0,"N")
    self.e_att.insert(0,"N")
    self.e_sigok.insert(0,"Y")
    self.e_apptyp.insert(0,"I")

    self.l_lname.grid(row=1,column=1)
    self.e_lname.grid(row=2,column=1)
    self.l_fname.grid(row=1,column=2)
    self.e_fname.grid(row=2,column=2)
    self.l_mi.grid(row=1,column=3)
    self.e_mi.grid(row=2,column=3)
    
    self.l_nmsuf.grid(row=4,column=1)
    self.e_nmsuf.grid(row=5,column=1)
    self.l_call.grid(row=4, column=3)
    self.e_call.grid(row=5, column=3)
   
    self.l_street.grid(row=6,column=1)
    self.e_street.grid(row=7,column=1)

    self.l_city.grid(row=8,column=1)
    self.e_city.grid(row=9,column=1)
    self.l_state.grid(row=8,column=2)
    self.e_state.grid(row=9,column=2)
    self.l_zipcd.grid(row=8,column=3)
    self.e_zipcd.grid(row=9,column=3)

    self.l_ssn.grid(row=10, column=1)
    self.e_ssn.grid(row=11,column=1)
    self.l_frn.grid(row=10,column=2)
    self.e_frn.grid(row=11,column=2)

    self.l_phone.grid(row=12,column=1)
    self.e_phone.grid(row=13,column=1)
    self.l_email.grid(row=12,column=2)
    self.e_email.grid(row=13,column=2)

    self.l_felon.grid(row=14,column=1)
    self.e_felon.grid(row=15,column=1)
    self.l_appcd.grid(row=14,column=2)
    self.e_appcd.grid(row=15,column=2)
    self.l_updcall.grid(row=14,column=3)
    self.e_updcall.grid(row=15,column=3)

    self.l_lnchg.grid(row=16,column=1)
    self.e_lnchg.grid(row=17,column=1)

    self.l_opclass.grid(row=16,column=2)
    self.e_opclass.grid(row=17,column=2)

    self.l_vafn.grid(row=16, column=3)
    self.e_vafn.grid(row=17, column=3)

    self.b_save.grid(row=18,column=1)
    self.b_close.grid(row=18,column=2)

    

    #set the widget tab-order properly.
    taborder=(self.e_lname, self.e_fname, self.e_mi, self.e_nmsuf,\
      self.e_call, self.e_street,self.e_city, self.e_state,\
      self.e_zipcd, self.e_ssn, self.e_frn,self.e_phone,\
      self.e_email, self.e_felon, self.e_appcd, self.e_updcall,\
      self.e_lnchg, self.e_opclass, self.e_vafn)
    for wid in taborder:
      wid.lift()
    
    def change_dropdown(*args):
        print( va_updcall.get() )

  
# preview Window Class.
class prevWin(Frame):
  def __init__(self,master=None):
    global VA_list
    Frame.__init__(self,master)
    self.master=master
    self.master.wm_title("Preview")
    frame_a=tk.Frame(self.master)
  
    VA_list = tk.Text(frame_a, width=150, height=10, bg="white")

    VA_list.pack()
    self.b_ret = tk.Button(frame_a, text="Close Window", 
      command=self.master.destroy)
    self.b_ret.pack()

    frame_a.pack()

  def rspUpdate(l):
    global VA_List
    VA_list.insert(END,l)

# Update Applicant Class.
class updApplicant(Frame):
  def __init__(self,master=None):
    Frame.__init__(self,master)
    self.master=master
    self.master.wm_title("Update Applicant")
    frame_a=tk.Frame(self.master)

    global VAs
    global vapl
    
    # set some local variables for holding onto dropdown selections
    va_state=""
    va_appcd=""
    va_opclass=""
    va_updcall=""
    va_felon=""

  
    self.b_ret = tk.Button(frame_a, text="Cancel Updates", 
      command=self.master.destroy)
    self.l_vafn = tk.Label(frame_a, text="Pending File Number")
    self.e_vafn = tk.Entry(frame_a)
    self.l_call = tk.Label(frame_a, text="Callsign, if licensed")
    self.e_call = tk.Entry(frame_a)
    self.l_ssn = tk.Label(frame_a, text="Social Security Number")
    self.e_ssn = tk.Entry(frame_a)
    self.l_ent = tk.Label(frame_a, text="Entity Name")
    self.e_ent = tk.Entry(frame_a)
    self.l_fname = tk.Label(frame_a, text="First Name")
    self.e_fname = tk.Entry(frame_a)
    self.l_mi = tk.Label(frame_a, text="Middle Initial")
    self.e_mi = tk.Entry(frame_a)
    self.l_lname = tk.Label(frame_a, text="Last Name")
    self.e_lname = tk.Entry(frame_a)
    self.l_nmsuf = tk.Label(frame_a, text="Suffix")
    self.e_nmsuf = tk.Entry(frame_a)
    self.l_attn = tk.Label(frame_a, text="Attention")
    self.e_attn = tk.Entry(frame_a)
    self.l_street = tk.Label(frame_a, text="Mailing Address")
    self.e_street = tk.Entry(frame_a)
    self.l_pobox = tk.Label(frame_a, text="P.O. Box")
    self.e_pobox = tk.Entry(frame_a)
    self.l_city = tk.Label(frame_a, text="City")
    self.e_city = tk.Entry(frame_a)
    self.l_state = tk.Label(frame_a, text="State / U.S. Territory")
    self.e_state = Combobox(frame_a, values=states,
      textvariable=va_state)
    self.l_zipcd = tk.Label(frame_a, text="Zip Code")
    self.e_zipcd = tk.Entry(frame_a)
    self.l_phone = tk.Label(frame_a, text="Phone Number")
    self.e_phone = tk.Entry(frame_a)
    self.l_fax = tk.Label(frame_a, text="Fax Number")
    self.e_fax = tk.Entry(frame_a)
    self.l_email = tk.Label(frame_a, text="E-Mail Address")
    self.e_email = tk.Entry(frame_a)
    self.l_appcd = tk.Label(frame_a, text="Application Purpose")
    self.e_appcd = Combobox(frame_a, values=apppur,
      textvariable=va_appcd)
    self.l_opclass = tk.Label(frame_a, text="Operator Class")
    self.e_opclass = Combobox(frame_a, values=liccls,
      textvariable=va_opclass)
    self.l_sigok = tk.Label(frame_a, text="Valid Signature")
    self.e_sigok = tk.Entry(frame_a)
    self.l_physcert = tk.Label(frame_a, text="Physician Certificate")
    self.e_physcert = tk.Entry(frame_a)
    self.l_reqexp = tk.Label(frame_a, text="Requested Expiration")
    self.e_reqexp = tk.Entry(frame_a)
    self.l_waiverreq = tk.Label(frame_a, text="Waiver Request")
    self.e_waiverreq = tk.Entry(frame_a)
    self.l_att = tk.Label(frame_a, text="Attachments")
    self.e_att = tk.Entry(frame_a)
    self.l_updcall = tk.Label(frame_a, 
      text="Change Callsign Systematically?")
    self.e_updcall = Combobox(frame_a, values=opts, 
      textvariable=va_updcall)
    self.l_trusteecall = tk.Label(frame_a, text="Trustee Callsign")
    self.e_trusteecall = tk.Entry(frame_a)
    self.l_apptyp = tk.Label(frame_a, text="Applicant Type")
    self.e_apptyp = tk.Entry(frame_a)
    self.l_frn = tk.Label(frame_a, 
      text="Federal Registration Number")
    self.e_frn = tk.Entry(frame_a)
    self.l_dob = tk.Label(frame_a, text="Date of Birth")
    self.e_dob = tk.Entry(frame_a)
    self.l_lnchg = tk.Label(frame_a, text="Licensee Name Change")
    self.e_lnchg = tk.Entry(frame_a)
    self.l_psqcd = tk.Label(frame_a, 
      text="Personal Security Question Code")
    self.e_psqcd = tk.Entry(frame_a)
    self.l_psq = tk.Label(frame_a, text="Custom PSQ")
    self.e_psq = tk.Entry(frame_a)
    self.l_psqa = tk.Label(frame_a, text="PSQ Answer")
    self.e_psqa = tk.Entry(frame_a)
    self.l_felon = tk.Label(frame_a, 
      text="Basic Qualification Question")
    self.e_felon = Combobox(frame_a, values=felony,
      textvariable=va_felon)

    self.b_save = tk.Button(frame_a, text="Save Updates", 
      command=self.uVA)
        
    # Force some static values for attachments, signature, applicant
    # type, and physician certificate
    self.e_physcert.insert(0,"N")
    self.e_att.insert(0,"N")
    self.e_sigok.insert(0,"Y")
    self.e_apptyp.insert(0,"I")
  
    self.e_lname.insert(0,VAs[vapl].lname)
    self.e_fname.insert(0,VAs[vapl].fname)
    self.e_mi.insert(0,VAs[vapl].mi)
    self.e_nmsuf.insert(0,VAs[vapl].nmsuf)
    self.e_call.insert(0,VAs[vapl].call)
    self.e_street.insert(0,VAs[vapl].street)
    self.e_city.insert(0,VAs[vapl].city)
    self.e_state.insert(0,VAs[vapl].state)
    self.e_zipcd.insert(0,VAs[vapl].zipcd)
    self.e_ssn.insert(0,VAs[vapl].ssn)
    self.e_frn.insert(0,VAs[vapl].frn)
    self.e_phone.insert(0,VAs[vapl].phone)
    self.e_email.insert(0,VAs[vapl].email)
    self.e_felon.insert(0,VAs[vapl].felon)
    self.e_appcd.insert(0,VAs[vapl].appcd)
    self.e_updcall.insert(0,VAs[vapl].updcall)
    self.e_lnchg.insert(0,VAs[vapl].lnchg)
    self.e_opclass.insert(0,VAs[vapl].opclass)
    self.e_vafn.insert(0,VAs[vapl].fn)

    self.l_lname.grid(row=1,column=1)
    self.e_lname.grid(row=2,column=1)
    self.l_fname.grid(row=1,column=2)
    self.e_fname.grid(row=2,column=2)
    self.l_mi.grid(row=1,column=3)
    self.e_mi.grid(row=2,column=3)
    
    self.l_nmsuf.grid(row=4,column=1)
    self.e_nmsuf.grid(row=5,column=1)
    self.l_call.grid(row=4, column=3)
    self.e_call.grid(row=5, column=3)
   
    self.l_street.grid(row=6,column=1)
    self.e_street.grid(row=7,column=1)

    self.l_city.grid(row=8,column=1)
    self.e_city.grid(row=9,column=1)
    self.l_state.grid(row=8,column=2)
    self.e_state.grid(row=9,column=2)
    self.l_zipcd.grid(row=8,column=3)
    self.e_zipcd.grid(row=9,column=3)

    self.l_ssn.grid(row=10, column=1)
    self.e_ssn.grid(row=11,column=1)
    self.l_frn.grid(row=10,column=2)
    self.e_frn.grid(row=11,column=2)

    self.l_phone.grid(row=12,column=1)
    self.e_phone.grid(row=13,column=1)
    self.l_email.grid(row=12,column=2)
    self.e_email.grid(row=13,column=2)

    self.l_felon.grid(row=14,column=1)
    self.e_felon.grid(row=15,column=1)
    self.l_appcd.grid(row=14,column=2)
    self.e_appcd.grid(row=15,column=2)
    self.l_updcall.grid(row=14,column=3)
    self.e_updcall.grid(row=15,column=3)

    self.l_lnchg.grid(row=16,column=1)
    self.e_lnchg.grid(row=17,column=1)

    self.l_opclass.grid(row=16,column=2)
    self.e_opclass.grid(row=17,column=2)

    self.l_vafn.grid(row=16, column=3)
    self.e_vafn.grid(row=17, column=3)

    self.b_save.grid(row=18,column=1)
    self.b_ret.grid(row=18,column=2)

    

    #set the widget tab-order properly.
    taborder=(self.e_lname, self.e_fname, self.e_mi, self.e_nmsuf,\
      self.e_call, self.e_street,self.e_city, self.e_state,\
      self.e_zipcd, self.e_ssn, self.e_frn,self.e_phone,\
      self.e_email, self.e_felon, self.e_appcd, self.e_updcall,\
      self.e_lnchg, self.e_opclass, self.e_vafn)
    for wid in taborder:
      wid.lift()
    frame_a.pack()

  ## Update VA
  #
  #  Update an applicant already in the applicants array for this
  #  session.
  def uVA(self):
    global vapl
    # Most of these probably don't need to be set like this, but it
    # does make the array append a little cleaner
    va_fn = self.e_vafn.get()
    va_call = self.e_call.get().upper()
    # Remove dashes from the ssn, if included
    va_ssn = self.e_ssn.get().replace("-","")
    va_ent = self.e_ent.get()
    # First name is 20 char max
    va_fname = self.e_fname.get()[:20]
    # MI is one char, and must be caps
    va_mi = self.e_mi.get().upper()[:1]
    # Last name is 20 char max
    va_lname = self.e_lname.get()[:20]
    # Suffix is 3 char max
    va_nmsuf = self.e_nmsuf.get()[:3]
    va_attn = self.e_attn.get()
    # Street address is 60 char max
    va_street = self.e_street.get()[:60]
    # P.O. Box is 20 char max
    va_pobox = self.e_pobox.get()[:20]
    # City is 20 char
    va_city = self.e_city.get()[:20]
    va_state = self.e_state.get()
    # Remove dashes from zip code (if present)
    va_zipcd = self.e_zipcd.get().replace("-","")
    # Remove formatting from phone number (if present)
    va_phone = self.e_phone.get().replace("(","").\
      replace(")","").replace("-","")
    # Remove formatting from fax number (if present)
    va_fax = self.e_fax.get().replace("(","").\
      replace(")","").replace("-","")
    # Email is 50 char max
    va_email = self.e_email.get()[:50]
    va_appcd = self.e_appcd.get()
    va_opclass = self.e_opclass.get()
    va_sigok = self.e_sigok.get()
    va_physcert = self.e_physcert.get()
    va_reqexp = self.e_reqexp.get()
    va_waivereq = self.e_waiverreq.get()
    va_att = self.e_att.get()
    va_updcall = self.e_updcall.get()
    va_trusteecall = self.e_trusteecall.get()
    va_apptyp = self.e_apptyp.get()
    va_frn = self.e_frn.get()
    va_dob = self.e_dob.get()
    va_lnchg = self.e_lnchg.get()
    va_psqcd = self.e_psqcd.get()
    va_psq = self.e_psq.get()
    va_psqa = self.e_psqa.get()
    va_felon = self.e_felon.get()

    # Formatted (zero-padded) FRN
    frn = ""

    # FRN supercedes ssn 
    if va_frn:
      va_ssn = ""
      #If the FRN is <10 digits, zero pad it
      frn = va_frn.zfill(10)
    else:
      if len(va_ssn)!=9:
        showerror(title="UVA SSN Error", message="SSN is not 9 digits.")
        return

    if va_felon == "null" or va_felon == "":
      va_felon = ""
      if va_appcd != "AU":
        showerror(title="Basic Qualification Question Error",
          message="'Basic Qualification Question' must be answered.")
        return

    if va_state == "-----" or va_state == "":
      showerror(title="State Error", 
        message="Please select a valid state.")
      return

    if va_opclass == "null" or va_opclass == "":
      showerror(title="Class Error",
        message="Please select a valid operator class.")
      return

    VAs[vapl].fn=va_fn
    VAs[vapl].call=va_call
    VAs[vapl].ssn=va_ssn
    VAs[vapl].entname=va_ent
    VAs[vapl].fname=va_fname
    VAs[vapl].mi=va_mi
    VAs[vapl].lname=va_lname
    VAs[vapl].nmsuf=va_nmsuf
    VAs[vapl].attn=va_attn 
    VAs[vapl].street=va_street 
    VAs[vapl].pobox=va_pobox 
    VAs[vapl].city=va_city 
    VAs[vapl].state=va_state 
    VAs[vapl].zipcd=va_zipcd 
    VAs[vapl].phone=va_phone 
    VAs[vapl].fax=va_fax 
    VAs[vapl].email=va_email 
    VAs[vapl].appcd=va_appcd 
    VAs[vapl].opclass=va_opclass 
    VAs[vapl].sigok=va_sigok
    VAs[vapl].physcert=va_physcert
    VAs[vapl].reqexp=va_reqexp
    VAs[vapl].waivereq=va_waivereq
    VAs[vapl].att=va_att 
    VAs[vapl].updcall=va_updcall 
    VAs[vapl].trusteecall=va_trusteecall
    VAs[vapl].apptyp=va_apptyp
    VAs[vapl].frn=frn
    VAs[vapl].dob=va_dob
    VAs[vapl].lnchg=va_lnchg
    VAs[vapl].psqcd=va_psqcd
    VAs[vapl].psq=va_psq
    VAs[vapl].psqa=va_psqa
    VAs[vapl].felon=va_felon
    
    # Reset the form for the next applicant.
    self.e_vafn.delete(0,'end')
    self.e_call.delete(0, 'end')
    self.e_ssn.delete(0, 'end')
    self.e_ent.delete(0, 'end')
    self.e_fname.delete(0, 'end')
    self.e_mi.delete(0, 'end')
    self.e_lname.delete(0, 'end')
    self.e_nmsuf.delete(0, 'end')
    self.e_attn.delete(0, 'end')
    self.e_street.delete(0, 'end')
    self.e_pobox.delete(0, 'end')
    self.e_city.delete(0, 'end')
    self.e_state.delete(0, 'end')
    self.e_zipcd.delete(0, 'end')
    self.e_phone.delete(0, 'end')
    self.e_fax.delete(0, 'end')
    self.e_email.delete(0, 'end')
    self.e_appcd.delete(0, 'end')
    self.e_opclass.delete(0, 'end')
    self.e_reqexp.delete(0, 'end')
    self.e_waiverreq.delete(0, 'end')
    self.e_updcall.delete(0, 'end')
    self.e_trusteecall.delete(0, 'end')
    self.e_frn.delete(0, 'end')
    self.e_dob.delete(0, 'end')
    self.e_lnchg.delete(0, 'end')
    self.e_psqcd.delete(0, 'end')
    self.e_psq.delete(0, 'end')
    self.e_psqa.delete(0, 'end')
    self.e_felon.delete(0, 'end')
    self.master.destroy()

    
    
    
    def change_dropdown(*args):
        print( va_updcall.get() )



app = mainWindow()
app.wm_title("FCC Electronic Batch File Generator v." \
    + maver + "." + miver + "." + ptver)
app.mainloop()
