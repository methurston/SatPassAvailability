#!/usr/bin/env python
from __future__ import print_function
from geocoder import google

def get_latlon(street_address):
    """ Get the latitude and longitude of an address """
    address_details = google(street_address)
    print(address_details)
    latlong = {'lat': address_details.lat, 'lon': address_details.lng}
    return latlong

def get_elevation(latlon):
    """Use google to get the elevation of a lat/long pair"""
    elevation = google([latlon['lat'],latlon['lon']], method='elevation')
    return elevation.meters


myaddress = ''
myloc = get_latlon(myaddress)
myloc['elevation'] = get_elevation(myloc)
print(myloc)