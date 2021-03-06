#!/usr/bin/env python
from __future__ import print_function
import arrow
from dateutil import tz
import datetime
import TimeSlotHandler
import SatTrack
import json
import sys
import falcon
import hooks


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


def angle_to_int(inputAngle):
    """Converts pyephem.Angle to an int for json output formatting"""
    angle_array = str(inputAngle).split(':')
    return int(angle_array[0])


def date_to_string(dateobject):
    """Helper function to convert the various DateTime back to strings for jsonification"""
    if isinstance(dateobject, arrow.arrow.Arrow):
        stringdate = dateobject.isoformat()
    elif isinstance(dateobject, datetime.datetime):
        stringdate = dateobject.isoformat()
    return stringdate


class AvailablePass(object):
    def __init__(self, name, ephem_pass):
        self.name = name
        self.rise_time = arrow.get(ephem_pass[0].datetime())
        self.rise_azimuth = ephem_pass[1]
        self.max_elev_time = arrow.get(ephem_pass[2].datetime())
        self.max_elevation = ephem_pass[3]
        self.set_time = arrow.get(ephem_pass[4].datetime())
        self.set_azimuth = ephem_pass[5]
        self.max_elev_az = None

    def convert_pass_tz(self, loc_timezone):
        self.rise_time = self.rise_time.astimezone(tz=loc_timezone)
        self.max_elev_time = self.max_elev_time.astimezone(tz=loc_timezone)
        self.set_time = self.set_time.astimezone(tz=loc_timezone)

    def format_output(self):
        formatted_dict = {"sat_name": self.name,
                          "aos": {
                              "time": self.rise_time.isoformat(),
                              "azimuth": angle_to_int(self.rise_azimuth)
                          },
                          "max_elevation": {
                              "time": self.max_elev_time.isoformat(),
                              "azimuth": angle_to_int(self.max_elev_az),
                              "elevation": angle_to_int(self.max_elevation)
                          },
                          "los": {
                              "time": self.set_time.isoformat(),
                              "azimuth": angle_to_int(self.set_azimuth)
                          }
                          }
        return formatted_dict


@falcon.before(hooks.get_sat_names)
class AvailablePassAPI(object):
    def on_get(self, req, resp, callsign):
        loc = SatTrack.fetch_location(callsign)
        loc_timeslots = TimeSlotHandler.LocationTimeSlots(callsign)
        loc_timeslots.fetch_timeslots()
        loc_timeslots.gen_start_times()
        available_passes = []
        try:
            min_elevation = int(req.params['min_elevation'])
        except KeyError as k:
            min_elevation = 0

        for pass_time in loc_timeslots.start_datetimes:
            for sat_name in req.params['sat_list']:
                sat = SatTrack.fetch_sat_tle(sat_name)
                sat.compute(loc)
                original_timezone = pass_time[1].datetime.tzinfo
                utc_start_time = pass_time[1].astimezone(tz=tz.gettz('UTC'))
                loc.date = utc_start_time
                satpass = loc.next_pass(sat)
                time_diff = abs(satpass[0].datetime() - loc.date.datetime())
                if time_diff.seconds <= pass_time[2]:
                    validpass = AvailablePass(sat_name, satpass)
                    validpass.convert_pass_tz(original_timezone)
                    loc.date = validpass.max_elev_time.astimezone(tz=tz.gettz('UTC'))
                    sat.compute(loc)
                    validpass.max_elev_az = sat.az
                    # This works, but seems inelegant
                    if angle_to_int(validpass.max_elevation) >= min_elevation:
                        available_passes.append(validpass.format_output())
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(sorted(available_passes, key=lambda t: t['aos']['time']))


if __name__ == '__main__':
    """sample code to show how functions work
       Compare to http://www.amsat.org/amsat-new/tools/predict/index.php
       or heavens-above.com
       or n2yo.com"""
    sat_names = ['SO-50']
    test_call = config['default_location']['callsign']
    loc = SatTrack.fetch_location(test_call)
    user_timeslots = TimeSlotHandler.LocationTimeSlots(test_call)
    user_timeslots.fetch_timeslots()
    user_timeslots.gen_start_times()
    available_passes = []

    for pass_time in user_timeslots.start_datetimes:
        # pass_time is a tuple of (starting time (user timezone), duration (seconds)
        for sat_name in sat_names:
            sat = SatTrack.fetch_sat_tle(sat_name)
            sat.compute(loc)
            original_timezone = pass_time[1].datetime.tzinfo
            utc_start_time = pass_time[1].astimezone(tz=tz.gettz('UTC'))
            loc.date = utc_start_time
            satpass = loc.next_pass(sat)
            time_diff = abs(satpass[0].datetime() - loc.date.datetime())
            if time_diff.seconds <= pass_time[2]:  # TODO - Change to duration. Just figure out scope
                print('Available starting time: {}'.format(pass_time[1]))
                validpass = AvailablePass(sat_name, satpass)
                validpass.convert_pass_tz(original_timezone)
                available_passes.append(validpass)
                loc.date = validpass.max_elev_time.astimezone(tz=tz.gettz('UTC'))
                sat.compute(loc)
                validpass.max_elev_az = sat.az
                test = validpass.format_output()
                print(test)
