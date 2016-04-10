#!/usr/bin/env python
from __future__ import print_function
import arrow
import sqlite3
import json

# globals
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


# daymap maps common day names and abbreviations to isoweekday() values i.e Monday = 1, Tuesday = 2 ...
daymap = {'m': 1,
          'mon': 1,
          "monday": 1,
          't': 2,
          'tu': 2,
          'tue': 2,
          'tues': 2,
          'tuesday': 2,
          'w': 3,
          'wed': 3,
          'wednesday': 3,
          'th': 4,
          'thur': 4,
          'thurs': 4,
          'thursday': 4,
          'f': 5,
          'fri': 5,
          'friday': 5,
          'sa': 6,
          'sat': 6,
          'saturday': 6,
          'su': 7,
          'sun': 7,
          'sunday': 7}


class TimeSlot(object):
    def __init__(self, callsign, days, start_time, duration):
        self.callsign = callsign
        self.days = days
        self.start_time = start_time
        self.duration = duration

    def store_timeslot(self):
        """Writes the timeslot record to the database.
           Called by check existing, probably better not to call this directly"""
        query = 'INSERT INTO timeslots (callsign, weekdays, start_time, duration) ' \
                'VALUES (?, ?, ?, ?)'
        params = (self.callsign,
                  self.days,
                  self.start_time,
                  self.duration)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_timeslots(self):
        """fetches existing timeslots"""
        query = 'SELECT callsign, weekdays, start_time, duration ' \
                'FROM timeslots WHERE callsign = ?'
        param = (self.callsign,)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        results = cursor.execute(query, param)
        existing = results.fetchall()
        for row in existing:
            print(row)
        return existing
        conn.close()

    def check_exists(self):
        """Queries to see if row exists"""
        query = 'SELECT callsign, weekdays, start_time, duration ' \
                'FROM timeslots ' \
                'WHERE callsign = ? ' \
                'AND weekdays = ? ' \
                'AND start_time = ? ' \
                'AND duration = ?'
        params = (self.callsign,
                  self.days,
                  self.start_time,
                  self.duration)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        results = cursor.execute(query, params)
        existing = results.fetchall()
        if len(existing) == 0:
            self.store_timeslot()
            print('Record Stored')
        else:
            print('Record Already Exists')
        conn.close()


    def calc_end_time(self):
        """Take the start time + duration to calculate end time
           Not sure if this will be used"""
        pass

    def gen_start_times(self):
        """take the starting time, combine with days, return an array of date time stamps"""
        int_days = []
        for day in self.days.split(','):
            int_days.append(daymap[day.lower().strip('.')])
        print(int_days)


if __name__ == '__main__':
    example = TimeSlot('N7DFL',
                       'M,T,W,Th,F',
                       '12:00',
                       '3600')
    example.fetch_timeslots()
    example.check_exists()
    example.gen_start_times()
