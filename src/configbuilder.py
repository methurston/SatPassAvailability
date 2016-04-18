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


def get_db_name():
    """Generates the datasource section of the config file.
    sqlite3 is the only type supported"""
    available_dbs = find_db()
    total_dbs = len(available_dbs)
    if total_dbs == 0:
        db_name = raw_input('Enter name for database: ')
    else:
        print('Multiple Databases found')
        for idx, db_name in enumerate(available_dbs):
            print('{} - {}'.format(idx, db_name))

        try:
            db_index = int(raw_input('Which database do you want to use? '))
            try:
                db_name = available_dbs[db_index]
            except IndexError:
                print('That is not a valid DB')
                get_db_name()
        except ValueError:
            print('Invalid entry, enter an integer.')
            get_db_name()
    return {'type': 'sqlite3',
            'filename': db_name,
            'Username': None,
            'Password': None}


def get_callinfo():
    callsign = raw_input('Enter Callsign: ')
    userzone = raw_input('Enter Timezone: ')
    try:
         pytz.timezone(userzone)
    except pytz.UnknownTimeZoneError as err:
        print('Invalid Timezone entered.')
        userzone = raw_input('Enter Timezone: ')
    return {'callsign': callsign.upper(),
            'timezone': userzone
            }


datasource= get_db_name()
default_location= get_callinfo()
usersource = {
    "host": "https://callook.info",
    "username": None
}
satsource = {
    "amsat": {
        "host": "www.amsat.org",
        "path": "/amsat/ftp/keps/current/",
        "filename": "nasabare.txt"
    },
    "celestrak": {
        "host": "www.celestrak.com",
        "path": None,
        "filenames": {
            "ham": "amateur.txt",
            "amateur": "amateur.txt",
            "weather": "weather.txt",
            "wx": "weather.txt",
            "noaa": "noaa.txt"}
    }
}

def get_age_threshold():
    pass

blah = {}
blah['datasource'] = datasource
blah['satsource'] = satsource
blah['default_location'] = default_location
blah['usersource'] = usersource



print(json.dumps(blah, indent=2))

