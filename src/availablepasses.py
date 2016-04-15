#!/usr/bin/env python
from __future__ import print_function
import arrow
from dateutil import tz
import TimeSlotHandler
import SatTrack

# """sample code to show how functions work
#    Compare to http://www.amsat.org/amsat-new/tools/predict/index.php"""
sat_names = ['SO-50', 'AO-85']

loc = SatTrack.fetch_location('N7DFL')

user_timeslots = TimeSlotHandler.LocationTimeSlots('N7DFL')
user_timeslots.fetch_timeslots()
user_timeslots.gen_start_times()
available_passes = []


class AvailablePass(object):
    def __init__(self, name, ephem_pass):
        self.name = name
        self.rise_time = arrow.get(ephem_pass[0].datetime())
        self.rise_azimuth = ephem_pass[1]
        self.max_elev_time = arrow.get(ephem_pass[2].datetime())
        self.max_elevation = ephem_pass[3]
        self.set_time = arrow.get(ephem_pass[4].datetime())
        self.set_azimuth = ephem_pass[5]

    def convert_pass_tz(self, loc_timezone):
        self.rise_time = self.rise_time.astimezone(tz=loc_timezone)
        self.max_elev_time = self.max_elev_time.astimezone(tz=loc_timezone)
        self.set_time = self.set_time.astimezone(tz=loc_timezone)

    def format_output(self):
        print(self.name)
        print('\tRise: {} - Azimuth: {}'.format(self.rise_time, self.rise_azimuth))
        print('\tMax elevation: {} - Azimuth: {}: '.format(self.max_elev_time, self.max_elevation))
        print('\tSet: {} - Azimuth of {}'.format(self.set_time, self.set_azimuth))

for startDTS in user_timeslots.start_datetimes:
    for sat_name in sat_names:
        sat = SatTrack.fetch_sat_tle(sat_name)
        sat.compute(loc)
        original_timezone = startDTS.datetime.tzinfo
        utc_start_time = startDTS.astimezone(tz = tz.gettz('utc'))
        loc.date = utc_start_time #.datetime
        satpass = loc.next_pass(sat)
        time_diff = abs(satpass[0].datetime() - loc.date.datetime())
        if time_diff.seconds <= 3600:
            print('Timeslot: {}'.format(startDTS))
            validpass = AvailablePass(sat_name, satpass)
            validpass.convert_pass_tz(original_timezone)
            available_passes.append(validpass)
            validpass.format_output()

