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
  - Clone from github: `git clone git@github.com:dpurgert/pyebfgen`
  - (Optional) add execute permissions: `chmod u+x ebfgen.py`
  - Run with `python3 ebfgen.py`; or if you added execute permissions, 
    `./ebfgen.py` 

### Windows
  - Install Python3 (as of writing, 3.8.5 is current)
  - Download Zip archive of this repository
  - Unzip to your prefered location (e.g. Desktop)
  - Double-click "ebfgen.py"

## changelog
v 0.0.5 - Input verification
  - verify input for SSN/FRN fields
  - verify input for Basic Question

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
