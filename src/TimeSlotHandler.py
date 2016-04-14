#!/usr/bin/env python
from __future__ import print_function
import arrow
from datetime import datetime, timedelta
from dateutil import tz
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
iso_day_name = {1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday',
                6: 'Saturday',
                7: 'Sunday'}

# def get_user_timezone(call):
#     query = 'SELECT timezone from locations WHERE callsign = ?'
#     params = (call, )
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     result = cursor.execute(query, params)
#     user_timezone =


class TimeSlot(object):
    """ This class generates and stores time slots for a specific location"""
    def __init__(self, callsign, days, start_time, duration):
        self.callsign = callsign
        self.days = days
        self.start_time = start_time
        self.duration = duration

    def store_timeslot(self):
        """Writes the timeslot record to the database.
           Called by check existing, If this function is called directly, the row will be duplicated."""
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

    def check_exists(self):
        """Queries to see if row exists, if not write it to DB."""
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

class LocationTimeSlots(object):
    """Time slots associated with a specific location."""
    def __init__(self, callsign):
        self.callsign = callsign

    def fetch_timeslots(self):
        """fetches existing timeslots"""
        query = 'SELECT ts.callsign, ts.weekdays, ts.start_time, ts.duration, l.timezone ' \
                'FROM timeslots ts JOIN locations l ' \
                'ON ts.callsign = l.callsign ' \
                'WHERE l.callsign = ?'
        param = (self.callsign,)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        results = cursor.execute(query, param)
        existing = results.fetchall()
        self.all_timeslots = existing
        conn.close()


    def gen_start_times(self):
        """take the starting time, combine with days, return an array of date time stamps"""
        final_start_dates = set() # This allows us to toss out duplicates.
        today_int = arrow.now().isoweekday()
        today_date = arrow.now().date()
        # print('Today is: {} - Int: {}'.format(today_date, today_int))
        for row in self.all_timeslots:
            for day in row[1].split(','):
                int_day = daymap[day.lower().strip('.')]
                daydiff = int_day - today_int  # TODO: Fix this calc so it wraps over a week.  Research needed
                if daydiff <= 0:
                    daydiff += 7
                str_date = '{}T{}'.format(str(today_date + timedelta(days=(daydiff))),row[2])
                final_start_dates.add(arrow.get(str_date).replace(tzinfo=tz.gettz(row[4])))
        self.start_datetimes = sorted(final_start_dates)

    def print_final_times(self):
        for final_date in self.start_datetimes:
            print('{} type {}'.format(final_date, type(final_date)))

    def calc_end_time(self):
        """Take the start time + duration to calculate end time
           Not sure if this will be used"""
        pass

if __name__ == '__main__':
    example_slot = TimeSlot('N7DFL',
                            'T,Th',
                            '03:00',
                            '3600')
    location_slots = LocationTimeSlots(example_slot.callsign)
    example_slot.check_exists()
    location_slots.fetch_timeslots()
    location_slots.gen_start_times()
    location_slots.print_final_times()
