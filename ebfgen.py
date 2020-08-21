#!/usr/bin/python3
########################################################################
#
#                       script: ebfgen
#                           by: Dan Purgert
#                    copyright: 2020
#                      version: 0.1.0
#                         date: Mon, 17 Aug 2020 15:13:45 -0400
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
import tkinter as tk
from tkinter import *
#from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import * 
from array import *

maver = "0" #major
miver = "1" #minor
ptver = "0" #patch

VAs=[]  # Array of VA objects.  Filled in as applicants are saved
c=0     # Array counter

# List of states / territories / etc.  
states=['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA'\
        ,'GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA'\
        ,'MI','MN','MO','MS','MT','NE','NV','NH','NJ','NM','NY','NC'\
        ,'ND','MP','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX'\
        ,'UM','UT','VT','VA','VI','WA','WV','WI','WY','-----','AE','AP'\
        ,'AA','-----','DX']

# List of application purpose codes
apppur=['AU','MD','NE','RM','RO']

# List of applicant license classes
liccls=['N','T','G','A','E']

# List for answers about the felony question
felony=['null','Y','N']

# Y|N option list for relevant dropdowns
opts=['Y','N']

#VE Record (batch file header) fields
VEC = ""
sdt = ""
vecity = ""
vestate = None
appt = ""
appp = ""
appf = ""
elmp = ""
elmf = ""
VE_str = ""
tloc = ""
tcnt = 1
vestidx = 0

#Applicant Attributes
va_fn = ""
va_call = ""
va_ssn = ""
va_ent = ""
va_fname = ""
va_mi = ""
va_lname = ""
va_nmsuf = ""
va_attn = ""
va_street = ""
va_pobox = ""
va_city = ""
va_state = ""             
va_zipcd = ""
va_phone = ""
va_fax = ""
va_email = ""
va_appcd = ""             
va_opclass = ""              
va_sigok = ""
va_physcert = ""
va_reqexp = ""
va_waivereq = ""
va_att = ""
va_updcall = ""             
va_trusteecall = ""
va_apptyp = ""
va_frn = ""
va_dob = ""
va_lnchg = ""
va_psqcd = ""
va_psq = ""
va_psqa = ""
va_felon = ""

VA_list = None

# Class to create an object to cram into an array, because apparently
# python doesn't do C-style structures.  Or I'm just an idiot.
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

class fileManager():
  def convertFile():
    # Read in a FCC Response File, and convert it into CSV
    
    inFN = askopenfilename (title="Select File",
      filetypes=(("EBF Response Files","*.rsp"),
      ("All Files","*.*")))

    if inFN is None:
      return

    inF = open(inFN, "r") 

    outFN = inFN[:-4] + ".csv"
    outF = open(outFN, "w")
    inDat=inF.readlines()
    for line in inDat:
      outln=line.replace("|",",")
      Window.rspUpdate(None, outln)  
      outF.writelines(outln)
    outF.close()
  
    showinfo(title="Convert complete", message="Saved as: " + outFN)


class Window(Frame):
  def __init__(self,master=None):
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

      global VA_list
      vestate = StringVar(root)


      Frame.__init__(self,master)
      self.master=master
      menu = Menu(self.master)
      self.master.config(menu=menu)

      fileMenu = Menu(menu)
      #fileMenu.add_command(label="Amateur Club Application",
      #  command=self.extVAwin)
      fileMenu.add_command(label="Individual License Application",
        command=self.stdVAwin)
      fileMenu.add_command(label="Add VEC & Session Numbers",
        command=self.updVE)
      fileMenu.add_command(label="Save Current Session",
        command=self.writeFile)
      fileMenu.add_command(label="Convert Response",
        command=fileManager.convertFile)
      fileMenu.add_command(label="Exit",command=self.exitProgram)
      menu.add_cascade(label="File", menu=fileMenu)

      frame_a=tk.Frame(self.master)
      frame_b=tk.Frame(self.master)
      frame_c=tk.Frame(self.master)

      vec_sec = tk.Label(frame_a, text="Session & VEC Information")
      self.l_VEC = tk.Label(frame_a, text="VEC Code: " + VEC)
      self.l_sess = tk.Label(frame_a, text="Session Date: "+ sdt)
      self.l_city = tk.Label(frame_a, text="Exam City: "+ vecity)
      self.l_state = tk.Label(frame_a, text="Exam State: "\
        + vestate.get())
      self.l_appT = tk.Label(frame_a, text="Applicants Tested: "+ appt)
      self.l_appP = tk.Label(frame_a, text="Applicants Passed: "+ appp)
      self.l_appF = tk.Label(frame_a, text="Applicants Failed: "+ appf)
      self.l_elmP = tk.Label(frame_a, text="Elements Passed: "+ elmp)
      self.l_elmF = tk.Label(frame_a, text="Elements Failed: "+ elmf)
      self.l_tloc = tk.Label(frame_a, text="Regional Identifier: "\
        + tloc)

      vec_sec.pack()
      self.l_VEC.pack()
      self.l_sess.pack()
      self.l_city.pack()
      self.l_state.pack()
      self.l_appT.pack()
      self.l_appP.pack()
      self.l_appF.pack()
      self.l_elmP.pack()
      self.l_elmF.pack()
      self.l_tloc.pack()
      
      l_blank = Label(frame_b, text=" ")
      l_blank.pack()

      self.l_VAcnt = Label(frame_c, text="Data File: "+str(tcnt).zfill(2))
      self.l_VAcnt.pack()
      l_VAlist = Label(frame_c, text="File Content:")
      l_VAlist.pack()
      VA_list = tk.Text(frame_c, width=150, height=10, bg="white")
      VA_list.pack()

      b_VAlist = tk.Button(frame_c, text="Clear Frame", 
        command=self.clrFrame)
      b_VAlist.pack()

      frame_a.pack()
      frame_b.pack()
      frame_c.pack()

  def clrFrame(self):
    VA_list.delete('1.0', END)

  def rspUpdate(self,l):
    VA_list.insert(END,l)

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

      global VE_str
  
      VEC = self.e_VEC.get().upper()
      sdt = self.e_sess.get()
      vecity = self.e_vecity.get()
      vestate = self.e_vestate.get()
      appt = self.e_appT.get()
      appp = self.e_appP.get()
      appf = self.e_appF.get()
      elmp = self.e_elmP.get()
      elmf = self.e_elmF.get()
      tloc = self.e_tloc.get()

      self.l_VEC['text']="VEC Code: " + VEC
      self.l_sess['text']="Session Date: "+ sdt
      self.l_city['text']="Exam City:"+ vecity
      self.l_state['text']="Exam State:" + vestate
      self.l_appT['text']="Applicants Tested:"+ appt
      self.l_appP['text']="Applicants Passed:"+ appp
      self.l_appF['text']="Applicants Failed:"+ appf
      self.l_elmP['text']="Elements Passed:"+ elmp
      self.l_elmF['text']="Elements Failed:"+ elmf
      self.l_tloc['text']="Regional Identifier:" +tloc

      VE_str="VE|" + VEC + "|" + sdt + "|" + vecity + \
          "|" + vestate + "|" + appt + "|" + appp + "|" \
          + appf + "|" + elmp + "|" + elmf
  
      self.rspUpdate(VE_str)


  def updVE(self):
      global vestidx
      # Set VE / EBF file header record.
      VEwin = Toplevel(root)
      VEwin.title("Session and VEC Info")
      def UpdateStateIdx (event):
        global vestidx
        vestidx = self.e_vestate.current()

      vec_sec = tk.Label(VEwin, text="")
      vec_sec.grid(row=0, column=2)
      l_VEC = tk.Label(VEwin, text="VEC Code:")
      self.e_VEC = tk.Entry(VEwin)
      self.e_VEC.insert(0,VEC)    
      l_sess = tk.Label(VEwin, text="Session Date:")
      self.e_sess = tk.Entry(VEwin)
      self.e_sess.insert(0,sdt)
      l_city = tk.Label(VEwin, text="Exam City:")
      self.e_vecity = tk.Entry(VEwin)
      self.e_vecity.insert(0,vecity)
      l_state = tk.Label(VEwin, text="Exam State:")
      self.e_vestate = Combobox(VEwin, values=states,
         textvariable=vestate)
      self.e_vestate.current(vestidx)
      self.e_vestate.bind("<<ComboboxSelected>>", UpdateStateIdx)
      l_appT = tk.Label(VEwin, text="Applicants Tested:")
      self.e_appT = tk.Entry(VEwin)
      self.e_appT.insert(0,appt)
      l_appP = tk.Label(VEwin, text="Applicants Passed:")
      self.e_appP = tk.Entry(VEwin)
      self.e_appP.insert(0,appp)
      l_appF = tk.Label(VEwin, text="Applicants Failed:")
      self.e_appF = tk.Entry(VEwin)
      self.e_appF.insert(0,appf)
      l_elmP = tk.Label(VEwin, text="Elements Passed:")
      self.e_elmP = tk.Entry(VEwin)
      self.e_elmP.insert(0,elmp)
      l_elmF = tk.Label(VEwin, text="Elements Failed:")
      self.e_elmF = tk.Entry(VEwin)
      self.e_elmF.insert(0,elmf)
      l_tloc = tk.Label(VEwin, text="Regional Identifier:")
      self.e_tloc = tk.Entry(VEwin)
      self.e_tloc.insert(0,tloc)
      l_tcnt = tk.Label(VEwin, text="File Counter:")
      self.e_tcnt = tk.Entry(VEwin)
      self.e_tcnt.insert(0,tcnt)
      ve_save = tk.Button(VEwin, text="Apply",
          command=self.sVE)
      ve_close = tk.Button(VEwin, text="Close",
          command=VEwin.destroy)

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
      ve_close.grid(row=9,column=2)
      

          
        
  def extVAwin(self):
      # EXTENDED Applicant entry window.
      VAwindow = Toplevel(root)
      VAwindow.title("Applicant Data")

      va_sec = tk.Label(VAwindow, text="Applicant Information")
      va_sec.grid(row=0, column=5)

      l_vafn = tk.Label(VAwindow, text="Pending File No.:")
      self.e_vafn = tk.Entry(VAwindow)
      l_call = tk.Label(VAwindow, text="Callsign:")
      self.e_call = tk.Entry(VAwindow)
      l_ssn = tk.Label(VAwindow, text="SSN:")
      self.e_ssn = tk.Entry(VAwindow)
      l_ent = tk.Label(VAwindow, text="Entity Name:")
      self.e_ent = tk.Entry(VAwindow)
      l_fname = tk.Label(VAwindow, text="First Name:")
      self.e_fname = tk.Entry(VAwindow)
      l_mi = tk.Label(VAwindow, text="Middle Initial:")
      self.e_mi = tk.Entry(VAwindow)
      l_lname = tk.Label(VAwindow, text="Last Name:")
      self.e_lname = tk.Entry(VAwindow)
      l_nmsuf = tk.Label(VAwindow, text="Suffix:")
      self.e_nmsuf = tk.Entry(VAwindow)
      l_attn = tk.Label(VAwindow, text="Attention:")
      self.e_attn = tk.Entry(VAwindow)
      l_street = tk.Label(VAwindow, text="Mailing Address:")
      self.e_street = tk.Entry(VAwindow)
      l_pobox = tk.Label(VAwindow, text="P.O. Box:")
      self.e_pobox = tk.Entry(VAwindow)
      l_city = tk.Label(VAwindow, text="City:")
      self.e_city = tk.Entry(VAwindow)
      l_state = tk.Label(VAwindow, text="State:")
      self.e_state = Combobox(VAwindow, values=states,
         textvariable=va_state)
      l_zipcd = tk.Label(VAwindow, text="Zip Code:")
      self.e_zipcd = tk.Entry(VAwindow)
      l_phone = tk.Label(VAwindow, text="Phone No.:")
      self.e_phone = tk.Entry(VAwindow)
      l_fax = tk.Label(VAwindow, text="Fax No.:")
      self.e_fax = tk.Entry(VAwindow)
      l_email = tk.Label(VAwindow, text="E-Mail Address:")
      self.e_email = tk.Entry(VAwindow)
      l_appcd = tk.Label(VAwindow, text="Application Purpose:")
      self.e_appcd = Combobox(VAwindow, values=apppur,
         textvariable=va_appcd)
      l_opclass = tk.Label(VAwindow, text="Operator Class:")
      self.e_opclass = Combobox(VAwindow, values=liccls,
         textvariable=va_opclass)
      l_sigok = tk.Label(VAwindow, text="Valid Signature:")
      self.e_sigok = tk.Entry(VAwindow)
      l_physcert = tk.Label(VAwindow, text="Physician Certificate:")
      self.e_physcert = tk.Entry(VAwindow)
      l_reqexp = tk.Label(VAwindow, text="Requested Expiration:")
      self.e_reqexp = tk.Entry(VAwindow)
      l_waiverreq = tk.Label(VAwindow, text="Waiver Request:")
      self.e_waiverreq = tk.Entry(VAwindow)
      l_att = tk.Label(VAwindow, text="Attachments:")
      self.e_att = tk.Entry(VAwindow)
      l_updcall = tk.Label(VAwindow, 
        text="Change Callsign Systematically?:")
      self.e_updcall = Combobox(VAwindow, values=opts, 
        textvariable=va_updcall)
      l_trusteecall = tk.Label(VAwindow, text="Trustee Callsign:")
      self.e_trusteecall = tk.Entry(VAwindow)
      l_apptyp = tk.Label(VAwindow, text="Applicant Type:")
      self.e_apptyp = tk.Entry(VAwindow)
      l_frn = tk.Label(VAwindow, text="Federal Registration No.:")
      self.e_frn = tk.Entry(VAwindow)
      l_dob = tk.Label(VAwindow, text="Date of Birth:")
      self.e_dob = tk.Entry(VAwindow)
      l_lnchg = tk.Label(VAwindow, text="Licensee Name Change:")
      self.e_lnchg = tk.Entry(VAwindow)
      l_psqcd = tk.Label(VAwindow, text="Personal Security Question Code:")
      self.e_psqcd = tk.Entry(VAwindow)
      l_psq = tk.Label(VAwindow, text="Custom PSQ:")
      self.e_psq = tk.Entry(VAwindow)
      l_psqa = tk.Label(VAwindow, text="PSQ Answer:")
      self.e_psqa = tk.Entry(VAwindow)
      l_felon = tk.Label(VAwindow, text="Basic Qualification Question:")
      self.e_felon = Combobox(VAwindow, values=felony,
         textvariable=va_felon)

      b_save = tk.Button(VAwindow, text="Save Applicant", command=self.sVA)
      b_close = tk.Button(VAwindow, text="Close Window", 
        command=VAwindow.destroy)
      l_vafn.grid(row=1, column=1)
      self.e_vafn.grid(row=1, column=3)
      l_call.grid(row=2, column=1)
      self.e_call.grid(row=2, column=3)
      l_ssn.grid(row=3, column=1)
      self.e_ssn.grid(row=3,column=3)
      l_ent.grid(row=4,column=1)
      self.e_ent.grid(row=4,column=3)
      l_fname.grid(row=5,column=1)
      self.e_fname.grid(row=5,column=3)
      l_mi.grid(row=6,column=1)
      self.e_mi.grid(row=6,column=3)
      l_lname.grid(row=7,column=1)
      self.e_lname.grid(row=7,column=3)
      l_nmsuf.grid(row=8,column=1)
      self.e_nmsuf.grid(row=8,column=3)
      l_attn.grid(row=9,column=1)
      self.e_attn.grid(row=9,column=3)
      l_street.grid(row=10,column=1)
      self.e_street.grid(row=10,column=3)
      l_pobox.grid(row=1,column=4)
      self.e_pobox.grid(row=1,column=6)
      l_city.grid(row=2,column=4)
      self.e_city.grid(row=2,column=6)
      l_state.grid(row=3,column=4)
      self.e_state.grid(row=3,column=6)
      l_zipcd.grid(row=4,column=4)
      self.e_zipcd.grid(row=4,column=6)
      l_phone.grid(row=5,column=4)
      self.e_phone.grid(row=5,column=6)
      l_fax.grid(row=6,column=4)
      self.e_fax.grid(row=6,column=6)
      l_email.grid(row=7,column=4)
      self.e_email.grid(row=7,column=6)
      l_appcd.grid(row=8,column=4)
      self.e_appcd.grid(row=8,column=6)
      l_opclass.grid(row=9,column=4)
      self.e_opclass.grid(row=9,column=6)
      l_sigok.grid(row=10,column=4)
      self.e_sigok.grid(row=10,column=6)
      l_physcert.grid(row=1,column=7)
      self.e_physcert.grid(row=1,column=9)
      l_reqexp.grid(row=2,column=7)
      self.e_reqexp.grid(row=2,column=9)
      l_waiverreq.grid(row=3,column=7)
      self.e_waiverreq.grid(row=3,column=9)
      l_att.grid(row=4,column=7)
      self.e_att.grid(row=4,column=9)
      l_updcall.grid(row=5,column=7)
      self.e_updcall.grid(row=5,column=9)
      l_trusteecall.grid(row=6,column=7)
      self.e_trusteecall.grid(row=6,column=9)
      l_apptyp.grid(row=7,column=7)
      self.e_apptyp.grid(row=7,column=9)
      l_frn.grid(row=8,column=7)
      self.e_frn.grid(row=8,column=9)
      l_dob.grid(row=9,column=7)
      self.e_dob.grid(row=9,column=9)
      l_lnchg.grid(row=10,column=7)
      self.e_lnchg.grid(row=10,column=9)
      l_psqcd.grid(row=11,column=3)
      self.e_psqcd.grid(row=11,column=5)
      l_psq.grid(row=12,column=3)
      self.e_psq.grid(row=12,column=5)
      l_psqa.grid(row=13,column=3)
      self.e_psqa.grid(row=13,column=5)
      l_felon.grid(row=14,column=3)
      self.e_felon.grid(row=14,column=5)
  
      b_save.grid(row=15,column=5)
      b_close.grid(row=16,column=5)
      
      def change_dropdown(*args):
          print( va_updcall.get() )

  def stdVAwin(self):
      # Standard Applicant setup.
      # Maybe the windows should be separate classes?
      VAwindow = Toplevel(root)
      VAwindow.title("Applicant Data")

      va_sec = tk.Label(VAwindow, text="Applicant Information")
      va_sec.grid(row=0, column=1)

      l_vafn = tk.Label(VAwindow, text="Pending File Number")
      self.e_vafn = tk.Entry(VAwindow)
      l_call = tk.Label(VAwindow, text="Callsign, if licensed")
      self.e_call = tk.Entry(VAwindow)
      l_ssn = tk.Label(VAwindow, text="Social Security Number")
      self.e_ssn = tk.Entry(VAwindow)
      l_ent = tk.Label(VAwindow, text="Entity Name")
      self.e_ent = tk.Entry(VAwindow)
      l_fname = tk.Label(VAwindow, text="First Name")
      self.e_fname = tk.Entry(VAwindow)
      l_mi = tk.Label(VAwindow, text="Middle Initial")
      self.e_mi = tk.Entry(VAwindow)
      l_lname = tk.Label(VAwindow, text="Last Name")
      self.e_lname = tk.Entry(VAwindow)
      l_nmsuf = tk.Label(VAwindow, text="Suffix")
      self.e_nmsuf = tk.Entry(VAwindow)
      l_attn = tk.Label(VAwindow, text="Attention")
      self.e_attn = tk.Entry(VAwindow)
      l_street = tk.Label(VAwindow, text="Mailing Address")
      self.e_street = tk.Entry(VAwindow)
      l_pobox = tk.Label(VAwindow, text="P.O. Box")
      self.e_pobox = tk.Entry(VAwindow)
      l_city = tk.Label(VAwindow, text="City")
      self.e_city = tk.Entry(VAwindow)
      l_state = tk.Label(VAwindow, text="State / U.S. Territory")
      self.e_state = Combobox(VAwindow, values=states,
         textvariable=va_state)
      l_zipcd = tk.Label(VAwindow, text="Zip Code")
      self.e_zipcd = tk.Entry(VAwindow)
      l_phone = tk.Label(VAwindow, text="Phone Number")
      self.e_phone = tk.Entry(VAwindow)
      l_fax = tk.Label(VAwindow, text="Fax Number")
      self.e_fax = tk.Entry(VAwindow)
      l_email = tk.Label(VAwindow, text="E-Mail Address")
      self.e_email = tk.Entry(VAwindow)
      l_appcd = tk.Label(VAwindow, text="Application Purpose")
      self.e_appcd = Combobox(VAwindow, values=apppur,
         textvariable=va_appcd)
      l_opclass = tk.Label(VAwindow, text="Operator Class")
      self.e_opclass = Combobox(VAwindow, values=liccls,
         textvariable=va_opclass)
      l_sigok = tk.Label(VAwindow, text="Valid Signature")
      self.e_sigok = tk.Entry(VAwindow)
      l_physcert = tk.Label(VAwindow, text="Physician Certificate")
      self.e_physcert = tk.Entry(VAwindow)
      l_reqexp = tk.Label(VAwindow, text="Requested Expiration")
      self.e_reqexp = tk.Entry(VAwindow)
      l_waiverreq = tk.Label(VAwindow, text="Waiver Request")
      self.e_waiverreq = tk.Entry(VAwindow)
      l_att = tk.Label(VAwindow, text="Attachments")
      self.e_att = tk.Entry(VAwindow)
      l_updcall = tk.Label(VAwindow, 
        text="Change Callsign Systematically?")
      self.e_updcall = Combobox(VAwindow, values=opts, 
        textvariable=va_updcall)
      l_trusteecall = tk.Label(VAwindow, text="Trustee Callsign")
      self.e_trusteecall = tk.Entry(VAwindow)
      l_apptyp = tk.Label(VAwindow, text="Applicant Type")
      self.e_apptyp = tk.Entry(VAwindow)
      l_frn = tk.Label(VAwindow, text="Federal Registration Number")
      self.e_frn = tk.Entry(VAwindow)
      l_dob = tk.Label(VAwindow, text="Date of Birth")
      self.e_dob = tk.Entry(VAwindow)
      l_lnchg = tk.Label(VAwindow, text="Licensee Name Change")
      self.e_lnchg = tk.Entry(VAwindow)
      l_psqcd = tk.Label(VAwindow, text="Personal Security Question Code")
      self.e_psqcd = tk.Entry(VAwindow)
      l_psq = tk.Label(VAwindow, text="Custom PSQ")
      self.e_psq = tk.Entry(VAwindow)
      l_psqa = tk.Label(VAwindow, text="PSQ Answer")
      self.e_psqa = tk.Entry(VAwindow)
      l_felon = tk.Label(VAwindow, text="Basic Qualification Question")
      self.e_felon = Combobox(VAwindow, values=felony,
         textvariable=va_felon)

      # Force some static values for attachments, signature, applicant
      # type, and physician certificate
      self.e_physcert.insert(0,"N")
      self.e_att.insert(0,"N")
      self.e_sigok.insert(0,"Y")
      self.e_apptyp.insert(0,"I")

      b_save = tk.Button(VAwindow, text="Save Application", 
        command=self.sVA)
      b_close = tk.Button(VAwindow, text="Close Window", 
        command=VAwindow.destroy)
      l_lname.grid(row=1,column=1)
      self.e_lname.grid(row=2,column=1)
      l_fname.grid(row=1,column=2)
      self.e_fname.grid(row=2,column=2)
      l_mi.grid(row=1,column=3)
      self.e_mi.grid(row=2,column=3)

      l_nmsuf.grid(row=4,column=1)
      self.e_nmsuf.grid(row=5,column=1)
      l_call.grid(row=4, column=3)
      self.e_call.grid(row=5, column=3)
     
      l_street.grid(row=6,column=1)
      self.e_street.grid(row=7,column=1)

      l_city.grid(row=8,column=1)
      self.e_city.grid(row=9,column=1)
      l_state.grid(row=8,column=2)
      self.e_state.grid(row=9,column=2)
      l_zipcd.grid(row=8,column=3)
      self.e_zipcd.grid(row=9,column=3)

      l_ssn.grid(row=10, column=1)
      self.e_ssn.grid(row=11,column=1)
      l_frn.grid(row=10,column=2)
      self.e_frn.grid(row=11,column=2)

      l_phone.grid(row=12,column=1)
      self.e_phone.grid(row=13,column=1)
      l_email.grid(row=12,column=2)
      self.e_email.grid(row=13,column=2)

      l_felon.grid(row=14,column=1)
      self.e_felon.grid(row=15,column=1)
      l_appcd.grid(row=14,column=2)
      self.e_appcd.grid(row=15,column=2)
      l_updcall.grid(row=14,column=3)
      self.e_updcall.grid(row=15,column=3)

      l_lnchg.grid(row=16,column=1)
      self.e_lnchg.grid(row=17,column=1)

      l_opclass.grid(row=16,column=2)
      self.e_opclass.grid(row=17,column=2)

      l_vafn.grid(row=16, column=3)
      self.e_vafn.grid(row=17, column=3)

      b_save.grid(row=18,column=1)
      b_close.grid(row=18,column=2)

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

  def updVA(self):
      # Update the VA Table listing on the main screen
      global c
      d=str(c)
      outTxt=d + ": VA|" + VAs[c].fn + "|" + VAs[c].call + "|" \
        + VAs[c].ssn + "|" + VAs[c].entname + "|" + VAs[c].fname \
        + "|" + VAs[c].mi + "|" + VAs[c].lname + "|" + VAs[c].nmsuf \
        + "|" + VAs[c].attn + "|" + VAs[c].street + "|" \
        + VAs[c].pobox + "|" + VAs[c].city + "|" + VAs[c].state \
        + "|" + VAs[c].zipcd + "|" + VAs[c].phone + "|" + VAs[c].fax \
        + "|" + VAs[c].email + "|" + VAs[c].appcd + "|" \
        + VAs[c].opclass + "|" + VAs[c].sigok + "|" \
        + VAs[c].physcert + "|" + VAs[c].reqexp + "|" \
        + VAs[c].waivereq + "|" + VAs[c].att + "|||" \
        + VAs[c].updcall + "|" + VAs[c].trusteecall + "|" \
        + VAs[c].apptyp + "|" +  VAs[c].frn + "|" + VAs[c].dob + "|" \
        + VAs[c].lnchg + "|" + VAs[c].psqcd + "|" + VAs[c].psq + "|" \
        + VAs[c].psqa + "|" + VAs[c].felon + "\n"
      
      VA_list.insert(END, outTxt)
      c=c+1

  def sVA(self):
      frn = ""
      # Save applicant data to VA array 
      va_fn = self.e_vafn.get()
      va_call = self.e_call.get().upper()
      va_ssn = self.e_ssn.get().replace("-","")
      va_ent = self.e_ent.get()
      va_fname = self.e_fname.get()[0:20]
      va_mi = self.e_mi.get().upper()[0:1]
      va_lname = self.e_lname.get()[0:20]
      va_nmsuf = self.e_nmsuf.get()[0:3]
      va_attn = self.e_attn.get()
      va_street = self.e_street.get()[0:60]
      va_pobox = self.e_pobox.get()[0:20]
      va_city = self.e_city.get()[0:20]
      va_state = self.e_state.get()
      va_zipcd = self.e_zipcd.get().replace("-","")
      va_phone = self.e_phone.get().replace("(","").\
        replace(")","").replace("-","")
      va_fax = self.e_fax.get().replace("(","").\
        replace(")","").replace("-","")
      va_email = self.e_email.get()[0:50]
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

      # FRN supercedes ssn 
      if va_frn:
        va_ssn = ""
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

      VAs.append(VA( va_fn, va_call, va_ssn, va_ent\
        , va_fname, va_mi, va_lname, va_nmsuf\
        , va_attn, va_street, va_pobox, va_city\
        , va_state, va_zipcd, va_phone, va_fax\
        , va_email, va_appcd, va_opclass, va_sigok\
        , va_physcert, va_reqexp, va_waivereq\
        , va_att, va_updcall, va_trusteecall\
        , va_apptyp, frn, va_dob, va_lnchg\
        , va_psqcd, va_psq, va_psqa, va_felon))
      
      
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
      self.updVA()
      
  
  def writeFile(self):
      # Save VEC Header and all applicant records to 
      # user-defined file.
      #VE Record string
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

      fdt = sdt.replace("/","")[:4]
      deffn = VEC+fdt+tloc+str(tcnt).zfill(2)
      tcnt+=1
      appt="0"
      appp="0"
      appf="0"
      elmp="0"
      elmf="0"
      
      F=asksaveasfile(initialfile=deffn+".dat", mode='w',
        defaultextension=".dat")
      if F is None:
        return

      F.write (VE_str+"\r\n")

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
#  Extra pipes here for attachment file / fax ind ^^^
          + VAs[i].updcall + "|" + VAs[i].trusteecall + "|" \
          + VAs[i].apptyp + "|" +  VAs[i].frn + "|" + VAs[i].dob + "|" \
          + VAs[i].lnchg + "|" + VAs[i].psqcd + "|" + VAs[i].psq + "|" \
          + VAs[i].psqa + "|" + VAs[i].felon + "\r\n")
      F.close()

      #clear VA array
      VAs.clear()
      #reset VA Counter
      c = 0
      #clear output frame and update VE info
      self.clrFrame()
      self.l_appT['text']="Applicants Tested:"+ appt
      self.l_appP['text']="Applicants Passed:"+ appp
      self.l_appF['text']="Applicants Failed:"+ appf
      self.l_elmP['text']="Elements Passed:"+ elmp
      self.l_elmF['text']="Elements Failed:"+ elmf
      self.l_VAcnt['text']="Data File: "+str(tcnt).zfill(2)

      



  def exitProgram(self):
      exit()


root = Tk()
app = Window(root)
root.wm_title("FCC Electronic Batch File Generator v." \
    + maver + "." + miver + "." + ptver)
root.mainloop()
