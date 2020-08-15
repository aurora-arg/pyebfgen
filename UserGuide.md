#pyEBFGen Guide

##Overview

This guide is intended to give you a quick overview of how to use the
pyEBFGen tool to generate the batch files necessary to submit
*individual* applications to the FCC automated processing system. The
creation of non-individual applications is currently outside the scope
of this tool.  In addition, this document does not cover any special
requirements the FCC may have for file upload.

##Getting Started

When launching the application, you will initially be presented with a
main window containing several blank data fields that correspond to a
given testing session (VEC Code, # tested, elements passed, and so on).
Before adding applicant information, the VEC information should be
supplied.  You can enter this information from the "File -> Add VEC &
Session Numbers" menu option. It is assumed that when creating the data
file, you have already totaled the number of individuals passing (or
failing) the test(s) they took.

When all the data fields have been filled in, press the "Apply" button,
then close the window.  You will be returned to the main window, and
will now see that the upper portion of the screen has been populated.

##Adding Applicants

To add applicant ("VA" record) information to the datafile, use the
"File -> Individual License Application" menu option from the main
window.  This will open a new window with the same general fields as the
FCC form 605.  When you complete an application, the "Save Application"
button will clear the form to allow you to enter additional applicants.
When you have added (and saved) the final applicant for a session, you
can click the "Close Window" button.

This form will validate the following data fields, or perform the
following actions:

  - If the applicant has provided an SSN, and it is not equal to 9
    digits, you will receive a warning and the application information 
    will not be saved.
  - If the applicant has provided a FRN, and it is not equal to 10
    digits, you will receive a warning and the application information
    will not be saved.
  - If the application form has both an SSN and FRN, the FRN takes
    precedence, and SSN will be removed from the application record, in
    accordance with FCC guidelines.
  - If the application purpose is not "AU", and the Basic Qualification
    Question is not answered, you will receive a warning and the
    application information will not be saved.
  - If a state / territorry separator is selected (i.e. "-----"), you
    will receive a warning and the application information will not be 
    saved.

In the event of one of the above warnings, the form will retain all
previously entered data (with the exception of dropdown options).
Correct the error and save.

##Generating the datafile

When all applicants have been added, you can generate the session
information with the "File -> Save Current Session" menu option.  This
will present you with a standard "save as" dialog menu, with a suggested
filename consisting of the VEC Code, date (from VEC input window, in
mmdd format), the Regional Identifier, and Data File counter, and the
file extension ".dat".  For example, "C0814A01.dat".   If the suggested
filename is not appropriate for the session / location, change it before
saving the file.

Upon saving the file, the program will partially reset itself, in
preparation for another session:

  - The applicant list will be cleared
  - The counts of "Applicants Tested" (Passed, Failed) and "Elements
    Passed" (Failed) will be reset to zero.
  - The data file counter will be incremented.


##Converting a response file

After submitting the batch file to the FCC, they will generate a
response file.  You can use pyEBFGen to read this file and convert the
records into comma-separated values.  This can be achieved by using the
"File -> Convert Response" option.  Response files converted in such a
manner will be simultaneously printed into the "File Content:" frame of
the main window AND saved to your computer's filesystem in ".csv"
format for easier viewing in your preferred spreadsheet application -
such as LibreOffice Calc or Microsoft Excel.

Files saved in such a manner will be saved to the same directory /
folder as you imported the response file from.
