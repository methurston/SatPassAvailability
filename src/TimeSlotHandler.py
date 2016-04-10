#!/usr/bin/env python
from __future__ import print_function
import arrow
import sqlite3




# globals
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
db_name = 'sats.db'


class TimeSlot(object):
    def __init__(self, callsign, days, start_time, duration):
        self.callsign = callsign
        self.days = days
        self.start_time = start_time
        self.duration = duration

    def store_timeslot(self):
        query = 'INSERT INTO timeslots (callsign, weekdays, start_time, duration) ' \
                'VALUES (\'{}\', \'{}\', \'{}\', {})'.format(self.callsign,
                                                                     self.days,
                                                                     self.start_time,
                                                                     self.duration)
        print(query)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()


    def calc_end_time(self):
        """Take the start time + duration to calculate end time"""
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
    example.store_timeslot()
    example.gen_start_times()
