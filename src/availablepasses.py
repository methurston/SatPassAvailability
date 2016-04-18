#!/usr/bin/env python
from __future__ import print_function
import arrow
from dateutil import tz
import datetime
import TimeSlotHandler
import SatTrack
import json
import sys

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


def date_to_string(dateobject):
    """Helper function to convert the various DateTime back to strings for jsonification"""
    if isinstance(dateobject, arrow.arrow.Arrow):
        stringdate = dateobject.isoformat()
        return stringdate
    elif isinstance(dateobject, datetime.datetime):
        stringdate = dateobject.isoformat()
    return stringdate
    raise TypeError ('Type not serilizeable')


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
        print('\tMax elevation: {} - Elevation: {}: '.format(self.max_elev_time, self.max_elevation))
        print('\tSet: {} - Azimuth of {}'.format(self.set_time, self.set_azimuth))

    def jsonify(self):
        """Return object as JSON string.  This is typeconversion hell."""
        todict = vars(self)
        return json.dumps(todict, indent=1, default=date_to_string)


if __name__ == '__main__':
    """sample code to show how functions work Compare to http://www.amsat.org/amsat-new/tools/predict/index.php"""
    sat_names = ['SO-50', 'LilacSat-2', 'AO-85']
    test_call = config['default_location']['callsign']
    loc = SatTrack.fetch_location(test_call)
    user_timeslots = TimeSlotHandler.LocationTimeSlots(test_call)
    user_timeslots.fetch_timeslots()
    user_timeslots.gen_start_times()
    available_passes = []

    for startDTS in user_timeslots.start_datetimes:
        for sat_name in sat_names:
            sat = SatTrack.fetch_sat_tle(sat_name)
            sat.compute(loc)
            original_timezone = startDTS.datetime.tzinfo
            utc_start_time = startDTS.astimezone(tz=tz.gettz('utc'))
            loc.date = utc_start_time
            satpass = loc.next_pass(sat)
            time_diff = abs(satpass[0].datetime() - loc.date.datetime())
            if time_diff.seconds <= 3600:
                print('Timeslot: {}'.format(startDTS))
                validpass = AvailablePass(sat_name, satpass)
                validpass.convert_pass_tz(original_timezone)
                available_passes.append(validpass)
                jsonpass = validpass.jsonify()
                print(jsonpass)
                #validpass.format_output()
