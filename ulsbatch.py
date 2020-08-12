#!/usr/bin/python3
########################################################################
#
#
#                       script: ulsbatch
#                           by: Dan Purgert
#                    copyright: 2016
#                      version: 0.5
#                         date: Mon, 10 Aug 2020 14:35:40 -0400
#                      purpose: Generates a batch file for upload to
#                             : the FCC ULS system.
#
#                      license: GPL v2 (only)
#                   repository: https://github.com/dpurgert
#
#
########################################################################
import tkinter as tk
from tkinter import *
#from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfile 
from array import *

VAs=[]
c=0
states=['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA'\
        ,'GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA'\
        ,'MI','MN','MO','MS','MT','NE','NV','NH','NJ','NM','NY','NC'\
        ,'ND','MP','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX'\
        ,'UM','UT','VT','VA','VI','WA','WV','WI','WY','-----','AE','AP'\
        ,'AA','-----','DX']
apppur=['AU','MD','NE','RM','RO']
liccls=['N','T','G','A','E']
felony=['null','Y','N']
opts=['Y','N']
#VE Record fields
VEC = ""
sdt = ""
vecity = ""
vestate = None
appt = ""
appp = ""
appf = ""
elmp = ""
elmf = ""
      

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
      self.attfn = "" #attachment filename MUST be null
      self.attfx = "" #attachment faxed MUST be null
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
      vestate = StringVar(root)

      #VA Attributes
      self.va_fn = ""
      self.va_call = ""
      self.va_ssn = ""
      self.va_ent = ""
      self.va_fname = ""
      self.va_mi = ""
      self.va_lname = ""
      self.va_nmsuf = ""
      self.va_attn = ""
      self.va_street = ""
      self.va_pobox = ""
      self.va_city = ""
      self.va_state = StringVar(root)
      self.va_zipcd = ""
      self.va_phone = ""
      self.va_fax = ""
      self.va_email = ""
      self.va_appcd = StringVar(root)
      self.va_opclass = StringVar(root)
      self.va_sigok = ""
      self.va_physcert = ""
      self.va_reqexp = ""
      self.va_waivereq = ""
      self.va_att = ""
      self.va_updcall = StringVar(root)
      self.va_trusteecall = ""
      self.va_apptyp = ""
      self.va_frn = ""
      self.va_dob = ""
      self.va_lnchg = ""
      self.va_psqcd = ""
      self.va_psq = ""
      self.va_psqa = ""
      self.va_felon = ""

      Frame.__init__(self,master)
      self.master=master
      menu = Menu(self.master)
      self.master.config(menu=menu)

      vaMenu = Menu(menu)
      vaMenu.add_command(label="Extended", command=self.extVAwin)
      vaMenu.add_command(label="Standard", command=self.stdVAwin)


      fileMenu = Menu(menu)
      fileMenu.add_cascade(label="VA",menu=vaMenu)
      fileMenu.add_command(label="VE",command=self.updVE)
      fileMenu.add_command(label="Save",command=self.writeFile)
      fileMenu.add_command(label="Exit",command=self.exitProgram)
      menu.add_cascade(label="File", menu=fileMenu)

      frame_a=tk.Frame(self.master)
      #VAwindow=tk.Frame(self.master)
      frame_c=tk.Frame(self.master)

      vec_sec = tk.Label(frame_a, text="VEC Information:")
      vec_sec.pack()
      self.l_VEC = tk.Label(frame_a, text="VEC Code:" + VEC)
      self.l_sess = tk.Label(frame_a, text="Session Date:"+ sdt)
      self.l_city = tk.Label(frame_a, text="Exam City:"+ vecity)
      self.l_state = tk.Label(frame_a, text="Exam State:" + vestate.get())
      self.l_appT = tk.Label(frame_a, text="Applicants Tested:"+ appt)
      self.l_appP = tk.Label(frame_a, text="Applicants Passed:"+ appp)
      self.l_appF = tk.Label(frame_a, text="Applicants Failed:"+ appf)
      self.l_elmP = tk.Label(frame_a, text="Elements Passed:"+ elmp)
      self.l_elmF = tk.Label(frame_a, text="Elements Failed:"+ elmf)

      self.l_VEC.pack()
      self.l_sess.pack()
      self.l_city.pack()
      self.l_state.pack()
      self.l_appT.pack()
      self.l_appP.pack()
      self.l_appF.pack()
      self.l_elmP.pack()
      self.l_elmF.pack()

      l_VAlist = Label(frame_c, text="Applicant List:")
      self.VA_list = tk.Text(frame_c, width=180, height=10, bg="white")
      l_VAlist.pack()
      self.VA_list.pack()

      frame_a.pack()
      #VAwindow.pack()
      frame_c.pack()

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
  
      VEC = self.e_VEC.get()
      sdt = self.e_sess.get()
      vecity = self.e_vecity.get()
      vestate = self.e_vestate.get()
      appt = self.e_appT.get()
      appp = self.e_appP.get()
      appf = self.e_appF.get()
      elmp = self.e_elmP.get()
      elmf = self.e_elmF.get()

      self.l_VEC['text']="VEC Code: " + VEC
      self.l_sess['text']="Session Date: "+ sdt
      self.l_city['text']="Exam City:"+ vecity
      self.l_state['text']="Exam State:" + vestate
      self.l_appT['text']="Applicants Tested:"+ appt
      self.l_appP['text']="Applicants Passed:"+ appp
      self.l_appF['text']="Applicants Failed:"+ appf
      self.l_elmP['text']="Elements Passed:"+ elmp
      self.l_elmF['text']="Elements Failed:"+ elmf


  def updVE(self):
      #back to parent function
      VEwin = Toplevel(root)
      VEwin.title("VE Entry")


      vec_sec = tk.Label(VEwin, text="VEC Information:")
      vec_sec.grid(row=0, column=2)
      l_VEC = tk.Label(VEwin, text="VEC Code:")
      self.e_VEC = tk.Entry(VEwin)
      l_sess = tk.Label(VEwin, text="Session Date:")
      self.e_sess = tk.Entry(VEwin)
      l_city = tk.Label(VEwin, text="Exam City:")
      self.e_vecity = tk.Entry(VEwin)
      l_state = tk.Label(VEwin, text="Exam State:")
      #self.e_vestate = tk.Entry(VEwin)
      #self.e_vestate = Combobox(VEwin, textvariable=self.vestate)
      self.e_vestate = Combobox(VEwin, values=states,
         textvariable=vestate)
      l_appT = tk.Label(VEwin, text="Applicants Tested:")
      self.e_appT = tk.Entry(VEwin)
      l_appP = tk.Label(VEwin, text="Applicants Passed:")
      self.e_appP = tk.Entry(VEwin)
      l_appF = tk.Label(VEwin, text="Applicants Failed:")
      self.e_appF = tk.Entry(VEwin)
      l_elmP = tk.Label(VEwin, text="Elements Passed:")
      self.e_elmP = tk.Entry(VEwin)
      l_elmF = tk.Label(VEwin, text="Elements Failed:")
      self.e_elmF = tk.Entry(VEwin)
      ve_save = tk.Button(VEwin, text="Save VE",
          command=self.sVE)
      ve_close = tk.Button(VEwin, text="Close",
          command=VEwin.destroy)

      l_VEC.grid(row=1, column=1)
      self.e_VEC.grid(row=1, column=3)
      l_sess.grid(row=2, column=1)
      self.e_sess.grid(row=2, column=3)
      l_city.grid(row=3, column=1)
      self.e_vecity.grid(row=3, column=3)
      l_state.grid(row=4, column=1)
      self.e_vestate.grid(row=4, column=3)
      l_appT.grid(row=5, column=1)
      self.e_appT.grid(row=5, column=3)
      l_appP.grid(row=6, column=1)
      self.e_appP.grid(row=6, column=3)
      l_appF.grid(row=7, column=1)
      self.e_appF.grid(row=7, column=3)
      l_elmP.grid(row=8, column=1)
      self.e_elmP.grid(row=8, column=3)
      l_elmF.grid(row=9, column=1)
      self.e_elmF.grid(row=9, column=3)
      ve_save.grid(row=10,column=1)
      ve_close.grid(row=10,column=2)
      

          
        
  def extVAwin(self):
      VAwindow = Toplevel(root)
      VAwindow.title("VA Entry")

      va_sec = tk.Label(VAwindow, text="Add VA Info:")
      va_sec.grid(row=0, column=5)

      l_vafn = tk.Label(VAwindow, text="File No. for Withdrawal/Amend:")
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
      l_street = tk.Label(VAwindow, text="Street:")
      self.e_street = tk.Entry(VAwindow)
      l_pobox = tk.Label(VAwindow, text="P.O. Box:")
      self.e_pobox = tk.Entry(VAwindow)
      l_city = tk.Label(VAwindow, text="City:")
      self.e_city = tk.Entry(VAwindow)
      l_state = tk.Label(VAwindow, text="State:")
      #self.e_state = tk.Entry(VAwindow)
      self.e_state = Combobox(VAwindow, values=states,
         textvariable=self.va_state)
      l_zipcd = tk.Label(VAwindow, text="Zip Code:")
      self.e_zipcd = tk.Entry(VAwindow)
      l_phone = tk.Label(VAwindow, text="Phone No.:")
      self.e_phone = tk.Entry(VAwindow)
      l_fax = tk.Label(VAwindow, text="Fax No.:")
      self.e_fax = tk.Entry(VAwindow)
      l_email = tk.Label(VAwindow, text="E-mail Address:")
      self.e_email = tk.Entry(VAwindow)
      l_appcd = tk.Label(VAwindow, text="Application Purpose:")
      #self.e_appcd = tk.Entry(VAwindow)
      self.e_appcd = Combobox(VAwindow, values=apppur,
         textvariable=self.va_appcd)
      l_opclass = tk.Label(VAwindow, text="Operator Class:")
      #self.e_opclass = tk.Entry(VAwindow)
      self.e_opclass = Combobox(VAwindow, values=liccls,
         textvariable=self.va_opclass)
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
      l_updcall = tk.Label(VAwindow, text="Change Callsign Systematically:")
      #self.e_updcall = tk.Entry(VAwindow)
      self.e_updcall = Combobox(VAwindow, values=opts, 
        textvariable=self.va_updcall)
      l_trusteecall = tk.Label(VAwindow, text="Trustee Callsign:")
      self.e_trusteecall = tk.Entry(VAwindow)
      l_apptyp = tk.Label(VAwindow, text="Applicant Type:")
      self.e_apptyp = tk.Entry(VAwindow)
      l_frn = tk.Label(VAwindow, text="FCC Registration No.:")
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
      l_felon = tk.Label(VAwindow, text="Felon:")
      #self.e_felon = tk.Entry(VAwindow)
      self.e_felon = Combobox(VAwindow, values=felony,
         textvariable=self.va_felon)

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
          print( self.va_updcall.get() )

  def stdVAwin(self):
      VAwindow = Toplevel(root)
      VAwindow.title("VA Entry")

      va_sec = tk.Label(VAwindow, text="Add VA Info:")
      va_sec.grid(row=0, column=5)

      l_vafn = tk.Label(VAwindow, text="File No. for Withdrawal/Amend:")
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
      l_street = tk.Label(VAwindow, text="Street:")
      self.e_street = tk.Entry(VAwindow)
      l_pobox = tk.Label(VAwindow, text="P.O. Box:")
      self.e_pobox = tk.Entry(VAwindow)
      l_city = tk.Label(VAwindow, text="City:")
      self.e_city = tk.Entry(VAwindow)
      l_state = tk.Label(VAwindow, text="State:")
      #self.e_state = tk.Entry(VAwindow)
      self.e_state = Combobox(VAwindow, values=states,
         textvariable=self.va_state)
      l_zipcd = tk.Label(VAwindow, text="Zip Code:")
      self.e_zipcd = tk.Entry(VAwindow)
      l_phone = tk.Label(VAwindow, text="Phone No.:")
      self.e_phone = tk.Entry(VAwindow)
      l_fax = tk.Label(VAwindow, text="Fax No.:")
      self.e_fax = tk.Entry(VAwindow)
      l_email = tk.Label(VAwindow, text="E-mail Address:")
      self.e_email = tk.Entry(VAwindow)
      l_appcd = tk.Label(VAwindow, text="Application Purpose:")
      #self.e_appcd = tk.Entry(VAwindow)
      self.e_appcd = Combobox(VAwindow, values=apppur,
         textvariable=self.va_appcd)
      l_opclass = tk.Label(VAwindow, text="Operator Class:")
      #self.e_opclass = tk.Entry(VAwindow)
      self.e_opclass = Combobox(VAwindow, values=liccls,
         textvariable=self.va_opclass)
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
      l_updcall = tk.Label(VAwindow, text="Change Callsign Systematically:")
      #self.e_updcall = tk.Entry(VAwindow)
      self.e_updcall = Combobox(VAwindow, values=opts, 
        textvariable=self.va_updcall)
      l_trusteecall = tk.Label(VAwindow, text="Trustee Callsign:")
      self.e_trusteecall = tk.Entry(VAwindow)
      l_apptyp = tk.Label(VAwindow, text="Applicant Type:")
      self.e_apptyp = tk.Entry(VAwindow)
      l_frn = tk.Label(VAwindow, text="FCC Registration No.:")
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
      l_felon = tk.Label(VAwindow, text="Felon:")
      #self.e_felon = tk.Entry(VAwindow)
      self.e_felon = Combobox(VAwindow, values=felony,
         textvariable=self.va_felon)

      #forcing default values
      self.e_physcert.insert(0,"N")
      self.e_att.insert(0,"N")
      self.e_sigok.insert(0,"Y")
      self.e_apptyp.insert(0,"I")

      b_save = tk.Button(VAwindow, text="Save Applicant", command=self.sVA)
      b_close = tk.Button(VAwindow, text="Close Window", 
        command=VAwindow.destroy)
      l_vafn.grid(row=1, column=1)
      self.e_vafn.grid(row=1, column=3)
      l_call.grid(row=2, column=1)
      self.e_call.grid(row=2, column=3)
      l_ssn.grid(row=3, column=1)
      self.e_ssn.grid(row=3,column=3)
      #l_ent.grid(row=4,column=1)
      #self.e_ent.grid(row=4,column=3)
      l_fname.grid(row=5,column=1)
      self.e_fname.grid(row=5,column=3)
      l_mi.grid(row=6,column=1)
      self.e_mi.grid(row=6,column=3)
      l_lname.grid(row=7,column=1)
      self.e_lname.grid(row=7,column=3)
      l_nmsuf.grid(row=8,column=1)
      self.e_nmsuf.grid(row=8,column=3)
      #l_attn.grid(row=9,column=1)
      #self.e_attn.grid(row=9,column=3)
      l_street.grid(row=10,column=1)
      self.e_street.grid(row=10,column=3)
      #l_pobox.grid(row=1,column=4)
      #self.e_pobox.grid(row=1,column=6)
      l_city.grid(row=2,column=4)
      self.e_city.grid(row=2,column=6)
      l_state.grid(row=3,column=4)
      self.e_state.grid(row=3,column=6)
      l_zipcd.grid(row=4,column=4)
      self.e_zipcd.grid(row=4,column=6)
      l_phone.grid(row=5,column=4)
      self.e_phone.grid(row=5,column=6)
      #l_fax.grid(row=6,column=4)
      #self.e_fax.grid(row=6,column=6)
      l_email.grid(row=7,column=4)
      self.e_email.grid(row=7,column=6)
      l_appcd.grid(row=8,column=4)
      self.e_appcd.grid(row=8,column=6)
      l_opclass.grid(row=9,column=4)
      self.e_opclass.grid(row=9,column=6)
      #l_sigok.grid(row=10,column=4)
      #self.e_sigok.grid(row=10,column=6)
      #l_physcert.grid(row=1,column=7)
      #self.e_physcert.grid(row=1,column=9)
      #l_reqexp.grid(row=2,column=7)
      #self.e_reqexp.grid(row=2,column=9)
      #l_waiverreq.grid(row=3,column=7)
      #self.e_waiverreq.grid(row=3,column=9)
      #l_att.grid(row=4,column=7)
      #self.e_att.grid(row=4,column=9)
      l_updcall.grid(row=5,column=7)
      self.e_updcall.grid(row=5,column=9)
      #l_trusteecall.grid(row=6,column=7)
      #self.e_trusteecall.grid(row=6,column=9)
      #l_apptyp.grid(row=7,column=7)
      #self.e_apptyp.grid(row=7,column=9)
      l_frn.grid(row=8,column=7)
      self.e_frn.grid(row=8,column=9)
      #l_dob.grid(row=9,column=7)
      #self.e_dob.grid(row=9,column=9)
      l_lnchg.grid(row=10,column=7)
      self.e_lnchg.grid(row=10,column=9)
      #l_psqcd.grid(row=11,column=3)
      #self.e_psqcd.grid(row=11,column=5)
      #l_psq.grid(row=12,column=3)
      #self.e_psq.grid(row=12,column=5)
      #l_psqa.grid(row=13,column=3)
      #self.e_psqa.grid(row=13,column=5)
      l_felon.grid(row=14,column=3)
      self.e_felon.grid(row=14,column=5)
  
      b_save.grid(row=15,column=5)
      b_close.grid(row=16,column=5)
      
      def change_dropdown(*args):
          print( self.va_updcall.get() )

  def updVA(self):
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
      
      self.VA_list.insert(END, outTxt)
      c=c+1

  def sVA(self):
      #save a VA Entry... eventually
      self.va_fn = self.e_vafn.get()
      self.va_call = self.e_call.get()
      self.va_ssn = self.e_ssn.get()
      self.va_ent = self.e_ent.get()
      self.va_fname = self.e_fname.get()
      self.va_mi = self.e_mi.get()
      self.va_lname = self.e_lname.get()
      self.va_nmsuf = self.e_nmsuf.get()
      self.va_attn = self.e_attn.get()
      self.va_street = self.e_street.get()
      self.va_pobox = self.e_pobox.get()
      self.va_city = self.e_city.get()
      self.va_state = self.e_state.get()
      self.va_zipcd = self.e_zipcd.get()
      self.va_phone = self.e_phone.get()
      self.va_fax = self.e_fax.get()
      self.va_email = self.e_email.get()
      self.va_appcd = self.e_appcd.get()
      self.va_opclass = self.e_opclass.get()
      self.va_sigok = self.e_sigok.get()
      self.va_physcert = self.e_physcert.get()
      self.va_reqexp = self.e_reqexp.get()
      self.va_waivereq = self.e_waiverreq.get()
      self.va_att = self.e_att.get()
      self.va_updcall = self.e_updcall.get()
      self.va_trusteecall = self.e_trusteecall.get()
      self.va_apptyp = self.e_apptyp.get()
      self.va_frn = self.e_frn.get()
      self.va_dob = self.e_dob.get()
      self.va_lnchg = self.e_lnchg.get()
      self.va_psqcd = self.e_psqcd.get()
      self.va_psq = self.e_psq.get()
      self.va_psqa = self.e_psqa.get()
      self.va_felon = self.e_felon.get()

      # FRN supercedes ssn 
      if self.va_frn:
        self.va_ssn = ""

      if self.va_felon == "null":
        self.va_felon = ""

      VAs.append(VA( self.va_fn, self.va_call, self.va_ssn, self.va_ent\
        , self.va_fname, self.va_mi, self.va_lname, self.va_nmsuf\
        , self.va_attn, self.va_street, self.va_pobox, self.va_city\
        , self.va_state, self.va_zipcd, self.va_phone, self.va_fax\
        , self.va_email, self.va_appcd, self.va_opclass, self.va_sigok\
        , self.va_physcert, self.va_reqexp, self.va_waivereq\
        , self.va_att, self.va_updcall, self.va_trusteecall\
        , self.va_apptyp, self.va_frn, self.va_dob, self.va_lnchg\
        , self.va_psqcd, self.va_psq, self.va_psqa, self.va_felon))
      
      
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
      #self.e_sigok.delete(0, 'end')
      #self.e_physcert.delete(0, 'end')
      self.e_reqexp.delete(0, 'end')
      self.e_waiverreq.delete(0, 'end')
      #self.e_att.delete(0, 'end')
      self.e_updcall.delete(0, 'end')
      self.e_trusteecall.delete(0, 'end')
      #self.e_apptyp.delete(0, 'end')
      self.e_frn.delete(0, 'end')
      self.e_dob.delete(0, 'end')
      self.e_lnchg.delete(0, 'end')
      self.e_psqcd.delete(0, 'end')
      self.e_psq.delete(0, 'end')
      self.e_psqa.delete(0, 'end')
      self.e_felon.delete(0, 'end')
      self.updVA()
      
  
  def writeFile(self):
      #VE Record fields
      global VEC
      global sdt
      global vecity
      global vestate
      global appp
      global appf
      global elmp
      global elmf
      
      #VEC = self.e_VEC.get()
      #sdt = self.e_sess.get()
      #vecity = self.e_vecity.get()
      #vestate = self.e_vestate.get()
      #appt = self.e_appT.get()
      #appp = self.e_appP.get()
      #appf = self.e_appF.get()
      #elmp = self.e_elmP.get()
      #elmf = self.e_elmF.get()

      #F=open("output.txt","w");
      F=asksaveasfile(mode='w',defaultextension=".dat")
      if F is None:
        return

      F.write("VE|" + VEC + "|" + sdt + "|" + vecity + \
          "|" + vestate + "|" + appt + "|" + appp + "|" \
          + appf + "|" + elmp + "|" + elmf + "\r\n")

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



  def exitProgram(self):
      exit()


root = Tk()
app = Window(root)
root.wm_title("ULS Batchfile Generator")
root.mainloop()
