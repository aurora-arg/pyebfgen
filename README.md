# pyulsbatch
Python ULS batchfile generator.

FCC Documentation can be found at:
https://www.fcc.gov/wireless/systems-utilities/uls-electronic-batch-filing

This should work cross-platform, although at the moment I only have
Linux machines available.  If you try on Mac / Windows and find bugs,
please let me know.

## Requirements
  - Python 3.5.3 (later versions may work)
  - python3-tk

## Installation / Execution
  - Clone from github: `git clone git@github.com:dpurgert/pyulsbatch`
  - (Optional) add execute permissions: `chmod u+x ebfgen.py`
  - Run with `python3 ebfgen.py`; or if you added execute permissions, 
    `./ebfgen.py` 

## changelog
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
      
