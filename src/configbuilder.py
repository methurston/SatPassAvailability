#!/usr/bin/env python
from __future__ import print_function
import json
import os
import fnmatch
import pytz
import sys


def find_db():
    """Search the directory tree and return and files named *.db"""
    matches = []
    pattern = '*.db'

    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                matches.append(os.path.join(root, name))
    return matches


def get_callinfo():
    callsign = raw_input('Enter Callsign: ')
    userzone = raw_input('Enter Timezone: ')
    try:
         pytz.timezone(userzone)
    except pytz.UnknownTimeZoneError as err:
        print('Invalid Timezone entered.')
        userzone = raw_input('Enter Timezone: ')
    return {'callsign': callsign,
            'timezone': userzone
            }



test = find_db()
blah = get_callinfo()
for i in test:
    print(i)

print(blah)
