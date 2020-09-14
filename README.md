# ebfgen

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this
document are to be interpreted as described in 
[RFC 2119](https://tools.ietf.org/html/rfc2119).

Python batch file generator for use with the FCC EBF system.  As this
program is intended for use by "remote" VE Teams to allow them to send
batch files to their VEC board / chairman for submission to the EBF
system, all output is encrypted with PGP as a default.  This is done to
ensure that applicant personal data remains secure.  

As the output is encrypted, generated batch files MUST NOT be
transmitted over the amateur radio service, as per 47 CFR part 97.309(b).

> [...] RTTY and data emissions using unspecified digital codes must not
> be transmitted for the purpose of obscuring the meaning of any
> communication.

FCC EBF Documentation can be found at:
https://www.fcc.gov/wireless/systems-utilities/uls-electronic-batch-filing

This should work cross-platform; however my main development environment
is Linux.  If you try on Mac / Windows and find platform-specific bugs,
please let me know.

The program is comprised of two parts:
 - ebfgen.py - The batch file generator itself
 - importkey.py - A small helper script to load the PGP key.

## Requirements
### General Use / VE Team
  - Python 3.5.3+
  - python3-tk
  - python-gnupg
  - Your VEC's PGP key.

### VEC Chairman 

## Installation / Execution
### Linux
  - Clone from github: `git clone
    https://github.com/dpurgert/pyebfgen.git`
  - Install python-gnupg: `pip3 install python-gnupg`
  - (Optional) add execute permissions: `chmod u+x ebfgen.py`
  - Run with `python3 ebfgen.py`; or if you added execute permissions, 
    `./ebfgen.py` (also see "Initial Execution" below)

### Windows
  - Install Python3 (as of writing, 3.8.5 is current)
    - Python can be downloaded by going to https://www.python.org/downloads/
  - Install python-gnupg: `pip install python-gnupg`
  - Download Zip archive of this repository
  - Unzip to your prefered location (e.g. Desktop)
  - Double-click "ebfgen.py" (also see "Initial Execution" below)

### First Run
The following preliminary actions need to be taken in order to use
pyEBFGen.  If they are not taken, the program will simply present an
error message and exit.

1. Obtain your VEC's (public) encryption key from your VEC Chairman
  1. Load key into the program's keystore with the import.py script.
      Usage: `./importkey.py keyfile.asc`
  2. Edit the key's trust: `gpg --homedir=./gpg --edit-key <KEY_ID>`
    - The key's information will be printed out, and the final line of
      the output will be the prompt `gpg>`.  At this prompt, type the
      command "trust", and hit <enter>.
    - You will then be asked how well you trust the key, from 1 (you do
      not trust it) to 5 (you trust it ultimately).  Choose "5", and
      press <enter>
    - You will be asked if you're sure.  Answer "Y", and press <enter>
    - You will be returned to the `gpg>` prompt at this point.  Type in
      "save", and GPG will finish, returning you to your normal system 
      prompt.
2. Set the default VEC settings in the `vec.cfg` configuration file.
  * __Mandatory:__ Set VEC encryption key in this file.  Default value 
    is BLANK, and program will generate errors if you attempt to run
    without the key defined. Example `key="VEC Key <vec@radio.group>"`.
    Key fingerprints (e.g. `key=7F08D422`) are also acceptable.
3. Create a test batch file to ensure all is working.

## IRC Support

If you have questions about the application, you can find us on the OFTC
IRC Network in the #efbgen channel.  IRC address is irc.oftc.net ... you
can connect via Port 6667 for non-secure, or use Port 6697 for SSL.

## changelog
v 2.0.0 - GPG Encryption
  - Batchfile output is now encrypted with GPG.

v 1.0.7 - Pending Filenumber
  - FCC updated requirement, force this to blank now.

v 1.0.6 - Minor pretty-factor updates
  - tabstops and other minor UX updates.

v 1.0.5 - Fix US Minor Outlying Islands
  - Region ID for US Minor Outlying Islands was incorrectly set.

v 1.0.4 - Update Region ID
  - Region ID automatically updates when VE State is changed.

v 1.0.3 - Update Applicant Data
  - Can now update applicant entries in the program, rather than needing
    to edit the batch file after saving.

v 1.0.2 - Blank State option
  - Allow the VEC state to be set to a blank (note, blank Applicant
    state will fail).

v 1.0.1 - Operator
  - Add check for operator class filled in

v 1.0.0 - Stable
  - Final polish, out of beta.

v 0.2.14 - Expanded Preview
  - Added EBF File Preview

v 0.2.13 - Response Preview
  - Added response file conversion "preview" window.  

v 0.2.12 - Button modifications
  - Changed the name to a couple of buttons for simplification purposes.

v 0.2.11 - Variable
  - there's a huge difference between "global var" and "var".

v 0.2.10 - Restore Operator class
  - Op class inadvertently removed in 0.2.9.  Restored.

v 0.2.9 - Multiple Window Woes
  - Gave up on multiple subwindows, and now it's all separate frames on
    the same single-pane window.  

v 0.2.8 - I'm a teapot
  - Forgot to reset defaults to something sane.  As WL1B from the
    Anchorage VEC asked for this, used Anchorage, AK.

v 0.2.7 - Config updates
  - fixed behavior with the config file.

v 0.2.6 - config file updated
  - renamed config file to 'vec.cfg' to make running from terminal less
    of a hassle
  - fixed the VA window class to be less of a pain code-wise.

v 0.2.5 - config file
  - configuration file ("ebf.cfg") added to allow "one time" setting of
    VEC code / city / state / regional ID information.
v 0.2.4 - Window order
  - Turns out window order / layering behavior is OS dependent.
    Scrapping 0.2.2 and 0.2.3 changes in that regard.
  - Added a "preview window" instead of the big pane, it just looks
    nicer.

v 0.2.3 - More VA Window patches
  - -.2 didn't fix it in windows.  Removing the preview pane to see if
    that helps.

v 0.2.2 - Fix Windows
  - VA window now appears to work as expected

v 0.2.1 - Begin Reorg
  - Start reorganizing the codebase to be less bad.

v 0.2.0 - Add Doxygen
  - add doxygen for internal documentation.

v 0.1.1 - Fix VEC labels
  - Label for "Regional Identifier" was missing the colon, and all
    labels now have a space between the 'title' and the value.

v 0.1.0 - Stable Beta
  - Should be stable now.  Future patches, etc. based on user experience
    requests

v. 0.0.16 - version string
  - broke the version string up into individual vars.

v 0.0.15 - UI Fixes
  - Force callsign to uppercase
  - Zero-pad the FRN (if provided) to 10 digits
  - Remove formatting (parenthesis, dashes, etc.) from SSN, Phone
    Number, etc.
  - Limit name fields to lengths imposed by FCC
  - Limit mailing address fields to lengths imposed by FCC
  - Updated user guide for readability & noted changes.

v 0.0.14 - Added missing applicant field
  - Added the name suffix field back into the application.
  - Tested...present and works.
  - Moved the callsign entry box to right side of same row.

v 0.0.13 - Updated applicant interface
  - Updated interface to follow the 605 form.

v 0.0.12 - Update regional ID
  - Allow lowercase region IDs

v 0.0.11 - Fix VEC & Session Numbers GUI
  - Fixed the interface to make it easier for the user to separate
    session date/location from actual numbers.
  - Moved the Regional Identifier to a location separating it from
    the remaining slots for organizational purposes.

v 0.0.10 - Fix CRLF
  - CRLF got eaten somewhere.  Replacing it

v 0.0.9 - Default Filename
  - Added region code to VEC form
  - Added default filename as (VEC + mmdd + Region Code + counter).dat
  - Applicant data is cleared on save
  - file counter incremented on save.  Can be set in VEC info form if
    necessary. Zero padding the number is automatic, if required
  - "working" output frame seems to have visual artifacts after reset.
    This is just a visual bug in the program, and does not affect
    output files.

v 0.0.8 - Force VEC Code case
  - VEC Code will always be stored capitalized.

v 0.0.7 - Embed GNU Public Liense
  - Embedded the GNU General Public License statement within source code.

v 0.0.6 - Updated response processing
  - Stick edited response file data into "applicant info" pane after
    importing.
  - Added button to clear frame on click.
  - NB: Frame data has no bearing on output file order.  VE Header is
    ALWAYS first, and ALWAYS followed in [0 .. n] order for VA records.

v 0.0.5 - Input verification
  - verify input for SSN/FRN fields
  - verify input for Basic Qualification Question

v 0.0.4 - Response Processing
  - File menu cleanup
  - Response file conversion to comma-separated

v 0.0.3 - Rename
  - rename ulsbatch.py to ebfgen.py

v 0.0.2 - Cosmetic modifications
  - Changed menu names to adequately reflect information collected from
    the 605 form.
  - Made the menu entries more compact for the Individual Amateur radio
    license data entry window for smaller screens.

v 0.0.1 - Initial alpha
  - VEC / Test data set via File -> VE
  - Add applicant data via File -> VA
    - "Standard" Applicant form assumes / hardcodes certain values
    - "Extended" applicant data also available, corresponds directly to
      FCC document.
