# pyEBFGen Guide v2.0.0

## Overview

This guide is intended to give you a quick overview of how to use the
pyEBFGen tool to generate the batch files necessary to submit
*individual* applications to the FCC automated processing system. The
creation of non-individual applications is currently outside the scope
of this tool.  In addition, this document does not cover any special
requirements the FCC may have for file upload.

## First Run
The following preliminary actions need to be taken in order to use
pyEBFGen.  If they are not taken, the program will simply present an
error message and exit.

1. Obtain your VEC's (public) encryption key from your VEC Chairman, and
Load key into the program's keystore with the import.py script. Usage:
`./importkey.py keyfile.asc`
2. Edit the key's trust: `gpg --homedir=./gpg --edit-key <KEY_ID>`. NOTE
that this must be run from the directory you will be running ebfgen
from.
  - The key's information will be printed out, and the final line of
    the output will be the prompt `gpg>`.  At this prompt, type the
    command "trust", and hit <enter>.  
  - You will then be asked how well you trust the key, from 1 (you do
    not trust it) to 5 (you trust it ultimately).  Choose "5", and
    press <enter>.  
  - You will be asked if you're sure.  Answer "Y", and press <enter>.  
  - You will be returned to the `gpg>` prompt at this point.  Type in
    "save", and GPG will finish, returning you to your normal system 
    prompt.  

3. Set the default VEC settings in the `vec.cfg` configuration file.
  * __Mandatory:__ Set VEC encryption key in this file.  Default value 
    is BLANK, and program will generate errors if you attempt to run
    without the key defined. Example `key="VEC Key <vec@radio.group>"`.
    Key fingerprints (e.g. `key=7F08D422`) are also acceptable.
4. Create a test batch file to ensure all is working.

## Using pyEBFGen

When launching the application, you will initially be presented with a
main window containing several blank data fields that correspond to a
given testing session (VEC Code, # tested, elements passed, and so on).

Until this is filled in, the "Save" button will remain RED as a visual
indicator that the VE header has not yet been generated.  

To generate the header, fill in the blank VE fields and click the "Apply
VEC" button.  Once the header has been successfully generated, the
"Save" button will turn GREEN.

## VEC & Session Information Window

First time users may not know what the required fields mean.  Here is
a breakdown of each field:

 - VEC Code:  That is the single letter code for your VEC.  You will 
need to enter that letter in all caps.
 - Session Date:  You will type in the date using DD/MM/YYYY. Do not
forget to use the "/" when typing in the date. If you don’t use it,
the batch file will require manual editing which can delay your session
from being processed by the FCC. Once you have typed in the date, contunue.
 - Exam City:  Self explanatory. You need to type in the city where the
session was held. Once you have typed in the city, continue.
 - Exam State:  Self explanatory. Select the state or territory from the
drop down menu in the cell.  If you are submitting a session that was held
outside the United States, or an APO location, select "DX" for the state.
Once you have selected the state or territory, continue.
 - Applicants Tested:  So, this is a cell where you need to type in the
number of people you had come to take a test. In essence, if you had a total
of 7 applicants at your session with 4 candidates to take a test and 3 doing
administrative updates, you would only indicate that you had 4 people taking
a test.  Once you have typed in the numeric value, continue.
 - Applicants Passed:  This is a count of all the candidates that actually
passed their exams during this session. Even if one or two failed their
first attempt and passed a second exam, you still count that as a candidate
that actually came out of the session with a CSCE.  Once you have typed
in the numeric value, continue.
 -  Applicants Failed:  This is a number of candidates that did NOT pass
an exam whatsoever during the session. Once you have typed in the value,
continue.
 -  Elements Passed:  This is a count of all the elements that were passed
during this particular testing session.  In essence, if you had 9 elements,
5 Technician, 2 General and 2 Amateur Extra with a total of these exams
receiving a passing score of 7, then you would type in the numeric value
of 7, which would indicate that 7 of the examinations administered received
a passing score.  Once you have typed in the numeric value, continue.
 -  Elements Failed:  This is a count of all the elements that were failed
during this particular testing session.  In essence, if you had 9 elements,
5 Technician, 2 General and 2 Amateur Extra with a total of these exams
receiving a failing score of 2, then you would type in the numeric value of
2, which would indicate that 2 of the examinations administered received a
failing score.
 - Regional Identifier:  This is a single letter code that is used to help
identify the location where the test session was held.  For a complete list
of codes, please read the `rid.md` file.  This is a required entry.

When all the data fields have been filled in, press the "Apply" button,
then close the window.  You will be returned to the main window, and
will now see that the upper portion of the screen has been populated.

### VEC Configuration File
In addition to the manual process outlined above, if your VEC happens to
perform frequent testing sessions at the same facility (e.g. library,
community center, etc.), you can set "default" information in the
configuration file "vec.cfg".  This uses standard ".ini file"
formatting of "key = value".  Leave the section header "[VEC_CFG]" on
the first line.

|  Key  | Description| Default| 
| ----- | -----------| -------|
| VEC   | Examiner Code| C    |
| city  | Examination City| Anchorage|
| state | Examination State| AK|
| regcd | "Region" Code| X    |
| visaid| Visual Aid| False |

Most of these are self-explanatory.  **visaid** is a visual aid setting,
in case you're red-green colorblind, replacing RED with YELLOW and GREEN
with BLUE.


**NOTE** - changes made within the program WILL NOT be reflected in the
configuration file.  

## Adding Applicants

To add applicant ("VA" record) information to the batch file, use the
"Add Applicant" option from the main window.  This will open a new
window with the same general fields as the FCC form 605.  When you
complete an application, the "Save Application" button will clear the
form to allow you to enter additional applicants. When you have added
(and saved) the final applicant for a session, you can click the "Close
Window" button.

This form will validate the following data fields, or perform the
following actions, in accordance with the FCC's EBF Userguide.

  - First name will be truncated to twenty (20) characters.
  - MI will be truncated to one (1) character, and forced uppercase.
  - Last name will be truncated to twenty (20) characters.
  - If the applicant has provided an SSN, and it is not equal to 9
    digits (after removing any dashes), you will receive a warning and
    data will not be saved to the batch file.
  - If the applicant has provided a FRN, and it is not equal to 10
    digits, the application will zero-pad the FRN to 10 digits.
  - If the application form has both an SSN and FRN, the FRN takes
    precedence, and SSN will be removed from the application record, in
    accordance with FCC guidelines.
  - If the application purpose is not "AU", and the Basic Qualification
    Question is not answered, you will receive a warning and the
    application information will not be saved.
  - If a state / territorry separator is selected (i.e. "-----"), you
    will receive a warning and the application information will not be 
    saved to the batch file. Likewise, if no state / territory option is
    selected.
  - If the application does not have an operator class selected, you
    will receive a warning, and the application information will not be
    saved.

In the event of one of the above warnings, the form will retain all
previously entered data (with the exception of dropdown options).
Correct the error and save.

## Application Fields Explained

By now you have completed the first line of data that is read by the
EBF system when it’s submitted to the FCC.  Each value listed in the 
VEC & Session Info windows above gives the NCVEC necessary statistics
that in turn allows them to see how the corresponding VEC is doing as
far as candidate numbers during each session. Now, we start with the
very important data, which is entering in the applicant information
from the 605 Form.  Let’s go through each field:

  - *Last Name*:  You will need to enter the last name, or surname of
    the applicant. If the applicant is applying for a new license,
    please use the same formatting technique for the first name by ONLY
    capitalizing the first letter. Once you have typed in the last name,
    continue. 
  - *First Name*:  Self explanatory.  Type in the first name of the
    applicant. If it is a new applicant for a new license, please type
    in their first name by capitalizing the first letter and leaving the
    rest in lower case format. It looks better in the ULS and rather
    proper.  Once you have filled in the field, continue.
  - *Middle Initial*:  This is for the applicant’s middle initial. If
    they do have a middle initial, please type it in ALL CAPS, without a
    period. Just the letter. If they have more than one middle name,
    please inform the candidate that we can only submit one middle
    initial on their application, as the FCC is not setup for multiple
    middle names at this time.  Once you have typed in the middle
    initial, if applicable, continue.
  - *Suffix*:  If the person is a Sr. Jr. or a Roman Numeral, thus being
    a I, II, III, etc, please type it in, without the period.  Just the
    letters. Once you have typed in the data, or if nothing needs to be
    placed in there, continue.
  - *Callsign*:  This is self explanatory.  If the applicant is already
    licensed, you will need to enter their amateur radio callsign, ALL
    CAPS will be enforced by the program. If the applicant does not have
    an amateur radio license, leave that field blank and continue.
  - *Mailing Address*:  You will type in the mailing address of the
    candidate. If the candidate has a post office box, proper formatting
    of listing a post office box will be as follows: "P.O. Box 1111"
    without the quotes of course.  If they have a street address, type
    that in and continue.
  - *City*:  Type in the city as printed on the 605 Form and continue.
  - *State*:  Select the state or U.S. Territory from the list as shown
    on the 605 Form and continue.
  - *Zip Code*:  So, on the 605 Form, it shows that the zip code can be 5 or
    9 characters. Dashes will automatically be removed by the
    application.
  - *Social Security Number*:  Again, another self explanatory item. If
    the applicant does NOT have a FRN and is testing for a new license,
    they MUST provide a Social Security Number or Tax ID number pursuant
    to the Debt Collection Act of 1996. If they refuse to provide that
    information, you are not legally permitted to administer a license
    examination. If they are testing for a new license and they do not
    have a FRN, please type in the SSN.
  - *Federal Registration Number*:  If the applicant is already
    licensed, you MUST type in their FRN. If the applicant already has
    an FRN but no other licenses with the FCC, please enter it in here,
    even if it has leading zeros. If an FRN needs to be entered here,
    type it in and continue.
    - *NOTE*:  If the user types in a Social Security Number and a
      Federal Registration Number, the Social Security Number will
      immediately be purged upon saving the data.
  - *Phone No.*:  When you type in the telephone number, we only need
    the numbers, no parenthesis or dashes.  For example, if the
    applicant gives you a phone number of (907) 465-3781, you will type
    it in as follows: 9074653781. Once you have typed in the telephone
    number, continue.
  - *E-Mail Address*:  Providing an email address is very helpful,
    because it allows for the FCC to send out a pdf copy of their
    license once it’s granted. As of February 2015, the Commission no
    longer sends out a paper copy unless you file the FCC form 605
    asking for one.  Providing an email address allows them to send one
    via email that you can download, archive and print from home. Much
    faster than waiting almost two weeks for a paper copy.  Once you
    have typed in the email address, continue.
  - *Basic Qualification Question*:  If this is for a new amateur radio
    license application, license upgrade, systematic callsign change or
    any type of renewal that is being submitted with this session, the
    question MUST be answered. If you are submitting an application for
    an administrative update (i.e. changing their mailing address) you 
    must leave that field blank.  Once you are done with this field,
    continue.
  - *Application Purpose*:  There are five options to chose from,
    depending on the reason for having an applicant at your session.
    Here is a breakdown of each option and how it applies:
    - *AU*:  Simply means the applicant is here to perform an
      administrative update, which includes changing their mailing
      address.
    - *MD*:  Modification of license...this is the selection you would
      make if an applicant was testing for a license upgrade, or you
      were performing an administrative update and the applicant wanted
      to also change their callsign systematically.
    - *NE*:  New license.  Select this if the applicant is here taking
      a test for the very first time, for a new amateur radio license.
    - *RM*:  Renewal and Modification...this is selected if the
      candidate is here to renew their license, whether it is within 90
      days of expiration or within the two year grace period.  Also
      would include a license upgrade. If they are taking a test to
      upgrade their license as well as seeking a renewal, you would
      select this option.
    - *RO*:  Renewal Only...select this if you are processing a renewal
      for a current licensee.  Make sure the license is within 90 days
      of expiring or if it has already expired, within the two year
      grace period.
    - Once you have selected the purpose of this specific application,
      continue.
  - *Change Callsign Systematically?*:  If the applicant has upgraded
    their license, performed an administrative update and asked to
    change their callsign to the next systematically available, you
    would select "Y" for yes.  If this is a new application, leave it
    blank.  If they have upgraded their license and do not want to
    change their callsign yout must select "N" for no.  Continue when
    completed with this field.
  - *Licensee Name Change*:  If an applicant needs to make a name
    change, whatever type of name change, you must select "Y" for yes.
    If the applicant is doing a name change, make sure you have their
    name entered that is to be reflected on their license. Otherwise,
    leave blank and continue.  
  - *Operator Class*:  If you have a new candidate and they take a test,
    you will select the class of license they have received a CSCE for.
    If you are submitting an administrative update or renewal, make sure
    you have correctly selected the class of license they hold otherwise
    it will cause an error in the application when it’s uploaded for
    batch processing with the FCC.  Once you have selected the class of
    license, continue.
  - The last field you will see is labeled *"Pending File No."*.  This
    corresponds to a question on the 605 Form asking if the applicant
    has another license application on file with the FCC that is
    awaiting action.  Most, if not all applicants, will not have a file
    awaiting action from the FCC unless it is a vanity callsign
    application or another license application where the individual
    answered "Yes" to the felony question.  That will happen from time
    to time and if you encounter an applicant with a pending application
    like that, you will need to enter the file number as it appears in
    the ULS.  The candidate should have that file number for you and
    include it in that section of the 605 Form. If there is no data, or
    pending application on file with the FCC, continue.
  - Once you have completed that application, please click on the 
    *"Save Application"* button.
  - You may immediately start on your next application, or click 
    *"Close Window"*.

## Previewing the batch file

At any time after applying the VEC information (i.e. when the "save"
button is Green or Blue), you can preview the current state of the batch
file by clicking on the "Batch File Preview" button.

## Updating an erroneous entry

If you notice an error in the preview window, take note of the
"Applicant ID" for that line item.  It starts at zero (0), and counts
upwards from there.  Take that value, and fill in the "Applicant ID"
field of the main EBFGen window and press the "Update Applicant" button.

A new window will be opened, identical to the standard "New Applicant"
view, but will be pre-populated with the values from the applicant line
item you selected.  Make the necessary corrections and click the "Save
Updates" button.  

The form has the same validations as the primary "Add Applicant" form.


## Generating the batch file

When all applicants have been added, you can generate the session
information with the "Save Current Session" option.  This will present
you with a standard "save as" dialog menu, with a suggested filename
consisting of the VEC Code, date (from VEC input window, in mmdd
format), the Regional Identifier, and Data File counter, and the file
extension ".dat".  For example, "C0814A01.dat".   If the suggested
filename is not appropriate for the session / location, change it before
saving the file.

Upon saving the file, the program will partially reset itself, in
preparation for another session:

  - The applicant list will be cleared
  - The counts of "Applicants Tested" (Passed, Failed) and "Elements
    Passed" (Failed) will be reset to zero.
  - The data file counter will be incremented.


## Converting a response file

After submitting the batch file to the FCC, they will generate a
response file.  You can use pyEBFGen to read this file and convert the
records into comma-separated values.  This can be achieved by using the
"Convert Response" option.  Response files converted in this fashion
will be saved to your computer's filesystem in ".csv" format for easier
viewing in your preferred spreadsheet application - such as LibreOffice
Calc or Microsoft Excel.  

Files saved in such a manner will be saved to the same directory /
folder as you imported the response file from.  It is recommended that
you save the response to a known location before attempting to convert.

In addition to saving the file, the application will pop up a small
preview window for quick review of the output.  

## FCC Response Codes
[FCC](https://www.fcc.gov/sites/default/files/ebf_error_codes_09072017.pdf)

## IRC Support
If you have questions about the application, you can find us on the OFTC
IRC Network in the #efbgen channel.  IRC address is irc.oftc.net ... you
can connect via Port 6667 for non-secure, or use Port 6697 for SSL.
