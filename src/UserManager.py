#!/usr/bin/env python
from __future__ import print_function
from geocoder import google
import requests
from model import *
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

callsign_url = config['usersource']['host']
db_name = config['datasource']['filename']


def lookup_callsign(callsign):
    finalurl = '{}/{}/json'.format(callsign_url, callsign)
    callook_info = requests.get(finalurl)
    return json.loads(callook_info.content.decode())


def get_elevation(latlon):
    """Use google to get the elevation of a lat/long pair"""
    elevation = google([latlon['lat'], latlon['lon']], method='elevation')
    return elevation.meters

def get_timezone(latlon):
    """Use google to get timezone for a lat/lon pair.  This is an extra API call I do not like"""
    lookuptz = google([latlon['lat'], latlon['lon']], method='timezone')
    return lookuptz.timeZoneId


class User(object):
    def __init__(self, callsign, lat, lon, timezone, street_address=None):
        self.callsign = callsign
        self.lat = lat
        self.lon = lon
        self.street_address = street_address
        if self.lat is not None and self.lon is not None:
            self.elevation = get_elevation({'lat': self.lat, 'lon': self.lon})
            self.timezone = get_timezone({'lat': self.lat, 'lon': self.lon})
        else:
            self.elevation = None
        # self.timezone = timezone
        self.new_user = False  # assume it's an existing

    def store_user(self):
        self.user_exist()
        if self.lat is None or self.lon is None or self.elevation is None:
            self.set_geo_stats()

        new_user = Location(callsign=self.callsign,
                            lat=self.lat,
                            lon=self.lon,
                            elevation=self.elevation,
                            timezone=self.timezone)
        new_user.save(force_insert=self.new_user)
        print('User Stored')

    def user_exist(self):
        """sets new_user to true if it's not in the Database."""
        try:
            Location.get(callsign=self.callsign)
        except Location.DoesNotExist as error_details:
            print('{} - Location does not exist'.format(error_details))
            self.new_user = True

    def set_geo_stats(self):
        address_details = google(self.street_address)
        print(address_details)
        self.lat = address_details.lat
        self.lon = address_details.lng
        self.elevation = get_elevation({'lat': self.lat, 'lon': self.lon})
        self.timezone = get_timezone({'lat': self.lat, 'lon': self.lon})


class UserAPI(object):
    @staticmethod
    def on_get(req, resp, callsign):
        try:
            user = Location.get(callsign=callsign)
        except Location.DoesNotExist:
            raise falcon.HTTPNotFound()
        userdict = {
            'callsign': user.callsign,
            'lat': user.lat,
            'lon': user.lon,
            'elevation': user.elevation,
            'timezone': user.timezone
        }
        resp.body = json.dumps(userdict)
        resp.content_type = 'Application/JSON'
        resp.status = falcon.HTTP_200

    # @falcon.before(hooks.validate_type_json)
    # def on_put(self, req, resp, callsign, input_object):
    #     resp_dict = {}
    #     if input_object['lat'] is None and input_object['long'] is None and input_object['street_address'] is None:
    #         lookup_data = lookup_callsign(callsign)
    #         if lookup_data['status'] == 'VALID':
    #             input_object['lat'] = lookup_data['location']['latitude']
    #             input_object['long'] = lookup_data['location']['longitude']
    #             resp.status = falcon.HTTP_204
    #         else:
    #             resp.status = falcon.HTTP_400
    #             resp_dict = {'error': 'Invalid Parameters',
    #                          'details': 'For Non US Callsigns, lat and long or street_address must be provided'}
    #     try:
    #         new_user = User(callsign,
    #                         input_object['lat'],
    #                         input_object['long'],
    #                         input_object['timezone'],
    #                         input_object['street_address'])
    #         new_user.store_user()
    #         resp.status = falcon.HTTP_204
    #     except TypeError as error_details:
    #         resp.status = falcon.HTTP_500
    #         resp_dict = {'error': 'Invalid value for property provided',
    #                      'details': error_details.args}
    #     except KeyError as k:
    #         resp.status = falcon.HTTP_400  # This should be 422, pip falcon install doesn't have it.
    #         resp_dict = {'error': 'Missing Property',
    #                      'property name': k.args[0]}
    #     resp.body = json.dumps(resp_dict)

    @falcon.before(hooks.validate_type_json)
    def on_post(self, req, resp, callsign, input_object):
        resp_dict = {}
        if input_object['lat'] is None and input_object['long'] is None and input_object['street_address'] is None:
            lookup_data = lookup_callsign(callsign)
            if lookup_data['status'] == 'VALID':
                input_object['lat'] = lookup_data['location']['latitude']
                input_object['long'] = lookup_data['location']['longitude']
                resp.status = falcon.HTTP_204
            else:
                resp.status = falcon.HTTP_400
                resp_dict = {'error': 'Invalid Parameters',
                             'details': 'For Non US Callsigns, lat and long or street_address must be provided'}
        try:
            new_user = User(callsign,
                            input_object['lat'],
                            input_object['long'],
                            input_object['timezone'],
                            input_object['street_address'])
            new_user.store_user()
            resp.status = falcon.HTTP_204
        except TypeError as error_details:
            resp.status = falcon.HTTP_500
            resp_dict = {'error': 'Invalid value for property provided',
                         'details': error_details.args}
        except KeyError as k:
            resp.status = falcon.HTTP_400  # This should be 422, pip falcon install doesn't have it.
            resp_dict = {'error': 'Missing Property',
                         'property name': k.args[0]}
        resp.body = json.dumps(resp_dict)



if __name__ == '__main__':
    # test_callsign = config['default_location']['callsign']
    test_callsign = 'N7M'
    test_timezone = config['default_location']['timezone']
    fullLoc = lookup_callsign(test_callsign)
    if fullLoc['status'] == 'VALID':
        myUser = User(test_callsign,
                      fullLoc['location']['latitude'],
                      fullLoc['location']['longitude'],
                      test_timezone)
        myUser.store_user()
    else:
        myUser = User(test_callsign, None, None, test_timezone)
        myUser.street_address = input(
            'Callsign of {} was not found, please enter a street address: '.format(test_callsign))
        myUser.store_user()
