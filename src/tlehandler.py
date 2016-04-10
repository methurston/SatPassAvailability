#!/usr/bin/env python
from __future__ import print_function
import requests
from datetime import datetime
import sqlite3
import dateutil.parser
import sys
import json

# Globals
try:
    with open('../config/config.json') as configuration_file:
        config = json.load(configuration_file)
except IOError:
    print('Config File not found')
    sys.exit()
except ValueError as e:
    print('Invalid JSON: Error was: {}'.format(e))
    sys.exit()

db_name = config['datasource']['filename']
file_age_threshold = config['age_thresholds']['tle_file']


class Tle(object):
    """Base Tle Class,
       This a simple class to store Two Line Elements for satellite info"""
    def __init__(self, name, lineone, linetwo):
        self.name = name
        self.lineone = lineone
        self.linetwo = linetwo
        self.age = datetime.now()

    def store(self):
        """write values to DB"""
        query = 'INSERT OR REPLACE INTO satellites (name, lineone, linetwo, updateDTS)' \
                'VALUES(\'{}\', \'{}\', \'{}\', \'{}\');'.format(self.name,
                                                                 self.lineone,
                                                                 self.linetwo,
                                                                 self.age.isoformat())
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

    def update_or_store(self):
        """Check the age of the existing record, if it's over 2 days, pull
           New values"""
        age_query = 'SELECT updateDTS FROM satellites where name = \'{}\''.format(self.name)
        cursor = conn.cursor()
        c = cursor.execute(age_query)
        all_match = c.fetchall()

        if len(all_match) == 0:
            self.store()
            print('{} Record Added'.format(self.name))
        elif len(all_match) > 1:
            print('Multiple rows returned, expected 1. Satellite name was {}'.format(self.name))
        else:
            self.store()
            print('{} Record Updated'.format(self.name))


def get_tle_file_age():
    age_query = 'select max(updateDTS) FROM satellites;'
    cursor = conn.cursor()
    result = cursor.execute(age_query).fetchall()

    if result[0][0] is None:
        tle_age = file_age_threshold + 1
    else:
        string_tle_age = result[0][0]
        time_tle_age = dateutil.parser.parse(string_tle_age)
        tle_age = (datetime.now() - time_tle_age).seconds/1200  # Right now this uses 3 hours. Could change to days.
    return tle_age


def fetch_tle_file(host, satellite_type):
    if host == 'celestrak':
        tle_config = config['satsource']['celestrak']
        finalurl = 'http://{}/NORAD/elements/{}'.format(tle_config['host'], tle_config['filenames'][satellite_type])
    elif host == 'amsat':
        tle_config = config['satsource']['amsat']
        print(tle_config)
        finalurl = 'http://{}/{}/{}'.format(tle_config['host'], tle_config['path'], tle_config['filename'])
        print(finalurl)
    else:
        print('Unknown host. String provided was: {}'.format(host))
        sys.exit()
    try:
        all_tle = requests.get(finalurl).content
        # print('All: {}'.format(all_tle))
    except Exception as e:
        print('Error Retreiving {},\n error is {}'.format(finalurl, e))
        sys.exit()
    return all_tle


def parse_tle_file(tle_file):
    """Takes the raw data from celestrak and parses the data into an object representing the
    two line format"""
    tle_objects = []
    tle_list = tle_file.splitlines()
    remain = len(tle_list)
    current_line = 0
    while current_line < remain:
        single_tle = []
        innercount = 0
        while innercount <= 2:
            single_tle.append(tle_list[current_line + innercount])
            innercount += 1
        tle_objects.append(Tle(single_tle[0].strip(), single_tle[1], single_tle[2]))
        current_line += 3
    return tle_objects


if __name__ == '__main__':
    conn = sqlite3.connect(db_name)
    file_age = get_tle_file_age()
    print('Age of newest record: {}'.format(file_age))
    if file_age >= file_age_threshold:
        print('Satellite records are out of date, updating')
        raw_tle = fetch_tle_file('celestrak', 'ham')
        parsed_tle = parse_tle_file(raw_tle)
        for tle in parsed_tle:
            tle.update_or_store()
    else:
        print('Satellite records are up to date.')
    conn.close()
