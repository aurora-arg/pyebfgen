#!/usr/bin/python3
import gnupg
import sys
from pprint import pprint

gpg = gnupg.GPG(gnupghome="./gpg")
key_data = open(sys.argv[1]).read()
import_result=gpg.import_keys(key_data)
pprint(import_result.results)
