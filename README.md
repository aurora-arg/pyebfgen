# ebfgen
Python batch file generator for use with the FCC EBF system.

FCC Documentation can be found at:
https://www.fcc.gov/wireless/systems-utilities/uls-electronic-batch-filing

This should work cross-platform; however my main development environment
is Linux.  If you try on Mac / Windows and find platform-specific bugs,
please let me know.

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
  - Download Zip archive of this repository
  - Unzip to your prefered location (e.g. Desktop)
  - Double-click "ebfgen.py"

## changelog
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
