#!/usr/bin/env python
from __future__ import print_function
import arrow
import sys
sys.path.append('../src')
from dateutil import tz
import TimeSlotHandler
import SatTrack

# """sample code to show how functions work
#    Compare to http://www.amsat.org/amsat-new/tools/predict/index.php"""
sat_name = 'SO-50'
sat = SatTrack.fetch_sat_tle(sat_name)
loc = SatTrack.fetch_location('N7DFL')
sat.compute(loc)

satpass = loc.next_pass(sat)

user_timeslots = TimeSlotHandler.LocationTimeSlots('N7DFL')
user_timeslots.fetch_timeslots()
user_timeslots.gen_start_times()

for startDTS in user_timeslots.start_datetimes:
    original_timezone = startDTS.datetime.tzinfo
    utc_start_time = startDTS.astimezone(tz = tz.gettz('utc'))
    loc.date = utc_start_time #.datetime
    satpass = loc.next_pass(sat)
    time_diff = abs(satpass[0].datetime() - loc.date.datetime())
    if time_diff.seconds <= 3600:
        print('Timeslot: {}'.format(startDTS))
        validpass = arrow.get(satpass[0].datetime())
        print('{} has a pass starting at: {}'.format(sat_name, validpass.astimezone(tz=original_timezone)))