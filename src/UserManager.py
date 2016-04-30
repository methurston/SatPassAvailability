#!/usr/bin/env python
from __future__ import print_function
from geocoder import google
import requests
from model import *
import sys
import falcon

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
    return callook_info.content


def get_elevation(latlon):
    """Use google to get the elevation of a lat/long pair"""
    elevation = google([latlon['lat'], latlon['lon']], method='elevation')
    return elevation.meters


class User(object):
    def __init__(self, callsign, lat, lon, timezone, street_address = None):
        self.callsign = callsign
        self.lat = lat
        self.lon = lon
        self.street_address = street_address
        if self.lat is not None and self.lon is not None:
            self.elevation = get_elevation({'lat': self.lat, 'lon': self.lon})
        else:
            self.elevation = None
        self.timezone = timezone
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
        except Exception as e:
            print('{} - Location does not exist'.format(e))
            self.new_user = True

    def set_geo_stats(self):
        address_details = google(self.street_address)
        print(address_details)
        self.lat = address_details.lat
        self.lon = address_details.lng
        self.elevation = get_elevation({'lat': self.lat, 'lon': self.lon})

class UserAPI(object):

    def on_get(self, req, resp, callsign):
        user = Location.get(callsign=callsign)
        userdict = {
            'callsign': user.callsign,
            'lat': user.lat,
            'lon': user.lon,
            'elevation': user.elevation
        }
        resp.body = json.dumps(userdict)
        resp.content_type = 'Application/JSON'
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, callsign):
        if req.content_type == 'application/json':
            api_input = req.stream.read().decode()
            input_obj = json.loads(api_input)
            if input_obj['lat'] is None and input_obj['long'] is None and input_obj['street_address'] is None:
                # TODO: add lookup here
                resp.status = falcon.HTTP_400
                resp_dict = {'error': 'Invalid Parameters',
                             'details': 'For Non US Callsigns, lat and long or street_address must be provided'}
                resp.body = json.dumps(resp_dict)
            else:
                try:
                    foo = User(input_obj['callsign'],
                               input_obj['lat'],
                               input_obj['long'],
                               input_obj['timezone'],
                               input_obj['street_address'])
                    foo.store_user()
                    resp.status = falcon.HTTP_204
                except TypeError as e:
                    resp.status = falcon.HTTP_500
                    resp_dict = {'error': 'Invalid value for property provided',
                                 'details': e.args}
                    resp.body = json.dumps(resp_dict)
                except KeyError as k:
                    resp.status = falcon.HTTP_400 # This should probably be 422, but my falcon install doesn't have it.
                    resp_dict = {'error': 'Missing Property',
                                 'property name': k.args[0]}
                    resp.body = json.dumps(resp_dict)
        else:
            resp.status = falcon.HTTP_415
            resp.body = '{"error":"Content must be sent with a type of application/json"}'


if __name__ == '__main__':
    # test_callsign = config['default_location']['callsign']
    test_callsign = 'N7M'
    test_timezone = config['default_location']['timezone']
    fullLoc = json.loads(lookup_callsign(test_callsign).decode())
    if fullLoc['status'] == 'VALID':
        myUser = User(test_callsign, fullLoc['location']['latitude'], fullLoc['location']['longitude'], test_timezone)
        myUser.store_user()
    else:
        myUser = User(test_callsign, None, None, test_timezone)
        myUser.street_address = input('Callsign of {} was not found, please enter a street address: '.format(test_callsign))
        myUser.store_user()

    print('Added {}'.format(myUser.callsign))
