#!/usr/bin/env python
from __future__ import print_function
import requests
from datetime import datetime
import dateutil.parser
from model import *
from peewee import *


# Globals
try:
    with open('../config/config.json') as configuration_file:
        config = json.load(configuration_file)
except IOError:
    print('Config File not found, run configbuilder.py from the parent directory')
    sys.exit()
except ValueError as e:
    print('Invalid JSON: Error was: {}'.format(e))
    sys.exit()

# Read in config values
file_age_threshold = config['age_thresholds']['tle_file']
tle_source = config['satsource']['amsat']


class Tle(object):
    """Base Tle Class,
       This a simple class to store Two Line Elements for satellite info"""
    def __init__(self, name, lineone, linetwo):
        self.name = name
        self.lineone = lineone
        self.linetwo = linetwo
        self.age = datetime.now()

    def store(self, first_load):
        new_sat = Satellite(name=self.name,
                            lineone=self.lineone,
                            linetwo=self.linetwo,
                            updateDTS=self.age)
        new_sat.save(force_insert=first_load)
        print('Saving: {}'.format(new_sat.name))


def get_tle_file_age():
    """get_tle_file_age:  Finds the age of the newest TLE record in the DB.
       Return: tuple (age, no_sats)
       if no satellites are loaded, no_sats is True"""
    max_age = Satellite.select(fn.Max(Satellite.updateDTS)).scalar()
    if max_age is None:
        tle_age = file_age_threshold + 1
        no_sats = True
    else:
        time_tle_age = dateutil.parser.parse(max_age)
        tle_age = (datetime.now() - time_tle_age).days
        no_sats = False
    return tle_age, no_sats


def fetch_tle_file(satellite_type):
    tle_config = config['satsource']['amsat']
    finalurl = 'http://{}/{}/{}'.format(tle_config['host'], tle_config['path'], tle_config['filename'][satellite_type])
    try:
        all_tle = requests.get(finalurl).content
        # print('All: {}'.format(all_tle))
    except Exception as err:
        print('Error Retreiving {},\n error is {}'.format(finalurl, err))
        sys.exit()
    return all_tle


def parse_tle_file(tle_file):
    """Takes the raw data from celestrak or amsat and parses the data into an object representing the
       two line format"""
    tle_objects = []
    tle_list = tle_file.splitlines()
    remain = len(tle_list)
    current_line = 0
    while current_line < remain:
        single_tle = []
        innercount = 0
        while innercount <= 2:
            single_tle.append(tle_list[current_line + innercount].strip())
            innercount += 1
        tle_objects.append(Tle(single_tle[0].strip(), single_tle[1], single_tle[2]))
        current_line += 3
    return tle_objects


if __name__ == '__main__':
    file_age = get_tle_file_age()
    print('Age of newest record: {}'.format(file_age))
    if file_age[0] >= file_age_threshold:
        print('Satellite records are out of date, updating.')
        raw_tle = fetch_tle_file('ham')
        parsed_tle = parse_tle_file(raw_tle)
        for tle in parsed_tle:
            tle.store(file_age[1])

