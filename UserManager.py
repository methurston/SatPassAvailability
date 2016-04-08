#!/usr/bin/env python
from __future__ import print_function
from geocoder import google
import requests
import json
import sqlite3

# Globals
callsign_url = 'https://callook.info'
db_name = 'sats.db'


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

    def store_user(self):
        query = 'INSERT OR REPLACE INTO locations (callsign, lat, lon, elevation, timezone) ' \
                'VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(self.callsign,
                                                                 self.lat,
                                                                 self.lon,
                                                                 self.elevation,
                                                                 self.timezone)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    test_callsign = 'W1AW'
    fullLoc = json.loads(lookup_callsign(test_callsign))
    myUser = User(test_callsign, fullLoc['location']['latitude'], fullLoc['location']['longitude'], 'US/Eastern')
    myUser.store_user()
    print(myUser.callsign)
