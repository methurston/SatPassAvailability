#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
import dateutil
import pytz

# TODO: Move timezone to UserManager.py


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


class TimeSlot(object):
    def __init__(self, callsign, days, start_time, duration, timezone):
        self.callsign = callsign
        self.days = days
        self.start_time = start_time
        self.duration = duration
        self.timezone = timezone

    def store_timeslot(self):
        query = 'INSERT INTO timeslot (callsign, days, startime, duration, timezone) ' \
                'VALUES (\'{}\', \'{}\', \'{}\', {}, \'{}\')'.format(self.callsign,
                                                                     self.days,
                                                                     self.start_time,
                                                                     self.duration,
                                                                     self.timezone.zone)
        print(query)

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
    example = TimeSlot('W1AW',
                       'M,Tu,Th,Sa',
                       '18:00',
                       '1.5',
                       pytz.timezone('US/Eastern'))
    example.store_timeslot()
    example.gen_start_times()
