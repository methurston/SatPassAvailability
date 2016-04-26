#!/usr/bin/env python
from __future__ import print_function
from geocoder import google
import requests
from model import *
import sys

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


def get_latlon(street_address):
    """ Get the latitude and longitude of an address from google.
        Not used, but I'm keeping it around for non us call signs"""
    address_details = google(street_address)
    print(address_details)
    latlong = {'lat': address_details.lat, 'lon': address_details.lng}
    return latlong


def get_elevation(latlon):
    """Use google to get the elevation of a lat/long pair"""
    elevation = google([latlon['lat'], latlon['lon']], method='elevation')
    return elevation.meters


class User(object):
    def __init__(self, callsign, lat, lon, timezone):
        self.callsign = callsign
        self.lat = lat
        self.lon = lon
        self.elevation = get_elevation({'lat': self.lat, 'lon': self.lon})
        self.timezone = timezone
        self.new_user = False  # assume it's an existing

    def store_user(self):
        self.user_exist()
        new_user = Location(callsign=self.callsign,
                            lat=self.lat,
                            lon=self.lon,
                            elevation=self.elevation,
                            timezone=self.timezone)
        new_user.save(force_insert=self.new_user)

    def user_exist(self):
        """sets new_user to true if it's not in the Database."""
        try:
            Location.get(callsign=self.callsign)
        except:
            print('Location does not exist')
            self.new_user = True


if __name__ == '__main__':
    test_callsign = config['default_location']['callsign']
    test_timezone = config['default_location']['timezone']
    fullLoc = json.loads(lookup_callsign(test_callsign))
    myUser = User(test_callsign, fullLoc['location']['latitude'], fullLoc['location']['longitude'], test_timezone)
    myUser.store_user()
    print('Added {}'.format(myUser.callsign))
