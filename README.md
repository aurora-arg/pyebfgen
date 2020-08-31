# ebfgen
Python batch file generator for use with the FCC EBF system.

FCC Documentation can be found at:
https://www.fcc.gov/wireless/systems-utilities/uls-electronic-batch-filing

This should work cross-platform; however my main development environment
is Linux.  If you try on Mac / Windows and find platform-specific bugs,
please let me know.

### Temp hiatus 

Taking the Extra exam on 2020-09-03.  Dev work on hiatus until
2020-09-04.

## Requirements
  - Python 3.5.3+
  - python3-tk

## Installation / Execution
### Linux
  - Clone from github: `git clone
    https://github.com/dpurgert/pyebfgen.git`
  - (Optional) add execute permissions: `chmod u+x ebfgen.py`
  - Run with `python3 ebfgen.py`; or if you added execute permissions, 
    `./ebfgen.py` 

### Windows
  - Install Python3 (as of writing, 3.8.5 is current)
    - Python can be downloaded by going to https://www.python.org/downloads/
  - Download Zip archive of this repository
  - Unzip to your prefered location (e.g. Desktop)
  - Double-click "ebfgen.py"

### IRC Support

If you have questions about the application, you can find us on the OFTC
IRC Network in the #efbgen channel.  IRC address is irc.oftc.net ... you
can connect via Port 6667 for non-secure, or use Port 6697 for SSL.

## changelog
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
