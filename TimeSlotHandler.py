#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
import dateutil
import pytz

# TODO: Move timezone to UserManager.py

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

if __name__ == '__main__':
    example = TimeSlot('W1AW',
                       'M,Tu,Th,Sa',
                       '18:00',
                       '1.5',
                       pytz.timezone('US/Eastern'))
    example.store_timeslot()
