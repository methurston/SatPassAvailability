#!/usr/bin/env python
from __future__ import print_function
import arrow
from datetime import timedelta
from dateutil import tz
from model import *
import falcon
import hooks

# globals
try:
    with open('../config/config.json') as configuration_file:
        config = json.load(configuration_file)
except IOError:
    print('Config File not found, run configbuilder.py from the parent directory')
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
          's': 6,
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





class TimeSlotObj(object):
    """ This class generates and stores time slots for a specific location"""
    def __init__(self, callsign, days, start_time, duration):
        self.callsign = callsign
        self.days = days
        self.start_time = start_time
        self.duration = duration
        self.new_timeslot = False
        self.deleted = False

    def timeslot_exists(self):
        try:
            Timeslot.get(callsign=self.callsign,
                         weekdays=self.days,
                         start_time=self.start_time,
                         duration=self.duration)
            print('Slot already exists')
        except Exception as error_details:
            print('Timeslot does not exist')
            self.new_timeslot = True

    def store_timeslot(self):
        self.timeslot_exists()
        if self.new_timeslot is True:
            new_timeslot = Timeslot(callsign=self.callsign,
                                    weekdays=self.days,
                                    start_time=self.start_time,
                                    duration=self.duration)
            new_timeslot.save()

    def delete_timeslot(self):
        self.timeslot_exists()
        if self.new_timeslot is False:
            try:
                delete_query = Timeslot.delete().where(Timeslot.callsign == self.callsign,
                                                       Timeslot.weekdays == self.days,
                                                       Timeslot.start_time == self.start_time,
                                                       Timeslot.duration == self.duration)
                delete_query.execute()
                self.deleted = True
            except Exception as error_details:
                print(error_details)


class LocationTimeSlots(object):
    """Time slots associated with a specific location."""
    def __init__(self, callsign, all_timeslots=None):
        self.callsign = callsign
        self.start_datetimes = None
        self.all_timeslots = all_timeslots

    def fetch_timeslots(self):
        """Fetch all stored timeslots for a callsign
        Set self.all_timeslots to the output"""
        self.all_timeslots = Timeslot.select(Timeslot.id,
                                             Timeslot.callsign,
                                             Timeslot.weekdays,
                                             Timeslot.start_time,
                                             Timeslot.duration).join(Location).where(Location.callsign == self.callsign)

    def gen_start_times(self):
        """take the starting time, combine with days, return an array of date time stamps"""
        final_start_dates = set()  # This allows us to toss out duplicates.
        today_int = arrow.now().isoweekday()
        today_date = arrow.now().date()
        for row in self.all_timeslots:
            for day in row.weekdays.split(','):
                int_day = daymap[day.lower().strip('. ')]
                daydiff = int_day - today_int
                if daydiff <= 0:
                    daydiff += 7
                str_date = '{}T{}'.format(str(today_date + timedelta(days=daydiff)), row.start_time)
                final_start_dates.add((row.id, arrow.get(str_date).replace(tzinfo=tz.gettz(row.callsign.timezone)),
                                       row.duration))
        self.start_datetimes = sorted(final_start_dates)

    def print_final_times(self):
        for final_date in self.start_datetimes:
            print('{} type {}'.format(final_date, type(final_date)))


class TimeSlotAPI(object):
    @staticmethod
    def on_get(req, resp, callsign):
        resp_list = []
        timeslots = LocationTimeSlots(callsign)
        timeslots.fetch_timeslots()
        timeslots.gen_start_times()
        for row in timeslots.start_datetimes:
            timedict = {
                'id': row[0],
                'date': row[1].isoformat(),
                'duration': row[2]
            }
            resp_list.append(timedict)
        resp_dict = {
            'user': callsign,
            'timeslots': resp_list
        }
        resp.body = json.dumps(resp_dict)
        resp.status = falcon.HTTP_200

    @falcon.before(hooks.validate_type_json)
    def on_put(self, req, resp, callsign, input_object):
        resp_dict = {}
        try:
            new_timeslot = TimeSlotObj(input_object['callsign'],
                                       input_object['days'],
                                       input_object['start_time'],
                                       input_object['duration'])
            new_timeslot.store_timeslot()
            resp.status = falcon.HTTP_204
        except TypeError as error_details:
            resp.status = falcon.HTTP_500
            resp_dict = {'error': 'Invalid value for property provided',
                         'details': error_details.args}
        except KeyError as k:
            resp.status = falcon.HTTP_400  # This should probably be 422, but my falcon install doesn't have it.
            resp_dict = {'error': 'Missing Property',
                         'property name': k.args[0]}
        resp.body = json.dumps(resp_dict)

    @falcon.before(hooks.validate_type_json)
    def on_delete(self, req, resp, callsign, input_object):
        resp_dict = {}
        try:
            sent_timeslot = TimeSlotObj(input_object['callsign'],
                                        input_object['days'],
                                        input_object['start_time'],
                                        input_object['duration'])
            sent_timeslot.delete_timeslot()
            if sent_timeslot.deleted is True:
                resp.status = falcon.HTTP_204
            else:
                resp.status = falcon.HTTP_400
                resp_dict = {'error': 'timeslot does not exist'}
        except TypeError as error_details:
            resp.status = falcon.HTTP_500
            resp_dict = {'error': 'Invalid value for property provided',
                         'details': error_details.args}
        except KeyError as k:
            resp.status = falcon.HTTP_400  # This should probably be 422, but my falcon install doesn't have it.
            resp_dict = {'error': 'Missing Property',
                         'property name': k.args[0]}
        resp.body = json.dumps(resp_dict)


if __name__ == '__main__':
    test_callsign = config['default_location']['callsign']
    example_slot = TimeSlotObj(test_callsign,
                               'M,T,W,Th,F',
                               '12:00',
                               '3600')
    example_slot.store_timeslot()
    location_slots = LocationTimeSlots(example_slot.callsign)
    location_slots.fetch_timeslots()
    location_slots.gen_start_times()
    location_slots.print_final_times()
